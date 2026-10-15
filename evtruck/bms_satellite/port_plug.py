"""Sealed plug for the square connector port on each battery box.

The port was cut for an Amphenol 350 A sealed power receptacle. This plug
fills it instead and passes the satellite's cell-tap and thermistor wires
through a central bore.

Coordinates: Z = 0 is the outer face of the battery box plate and +Z points
out of the box. The port is centered on the origin.

Sealing:
* Two o-ring cords in perimeter grooves on the square body seal against the
  walls of the port (radial seal, so flange flatness doesn't matter).
* Two o-rings on the round spigot seal into the enclosure socket.
* M4 flat head screws go through the flange into the existing holes. Seal
  the nuts inside the box with bonded washers, because those holes are
  outside the port seal.
* Pot the wire bore with epoxy after the wires are pulled through, so the
  enclosure doesn't share air with the battery box.
"""

from __future__ import annotations

from bdbox import Model, Preset
from build123d import (
    MM,
    Align,
    Axis,
    BuildPart,
    BuildSketch,
    Circle,
    Color,
    CounterSinkHole,
    Cylinder,
    GeomType,
    Locations,
    Mode,
    Part,
    Plane,
    Pos,
    RectangleRounded,
    SlotCenterToCenter,
    chamfer,
    extrude,
    insert,
)

from .coupling import Coupling, ring


class PortPlug(Model):
    # Port opening, estimated from photos. Measure before printing.
    port_width: float = 38 * MM
    port_height: float = 38 * MM
    port_corner_radius: float = 3 * MM
    port_depth: float = 10 * MM  # Plate thickness, or how far the plug goes in
    port_fit: float = 0.2 * MM  # Clearance per side

    # Radial seal: o-ring cord (2 mm) in grooves around the square body
    seal_rings: int = 2
    seal_cord_diameter: float = 2 * MM
    seal_squeeze: float = 0.2  # Fraction of cord diameter
    seal_groove_width: float = 2.7 * MM
    seal_groove_pitch: float = 4 * MM

    flange_lip: float = 5 * MM
    flange_thickness: float = 7 * MM

    # Existing mounting holes: two holes on one side of the port, estimated
    # from photos as 46 mm apart and 11.5 mm below the port center.
    mount_hole_spacing: float = 46 * MM
    mount_hole_offset: float = -11.5 * MM
    mount_hole_diameter: float = 4.5 * MM  # M4 flat head screws
    mount_head_diameter: float = 8.5 * MM
    mount_boss_diameter: float = 11 * MM

    # Thin print to check port fit and hole positions before the real part
    fit_test: bool = False

    presets = (
        Preset(
            "fit-test",
            description="Thin print to check port fit and hole positions",
            fit_test=True,
        ),
        Preset(
            "single-seal",
            description="One port o-ring, for ports less than 9.5 mm deep",
            seal_rings=1,
        ),
    )

    def build(self) -> Model.Geometry:
        part = self.plug
        part.label = "Port plug (fit test)" if self.fit_test else "Port plug"
        part.color = Color(0x3366CC)
        return part

    @property
    def body_length(self) -> float:
        return 3 * MM if self.fit_test else self.port_depth

    @property
    def body_flange_thickness(self) -> float:
        return 2 * MM if self.fit_test else self.flange_thickness

    @property
    def seal_groove_depth(self) -> float:
        # Gland depth (groove + fit clearance) sets the squeeze
        gland = self.seal_cord_diameter * (1 - self.seal_squeeze)
        return gland - self.port_fit

    @property
    def seal_groove_centers(self) -> list[float]:
        first = self.seal_groove_width / 2 + 1.5 * MM
        return [
            first + i * self.seal_groove_pitch for i in range(self.seal_rings)
        ]

    def _check(self) -> None:
        body_radius = self.port_corner_radius - self.port_fit
        if body_radius - self.seal_groove_depth <= 0:
            raise ValueError(
                "port_corner_radius is too small for the seal groove depth"
            )
        centers = self.seal_groove_centers
        if centers and (
            centers[-1] + self.seal_groove_width / 2 + 1 * MM > self.port_depth
        ):
            raise ValueError(
                f"{self.seal_rings} seal rings don't fit in a"
                f" {self.port_depth} mm deep port; use fewer seal_rings"
            )

    @property
    def plug(self) -> Part:
        self._check()
        body_w = self.port_width - 2 * self.port_fit
        body_h = self.port_height - 2 * self.port_fit
        body_r = self.port_corner_radius - self.port_fit
        flange_t = self.body_flange_thickness
        spigot_base = flange_t + Coupling.pedestal_height

        with BuildPart() as p:
            # Square body that sits in the port
            with BuildSketch(Plane.XY):
                RectangleRounded(body_w, body_h, body_r)
            extrude(amount=-self.body_length)
            chamfer(
                p.faces().sort_by(Axis.Z)[0].edges(),
                0.6 * MM,
            )

            # Flange: a lip around the port plus a bar to the mounting holes
            with BuildSketch(Plane.XY):
                RectangleRounded(
                    self.port_width + 2 * self.flange_lip,
                    self.port_height + 2 * self.flange_lip,
                    self.port_corner_radius + self.flange_lip,
                )
                with Locations((0, self.mount_hole_offset)):
                    SlotCenterToCenter(
                        self.mount_hole_spacing, self.mount_boss_diameter
                    )
            extrude(amount=flange_t)

            if not self.fit_test:
                # Pedestal the enclosure floor rests on
                with Locations((0, 0, flange_t)):
                    Cylinder(
                        Coupling.pedestal_diameter / 2,
                        Coupling.pedestal_height,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
                # Round spigot that plugs into the enclosure socket
                with Locations((0, 0, spigot_base)):
                    Cylinder(
                        Coupling.spigot_diameter / 2,
                        Coupling.spigot_length,
                        align=(Align.CENTER, Align.CENTER, Align.MIN),
                    )
                chamfer(
                    p.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1],
                    Coupling.lead_in,
                )
                # Spigot o-ring grooves
                for offset in Coupling.groove_offsets:
                    insert(
                        ring(
                            spigot_base + offset - Coupling.groove_width / 2,
                            Coupling.spigot_diameter,
                            Coupling.groove_root_diameter / 2,
                            Coupling.groove_width,
                        ),
                        mode=Mode.SUBTRACT,
                    )
                # Port seal grooves around the square body
                for center in self.seal_groove_centers:
                    with BuildSketch(
                        Plane.XY.offset(-center - self.seal_groove_width / 2)
                    ):
                        RectangleRounded(body_w + 2, body_h + 2, body_r + 1)
                        RectangleRounded(
                            body_w - 2 * self.seal_groove_depth,
                            body_h - 2 * self.seal_groove_depth,
                            body_r - self.seal_groove_depth,
                            mode=Mode.SUBTRACT,
                        )
                    extrude(amount=self.seal_groove_width, mode=Mode.SUBTRACT)
                # Heat-set inserts for the enclosure retention screws
                top = spigot_base
                with (
                    BuildSketch(Plane.XY.offset(top)),
                    Locations(
                        (0, Coupling.retention_screw_offset),
                        (0, -Coupling.retention_screw_offset),
                    ),
                ):
                    Circle(Coupling.insert_hole_diameter / 2)
                extrude(amount=-Coupling.insert_hole_depth, mode=Mode.SUBTRACT)

            # Wire bore, straight through
            top_z = flange_t + (
                0
                if self.fit_test
                else Coupling.pedestal_height + Coupling.spigot_length
            )
            with BuildSketch(Plane.XY.offset(-self.body_length)):
                Circle(Coupling.wire_bore_diameter / 2)
            extrude(amount=self.body_length + top_z, mode=Mode.SUBTRACT)

            # Countersunk mounting holes through the flange, with clearance
            # in the pedestal so the screw heads can be reached
            mount_holes = [
                (x, self.mount_hole_offset)
                for x in (
                    -self.mount_hole_spacing / 2,
                    self.mount_hole_spacing / 2,
                )
            ]
            if not self.fit_test:
                with (
                    BuildSketch(Plane.XY.offset(flange_t)),
                    Locations(*mount_holes),
                ):
                    Circle(self.mount_head_diameter / 2 + 0.5 * MM)
                extrude(amount=Coupling.pedestal_height, mode=Mode.SUBTRACT)
            with Locations(*(Pos(x, y, flange_t) for x, y in mount_holes)):
                CounterSinkHole(
                    self.mount_hole_diameter / 2,
                    self.mount_head_diameter / 2,
                    depth=flange_t,
                    counter_sink_angle=90,
                )

        if not p.part:
            raise RuntimeError("Empty part")
        return p.part
