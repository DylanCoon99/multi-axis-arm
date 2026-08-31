# Phase 2 — Custom Three-Revolute Arm: Detailed Build Plan

*Design, fabrication, kinematics, and control for a self-designed serial manipulator.*

**Prerequisite:** Phase 1 (auto-tracking camera gimbal) — complete.
**Duration:** Eight to ten weeks, with the software and mechanical tracks running in parallel.
**Successor:** Phase 3 (vision-based, voice-controlled manipulation on the SO-101).

**Actuation:** Mixed. Stepper motor at the base rotation (J1), hobby servos at shoulder (J2), elbow (J3), and gripper.

---

## 1. Objective and Scope

Acquire the mathematics of serial manipulators and validate it against a physical machine of your own design.

The substitution of a self-designed arm for a printed kit changes the character of the phase. The EEZYbotARM's parallelogram linkage would have forced derivation of a nontrivial actuator-space to joint-space mapping; a straightforward serial arm removes that lesson, since servo angles correspond directly to joint angles. In exchange, you choose the link lengths, and therefore own the workspace geometry and singularity structure rather than inheriting them.

The cost is time: expect two to three additional weeks for mechanical design and print iteration, and expect at least two revisions.

### Configuration

| Joint | Axis | Actuator | Function |
|---|---|---|---|
| J1 | Vertical | NEMA 17 stepper | Base rotation |
| J2 | Horizontal | MG996R servo | Shoulder |
| J3 | Horizontal, parallel to J2 | MG996R servo | Elbow |
| — | — | SG90 / MG90S servo | Gripper (binary open/close) |

J2 and J3 have parallel axes; J1 is perpendicular to both. **This orthogonality is what makes the inverse kinematics tractable** — J1 is determined entirely by the horizontal bearing to the target, and rotating into the vertical plane containing the arm reduces J2 and J3 to a two-link planar problem solvable on paper. Tilting J1 or making the shoulder and elbow axes non-parallel would collapse that decomposition and force a numerical solver from the outset.

**Do not add a wrist.** Additional degrees of freedom would permit orientation control, but triple the difficulty of the inverse kinematics and introduce singularity behaviour that is genuinely difficult to reason about on a first arm.

**Consequence to accept:** with three joints you determine end-effector position only. The gripper's approach angle is whatever falls out of the J2/J3 solution — steeper for near targets, shallower near the workspace boundary. Design the jaws to tolerate a range of approach angles.

---

## 2. Actuation Rationale

### 2.1 Why a stepper at J1

The base joint carries the entire arm axially — roughly 500 to 700 g of structure, actuators, and payload — but carries no gravitational **moment**, because the load acts along the rotation axis rather than perpendicular to it. Torque demand is therefore genuinely low; the motor fights inertia and friction only.

The stepper is justified by two other properties:

**Resolution.** A 1.8° stepper at 1/16 microstepping yields 3200 increments per revolution. An MG996R offers roughly 1000 usable increments across 180°, and those increments are not uniform — the pulse-width-to-angle mapping is nonlinear near the extremes. Base rotation scales lateral positioning error directly: one degree of error at J1 becomes several millimetres at 300 mm reach. This is the joint where resolution buys the most.

**Unlimited travel.** A hobby servo is mechanically limited to approximately 180°. A stepper rotates continuously, materially enlarging the workspace and removing reachability gaps behind the arm.

Both will appear in the M7 repeatability measurement.

### 2.2 The bearing consequence at J1

**Low torque does not mean low load.** The axial load at J1 is the highest of any joint, and a deep-groove ball bearing takes axial load poorly. The 608ZZ arrangement used at J2 and J3 is wrong here.

J1 requires one of:

- A thrust bearing (51105 or similar) plus a radial bearing for lateral constraint
- A printed slewing race running airsoft BBs or 6 mm steel balls
- A Lazy-Susan turntable bearing, 100 mm or larger

**The stepper's output shaft must not carry the arm's weight through the motor's internal bearings.** The thrust arrangement takes the axial load; the shaft transmits torque only. This is the same principle as the horn-and-bearing arrangement at J2 and J3, applied to a different load case.

### 2.3 Why servos remain at J2 and J3

Retaining servos at the loaded joints preserves the pedagogical content of the phase — the pulse-width calibration exercise, and the open-loop error problem that motivates the feedback-equipped actuators in Phase 3. It also keeps mass low at J3, where a 280 g stepper would sit at the full upper-link moment arm and add roughly 3.4 kgf·cm to the shoulder demand.

### 2.4 The homing requirement

The stepper does not know its position at power-up. **J1 requires a reference switch and a homing routine executed before any commanded motion is permitted.** Without it, the arm will drive into its own wiring on the first move after a power cycle.

Implementation: a mechanical microswitch or optical endstop positioned so a flag on the rotating base trips it near one travel extreme. On startup, rotate slowly toward the switch, stop on trigger, zero the step counter, then move to a defined home pose.

**Silent failure.** A servo that cannot reach its commanded position buzzes audibly and draws visible current. A stepper that loses steps does so quietly, and every subsequent position carries the offset with no indication. Re-home periodically during long sessions, and treat any unexplained positional discrepancy as suspected step loss until eliminated.

---

## 3. Mechanical Design

### 3.1 Link geometry

Two links of approximately equal length maximize workspace area for a given total reach. Deliberately unequal lengths create an unreachable void around the base — worth understanding, probably not worth building into a first arm.

**Suggested scale:** 120–180 mm per link.

Do not finalize these numbers before completing the torque calculation in §3.2 and the workspace plot in §5.5. Both will likely revise them downward.

### 3.2 Torque: the binding constraint at J2

Compute static torque at the shoulder with the arm fully extended, summing each mass times its distance from the joint — **including the links themselves**, not merely the payload.

An MG996R is rated at approximately 10 kgf·cm at 6 V. **Design to no more than half that value** to retain margin for dynamic loads and avoid operation near stall.

Worked illustration for a 150 mm upper link and 150 mm forearm:

| Contribution | Mass | Moment arm | Torque |
|---|---|---|---|
| Upper link | 60 g | 75 mm | 0.45 kgf·cm |
| Elbow servo | 55 g | 150 mm | 0.83 kgf·cm |
| Forearm | 50 g | 225 mm | 1.13 kgf·cm |
| Gripper assembly | 70 g | 300 mm | 2.10 kgf·cm |
| Payload | 50 g | 310 mm | 1.55 kgf·cm |
| **Total at shoulder** | | | **≈ 6.1 kgf·cm** |

This example exceeds the 5 kgf·cm design target and would require shorter links, a lighter gripper, or a counterbalance. Perform this calculation with your own measured masses before printing anything.

Note that the stepper at J1 does not appear in this calculation — its mass sits on the base, below the shoulder joint, and contributes nothing to the shoulder moment. This is the principal mechanical advantage of the arrangement.

### 3.3 Counterbalancing

An extension spring or counterweight acting on the shoulder substantially reduces static load and improves positional accuracy under gravity. **Defer to the second revision**, once the first has revealed how much sag you actually have. Designing a counterbalance for an unmeasured load is guesswork.

Given that §3.2's worked example runs over budget, expect this to become necessary rather than optional.

### 3.4 Joint construction at J2 and J3

**Do not load the servo output spline in bending.** This is the most common failure in printed arms.

The arrangement is a U-shaped fork carrying the servo in one plate and a bearing in the other:

- The servo's spline engages a metal horn bolted to the distal link. **The horn transmits torque only.**
- A stub shaft integral to the distal link runs in a 608ZZ bearing seated in the opposite plate. **The bearing carries the radial load** — everything outboard of the joint, plus payload.
- Both fork plates must be rigidly joined by a yoke. If they splay, shaft and spline lose alignment, which binds the bearing and loads the spline in exactly the manner the design prevents.

**Concentricity between spline and bearing bore is the tolerance that matters most.** Any offset forces the shaft to orbit as the joint rotates, producing cyclic side load on the spline. Print both plates in the same orientation and, where possible, as a single body so the two features share a datum rather than being aligned during assembly.

Bore the stub shaft to a light interference fit with the bearing's inner race, or use a shoulder and retaining screw. A loose shaft is a backlash source that will appear directly in the M7 measurement.

Use metal servo horns at J2 and J3. Plastic horns strip.

### 3.5 Printing

Layer adhesion is the dominant failure mode.

- Orient links so bending loads act **across** layers rather than along them
- PETG for load-bearing parts; PLA acceptable for the base plate and non-structural covers
- Four or more perimeters on structural parts — perimeter count matters more than infill for bending stiffness
- Generous fillets at stress concentrations, particularly where links meet joint housings

### 3.6 The single-joint test article

**Build this before committing to the full assembly.**

With the mixed actuation, build **two** test articles:

1. **Servo joint:** one MG996R, one link, one 608 bearing, one metal horn. Validates the fork geometry, print settings, and torque calculation. Hang the calculated load at the calculated moment arm and confirm the servo holds without buzzing.
2. **Base joint:** stepper, driver, thrust arrangement, limit switch. Validates the thrust bearing choice, driver current setting, and homing routine.

Both are an afternoon each and vastly less painful to revise than a complete arm. The base joint is now the least-proven element of the design and warrants the extra attention.

---

## 4. Electrical

Two supply rails are now required, with a common ground.

| Rail | Voltage | Current | Serves |
|---|---|---|---|
| Servo | 6 V | ≥5 A | J2, J3, gripper, PCA9685 |
| Stepper | 12 V | ≥2 A | J1 driver |

**Tie the grounds together.** Without a common reference, the step and direction signals have no defined level relative to the driver.

Retain the 1000 µF bulk capacitance across the servo rail near the connectors, as established during the gimbal. Fit a heatsink to the stepper driver and set its current limit by measuring the reference voltage — do not leave it at the factory setting.

---

## 5. Software Track

Begin immediately, in parallel with mechanical design. This track does not depend on hardware existing and should be substantially complete before assembly, so that when the arm arrives you are debugging mechanics rather than mathematics.

### 5.1 Rigid-body transforms

Rotation matrices, homogeneous transformation matrices in SE(3), composition along a kinematic chain. Forward kinematics is the product of link transforms.

**On convention.** Learn the product-of-exponentials formulation as your working representation. Denavit-Hartenberg parameters pervade the older literature and existing code, so retain enough familiarity to read a DH table — but the arbitrary frame-placement rules make DH tedious to derive.

**Deliverable:** a function accepting three joint angles and returning end-effector position, verified against hand calculation at several configurations.

### 5.2 Analytical inverse kinematics

Begin with the two-link planar case. Small enough to solve on paper, rich enough to expose everything that matters:

- Two solutions, elbow-up and elbow-down
- The workspace boundary
- The unreachable interior region when link lengths differ
- The singularity at full extension, where the two solutions coalesce and one direction of motion becomes unavailable

For your three-revolute arm: **J1 is determined by the horizontal projection of the target; the remainder reduces to the two-link planar case in the vertical plane containing the arm.**

Deriving this for your own geometry is the single most valuable exercise in the phase. Do not copy it.

**Deliverable:** a closed-form solver returning both configurations, with an explicit unreachable-target signal.

### 5.3 Numerical inverse kinematics

Construct the manipulator Jacobian relating joint velocities to end-effector velocities. Implement three solvers **in this order**:

1. **Jacobian transpose** — simple, slow, always stable
2. **Pseudoinverse** — faster; unstable near singularities
3. **Damped least squares** (Levenberg-Marquardt) — trades exactness for numerical stability; what production systems use

Implementing all three in sequence makes the motivation for damping self-evident. Add joint-limit handling, and observe solver behaviour when asked for an unreachable pose.

**Deliverable:** a convergence comparison plot for all three methods, including a case initialized near a singularity.

### 5.4 The joint abstraction layer

**New requirement arising from mixed actuation.**

Define a per-joint interface exposing `move_to(angle)` and `current_angle()`, hiding whether the command becomes a pulse width or a step target. Implement two concrete types behind it: one wrapping the PCA9685 channel, one wrapping the stepper driver.

Do this early. The distinction must not leak into the trajectory code, because Phase 3 replaces all four actuators with serial-bus servos and only this layer should need to change.

**Asymmetry to remain conscious of:** the trapezoidal velocity profile from §5.6 has real authority over J1, where you generate every step pulse. For the servo joints it is merely advisory — the servo's internal controller decides how it gets to the commanded position. Coordinated multi-axis moves must be timed with this in mind.

Use **AccelStepper** for step timing rather than writing pulse generation yourself. Non-blocking multi-axis coordination is a solved problem and not what this phase is for.

### 5.5 Workspace analysis before printing

Once you have a candidate geometry, implement forward kinematics and **plot the reachable workspace before printing anything.** Sweep the joint ranges, accumulate end-effector positions, examine the cloud.

Note that J1's unlimited travel makes the workspace a full solid of revolution rather than the partial sector a servo base would produce. This is worth seeing plotted.

You will likely revise link lengths on the strength of this plot. It costs nothing now and costs a print later.

### 5.6 Trajectory generation

A sequence of IK solutions is not a motion. Naive interpolation produces discontinuous velocity and a machine that jerks.

Implement, in order:

1. Joint-space interpolation with a trapezoidal velocity profile
2. Quintic polynomial interpolation (continuous position, velocity, acceleration)
3. Straight-line motion in task space

The third requires solving IK along the path and can fail mid-trajectory if the path crosses a singularity or exits the workspace. **Induce that failure deliberately once.**

**Deliverable:** plots of joint position, velocity, and acceleration against time for each method.

### 5.7 Homing and startup sequence

**New requirement.** Before any commanded motion:

1. Drive J1 slowly toward the limit switch
2. Stop on trigger; zero the step counter
3. Command the servo joints to a defined home pose
4. Only then accept motion commands

Refuse all motion commands until homing has completed successfully. Treat a homing timeout as a hard fault.

### 5.8 URDF model

Describe the arm in Unified Robot Description Format as the design solidifies. Loading it into PyBullet or MuJoCo and verifying that simulated forward kinematics match measured physical positions gives you a digital twin, validates the kinematic model against reality, and produces an artefact reusable in Phase 3 and in any subsequent ROS 2 work.

### 5.9 Tooling

| Tool | Role |
|---|---|
| NumPy, Matplotlib | Sufficient for §5.1–5.6 in their entirety |
| AccelStepper | Step timing and acceleration for J1 |
| Adafruit CircuitPython ServoKit | PCA9685 interface, as used in Phase 1 |
| `roboticstoolbox-python` | Reference implementation for checking your own work |
| PyBullet | Lighter-weight simulator at this scale |

**Implement first, compare second.** The pedagogical value resides entirely in the implementation.

---

## 6. Calibration and the Open-Loop Problem

Neither actuator type reports its actual position. The arm is entirely open-loop, and the two types fail differently.

**Servos (J2, J3, gripper).** Accept a pulse width and report nothing. Present and significant: gravitational sag under load varying with configuration; backlash on direction reversal in both gearbox and printed joints; a nonlinear, per-unit mapping from pulse width to angle, with substantial manufacturing variation between nominally identical units.

**Stepper (J1).** Position is known exactly *provided no steps have been lost*. Loss is silent. The mitigation is periodic re-homing and conservative acceleration limits.

**Required exercise:** calibrate the pulse-width-to-angle mapping for each servo individually, and quantify the resulting positional repeatability. Separately, determine the maximum acceleration at which J1 completes a full sweep without losing steps, and set your working limit well below it.

You met the calibration problem on the gimbal, where it was invisible because the camera closed an outer loop that absorbed the error. Here there is no outer loop. Whatever error exists propagates directly to end-effector position and stays there. **That absence is the pedagogical point of the phase.**

---

## 7. Milestones

### M1 — Two test articles (week 2)
**M1a:** one servo, one link, one bearing, one metal horn — holding the calculated load at the calculated moment arm without buzzing or excess sag. Fork geometry and print settings validated.
**M1b:** stepper, driver, thrust arrangement, limit switch — homing routine executing reliably, driver current set by measurement, no audible resonance across the working speed range.

### M2 — Forward kinematics verified in software (week 3)
FK agreeing with hand calculation at five or more configurations. Workspace plotted; link lengths finalized on the strength of it.

### M3 — Analytical IK solved and verified (week 4)
Closed-form solver for your geometry, returning both configurations, verified by round-trip: IK to FK returns the original target to within numerical tolerance across the workspace.

### M4 — Arm assembled, homed, and calibrated (week 6)
Full assembly complete. J1 homing reliable from arbitrary starting positions. Per-servo pulse-width-to-angle mapping established. Joint limits determined and enforced in software. Arm holds arbitrary commanded configurations under its own weight.

### M5 — Coordinated trajectory execution (week 7)
Arm moves between commanded joint configurations along a smooth profile, with no visible jerk at segment boundaries and no step loss at J1. Straight-line task-space motion demonstrated, including one deliberately induced mid-trajectory failure.

### M6 — Blind pick-and-place *(primary milestone, week 8–10)*
The arm moves to coordinates specified in Cartesian space, closes the gripper, transports an object to a second specified pose, and releases it — executing a smooth trajectory throughout.

**No vision, no perception; the object position is given.**

Achieving this reliably requires every component of the phase to be correct, and the failure modes are individually diagnosable. This is the gate to Phase 3.

### M7 — Repeatability characterization *(supplementary)*
Command the same pose from ten different starting configurations and quantify the spread. Report J1 and the servo joints separately — you should be able to demonstrate that the stepper axis contributes materially less error, which is the empirical justification for the actuation choice.

Understanding the servo-side number — backlash, gravitational sag, deadband, print compliance — is the argument for the feedback-equipped serial-bus servos in Phase 3.

---

## 8. Resources

### Primary texts

| Text | Role |
|---|---|
| Lynch & Park, *Modern Robotics* | Chapters 3–6 align almost exactly with this phase. Primary reference; freely available from the authors with an accompanying video course |
| Corke, *Robotics, Vision and Control* | More applied, with worked code. Better companion if Lynch and Park's formalism proves heavy going |

### Software

- `roboticstoolbox-python` — Corke's toolbox; reference implementations and URDF handling
- AccelStepper — non-blocking step generation with acceleration profiles
- PyBullet — lightweight simulation, straightforward URDF loading
- Adafruit CircuitPython ServoKit — PCA9685 interface
- The ROS 2 URDF tutorials are the clearest documentation of the format, useful independently of whether you adopt ROS

### Mechanical reference

- Thingiverse and Printables listings for the EEZYbotARM MK2 and similar printed arms — worth examining for joint construction and horn interface detail
- Printed slewing bearing designs — search for turntable or Lazy-Susan bearings for J1 if not buying a thrust bearing
- Servo and stepper datasheets: obtain actual torque figures for your specific units rather than relying on catalogue values

---

## 9. Schedule

| Week | Mechanical track | Software track |
|---|---|---|
| 1 | Concept design, torque calculation | Transforms, forward kinematics |
| 2 | Test articles M1a and M1b | FK verified, workspace plotted (**M2**) |
| 3 | Full CAD, first print run | Analytical IK derivation |
| 4 | Assembly, first revision identified | IK verified by round-trip (**M3**) |
| 5 | Revision printed and assembled | Numerical IK; joint abstraction layer |
| 6 | Homing, calibration (**M4**) | Trajectory generation |
| 7 | Integration | Coordinated execution (**M5**) |
| 8–10 | Tuning, gripper refinement | Pick-and-place (**M6**), repeatability (**M7**) |

The critical path is mechanical. The software track should be substantially complete by week 7, leaving the final weeks for the inevitable discovery that the physical arm does not behave as the model predicted.

---

## 10. Anticipated Difficulties

1. **Torque underestimation at J2.** The most likely cause of a first revision, and the worked example in §3.2 already exceeds budget. Mitigated by performing the calculation with measured masses and by building M1a before the full assembly.
2. **Axial load at J1.** The joint whose load case is most easily misjudged. Low torque, high axial force. A thrust arrangement is mandatory.
3. **Silent step loss.** Distinguishable from other error sources only by re-homing. Build the re-home routine early and use it liberally during debugging.
4. **Servo horn failure at J2.** Use metal horns; ensure the load path runs through the screw pattern rather than the spline.
5. **Print compliance.** Printed links flex measurably under load, introducing error no amount of kinematic accuracy will correct. Increase perimeter count before infill.
6. **Backlash asymmetry.** Repeatability will differ by approach direction. Approaching every target from a consistent direction is a legitimate and widely used mitigation.
7. **Confusing model error with calibration error.** When the end effector does not arrive where commanded, the cause may lie in the kinematic model, the servo mapping, the step count, or the mechanics. Verify the model in simulation, calibrate each actuator in isolation, then assemble — in that order — so each is eliminated independently.
