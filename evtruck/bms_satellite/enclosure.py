"""Sealed enclosure for a bare Dilithium BMSS24 satellite board.

The board comes out of its Serpac WM031 case and mounts on standoffs in
this box. A round pad under the wiring bay clamps against the outside of the
battery box wall, with an o-ring in its face and four M4 heat-set inserts
for the screws from the inner flange (see ``port_interface.py`` and
``port_flange.py``). The cell-tap and thermistor wires come up through the
wire hole into the bay.

Sealed 4-pin panel connectors on the far end wall carry the isoSPI daisy
chain. By default there are two, one for the pair in (IPI/IMI) and one for
the pair out (IPO/IMO), so plain point-to-point cables link the boxes. Set
``isospi_connectors = 1`` to carry both pairs on one connector. The holes
fit M12 A-coded panel receptacles with an M16 x 1.5 rear thread.

The lid seals on a 2 mm o-ring cord in a groove on the wall rim. The lid
screws are in bosses outside the seal.

Coordinates: Z = 0 is the enclosure floor's underside. The pad hangs below
it, and the wire hole is on the Z axis.
"""

from __future__ import annotations

from bdbox import Model, Preset
from build123d import (
    MM,
    Align,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Color,
    Cylinder,
    Locations,
    Mode,
    Part,
    Plane,
    Pos,
    RectangleRounded,
    Rot,
    extrude,
)

from .port_flange import PortFlange
from .port_interface import PortInterface as Port

M3_INSERT_HOLE_DIAMETER = 4.0 * MM  # M3 heat-set insert
M3_INSERT_HOLE_DEPTH = 6 * MM
M3_CLEARANCE_DIAMETER = 3.4 * MM


class SatelliteEnclosure(Model):
    # BMSS24 board, measured from photos (2026-10-15). The cell-tap
    # connectors face the wiring bay and the isoSPI connectors face the far
    # end. The 10-pin thermistor connectors face out of the long sides.
    board_length: float = 100 * MM  # PCB only; connectors overhang the ends
    board_width: float = 74 * MM  # PCB only; connectors overhang the sides
    board_thickness: float = 1.6 * MM
    board_hole_spacing_length: float = 52 * MM
    board_hole_spacing_width: float = 62 * MM
    board_hole_offset: float = -3.5 * MM  # Hole pattern shift toward the bay
    component_height: float = 10 * MM  # 11 mm overall with the PCB
    standoff_height: float = 8 * MM
    side_clearance: float = 18 * MM  # Thermistor plugs and wire bends
    end_clearance: float = 25 * MM  # isoSPI plugs at the far end

    bay_length: float = 56 * MM  # Wiring bay over the wall pad
    pad_height: float = 6.5 * MM  # Floor clearance off the battery box wall
    wall_thickness: float = 4.5 * MM
    floor_thickness: float = 3 * MM
    inner_corner_radius: float = 2 * MM

    lid_thickness: float = 3 * MM
    lid_boss_diameter: float = 9 * MM
    lid_boss_offset: float = 3.5 * MM  # Boss center outside the wall
    seal_groove_width: float = 2.6 * MM  # 2 mm o-ring cord
    seal_groove_depth: float = 1.5 * MM

    connector_hole_diameter: float = 16.2 * MM  # M12 receptacle, M16 thread
    isospi_connectors: int = 2  # In and out, or 1 for both pairs on one
    connector_spacing: float = 30 * MM

    printable: bool = False  # Body and lid only, laid out for printing
    show_flange: bool = True

    presets = (
        Preset(
            "print",
            description="Body and lid laid flat for printing",
            printable=True,
        ),
        Preset(
            "one-connector",
            description="Both isoSPI pairs on a single connector",
            isospi_connectors=1,
        ),
    )

    def build(self) -> Model.Geometry:
        if self.printable:
            return self.print_layout
        geometry = [self.body, self.lid, self.board]
        if self.show_flange:
            geometry.append(self.placed_flange)
        return geometry

    @property
    def print_layout(self) -> list[Part]:
        """Body upright on its pad and lid flipped beside it, on the bed.

        The floor overhangs the pad, so print the body with supports.
        """
        lid = Pos(0, self.outer_width + 15 * MM, self.lid_thickness) * (
            Rot(180, 0, 0) * Pos(0, 0, -self.wall_top) * self.lid
        )
        lid.label = "Satellite enclosure lid"
        body = Pos(0, 0, self.pad_height) * self.body
        body.label = "Satellite enclosure"
        return [body, lid]

    @property
    def placed_flange(self) -> Part:
        """Inner flange in place across the battery box wall, for reference."""
        flange = (
            Pos(0, 0, -self.pad_height - Port.wall_thickness)
            * Rot(180, 0, 0)
            * PortFlange().flange
        )
        flange.label = "Port flange"
        flange.color = Color(0x3366CC, 0x80)
        return flange

    @property
    def interior_length(self) -> float:
        return self.bay_length + self.board_length + self.end_clearance

    @property
    def interior_width(self) -> float:
        return self.board_width + 2 * self.side_clearance

    @property
    def interior_height(self) -> float:
        return (
            self.standoff_height
            + self.board_thickness
            + self.component_height
            + 1 * MM
        )

    @property
    def interior_x0(self) -> float:
        # The wall pad sits in the middle of the wiring bay
        return -self.bay_length / 2

    @property
    def interior_center_x(self) -> float:
        return self.interior_x0 + self.interior_length / 2

    @property
    def wall_top(self) -> float:
        return self.floor_thickness + self.interior_height

    @property
    def outer_width(self) -> float:
        return self.interior_width + 2 * self.wall_thickness

    @property
    def board_center_x(self) -> float:
        return self.interior_x0 + self.bay_length + self.board_length / 2

    @property
    def connector_offsets(self) -> list[float]:
        n = self.isospi_connectors
        if n not in (1, 2):
            raise ValueError("isospi_connectors must be 1 or 2")
        return [(i - (n - 1) / 2) * self.connector_spacing for i in range(n)]

    @property
    def board_hole_locations(self) -> list[tuple[float, float]]:
        cx = self.board_center_x + self.board_hole_offset
        dx = self.board_hole_spacing_length / 2
        dy = self.board_hole_spacing_width / 2
        return [(cx + sx * dx, sy * dy) for sx in (-1, 1) for sy in (-1, 1)]

    @property
    def lid_boss_locations(self) -> list[tuple[float, float]]:
        out = self.wall_thickness + self.lid_boss_offset
        cx = self.interior_center_x
        half_l = self.interior_length / 2
        half_w = self.interior_width / 2
        sides = [
            (cx + dx, sy * (half_w + out))
            for dx in (-half_l + 8 * MM, 0, half_l - 8 * MM)
            for sy in (-1, 1)
        ]
        ends = [
            (cx + sx * (half_l + out), sy * half_w / 2)
            for sx in (-1, 1)
            for sy in (-1, 1)
        ]
        return sides + ends

    def _outline(self, grow: float, mode: Mode = Mode.ADD) -> RectangleRounded:
        """Rounded rectangle offset outward from the interior by ``grow``."""
        return RectangleRounded(
            self.interior_length + 2 * grow,
            self.interior_width + 2 * grow,
            self.inner_corner_radius + grow,
            mode=mode,
        )

    @property
    def body(self) -> Part:
        wall = self.wall_thickness
        cx = self.interior_center_x
        with BuildPart() as p:
            # Shell
            with BuildSketch(), Locations((cx, 0)):
                self._outline(wall)
            extrude(amount=self.wall_top)
            with (
                BuildSketch(Plane.XY.offset(self.floor_thickness)),
                Locations((cx, 0)),
            ):
                self._outline(0)
            extrude(amount=self.interior_height, mode=Mode.SUBTRACT)

            # Lid screw bosses outside the seal
            with Locations(*self.lid_boss_locations):
                Cylinder(
                    self.lid_boss_diameter / 2,
                    self.wall_top,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )

            # Board standoffs
            with Locations(
                *(
                    Pos(x, y, self.floor_thickness)
                    for x, y in self.board_hole_locations
                )
            ):
                Cylinder(
                    3.5 * MM,
                    self.standoff_height,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                )

            # Mounting pad against the battery box wall
            Cylinder(
                Port.pad_diameter / 2,
                self.pad_height,
                align=(Align.CENTER, Align.CENTER, Align.MAX),
            )
            # Wire hole through the pad and floor
            with BuildSketch(Plane.XY.offset(-self.pad_height)):
                Circle(Port.wire_hole_diameter / 2)
            extrude(
                amount=self.pad_height + self.floor_thickness,
                mode=Mode.SUBTRACT,
            )
            # Face o-ring groove and M4 inserts for the inner flange screws
            with BuildSketch(Plane.XY.offset(-self.pad_height)):
                Circle(Port.outer_groove_radius + Port.groove_width / 2)
                Circle(
                    Port.outer_groove_radius - Port.groove_width / 2,
                    mode=Mode.SUBTRACT,
                )
            extrude(amount=Port.groove_depth, mode=Mode.SUBTRACT)
            with (
                BuildSketch(Plane.XY.offset(-self.pad_height)),
                Locations(*Port.screw_locations()),
            ):
                Circle(Port.insert_hole_diameter / 2)
            extrude(amount=Port.insert_hole_depth, mode=Mode.SUBTRACT)

            # Heat-set insert holes: lid bosses and board standoffs
            with (
                BuildSketch(Plane.XY.offset(self.wall_top)),
                Locations(*self.lid_boss_locations),
            ):
                Circle(M3_INSERT_HOLE_DIAMETER / 2)
            extrude(amount=-M3_INSERT_HOLE_DEPTH, mode=Mode.SUBTRACT)
            with (
                BuildSketch(
                    Plane.XY.offset(
                        self.floor_thickness + self.standoff_height
                    )
                ),
                Locations(*self.board_hole_locations),
            ):
                Circle(M3_INSERT_HOLE_DIAMETER / 2)
            extrude(amount=-5 * MM, mode=Mode.SUBTRACT)

            # Lid seal groove centered on the wall rim
            gw = self.seal_groove_width
            with (
                BuildSketch(Plane.XY.offset(self.wall_top)),
                Locations((cx, 0)),
            ):
                self._outline(wall / 2 + gw / 2)
                self._outline(wall / 2 - gw / 2, mode=Mode.SUBTRACT)
            extrude(amount=-self.seal_groove_depth, mode=Mode.SUBTRACT)

            # isoSPI connector holes in the far end wall, by the board's
            # isoSPI connectors
            with Locations(
                *(
                    Pos(
                        self.interior_x0 + self.interior_length + wall / 2,
                        y,
                        self.floor_thickness + self.interior_height / 2,
                    )
                    for y in self.connector_offsets
                )
            ):
                Cylinder(
                    self.connector_hole_diameter / 2,
                    wall * 2,
                    rotation=(0, 90, 0),
                    mode=Mode.SUBTRACT,
                )

        if not p.part:
            raise RuntimeError("Empty part")
        p.part.label = "Satellite enclosure"
        p.part.color = Color(0x444444)
        return p.part

    @property
    def lid(self) -> Part:
        with BuildPart() as p:
            with BuildSketch(Plane.XY.offset(self.wall_top)):
                with Locations((self.interior_center_x, 0)):
                    self._outline(self.wall_thickness)
                with Locations(*self.lid_boss_locations):
                    Circle(self.lid_boss_diameter / 2)
            extrude(amount=self.lid_thickness)
            with (
                BuildSketch(Plane.XY.offset(self.wall_top)),
                Locations(*self.lid_boss_locations),
            ):
                Circle(M3_CLEARANCE_DIAMETER / 2)
            extrude(amount=self.lid_thickness, mode=Mode.SUBTRACT)
        if not p.part:
            raise RuntimeError("Empty part")
        p.part.label = "Satellite enclosure lid"
        p.part.color = Color(0x666666, 0xC0)
        return p.part

    @property
    def board(self) -> Part:
        board = Pos(
            self.board_center_x,
            0,
            self.floor_thickness + self.standoff_height,
        ) * Box(
            self.board_length,
            self.board_width,
            self.board_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        board.label = "BMSS24 board"
        board.color = Color(0x228833)
        return board
