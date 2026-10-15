# Sealed BMS satellite enclosure and port plug

Each battery box has a square port that was cut for the Amphenol 350 A sealed
power receptacle (sold by ampREVOLT). These two 3D-printed parts use that port
to bring the BMSS24 satellite's wiring out of the box, and keep the bare board
dry in its own sealed enclosure.

Models (build123d + bdbox):

- `evtruck/bms_satellite/port_plug.py`: `PortPlug`, presets `fit-test` and `single-seal`
- `evtruck/bms_satellite/enclosure.py`: `SatelliteEnclosure`, preset `print`
- `evtruck/bms_satellite/coupling.py`: spigot and socket sizes both parts share

Export STLs with `uv run bdbox export <model file> <dir> -f stl` (add `-a` for every preset).

## How it seals

```
        lid ── 2 mm o-ring cord in the wall rim groove
 ┌───────────────────────────────┐
 │ bay │   BMSS24 board          │   enclosure
 │ ┌─┐ │                         │◄── M12 4-pin panel connector (isoSPI in + out)
 └─┤ ├─┴─────────────────────────┘
   │ │ ◄── socket over the spigot, two 20 x 2 mm o-rings
 ══╧═╧══ port plug flange (M4 flat head screws in the existing holes)
   █ █  ◄── square body in the port, two 2 mm o-ring cords (radial seal)
 battery box wall
```

1. **Port to plug:** two o-ring cords in grooves around the square body seal
   against the port walls. This is a radial seal, so the flange doesn't need to
   be flat against the plate. A 2 mm cord bends tightly around the port's
   corners, so put a little silicone grease on it and check it with the
   fit-test print. If the port is less than 9.5 mm deep, use the
   `single-seal` preset.
2. **Plug to enclosure:** two 20 x 2 mm o-rings on a round 24 mm spigot. This
   is a round piston seal, which is the most reliable o-ring joint you can
   print. Two M3 screws into heat-set inserts in the plug hold the enclosure
   down. Put sealing washers under their heads, because these holes are inside
   the box.
3. **Lid:** a 2 mm o-ring cord in a groove on the wall rim. The ten M3 lid
   screws go into bosses outside the seal.
4. **Wires:** pot the plug's 14 mm wire bore with epoxy after the cell-tap and
   thermistor wires are pulled through. Then the enclosure doesn't share air
   or moisture with the battery box, and the wires get strain relief.
5. **Mounting screws:** the port's two existing holes are outside the port
   seal. Put bonded sealing washers under the nuts inside the battery box.

## isoSPI connector

One 4-pin sealed connector carries the whole chain: IPI/IMI in from the
previous device and IPO/IMO out to the next one. The default hole (16.2 mm)
fits M12 A-coded panel receptacles with an M16 x 1.5 rear thread. Each
inter-box cable then carries two twisted pairs. On the last satellite, the
out pair stays unconnected.

## Print notes

- Use PETG or ASA, with 4+ perimeters and 100% infill around the grooves and
  the socket. PLA softens too easily in a vehicle.
- Print the plug standing on the square body, with supports under the flange.
- Print the enclosure upright and the lid flat (the `print` preset lays them out).
- Use M3 heat-set inserts 4.0 mm OD x 5.7 mm long.

## Measurements still needed

The defaults were estimated from photos and the Serpac WM031 case size. Check
them before printing anything but the fit test:

| Parameter | Default | What to measure |
|---|---|---|
| `port_width`, `port_height` | 38 mm | Port opening |
| `port_corner_radius` | 3 mm | Corner radius of the opening |
| `port_depth` | 10 mm | Plate thickness at the port, and whether the port goes all the way through |
| `mount_hole_spacing` | 46 mm | Center-to-center of the two mounting holes |
| `mount_hole_offset` | -11.5 mm | Hole centers from the port center, toward the holes |
| `board_length`, `board_width` | 125 x 74 mm | BMSS24 board outline |
| `board_hole_inset` | 4 mm | Board mounting holes from the edges |
| `component_height` | 18 mm | Tallest part on the board, including mated plugs |
