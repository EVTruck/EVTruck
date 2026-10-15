"""Double o-ring coupling between the port plug and the satellite enclosure.

The port plug carries a round spigot with two o-rings. The enclosure floor
has a matching socket. Both parts import their sizes from here so they stay
in step.
"""

from __future__ import annotations

from build123d import MM, Align, Cylinder, Part, Pos


class Coupling:
    """Spigot and socket sizes, for two 20 x 2 mm (ID x CS) nitrile o-rings.

    Groove depth gives about 17% squeeze on the 2 mm cross section, and the
    groove root (20.9 mm) stretches the 20 mm o-ring about 4.5%.
    """

    spigot_diameter = 24 * MM
    spigot_length = 16 * MM
    socket_clearance = 0.2 * MM  # Diametral
    wire_bore_diameter = 14 * MM
    groove_depth = 1.55 * MM
    groove_width = 2.7 * MM
    groove_offsets = (5 * MM, 11 * MM)  # Groove centers from the spigot base
    lead_in = 1 * MM

    # Spacer under the enclosure floor, so it clears nearby screw heads
    pedestal_diameter = 46 * MM
    pedestal_height = 2 * MM

    # Two M3 screws hold the enclosure to the plug, either side along Y
    retention_screw_offset = 19.5 * MM
    insert_hole_diameter = 4.0 * MM  # M3 heat-set insert
    insert_hole_depth = 6 * MM
    screw_clearance_diameter = 3.4 * MM

    socket_diameter = spigot_diameter + socket_clearance
    groove_root_diameter = spigot_diameter - 2 * groove_depth


def ring(
    z: float, outer_radius: float, inner_radius: float, height: float
) -> Part:
    """Annular solid on the Z axis, from ``z`` up by ``height``.

    Subtract it from a part to cut an o-ring groove.
    """
    align = (Align.CENTER, Align.CENTER, Align.MIN)
    solid = Cylinder(outer_radius, height, align=align) - Cylinder(
        inner_radius, height, align=align
    )
    if not isinstance(solid, Part):
        raise TypeError("Expected a Part")
    return Pos(0, 0, z) * solid
