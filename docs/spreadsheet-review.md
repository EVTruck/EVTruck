# Truck Stuff.xlsx review (2026-10-02)

This is a review of [`truck-stuff.xlsx`](truck-stuff.xlsx), the project spreadsheet as exported from Google Sheets on 2026-10-02. Each problem has a GitHub issue, linked in parentheses.

The truck uses 7 Tesla 5.3 kWh modules (85 kWh pack, 55 lb each), installed in 3 battery boxes.

## What it tracks

| Sheet | What's in it | Key numbers |
|---|---|---|
| Project Management | 10 open tasks (BMS, charger, HV cable length, battery boxes, contactor box, cooling plumbing, data ports) | Only 3 tasks have an owner (Derek: buy modules; John: BMS, charger) |
| Truck specs | Stock truck figures | 2,800 lb curb, 4,400 lb GVW, 1,600 lb payload, 106 hp / 137 ft-lb, ~280 Wh/mile estimate |
| Conversion List | ~50 conversion parts with cost, links, notes, plus a cost-tally log | **$29,014.32** total; batteries $11,485 and motor kit $5,000 are the big items |
| Comparisons | Motor options (HyPer9HV picked), battery options, Tesla pack sizing for 5–8 modules | 7 modules = 159.6 V nominal, 176.4 V max, ~37 kWh |
| Conversion Weights | Parts removed vs. added | Net **+96.5 lb** |
| Truck Costs | Purchase, registration, tires, repair parts | Vehicle $1,913.51 + repairs $694.80 = **$2,608.31** |
| Maintenance | Fluid types and capacities (FS5W71C trans, GL-4/GL-5, DOT 3) | — |

All-in so far: about **$31,600** (conversion list + truck costs).

## Likely errors

1. **Truck Costs F5 ("Truck Cost including tools") double-counts the repair parts.** It's `SUM(F2, D:D)`, but F2 already includes D:D, so it adds $694.80 twice ($3,303.11). It also doesn't pull in any tools. (#15)
2. **Conversion List row 55 has a $147.52 cost with no item name.** It's included in the $29,014 total. (#16)
3. **Battery hose fittings: $298.50 doesn't match its note** ("$22.50 × 2 ports/box × 3 boxes" = $135). (#17)
4. **Comparisons D12: a 6.3 kWh Tesla module listed at $19,000.** Probably a typo (the 5.3 kWh one is $1,580). The "5.6 kWh Tesla" row is empty, and its link actually points to a 6.2 kWh module. (#18)
5. **CALB 180 pack weight uses 5.6 kg per cell, but the lbs column says 55 lb.** One of the two is wrong (5.6 kg is about 12 lb). (#19)
6. **Range math disagrees.** The pack table assumes 2.5 mi/kWh (400 Wh/mile), but Truck specs estimates 280 Wh/mile. At 280 Wh/mile, 7 modules gives about 130 miles, not 93. (#20)
7. **Cost-tally log is out of date.** Last entry (2026-06-18) is $28,614, while the current total is $29,014.32. (#21)
8. **Possible charger double-count.** Row 15 ($1,200) is a 3.3 kW charger + DC-DC combo, and row 32 "BMS/Charger" is another $420. Also, $420 looks low for the EVWest MCU + satellite board noted in Project Management. (#22)

## Incomplete

- **Parts with no cost yet:** HV shrink tubing, safety interlock, inertia switch, low-voltage cutoff, 12V fuses, fuse blocks, KSI relay, radiator, coolant reservoir, coolant lines, power steering, milspec shrink wrap, clutch fork dust cover. The real total will be higher than $29k. (#23)
- **Open questions in the notes:** Does the controller need its own thermostat? Can the BMS handle the interlock and the low-voltage cutoff? (#25)
- **Weight list is missing heavy items:** the battery boxes, contactor box, vacuum pump, charger/DC-DC, heater, new radiator, coolant and pumps. The +96.5 lb is low. Battery modules are estimated at 450 lb, but the 7 modules actually bought weigh 7 × 55 lb = 385 lb. (#24)
- **Truck specs:** the wheel-height labels have no measurements. (#26)
- **Project Management:** most tasks have no owner or priority. "Buy Tesla Modules" is still listed even though the tally says battery pricing was locked in June 2026. The Data Ports note still says "X number of data wires". Columns F/G are still named "Column 1/2". (#26)

## Small stuff

- The Hyper9HV stats say "kWh Peak/Continuous" but mean kW. (#27)
- The AC Motor and throttle reasons say "charge controller" but mean motor controller. (#27)
- Formulas use Google Sheets functions (MINUS, DIVIDE, MULTIPLY). They won't recalculate if the file is opened in Excel. (#27)
- 8 modules (201.6 V max) would exceed the HyPer9HV's 180 V limit, so 7 is the ceiling with this motor.
- The Conversion List total includes about $473 of tools and $216 of replacement parts, so the "conversion" number isn't purely conversion parts.
