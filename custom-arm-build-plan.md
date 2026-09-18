# Phase 2 — Custom Three-Revolute Arm: Build Plan and Checklists

*Design, fabrication, and control for a self-designed serial manipulator.*

**Prerequisite:** Phase 1 (auto-tracking camera gimbal) — complete.
**Successor:** Phase 3 (vision-based, voice-controlled manipulation on the SO-101).

**Goal:** Pick up an object with the arm and place it at a target location using joint-angle commands.

**Actuation:** Belt-driven NEMA 17 stepper at the base rotation (J1); dual MG996R servos at shoulder (J2); MG996R servo at elbow (J3); micro servo gripper.

---

## Part I — Reference

## 1. Objective and Scope

Design, build, and program a three-joint robotic arm capable of executing a pick-and-place sequence using direct joint-angle control.

### Configuration

| Joint | Axis | Actuator | Function |
|---|---|---|---|
| J1 | Vertical | NEMA 17 stepper, belt-driven | Base rotation |
| J2 | Horizontal | Dual MG996R servos | Shoulder |
| J3 | Horizontal, parallel to J2 | MG996R servo | Elbow |
| — | — | SG90 / MG90S servo | Gripper (binary open/close) |

---

## 2. The Base Joint

### 2.1 Why a belt-driven stepper at J1

The base joint carries the entire arm but produces no gravitational torque, since the load acts along the rotation axis. Torque demand is low. The stepper is justified by two other properties:

**Resolution.** A 1.8° motor at 1/16 microstepping through an 8.3125:1 belt reduction yields ~21,280 increments per revolution — roughly 0.017°. The joint effectively stops being an error source.

**Unlimited travel** (subject to cable routing, §2.4). A hobby servo is limited to approximately 180°.

The belt, rather than direct drive, additionally relieves the motor shaft of all axial load, keeps the motor serviceable without disassembling the joint, and lets the base sit flat rather than being raised on standoffs to clear a motor body.

### 2.2 The load case is a moment, not axial force

With the arm extended, the weight acts at a horizontal distance from the base axis, applying an **overturning moment** to the disc.

**Selected part: 6812-2RS thin-section deep groove bearing.** 60 mm bore, 78 mm outer diameter, 10 mm width, sealed and pre-greased.

### 2.3 Belt drive

**6 mm GT2, open length.** 133T disc at 84.6mm pitch diameter, 16T motor pulley, 8.3125:1 ratio. Custom belt tensioner.

### 2.4 Cable routing limits rotation

Software limit ±170°, service loop of slack cable through the centre bore.

---

## 3. Motor and Driver

**Motor:** Anet 42SHDC3025-24B (NEMA 17, 4-lead bipolar in 6-pin housing, 0.9A rated).

**Driver:** BigTreeTech TMC2209 via single-wire UART on Pi 5.
- UART port: `/dev/ttyAMA0` (GPIO 14 TX through 1kΩ resistor + GPIO 15 RX → TMC2209 RX/PDN_UART)
- Current: 630mA RMS (70% of rated)
- Microstepping: 1/16 with interpolation to 256
- Mode: StealthChop
- MS1/MS2: LOW (address 0x00)
- EN: tied LOW; enable controlled via TmcEnableControlToff register

---

## 4. Mechanical Design

### 4.1 Link geometry

120 mm upper arm, ~130 mm forearm.

### 4.2 Torque: the binding constraint at J2

Dual MG996Rs at J2, combined budget 10 kgf·cm (50% of rated).

| Contribution | Mass | Moment arm | Torque |
|---|---|---|---|
| Upper link | 50 g | 60 mm | 0.30 kgf·cm |
| Elbow servo | 55 g | 120 mm | 0.66 kgf·cm |
| Forearm | 50 g | 185 mm | 0.93 kgf·cm |
| Gripper assembly | 50 g | 250 mm | 1.25 kgf·cm |
| Payload | 50 g | 260 mm | 1.30 kgf·cm |
| **Total at shoulder** | | | **≈ 4.4 kgf·cm** |

5.6 kgf·cm of margin. Counterbalance likely unnecessary.

### 4.3 Joint construction at J2 and J3

**J2 (dual servo):** Two MG996Rs mounted side by side, both driving the same shaft through individual metal horns. Both servos receive the same PWM signal from the PCA9685. Calibrated offsets: servo 14 = 0, servo 15 = 36. Effective range: 36°–150°.

**J3 (single servo):** U-shaped fork with servo in one plate and 608ZZ bearing in the other.

### 4.4 Printing

- Orient links so bending loads act **across** layers rather than along them
- PETG for load-bearing parts; PLA acceptable for base plate and covers
- Four or more perimeters on structural parts
- Print bearing seats slightly undersize and open them by boring or careful sanding

---

## 5. Electrical

| Rail | Voltage | Current | Serves |
|---|---|---|---|
| Servo | 6 V | ≥7 A | J2 (×2), J3, gripper, PCA9685 |
| Stepper | 12 V | ≥2 A | J1 driver |

12V supply with buck converter stepping down to 6V for the servo rail. Shared ground between all rails. 1000 µF bulk capacitance across the servo rail.

---

## 6. Software

### 6.1 Joint abstraction layer

Per-joint interface exposing `move_to(angle)`, hiding whether the command becomes a pulse width or a step target. Three implementations: `StepperJoint`, `ServoJoint`, `DualServoJoint`.

Configuration loaded from YAML via `RobotConfig.from_yaml()`.

### 6.2 Robot interface

`Robot` class that owns all joints and the shared ServoKit. Methods: `move_to_angles()`, `home()`.

### 6.3 Pick-and-place sequence

Sequence a full pick-and-place: approach, descend, close gripper, lift, transit, descend, release, retreat. All via direct joint-angle commands.

---

## 7. Calibration

**Servos (J2, J3, gripper).** Accept a pulse width, report nothing. Per-servo pulse width calibration and offset trimming required.

**Stepper (J1).** Position known exactly provided no steps have been lost. Mitigated by conservative acceleration limits.

---

## Part II — Checklists

## Mechanical — Design and Fabrication

- [x] Weigh every candidate component on a scale reading to 1 g
- [x] Complete the torque calculation with measured masses
- [x] Revise link lengths until shoulder torque is within dual-servo budget
- [x] Probe the stepper connector; determine winding configuration
- [x] Read the motor's rated phase current from its label
- [x] Wire TMC2209 driver via UART and verify stepper runs
- [x] Choose the belt reduction ratio and disc tooth count; 133T disc, 8.3125:1 ratio with 16T motor pulley
- [x] Order the 6812-2RS bearing, GT2 open belt, pulleys, and driver
- [x] Print and test servo joint (M1a): 300g at 150mm per servo confirmed
- [x] Print and test base joint (M1b): bearing, belt, tensioner, motor all verified
- [x] Model the complete arm in CAD
- [x] Design the centre bore for cable routing
- [x] Design and print custom belt tensioner
- [x] Print both fork plates as single body for datum sharing
- [x] Install heat-set inserts and assemble the arm
- [x] Print revised parts and reassemble
- [x] Measure actual link lengths on the physical arm
- [x] Verify belt tension; confirm no skipping under maximum acceleration
- [x] Print and fit the gripper; verify jaw travel and closing force

## Electrical

- [x] Wire both power rails (12V stepper, 6V servo via buck converter); tie grounds together
- [x] Fit bulk capacitance across the servo rail
- [x] Confirm cable service loop functions through full J1 travel

## Software

- [x] Implement the joint abstraction layer with servo and stepper backends
- [x] Implement YAML config parsing with RobotConfig.from_yaml()
- [x] Calibrate dual J2 servos: offset_14 = 0, offset_15 = 36, effective range 36°–150°
- [ ] Put the reduction ratio in one constant; derive steps-per-degree from it
- [ ] Enforce joint limits in software for all joints
- [ ] Implement Robot.home() — move all joints to a known starting position
- [ ] Implement Robot.move_to_angles() — coordinated joint moves
- [ ] Sequence a full pick-and-place cycle
- [ ] **Project complete:** arm picks up an object and places it at a target location

---

## Part III — Reference Material

## 8. Parts List

**Actuators**
- NEMA 17 stepper × 1 (salvaged) — J1
- MG996R metal-gear servo × 3 — J2 (×2), J3
- SG90 or MG90S micro servo × 1 — gripper
- MG996R × 1 spare

**Motion control**
- TMC2209 stepper driver × 1, with heatsink
- PCA9685 16-channel PWM driver × 1 (carried over from Phase 1)
- Raspberry Pi 5 (existing)

**Belt drive**
- GT2 open belt, 6 mm wide, 2 m
- 16T GT2 pulley, 5 mm bore
- 133T printed disc
- Custom belt tensioner (printed)

**Bearings**
- 6812-2RS thin-section bearing × 1 — 60×78×10 mm, J1
- 608ZZ bearings × 4 — J2 and J3, plus one spare pair
- 8 mm shaft stock or M8 shoulder bolts × 2 — stub shafts

**Power**
- 12 V supply, 2 A minimum — stepper rail
- Buck converter, 12V → 6V, 5A+ — servo rail
- 1000 µF electrolytic capacitors × 2
- Inline fuse, 5 A
- Terminal blocks, 18 AWG wire, Dupont jumpers

**Fasteners**
- M3 socket-head screws, 8–30 mm, ~50
- M3 nuts and washers, ~50
- M3 heat-set inserts, ~30, plus installation tip
- M2 screws, 6–10 mm — horn attachment
- Metal servo horns × 3
- Threadlocker, medium strength

**Printing**
- PETG, 1 kg — structural
- PLA, 1 kg — base plate, covers, test fitments
