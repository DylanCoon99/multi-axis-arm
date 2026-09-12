# Phase 2 — Custom Three-Revolute Arm: Build Plan and Weekly Checklists

*Design, fabrication, kinematics, and control for a self-designed serial manipulator.*

**Prerequisite:** Phase 1 (auto-tracking camera gimbal) — complete.
**Duration:** Ten weeks, with the software and mechanical tracks running in parallel.
**Successor:** Phase 3 (vision-based, voice-controlled manipulation on the SO-101).

**Actuation:** Belt-driven NEMA 17 stepper at the base rotation (J1); dual MG996R servos at shoulder (J2); MG996R servo at elbow (J3); micro servo gripper.

---

## Part I — Reference

## 1. Objective and Scope

Acquire the mathematics of serial manipulators and validate it against a physical machine of your own design.

Designing the arm rather than printing a kit means you choose the link lengths, and therefore own the workspace geometry and singularity structure rather than inheriting them. The cost is two to three weeks of mechanical design and print iteration, and at least two revisions.

### Configuration

| Joint | Axis | Actuator | Function |
|---|---|---|---|
| J1 | Vertical | NEMA 17 stepper, belt-driven | Base rotation |
| J2 | Horizontal | Dual MG996R servos | Shoulder |
| J3 | Horizontal, parallel to J2 | MG996R servo | Elbow |
| — | — | SG90 / MG90S servo | Gripper (binary open/close) |

J2 and J3 have parallel axes; J1 is perpendicular to both. **This orthogonality is what makes the inverse kinematics tractable** — J1 is determined entirely by the horizontal bearing to the target, and rotating into the vertical plane containing the arm reduces J2 and J3 to a two-link planar problem solvable on paper.

**Do not add a wrist.** It would triple the difficulty of the inverse kinematics and introduce singularity behaviour that is hard to reason about on a first arm.

**Consequence to accept:** with three joints you determine end-effector position only. The gripper's approach angle is whatever falls out of the J2/J3 solution — steeper for near targets, shallower near the workspace boundary. Design the jaws to tolerate a range of approach angles.

---

## 2. The Base Joint

### 2.1 Why a belt-driven stepper at J1

The base joint carries the entire arm but produces no gravitational torque, since the load acts along the rotation axis. Torque demand is low. The stepper is justified by two other properties:

**Resolution.** A 1.8° motor at 1/16 microstepping through a 5:1 belt reduction yields 16,000 increments per revolution — roughly 0.023°. At 300 mm reach that is 0.12 mm of lateral increment, well below the mechanical repeatability of the rest of the arm. The joint effectively stops being an error source.

**Unlimited travel** (subject to cable routing, §2.4). A hobby servo is limited to approximately 180°.

The belt, rather than direct drive, additionally relieves the motor shaft of all axial load, keeps the motor serviceable without disassembling the joint, and lets the base sit flat rather than being raised on standoffs to clear a motor body.

### 2.2 The load case is a moment, not axial force

With the arm extended, the weight acts at a horizontal distance from the base axis, applying an **overturning moment** to the disc. A 500 g arm with its centre of mass 150 mm out produces roughly 7.5 kgf·cm of tipping load.

A small thrust bearing cannot resist this — it carries force through a single small annulus, so any tipping moment simply lifts one side. **What resists a moment is a bearing of large diameter**, where the moment is reacted as a force couple across the race.

**Selected part: 6812-2RS thin-section deep groove bearing.** 60 mm bore, 78 mm outer diameter, 10 mm width, sealed and pre-greased. Ten to twenty dollars from VXB, Bearings Direct, or Amazon.

Three reasons it fits:

- The 60 mm bore is a genuine open centre — cables or a slip ring pass straight through the rotation axis
- The 78 mm outer diameter gives adequate moment arm for the overturning load
- The 10 mm section disappears into a printed seat without adding stack height

The static rating of 10,600 N is roughly two orders of magnitude above the imposed load. That matters less for capacity than for what it implies about clearance: an underloaded precision bearing runs with essentially no play.

**Sizing consequence:** the disc must be at least as large as the 78 mm outer race. An 80-tooth GT2 pulley is only 51 mm pitch diameter, so **size the disc to the bearing rather than the reverse** — 100 or 120 teeth gives 5:1 or 6:1 reduction as a bonus and comfortably accommodates the seat.

*Alternatives considered:* a 4-inch Lazy Susan turntable bearing is cheaper and larger, but is stamped steel with loose races and a millimetre of play that would dominate the M7 repeatability measurement. A crossed-roller turntable is what a commercial arm uses, but at sixty to two hundred dollars it is disproportionate to a first arm whose printed structure contributes more compliance than the bearing does.

### 2.3 Belt drive

**6 mm GT2, open length, joined with clamps.** Do not buy a closed loop. Open belt costs a few dollars per metre, accommodates the fact that your centre distance will change between revisions, and turns a sizing error into a five-minute fix rather than a reorder.

**Centre distance is a design decision, not a derived value.** Position the motor so the belt wraps at least 90° around the small pulley — aim for a centre distance of roughly two to three times the large pulley's radius. For a 100-tooth disc at 63.7 mm pitch diameter, that is 70 to 100 mm.

Belt length, if you need it:

```
L ≈ 2C + (π/2)(D₁ + D₂) + (D₂ − D₁)² / (4C)

GT2 pitch diameter = teeth × 2 / π
  20T  = 12.73 mm
  100T = 63.66 mm
```

At C = 85 mm this gives approximately 298 mm.

**Slot the motor mount** along the line between the two shaft centres. Tensioning is then a matter of sliding the motor away from the disc and locking it. Too loose and teeth skip under acceleration — silent step loss by another mechanism. Too tight and you load the motor shaft unnecessarily.

**Raise the motor** on a printed mount so its own output shaft lands at belt height, with the pulley seated close against the motor face. A shaft extension or coupled stub introduces compliance and a cantilever the motor bearings were not sized for.

**Print the disc flat**, teeth formed by the perimeters in the XY plane, four or more perimeters so teeth are solid material rather than partly infill.

### 2.4 Cable routing limits rotation

Everything above the disc — two servos, the gripper, any future sensor — needs power and signal from below, and those cables cross the rotating interface. **Design the centre bore now**; adding one later means reprinting the disc, the bearing seat, and the base.

| Option | Rotation available | Cost |
|---|---|---|
| Software limit ±170°, service loop of slack cable | Under one turn | Free |
| Cable bundle down the rotation axis through the bore | Several turns | Free |
| Slip ring capsule, 12.5 mm, 6 or 12 circuits | Unlimited | ~$15 |

### 2.5 Homing

The stepper does not know its position at power-up. **J1 requires a reference switch and a homing routine executed before any commanded motion is permitted.** Without it, the arm will drive into its own wiring on the first move after a power cycle.

A flag on the rotating disc trips a microswitch fixed to the base. Choose the trip angle deliberately — a point at the rear of the workspace where the arm is unlikely to be operating and a slow sweep is harmless.

**Silent failure.** A servo that cannot reach position buzzes audibly. A stepper that loses steps does so quietly, and every subsequent position carries the offset with no indication. Re-home periodically and treat any unexplained discrepancy as suspected step loss until eliminated.

**Put the reduction ratio in one place** and derive steps-per-degree from it. A 1.8° motor at 1/16 microstepping through 5:1 is 16,000 steps per column revolution — never hard-code that product somewhere and lose track of which number you meant.

---

## 3. Motor and Driver

### 3.1 Identify the winding configuration first

A NEMA 17 is a frame size, not a winding configuration. Six leads almost always indicates a **unipolar-capable** motor: two coils, each with a centre tap. Your driver — A4988, DRV8825, TMC2209 — is a bipolar driver and expects four wires.

A six-lead motor can be driven bipolar: leave both centre taps disconnected and use the four coil ends. This gives the full winding and more low-speed torque than the half-coil alternative.

**Six pins on a connector does not necessarily mean six leads on the motor.** Printer steppers frequently use a six-position housing with only four positions populated. Verify with a multimeter before buying anything:

- Two isolated pairs, a few ohms each → four-lead bipolar motor in a six-pin housing. Wire directly.
- Groups of three with a centre tap, where the outer pins read roughly twice the resistance of either outer pin to the middle → genuine six-lead unipolar. Identify the two centre taps, insulate them individually, wire the four ends as two pairs.
- Five leads with both taps joined internally → cannot be driven bipolar; replace the motor. Uncommon on printer steppers.

### 3.2 Driver selection

| Driver | Microstepping | Notes | Cost |
|---|---|---|---|
| TMC2209 | to 1/256 | Substantially quieter via StealthChop; recommended if buying | $6–10 |
| DRV8825 | to 1/32 | Higher current than A4988; audibly noisier | Salvage |
| A4988 | to 1/16 | Entirely adequate; noisiest | Salvage |

Requires a StepStick carrier or breakout board, plus a heatsink on the exposed pad.

**Set the current limit by measurement, not by ear.** Find the motor's rated phase current from its label — typically 1.2 to 1.7 A. Set the reference voltage with a multimeter: roughly `Vref = I × 8 × Rsense` for the A4988, `Vref = I / 2` for the DRV8825. Target about 70 percent of rated current; the duty cycle is light and cooler operation is worth more than peak torque here.

---

## 4. Mechanical Design

### 4.1 Link geometry

Two links of approximately equal length maximize workspace area for a given total reach. Suggested scale 120–180 mm per link. **Do not finalize before completing the torque calculation in §4.2 and the workspace plot in §6.5.** Both will likely revise them downward.

### 4.2 Torque: the binding constraint at J2

Compute static torque at the shoulder with the arm fully extended, summing each mass times its distance from the joint — **including the links themselves**, not merely the payload.

A single MG996R is rated at approximately 10 kgf·cm at 6 V. With dual MG996Rs at J2, the combined rating is roughly 20 kgf·cm. **Design to no more than half that (10 kgf·cm)** for dynamic margin.

Worked illustration, 120 mm upper arm, 130 mm forearm:

| Contribution | Mass | Moment arm | Torque |
|---|---|---|---|
| Upper link | 50 g | 60 mm | 0.30 kgf·cm |
| Elbow servo | 55 g | 120 mm | 0.66 kgf·cm |
| Forearm | 50 g | 185 mm | 0.93 kgf·cm |
| Gripper assembly | 50 g | 250 mm | 1.25 kgf·cm |
| Payload | 50 g | 260 mm | 1.30 kgf·cm |
| **Total at shoulder** | | | **≈ 4.4 kgf·cm** |

This is well within the 10 kgf·cm dual-servo budget, with roughly 5.6 kgf·cm of margin. **Perform this with your own measured masses before printing anything.**

The stepper does not appear here — it sits on the base, below J2, and contributes nothing to the shoulder moment. That is the principal mechanical advantage of the arrangement.

### 4.3 Joint construction at J2 and J3

**Do not load the servo output spline in bending.** This is the most common failure in printed arms.

**J2 (dual servo):** Two MG996Rs mounted side by side, both driving the same shaft through individual metal horns. Both servos receive the same PWM signal from the PCA9685. The fork must be wide enough to seat both servos with their horns engaging a common cross-shaft. A 608ZZ bearing in the opposite plate carries the radial load; the horns transmit torque only. Watch for buzzing or heat from minor unit-to-unit variation between the two servos — the gearbox compliance absorbs small differences, but if one servo fights the other noticeably, trim its pulse range slightly.

**J3 (single servo):** A U-shaped fork carries the servo in one plate and a bearing in the other:

- The servo spline engages a metal horn bolted to the distal link. **The horn transmits torque only.**
- A stub shaft integral to the distal link runs in a 608ZZ bearing seated in the opposite plate. **The bearing carries the radial load.**
- Both fork plates must be rigidly joined by a yoke. If they splay, shaft and spline lose alignment, binding the bearing and loading the spline in exactly the manner the design prevents.

**Concentricity between spline and bearing bore is the tolerance that matters most.** Print both plates in the same orientation and, where possible, as a single body so the two features share a datum rather than being aligned during assembly.

Bore the stub shaft to a light interference fit, or use a shoulder and retaining screw. A loose shaft is a backlash source that appears directly in the M7 measurement.

### 4.4 Printing

- Orient links so bending loads act **across** layers rather than along them
- PETG for load-bearing parts; PLA acceptable for base plate and covers
- Four or more perimeters on structural parts — perimeter count matters more than infill for bending stiffness
- Generous fillets where links meet joint housings
- Print bearing seats slightly undersize and open them by boring or careful sanding rather than trying to hit the dimension directly

### 4.5 Counterbalancing

An extension spring or counterweight on the shoulder substantially reduces static load. **Defer to the second revision**, once the first has revealed actual sag. With dual servos at J2, the torque budget has substantial margin, so a counterbalance may prove unnecessary.

---

## 5. Electrical

| Rail | Voltage | Current | Serves |
|---|---|---|---|
| Servo | 6 V | ≥7 A | J2 (×2), J3, gripper, PCA9685 |
| Stepper | 12 V | ≥2 A | J1 driver |

**Tie the grounds together.** Without a common reference the step and direction signals have no defined level relative to the driver.

Retain 1000 µF bulk capacitance across the servo rail near the connectors, as established during the gimbal. Fit a heatsink to the stepper driver.

---

## 6. Software Track

### 6.1 Rigid-body transforms
Rotation matrices, homogeneous 4×4 transforms, composition along a kinematic chain. Forward kinematics is the product of link transforms.

**Skip the formalisms.** For a three-joint arm you do not need product-of-exponentials or Denavit-Hartenberg parameters. Both exist to systematize FK for arms with many joints and awkward geometry; yours has three joints and a convenient geometry, so composing transforms directly is shorter, clearer, and produces identical answers. Learn enough about DH to recognize a parameter table if you meet one in someone else's code — that is a twenty-minute exercise, not a chapter.

### 6.2 Analytical inverse kinematics
Begin with the two-link planar case — small enough to solve on paper, rich enough to expose two solutions (elbow-up and elbow-down), the workspace boundary, the unreachable interior region when link lengths differ, and the singularity at full extension.

For your arm: **J1 is determined by the horizontal projection of the target; the remainder reduces to the two-link planar case in the vertical plane containing the arm.** Derive this yourself for your own geometry. Do not copy it.

### 6.3 Numerical inverse kinematics
Construct the manipulator Jacobian. Implement three solvers **in order**: Jacobian transpose (simple, slow); pseudoinverse (faster, unstable near singularities); damped least squares (stable, what production systems use). The sequence makes the motivation for damping self-evident.

### 6.4 Joint abstraction layer
Define a per-joint interface exposing `move_to(angle)` and `current_angle()`, hiding whether the command becomes a pulse width or a step target. Two concrete types behind it: one wrapping the PCA9685 channel, one wrapping the stepper driver.

**Do this early.** The distinction must not leak into trajectory code, because Phase 3 replaces all four actuators with serial-bus servos and only this layer should change.

**Asymmetry to remain conscious of:** the velocity profile has real authority over J1, where you generate every step pulse. For servo joints it is advisory — the servo's internal controller decides how it reaches the commanded position.

Use **AccelStepper** for step timing rather than writing pulse generation yourself.

### 6.5 Workspace analysis before printing
Sweep the joint ranges, accumulate end-effector positions, plot the cloud. J1's near-unlimited travel makes the workspace a solid of revolution rather than the partial sector a servo base would produce. **You will likely revise link lengths on the strength of this plot. It costs nothing now and costs a print later.**

### 6.6 Trajectory generation
Joint-space interpolation with a trapezoidal velocity profile, then quintic polynomial interpolation, then straight-line motion in task space. The third can fail mid-trajectory if the path crosses a singularity or exits the workspace. **Induce that failure deliberately once.**

### 6.7 Homing and startup sequence
Drive J1 slowly toward the limit switch; stop on trigger; zero the step counter; command servos to a defined home pose; only then accept motion commands. Refuse all motion until homing completes. Treat a homing timeout as a hard fault.

### 6.8 URDF model
Describe the arm in URDF as the design solidifies. Loading it into PyBullet and verifying simulated forward kinematics against measured physical positions gives a digital twin, validates the model, and produces an artefact reusable in Phase 3.

### 6.9 Tooling

| Tool | Role |
|---|---|
| NumPy, Matplotlib | Sufficient for §6.1–6.6 entirely |
| AccelStepper | Step timing and acceleration for J1 |
| Adafruit CircuitPython ServoKit | PCA9685 interface, as used in Phase 1 |
| `roboticstoolbox-python` | Reference implementation for checking your own work |
| PyBullet | Lightweight simulator, straightforward URDF loading |

**Implement first, compare second.** The pedagogical value resides entirely in the implementation.

---

## 7. Calibration and the Open-Loop Problem

Neither actuator type reports actual position, and the two fail differently.

**Servos (J2, J3, gripper).** Accept a pulse width, report nothing. Gravitational sag varying with configuration; backlash on direction reversal; a nonlinear, per-unit mapping from pulse width to angle with substantial variation between nominally identical units.

**Stepper (J1).** Position known exactly *provided no steps have been lost*. Loss is silent. Mitigated by periodic re-homing and conservative acceleration limits.

You met calibration on the gimbal, where it was invisible because the camera closed an outer loop that absorbed the error. **Here there is no outer loop.** Whatever error exists propagates directly to end-effector position and stays there. That absence is the pedagogical point of the phase.

---

## Part II — Weekly Checklists

## Week 1 — Concept design and first mathematics

**Mechanical**
- [x] Weigh every candidate component on a scale reading to 1 g: servos, printed link estimates, gripper, bearings
- [x] Complete the §4.2 torque calculation with measured masses, not catalogue estimates
- [x] Revise link lengths until shoulder torque is at or below 10 kgf·cm (dual-servo budget), or accept that a counterbalance is required
- [x] Probe the stepper connector with a multimeter; record the resistance between every pin pair
- [x] Determine whether the motor is four-lead bipolar or six-lead unipolar; identify and insulate centre taps if present
- [x] Read the motor's rated phase current from its label; record it
- [x] Wire TMC2209 driver via UART and verify stepper runs (test_stepper.py)
- [x] Choose the belt reduction ratio and disc tooth count; 133T disc at 84.6mm pitch diameter, 6.65:1 ratio with 20T motor pulley
- [x] Order the 6812-2RS bearing, GT2 open belt, 20T pulleys, and any driver not salvaged

**Software**
- [ ] Watch *Modern Robotics* Ch. 3 videos on rotation matrices and frames (~30 min): https://www.youtube.com/playlist?list=PLggLP4f-rq02vX0OQQ5vrCxbJrzamYDfx
- [ ] Watch *Modern Robotics* Ch. 4 videos on forward kinematics (~20 min): same playlist
- [ ] Read Angela Sodemann's FK walkthrough for a practical worked example: https://www.youtube.com/watch?v=VjsuBT4Npvk
- [ ] Work through FK by hand for your 3-joint arm: pick 3 joint angle sets, compute end-effector position with pen and paper
- [ ] Implement rotation matrices and homogeneous transforms in SE(3)
- [ ] Implement forward kinematics as a product of link transforms
- [ ] Verify FK code against your hand calculations at the same three configurations

**Gate:** do not order printed-part filament or begin CAD until the torque calculation closes.

**Reading** *(roughly two hours)*
- *Modern Robotics* YouTube playlist Ch. 3–4 (listed above). Short segments, practical, and free. Skip the proofs — focus on how to build a 4×4 transform and multiply a chain of them.
- Angela Sodemann's FK video walks through a complete example with real joint geometry. Good for seeing the process end-to-end before implementing.
- Pololu's product page for your specific driver, for the Vref formula. It differs between drivers and between board revisions, so confirm against your board rather than a video.
- Your stepper's label. The rated phase current is the only figure you strictly need.

---

## Week 2 — Test articles and workspace *(M1, M2)*

**Mechanical — M1a, servo joint**
- [x] Print one fork, one link, one horn interface
- [x] Assemble with 608ZZ bearing and metal servo horn
- [x] Hang the calculated load at the calculated moment arm
- [x] Confirm the servo holds without buzzing and with acceptable sag (300g at 150mm per servo, dual J2 gives ~9 kgf·cm)
- [x] Record any print-setting changes required

**Mechanical — M1b, base joint**
- [x] Print the bearing seat and a test disc
- [x] Fit the 6812-2RS; verify the press fit is snug without cracking the print
- [x] Mount the motor on a slotted plate; fit pulley and belt
- [x] Set the driver current by measuring Vref; target 70 percent of rated
- [x] Design and print custom belt tensioner
- [x] Confirm the belt wraps at least 90° on the small pulley
- [x] Rotate the disc by hand; check for play, binding, and belt tracking
- [x] Command a full revolution under power; listen for skipped teeth

**Software**
- [ ] Sweep joint ranges and plot the reachable workspace
- [ ] Finalize link lengths on the strength of the plot
- [ ] **M2 complete:** FK verified, geometry frozen

**Gate:** both test articles pass before full CAD begins.

**Reading** *(roughly one hour)*
- A GT2 pitch-diameter reference. You need `d = teeth × 2 / π` and the idea of wrap angle. Nothing deeper.
- Comments on a few printed GT2 pulley listings on Printables, for tooth-profile print settings before committing your own disc.

---

## Week 3 — Full CAD and analytical inverse kinematics

**Mechanical**
- [x] Model the complete arm in CAD using frozen link lengths
- [x] Design the centre bore through disc, bearing, and base for cable routing
- [x] Decide the cable strategy: software limit, axial bundle, or slip ring
- [x] Slot the motor mount along the shaft-centre line
- [ ] Design the homing flag and switch bracket; choose the trip angle
- [x] Print both fork plates as a single body where possible, for datum sharing
- [x] Start the first full print run

**Software**
- [ ] Derive closed-form IK for the two-link planar case by hand
- [ ] Extend to your three-joint geometry, decomposing J1 from the horizontal projection
- [ ] Implement the solver returning both elbow-up and elbow-down solutions
- [ ] Add an explicit unreachable-target signal

**Reading** *(roughly two hours — the most valuable reading in the plan)*
- Any worked derivation of two-link planar inverse kinematics. There are dozens; find one that uses the law of cosines and `atan2` rather than one that jumps to a matrix method. Work through it with pen and paper for your own link lengths rather than reading passively — this single derivation is the conceptual core of the whole phase.
- Peter Corke's *Robot Academy* short lessons on inverse kinematics, if you want a video treatment. They are five to ten minutes each and deliberately applied.
- Slip ring product documentation, if you chose that route. Capsule dimensions dictate your centre bore, so read before finalizing the CAD.

---

## Week 4 — First assembly and IK verification *(M3)*

**Mechanical**
- [x] Install heat-set inserts in all printed parts
- [x] Assemble the arm
- [x] Record every fit problem, tolerance miss, and interference as you find it
- [x] Identify the first revision's scope; do not fix problems piecemeal

**Software**
- [ ] Verify IK by round-trip: IK to FK returns the original target within tolerance
- [ ] Test across the full workspace, including boundary and near-singular cases
- [ ] **M3 complete:** analytical IK verified

**Reading**
- None. This is an assembly week.

---

## Week 5 — Revision and numerical methods

**Mechanical**
- [x] Print revised parts
- [x] Reassemble
- [x] Measure actual link lengths on the physical arm; these are your model parameters, not the CAD nominals
- [x] Verify belt tension; confirm no skipping under maximum acceleration

**Software**
- [ ] Implement Jacobian transpose IK
- [ ] Implement pseudoinverse IK
- [ ] Implement damped least squares IK
- [ ] Plot convergence for all three, including a case initialized near a singularity
- [x] Implement the joint abstraction layer with servo and stepper backends
- [ ] Put the reduction ratio in one constant; derive steps-per-degree from it

**Reading** *(roughly two hours)*
- Buss, *Introduction to Inverse Kinematics with Jacobian Transpose, Pseudoinverse and Damped Least Squares Methods*. Around fifteen pages, freely available, and it covers exactly the three solvers in this week's checklist in the same order. **This one document replaces a chapter of theory** — read it and skip everything else on the Jacobian.
- AccelStepper documentation and examples. Read `MultiStepper` and the acceleration model before writing the stepper backend.

You need one idea from all of this: the Jacobian maps joint velocities to end-effector velocities, it becomes ill-conditioned near singularities, and damping is what stops your solver exploding there. The geometric theory behind why is genuinely interesting and genuinely optional.

---

## Week 6 — Homing and calibration *(M4)*

**Mechanical / electrical**
- [ ] Wire both power rails; tie grounds together
- [ ] Fit bulk capacitance across the servo rail
- [ ] Install the limit switch and flag

**Calibration**
- [x] Determine pulse-width-to-angle mapping for each servo individually
- [x] Calibrate dual J2 servos: offset_14 = 0, offset_15 = 36, effective range 36°–150°
- [ ] Record the extremes at which each servo stalls; back off and set limits in software
- [ ] Determine the maximum J1 acceleration at which a full sweep completes without step loss; set the working limit well below it
- [ ] Enforce joint limits in software for all four actuators

**Software**
- [ ] Implement the homing routine
- [ ] Verify homing from ten arbitrary starting positions
- [ ] Implement the startup gate: refuse motion commands until homing completes
- [ ] Implement homing timeout as a hard fault
- [ ] **M4 complete:** arm assembled, homed, calibrated, holding arbitrary configurations under its own weight

**Reading** *(under an hour)*
- Adafruit's PCA9685 servo guide, specifically the section on per-servo `min_pulse` and `max_pulse`. That is exactly the calibration you are performing.
- Marlin or Klipper homing documentation — not because you are using either, but because their treatment of homing state machines, timeouts, and endstop debouncing is more thorough than anything written for hobby arms.

---

## Week 7 — Trajectory execution *(M5)*

**Software**
- [ ] Implement joint-space interpolation with a trapezoidal velocity profile
- [ ] Implement quintic polynomial interpolation
- [ ] Implement straight-line task-space motion
- [ ] Deliberately induce a mid-trajectory IK failure; observe and handle it
- [ ] Plot joint position, velocity, and acceleration against time for each method

**Integration**
- [ ] Execute coordinated multi-joint moves; verify no visible jerk at segment boundaries
- [ ] Verify no J1 step loss during coordinated moves by re-homing after each test
- [ ] **M5 complete:** smooth coordinated trajectory execution

**Reading** *(under an hour)*
- Any practical explanation of trapezoidal and S-curve velocity profiles. Motion-control vendor application notes are better than textbooks here — they are written for people implementing the thing rather than proving properties about it.
- The quintic polynomial you need is fully determined by six boundary conditions: position, velocity, and acceleration at each end. Find a worked solution of those coefficients rather than deriving them; it is a linear system, not an insight.

---

## Week 8 — Gripper and first pick-and-place attempts

**Mechanical**
- [ ] Print and fit the gripper; verify jaw travel and closing force
- [ ] Confirm jaws tolerate the range of approach angles the workspace imposes
- [ ] Add a counterbalance spring if sag measured in week 6 warrants it

**Software**
- [ ] Sequence a full pick-and-place: approach, descend, close, lift, transit, descend, release, retreat
- [ ] Add pre-grasp and post-grasp standoff poses rather than moving directly to the object

**Reading** *(browsing, not study)*
- Printed gripper designs on Printables. Survey several before committing — parallel-jaw, scissor, and compliant designs each fail differently, and looking at three is faster than iterating on one.
- No grasping theory. For a two-jaw gripper picking known objects from known positions, it would not change a single design decision you make this week.

---

## Week 9 — Reliability

- [ ] Run the pick-and-place cycle twenty times; log every failure and its cause
- [ ] Distinguish model error, calibration error, step loss, and mechanical compliance as separate causes
- [ ] Re-home between cycles to isolate step loss from other errors
- [ ] Address the dominant failure mode only; resist fixing everything at once
- [ ] **M6 complete:** blind pick-and-place executing reliably from Cartesian coordinates, no vision

**Reading**
- None. This week is empirical, and reading is a way of avoiding the twenty cycles.

---

## Week 10 — Characterization and closeout *(M7)*

- [ ] Command the same pose from ten different starting configurations; measure the spread
- [ ] Report J1 and the servo joints separately
- [ ] Measure repeatability approaching from clockwise and anticlockwise separately, to quantify backlash asymmetry
- [ ] Measure sag by commanding the same pose with and without payload
- [ ] Finalize the URDF and verify simulated FK against measured physical positions
- [ ] Write up the measured parameters — link lengths, servo mappings, steps-per-degree, joint limits — as the handoff document for Phase 3

**Expected outcome:** the number will be poor, and the stepper axis should demonstrably contribute less error than the servo joints. Understanding the servo-side figure — backlash, sag, deadband, print compliance — is the argument for the feedback-equipped serial-bus servos in Phase 3.

**Reading** *(roughly an hour)*
- The distinction between **repeatability** and **accuracy**, which is one paragraph of reading and determines what your week-10 numbers actually mean. Repeatability is the spread about your own mean; accuracy is the distance from the pose you commanded. Your arm will be far better at the former. Knowing which you measured determines whether the fix lies in calibration or in mechanics.
- ROS 2 `urdf` tutorial, for finalizing the model as the Phase 3 handoff artefact.
- Skim the SO-101 and LeRobot documentation as Phase 3 preparation. Having just measured what open-loop actuation costs you, the case for position feedback will read very differently than it would have ten weeks ago.

---

## Part III — Reference Material

## 8. Parts List

**Actuators**
- NEMA 17 stepper × 1 (salvaged) — J1
- MG996R metal-gear servo × 3 — J2 (×2), J3
- SG90 or MG90S micro servo × 1 — gripper
- MG996R × 1 spare

**Motion control**
- TMC2209 stepper driver × 1 (or salvaged A4988 / DRV8825), with heatsink
- StepStick carrier or breakout board
- PCA9685 16-channel PWM driver × 1 (carried over from Phase 1)
- Limit switch × 1, mechanical or optical
- Microcontroller or Raspberry Pi (existing)

**Belt drive**
- GT2 open belt, 6 mm wide, 2 m
- 20T GT2 pulley, 5 mm bore × 2
- Belt clamps (printed)
- Smooth idler pulleys, 3 mm bore × 2 — if wrap angle proves marginal

**Bearings**
- 6812-2RS thin-section bearing × 1 — 60×78×10 mm, J1
- 608ZZ bearings × 4 — J2 and J3, plus one spare pair
- 8 mm shaft stock or M8 shoulder bolts × 2 — stub shafts

**Power**
- 6 V regulated supply, 5 A minimum — servo rail
- 12 V supply, 2 A minimum — stepper rail
- 1000 µF electrolytic capacitors × 2
- Inline fuse, 5 A
- Barrel jacks, terminal blocks, 18 AWG wire, Dupont jumpers

**Fasteners**
- M3 socket-head screws, 8–30 mm, ~50
- M3 nuts and washers, ~50
- M3 heat-set inserts, ~30, plus installation tip
- M2 screws, 6–10 mm — horn attachment
- Metal servo horns × 3
- Threadlocker, medium strength

**Optional**
- Slip ring capsule, 12.5 mm, 6 or 12 circuits — for unlimited J1 rotation
- Extension springs, assorted — shoulder counterbalance, second revision

**Printing**
- PETG, 1 kg — structural
- PLA, 1 kg — base plate, covers, test fitments

**Measurement**
- Digital calipers
- Multimeter — winding identification and driver current setting
- Small machinist's square — fork plate parallelism
- Kitchen scale reading to 1 g — required for §4.2
- Dial indicator with magnetic base — optional; makes M7 a number rather than an impression

**Test payloads**
- Objects of known mass, 25 g to 100 g

**Estimated cost:** $110–150, assuming stepper, driver, endstop, and 12 V supply are salvaged.

---

## 9. Resources

**Approach to reading**

The total reading in this plan is roughly eight hours across ten weeks, deliberately. The objective is working understanding of how robot motion is computed, not exam-readiness. Every item below is either short, directly actionable, or both.

Two textbooks — Lynch & Park's *Modern Robotics* and Corke's *Robotics, Vision and Control* — are the standard references and are worth knowing exist. **Do not read either cover to cover for this phase.** Use them the way you would use any reference: when a specific concept resists a shorter explanation, find that section and read it. Lynch & Park is freely available from the authors and has an accompanying video course whose individual segments are five to fifteen minutes, which is the more efficient way in if you want it.

**Core items, in order of value**

| Resource | Week | Why |
|---|---|---|
| A worked two-link planar IK derivation | 3 | The conceptual core of the phase. Do it with pen and paper for your own link lengths |
| Buss, *Introduction to Inverse Kinematics with Jacobian Transpose, Pseudoinverse and Damped Least Squares* | 5 | ~15 pages covering exactly the three solvers you implement, in order. Replaces a chapter of theory |
| Rotation matrices and 4×4 homogeneous transforms | 1 | Enough to build and multiply a transform chain. Any course's first lecture notes suffice |
| Peter Corke's *Robot Academy* short lessons | 3 | Five to ten minutes each, deliberately applied. Good if you prefer video |
| Trapezoidal and quintic velocity profiles | 7 | Vendor application notes beat textbooks here |
| Repeatability versus accuracy | 10 | One paragraph; determines what your final measurements mean |

**What this plan deliberately omits**

Product-of-exponentials and Denavit-Hartenberg formalisms, screw theory, contact and grasping theory, dynamics and control of manipulators. Each is genuinely useful for arms more complex than yours, and none would change a design decision or a line of code in this phase. If a future project needs them, you will know why, which is a better time to learn them.

**Software**
- `roboticstoolbox-python` — reference implementations and URDF handling
- AccelStepper — non-blocking step generation with acceleration profiles
- PyBullet — lightweight simulation
- Adafruit CircuitPython ServoKit — PCA9685 interface
- ROS 2 URDF tutorials — clearest documentation of the format, useful independently of adopting ROS

**Suppliers**
- VXB, Bearings Direct, Amazon — 6812-2RS and 608ZZ bearings
- Printables and Thingiverse — EEZYbotARM MK2 and similar, worth examining for joint construction detail

---

## 10. Anticipated Difficulties

1. **Torque underestimation at J2.** The most likely cause of a first revision; the worked example already exceeds budget. Mitigated by measuring masses and building M1a first.
2. **Moment load at J1.** Low torque, high overturning moment. A small thrust bearing will not do; diameter is what resists a moment.
3. **Silent step loss.** Distinguishable from other errors only by re-homing. Build the routine early and use it liberally during debugging.
4. **Belt tension.** Too loose skips teeth silently; too tight loads the motor shaft. Slot the mount from the start.
5. **Cable twist at J1.** The reason to design the centre bore before printing anything.
6. **Servo horn failure at J2.** Metal horns; load path through the screw pattern, never the spline.
7. **Print compliance.** Printed links flex measurably under load, introducing error no kinematic accuracy will correct. Increase perimeter count before infill.
8. **Backlash asymmetry.** Repeatability differs by approach direction. Approaching every target from a consistent direction is a legitimate mitigation.
9. **Confusing model error with calibration error.** Verify the model in simulation, calibrate each actuator in isolation, then assemble — in that order — so each is eliminated independently.
