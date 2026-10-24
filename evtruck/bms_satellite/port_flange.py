"""Inner clamp flange for the satellite enclosure, and a drilling template.

The flange sits inside the battery box against the wall. Its face o-ring
seals around the wire hole and screws, and four M4 socket head screws pass
through it and the wall into the enclosure's mounting pad (see
``port_interface.py``).

The ``template`` preset prints a thin disc the size of the enclosure pad,
with a square nub that drops into the pocket. Use it to check that the pad
clears nearby screw heads, then drill the four screw holes and mark the wire
hole through it.

Coordinates: Z = 0 is the wall face the part sits against. The flange
extends to +Z (into the box); the template's nub extends to -Z (into the
pocket).
"""

from __future__ import annotations

from bdbox import Model, Preset
from build123d import (
    MM,
    Align,
    BuildPart,
    BuildSketch,
    Circle,
    Color,
    CounterBoreHole,
    Cylinder,
    Locations,
    Mode,
    Part,
    Plane,
    Pos,
    RectangleRounded,
    extrude,
)

from .port_interface import PortInterface as Port


class PortFlange(Model):
    thickness: float = 6 * MM
    counterbore_diameter: float = 8 * MM  # M4 socket head
    counterbore_depth: float = 4 * MM

    template: bool = False
    template_thickness: float = 2.5 * MM
    template_fit: float = 0.3 * MM  # Per side, nub in the pocket

    presets = (
        Preset(
            "template",
            description="Drilling template that drops into the pocket",
            template=True,
        ),
    )

    def build(self) -> Model.Geometry:
        return self.drill_template if self.template else self.flange

    @property
    def flange(self) -> Part:
        with BuildPart() as p:
            with BuildSketch():
                RectangleRounded(Port.flange_size, Port.flange_size, 6 * MM)
            extrude(amount=self.thickness)
            Cylinder(
                Port.wire_hole_diameter / 2,
                self.thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )
            with Locations(
                *(Pos(x, y, self.thickness) for x, y in Port.screw_locations())
            ):
                CounterBoreHole(
                    Port.screw_clearance_diameter / 2,
                    self.counterbore_diameter / 2,
                    self.counterbore_depth,
                    depth=self.thickness,
                )
            # Face o-ring groove against the wall
            with BuildSketch():
                Circle(Port.inner_groove_radius + Port.groove_width / 2)
                Circle(
                    Port.inner_groove_radius - Port.groove_width / 2,
                    mode=Mode.SUBTRACT,
                )
            extrude(amount=Port.groove_depth, mode=Mode.SUBTRACT)
        if not p.part:
            raise RuntimeError("Empty part")
        p.part.label = "Port flange"
        p.part.color = Color(0x3366CC)
        return p.part

    @property
    def drill_template(self) -> Part:
        nub = Port.pocket_size - 2 * self.template_fit
        with BuildPart() as p:
            Cylinder(
                Port.pad_diameter / 2,
                self.template_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
            with BuildSketch(Plane.XY):
                RectangleRounded(nub, nub, 3 * MM)
            extrude(amount=-2 * MM)
            with BuildSketch(Plane.XY.offset(-2 * MM)):
                Circle(Port.wire_hole_diameter / 2)
                with Locations(*Port.screw_locations()):
                    Circle(Port.screw_clearance_diameter / 2)
            extrude(
                amount=self.template_thickness + 2 * MM, mode=Mode.SUBTRACT
            )
        if not p.part:
            raise RuntimeError("Empty part")
        p.part.label = "Port drilling template"
        p.part.color = Color(0xCC8833)
        return p.part
