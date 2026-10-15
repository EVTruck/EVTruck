from typing import Any

import pytest

from evtruck.bms_satellite.coupling import Coupling
from evtruck.bms_satellite.enclosure import SatelliteEnclosure
from evtruck.bms_satellite.port_plug import PortPlug


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"fit_test": True},
        {"seal_rings": 1, "port_depth": 6},
    ],
)
def test_port_plug_builds(params: dict[str, Any]) -> None:
    part = PortPlug(**params).plug
    assert part.is_valid
    assert len(part.solids()) == 1


def test_port_plug_rejects_too_many_seal_rings() -> None:
    with pytest.raises(ValueError, match="seal rings"):
        _ = PortPlug(seal_rings=2, port_depth=6).plug


def test_enclosure_parts_do_not_overlap() -> None:
    enclosure = SatelliteEnclosure()
    body, lid = enclosure.body, enclosure.lid
    board, plug = enclosure.board, enclosure.placed_plug
    for part in (body, lid, plug):
        assert part.is_valid
        assert len(part.solids()) == 1
    assert (plug & body).volume == pytest.approx(0, abs=1e-3)
    assert (lid & body).volume == pytest.approx(0, abs=1e-3)
    assert (board & body).volume == pytest.approx(0, abs=1e-3)


def test_enclosure_printable_layout() -> None:
    body, lid = SatelliteEnclosure().print_layout
    assert pytest.approx(0) == body.bounding_box().min.Z
    assert pytest.approx(0) == lid.bounding_box().min.Z


def test_coupling_o_ring_squeeze() -> None:
    cross_section = 2.0
    gland = (Coupling.socket_diameter - Coupling.groove_root_diameter) / 2
    squeeze = 1 - gland / cross_section
    assert 0.1 < squeeze < 0.25


@pytest.mark.parametrize("connectors", [1, 2])
def test_enclosure_connector_holes(connectors: int) -> None:
    enclosure = SatelliteEnclosure(isospi_connectors=connectors)
    assert len(enclosure.connector_offsets) == connectors
    assert enclosure.body.is_valid
