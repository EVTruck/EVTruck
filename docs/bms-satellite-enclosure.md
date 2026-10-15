# Sealed BMS satellite enclosure

Each battery box has a square pocket on its outer wall that was cut for an
Amphenol SurLok Plus receptacle (sold by ampREVOLT). The satellite enclosure
clamps onto the wall over that pocket, and a printed flange clamps on from
the inside, so the bare BMSS24 board stays dry and its wiring passes straight
into the battery box.

Models (build123d + bdbox):

- `evtruck/bms_satellite/enclosure.py`: `SatelliteEnclosure`, presets `print` and `one-connector`
- `evtruck/bms_satellite/port_flange.py`: `PortFlange` (inner flange), preset `template` (drilling template)
- `evtruck/bms_satellite/port_interface.py`: hole, screw and o-ring sizes both sides share

Export STLs with `uv run bdbox export <model file> <dir> -f stl` (add `-a` for every preset).

## How it seals

```
        lid ── 2 mm o-ring cord in the wall rim groove
 ┌──────────────────────────────────┐
 │  bay  │   BMSS24 board           │◄── two M12 4-pin connectors (isoSPI in, out)
 └─┬───┬─┴──────────────────────────┘
   │pad│ ◄── 52 x 2 mm o-ring on the wall face, M4 heat-set inserts
 ══╛   ╘══ battery box wall (pocket + 25 mm wire hole)
   ╒═══╕ ◄── inner flange, 44 x 2 mm o-ring on the inside face
     ▲ four M4 socket head screws from inside the box
```

1. **Outside:** a round pad under the enclosure's wiring bay sits on the wall
   face. The 52 x 2 mm o-ring in its face goes around the whole pocket.
2. **Inside:** the printed flange sits on the inner face of the wall, with a
   44 x 2 mm o-ring around the wire hole and screws.
3. **Screws:** four M4 socket head screws go through the flange and the wall
   into heat-set inserts in the pad. They're inside both o-rings, so their
   holes stay dry and need no extra sealing. Use M4 x 10 mm: 2 mm of flange
   under the head plus the 2 mm wall leaves 6 mm in the inserts. M4 x 12
   also fits but bottoms out at the end of the 8 mm insert.
4. **Lid:** a 2 mm o-ring cord in a groove on the wall rim. The ten M3 lid
   screws go into bosses outside the seal.
5. **Wires:** the 25 mm wire hole passes the 14-pin cell-tap plugs, so
   pre-made harnesses thread through.

## Cutting the wall

The pocket isn't cut all the way through. Print the `template` preset: a
disc the size of the pad, with a square nub that drops into the pocket.

1. Check that the disc sits flat with nothing under it. The pad covers a
   64 mm circle centered on the pocket.
2. Drill the four 4.5 mm screw holes through the template.
3. Mark the 25 mm wire hole, then cut it with a hole saw or step drill.
   Deburr it, because the wires pass over its edge.

## isoSPI connectors

The chain runs MCU → box 1 → box 2 → box 3. Each enclosure has two M12
A-coded 4-pin connectors on the end wall by the board's isoSPI plugs: one
for the pair in (IPI/IMI) and one for the pair out (IPO/IMO). The holes
(16.2 mm) fit panel receptacles with an M16 x 1.5 rear thread. Leave box 3's
out connector capped.

Make the three cables to length from 2-pair twisted shielded cable with
field-attachable M12 plugs (screw terminals). Put one pair on pins 1-2 and
the other on pins 3-4, and wire both ends the same way.

The `one-connector` preset carries both pairs on one connector, but then
the cables have to be a branched harness.

## Print notes

- Use PETG or ASA, with 4+ perimeters and 100% infill around the grooves and
  the inserts. PLA softens too easily in a vehicle.
- Print the enclosure upright on its pad, with supports under the floor (the
  `print` preset lays out the body and the lid).
- Print the flange groove-side up.
- Inserts: M3 heat-set inserts 4.0 mm OD x 5.7 mm long for the lid and
  board. M4 inserts 5.7 mm OD x 8 mm long for the wall screws.

## Measurements

The board sizes were measured from ruler photos on 2026-10-15 (about ±1 mm),
with an 11 mm overall thickness confirmed by hand. The pocket is about 35 mm
square, and the box wall is 2 mm sheet metal.

| Parameter | Value | Notes |
|---|---|---|
| `PortInterface.pocket_size` | 35 mm | The outer o-ring must clear the pocket's corners |
| `PortInterface.wall_thickness` | 2 mm | Measured; sets the screw length (M4 x 10) |
| `board_length`, `board_width` | 100 x 74 mm | PCB outline; connectors add about 10 mm overall |
| `board_hole_spacing_length`, `_width` | 52 x 62 mm | Four plated M3 holes |
| `component_height` | 10 mm | Tallest part above the PCB |
