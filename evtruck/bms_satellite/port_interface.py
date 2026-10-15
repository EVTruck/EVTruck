"""Sizes shared by the satellite enclosure and its battery box mount.

The enclosure clamps onto the outside of the battery box wall over the square
pocket that was cut for an Amphenol SurLok Plus receptacle. A printed flange
clamps on from the inside. Four M4 screws pass through the inner flange and
the wall into heat-set inserts in the enclosure's mounting pad, and a face
o-ring on each side seals around the wire hole and the screws:

* Outside: a 52 x 2 mm o-ring in the enclosure pad, sealing on the wall face
  around the pocket.
* Inside: a 44 x 2 mm o-ring in the inner flange, sealing on the inner face.

The screws sit inside both seals, so their holes never see water.

The wire hole goes through the bottom of the pocket. At 25 mm it passes the
satellite's 14-pin Micro-Fit cell-tap plugs, so pre-made harnesses can be
threaded through.
"""

from __future__ import annotations

from build123d import MM


class PortInterface:
    # Existing square pocket on the outside of the battery box wall
    pocket_size = 35 * MM

    wire_hole_diameter = 25 * MM
    screw_offset = 13 * MM  # Four M4 screws at (+/-13, +/-13) from the hole
    screw_clearance_diameter = 4.5 * MM
    insert_hole_diameter = 5.6 * MM  # M4 heat-set insert, 5.7 mm OD
    insert_hole_depth = 8.5 * MM

    # Face seals for 2 mm cross-section o-rings (about 25% squeeze)
    groove_width = 2.7 * MM
    groove_depth = 1.5 * MM
    outer_groove_radius = 27 * MM  # Centerline; 52 x 2 mm o-ring
    inner_groove_radius = 23 * MM  # Centerline; 44 x 2 mm o-ring

    pad_diameter = 64 * MM  # Enclosure mounting pad, outside the box
    flange_size = 54 * MM  # Inner flange, inside the box

    # Only used to place parts in the assembly view
    wall_thickness = 8 * MM

    @classmethod
    def screw_locations(cls) -> list[tuple[float, float]]:
        o = cls.screw_offset
        return [(sx * o, sy * o) for sx in (-1, 1) for sy in (-1, 1)]
