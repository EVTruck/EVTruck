# Wiring 3 Dilithium satellites to the Thunderstruck MCU v1.0

Layout: 3 battery boxes with 2, 2 and 3 Tesla 6S modules (12 / 12 / 18 cells), one satellite per box.

Sources (Thunderstruck):
- MCU wiring diagram: https://www.thunderstruck-ev.com/images/companies/1/Circuits/MCU-Basic-Wiring.pdf?1672268007712
- MCU manual: https://www.thunderstruck-ev.com/images/companies/1/BMS/MCU-Manual.pdf
- BMSC manual (same BMSS24 hardware): https://www.thunderstruck-ev.com/images/companies/1/BMS/BMSC-Manual.pdf
- Harness test guide: https://www.thunderstruck-ev.com/images/companies/1/BMS/BMSHarnessVerify-Safety1.pdf?1680799098478
- EVWest Tesla tap board pinout: https://www.thunderstruck-ev.com/images/product/Tesla%20Model%20S%205.3%20BMS%20Board%2022.pdf?1785369108394

Items marked *(inferred)* are not stated in the docs. Get Thunderstruck to confirm them before relying on them.

## 1. Communication chain (IsoSPI)

Daisy-chain all three satellites off **port A** on MCU Connector A:

```
MCU IPO_A (pin 6) ──► Sat 1 IPI      Sat 1 IPO ──► Sat 2 IPI      Sat 2 IPO ──► Sat 3 IPI
MCU IMO_A (pin 7) ──► Sat 1 IMI      Sat 1 IMO ──► Sat 2 IMI      Sat 2 IMO ──► Sat 3 IMI
```

- Use one **twisted pair** per hop. The terminals take 20 to 24 AWG wire, and 20 AWG stranded is recommended. Route the pairs away from motor, controller and traction cables, not parallel to them.
- No terminating resistors are needed, because they are built into every Dilithium device.
- Leave Sat 3's output unconnected.
- Port A takes up to 8 measurement devices (LTCs). Each BMSS24 has 2 LTCs and each BMSS18 has 1, so 3 satellites fit on port A alone. Port B (pins 8 and 9) is available if one box is far away, but the docs don't require using it.
- LTCs are numbered A1, A2 and so on in chain order. Cell order can be fixed later with `cmap`.
- The satellites take no 12V. They are powered by the cells they measure, and only the MCU gets 12V and GND.

## 2. Cell harness per box

Wire each harness in series order, starting at the box's most negative point:

- w0 / C0 → the first module's **C1-** (EVWest board pos 8, black)
- w1 to w6 → the first module's **C1+ to C6+** (pos 10, 7, 11, 6, 12, 5)
- w7 to w12 → the second module's C1+ to C6+, and so on

Rules:
- A cell group must **not span a fuse, contactor or service disconnect**. If that device opens while the harness is connected, the satellite can be destroyed. With one satellite per box this holds as long as no fuse or disconnect sits *inside* a box. *(inferred)*
- If a group has fewer cells than the satellite has inputs, tie the unused top inputs to the last positive tap.
- Minimum group size is 4 cells on a BMSS24 LTC and 6 cells on a BMSS18.
- Only one architecture can be set per MCU, so don't mix BMSS24 and BMSS18 satellites. *(inferred)*
- Thermistors: each LTC takes 5. Find the Tesla pairs on pos 1 to 4 (5 to 10 kΩ) and enable them with `enable th`.

**Satellite type:**
- **BMSS18:** one LTC per box, carrying 12, 12 and 18 cells. Tie the top 6 inputs together in each 12-cell box.
- **BMSS24 (2 LTCs each):** in the 12-cell boxes, use 6 + 6 so both LTCs are powered. In the 18-cell box, use 12 + 6, split at a module boundary.

## 3. Test before plugging in

1. **Test every harness** on the matching tester board: the 12-cell board for BMSS24, the 18-cell board for BMSS18. With the meter's negative lead on C0, voltage should rise by one cell at each pad. A miswired harness can permanently destroy the satellite.
2. The 18-cell box can reach about 75V (18 × 4.2V). Work on a nonconductive surface with taped probes.
3. Plug a harness into its satellite **last**, and unplug it **first** before changing any pack connections.

## 4. Configure the MCU (serial terminal, 115200 baud)

```
bms
set arch ltc18        (or ltc12 for BMSS24)
show ltc              (check that all LTCs are detected)
show cells            (check that every cell reads plausibly)
set cmap A1 1 1 ...   (only if chain order differs from cell order; check the syntax in the manual)
enable th all
lock                  (saves the cell census and clears NOTLOCKED)
```

Thunderstruck can confirm the exact `cmap` syntax and the IsoSPI connector part number: connect@thunderstruck-ev.com, 707-578-7973.
