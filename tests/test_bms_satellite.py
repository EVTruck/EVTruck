import pytest

from evtruck.bms_satellite.enclosure import SatelliteEnclosure
from evtruck.bms_satellite.port_flange import PortFlange
from evtruck.bms_satellite.port_interface import PortInterface as Port


@pytest.mark.parametrize("template", [False, True])
def test_port_flange_builds(*, template: bool) -> None:
    flange = PortFlange(template=template)
    part = flange.drill_template if template else flange.flange
    assert part.is_valid
    assert len(part.solids()) == 1


def test_enclosure_parts_do_not_overlap() -> None:
    enclosure = SatelliteEnclosure()
    body, lid = enclosure.body, enclosure.lid
    board, flange = enclosure.board, enclosure.placed_flange
    for part in (body, lid, flange):
        assert part.is_valid
        assert len(part.solids()) == 1
    assert (flange & body).volume == pytest.approx(0, abs=1e-3)
    assert (lid & body).volume == pytest.approx(0, abs=1e-3)
    assert (board & body).volume == pytest.approx(0, abs=1e-3)


def test_enclosure_printable_layout() -> None:
    body, lid = SatelliteEnclosure().print_layout
    assert pytest.approx(0) == body.bounding_box().min.Z
    assert pytest.approx(0) == lid.bounding_box().min.Z


def test_port_seals_surround_screws_and_pocket() -> None:
    screw_reach = (2**0.5) * Port.screw_offset + Port.insert_hole_diameter / 2
    wire_reach = Port.wire_hole_diameter / 2
    pocket_corner = (2**0.5) * Port.pocket_size / 2
    half_groove = Port.groove_width / 2
    assert Port.inner_groove_radius - half_groove > screw_reach
    assert Port.outer_groove_radius - half_groove > pocket_corner
    assert Port.outer_groove_radius + half_groove < Port.pad_diameter / 2
    assert Port.inner_groove_radius + half_groove < Port.flange_size / 2
    # Web between the wire hole and each screw hole
    gap = (2**0.5) * Port.screw_offset - wire_reach
    assert gap - Port.insert_hole_diameter / 2 > 1


@pytest.mark.parametrize("connectors", [1, 2])
def test_enclosure_connector_holes(connectors: int) -> None:
    enclosure = SatelliteEnclosure(isospi_connectors=connectors)
    assert len(enclosure.connector_offsets) == connectors
    assert enclosure.body.is_valid
