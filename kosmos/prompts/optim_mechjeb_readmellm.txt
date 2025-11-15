# MechJeb LLM Reference for kRPC Mission Control
## Overview
This reference is for using the MechJeb kRPC service to control rockets and automate complex missions through programmatic agents (AIs or bots). It contains all necessary detail on every available method, class, and attribute, as needed for accurate mission automation and control.
To use this API, ensure you have `MechJeb 2` (https://github.com/MuMech/MechJeb2) installed and the kRPC server running with the MechJeb service enabled.
### Module: `MechJeb`
This module provides programmatic access to MechJeb flight systems. Most features are only available within the Flight scene.
---
### Service-level Attributes
- **`api_ready: bool (read-only)`** — Indicates if the MechJeb API is available.
- **`airplane_autopilot: AirplaneAutopilot (read-only)`** — Airplane autopilot system.
- **`antenna_controller: DeployableController (read-only)`** — Deploy/command antennas.
- **`ascent_autopilot: AscentAutopilot (read-only)`** — Handles launch/ascent control.
- **`docking_autopilot: DockingAutopilot (read-only)`** — Handles vessel docking procedures.
- **`landing_autopilot: LandingAutopilot (read-only)`** — Handles landing sequences.
- **`maneuver_planner: ManeuverPlanner (read-only)`** — Create, plan, and execute maneuver nodes.
- **`node_executor: NodeExecutor (read-only)`** — Execute maneuver nodes.
- **`rcs_controller: RCSController (read-only)`** — Control RCS (reaction control system).
- **`rendezvous_autopilot: RendezvousAutopilot (read-only)`** — Rendezvous planning and approach.
- **`smart_ass: SmartASS (read-only)`** — Automated attitude control and targeting.
- **`smart_rcs: SmartRCS (read-only)`** — Advanced RCS automation.
- **`solar_panel_controller: DeployableController (read-only)`** — Deploy/command solar panels.
- **`staging_controller: StagingController (read-only)`** — Controls rocket stage separation/automation.
- **`target_controller: TargetController (read-only)`** — Target selection and handling.
- **`thrust_controller: ThrustController (read-only)`** — Advanced thrust and engine group control.
- **`translatron: Translatron (read-only)`** — Control vessel translation/throttling.
---
## Main Subsystems (Class Structure, Methods, and Attributes)
### `AscentAutopilot`
Controls launch guidance and ascent to orbit.
**Attributes:**
- `enabled: bool (r/w)` — Enable/disable autopilot.
- `status: str (read-only)` — Current status description.
- `ascent_path_index: int (r/w)` — 0=Classic, 1=GT, 2=PVG. Corresponds to ascent path profile.
- `ascent_path_classic: AscentClassic (read-only)` — Classic Profile settings.
- `ascent_path_gt: AscentGT (read-only)` — Gravity Turn Profile settings.
- `ascent_path_pvg: AscentPVG (read-only)` — Primer Vector Guidance (RSS/RO) Profile settings.
- `desired_inclination: float (r/w)` — Inclination (deg) for target orbit.
- `desired_orbit_altitude: float (r/w)` — Orbit altitude (km).
- `thrust_controller: ThrustController (read-only)`
- `force_roll: bool (r/w)` — Enable force roll.
- `turn_roll: float (r/w)` — Turn roll angle.
- `vertical_roll: float (r/w)` — Roll at vertical.
- `limit_ao_a: bool (r/w)` — Limit angle of attack.
- `max_ao_a: float (r/w)` — Max angle of attack.
- `ao_a_limit_fadeout_pressure: float (r/w)` — Pressure when AoA limit turns off.
- `corrective_steering: bool (r/w)`
- `corrective_steering_gain: float (r/w)`
- `autostage: bool (r/w)` — Enable autostaging. Set params in StagingController.
- `staging_controller: StagingController (read-only)`
- `autodeploy_solar_panels: bool (r/w)` — Deploy panels after ascent.
- `auto_deploy_antennas: bool (r/w)` — Deploy antennas after ascent.
- `skip_circularization: bool (r/w)`
- `warp_count_down: int (r/w)`
- `launch_lan_difference: float (r/w)`
- `launch_phase_angle: float (r/w)`
- `launch_mode: AscentLaunchMode (read-only)`
**Methods:**
- `abort_timed_launch()`: Abort a scheduled launch before countdown ends.
- `launch_to_rendezvous()`: Start launch/target rendezvous.
- `launch_to_target_plane()`: Launch into the target's plane.
---
#### `AscentClassic` (AscentAutopilot.ascent_path_classic)
**Classic Profile Attributes:**
- `auto_path: bool (r/w)` — Enable auto turn.
- `auto_turn_percent: float (r/w)` — [0,1] fraction.
- ... (Full attribute list as above)
---
#### `AscentGT`, `AscentPVG` are alternate path profiles, each with detailed attributes as in source.
---
### `DockingAutopilot`
Controls automated docking with targets.
**Attributes**:
- `enabled: bool (r/w)`
- `status: str (read-only)`
- `speed_limit: float (r/w)`
- `override_safe_distance: bool (r/w)`
- `overriden_safe_distance: float (r/w)`
- `override_target_size: bool (r/w)`
- `overriden_target_size: float (r/w)`
- `safe_distance: float (read-only)`
- `target_size: float (read-only)`
- `force_roll: bool (r/w)`
- `roll: float (r/w)`
---
### `LandingAutopilot`
Automates landing procedures, including chute/gear management.
**Attributes:**
- `enabled: bool (r/w)`
- `status: str (read-only)`
- `deploy_chutes: bool (r/w)`
- `deploy_gears: bool (r/w)`
- `limit_chutes_stage: int (r/w)`
- `limit_gears_stage: int (r/w)`
- `rcs_adjustment: bool (r/w)`
- `touchdown_speed: float (r/w)`
**Methods:**
- `land_at_position_target()`
- `land_untargeted()`
- `stop_landing()`
---
### `RendezvousAutopilot`
Plans and performs rendezvous maneuvers with target vessels.
**Attributes:**
- `enabled: bool (r/w)`
- `status: str (read-only)`
- `desired_distance: float (r/w)`
- `max_phasing_orbits: float (r/w)`
---
### `ManeuverPlanner`
Creates maneuver node(s) for a variety of orbital ops—each as an operation object (see below).
**Attributes (each is read-only and returns an op class):**
- `operation_apoapsis: OperationApoapsis`
- `operation_circularize: OperationCircularize`
- ... and more for: course correction, ellipticize, inclination, interplanetary transfer, kill rel vel, lambert, lan, longitude, moon return, periapsis, plane, resonant orbit, semi major, transfer.
#### Example Operation: `OperationApoapsis`
**Attributes:**
- `error_message: str (read-only)`
- `new_apoapsis: float (r/w)`
- `time_selector: TimeSelector (read-only)`
**Methods:**
- `make_node()`: (DEPRECATED) Creates single maneuver node, returns Node.
- `make_nodes()`: Creates all needed nodes, returns list(Node).
_(All operation objects follow this pattern; refer to each for details.)_
#### `TimeSelector` for Maneuver Timing
- `circularize_altitude: float (r/w)`
- `lead_time: float (r/w)`
- `time_reference: TimeReference (r/w)` _(one of: altitude, apoapsis, computed, periapsis, etc.)_

**IMPORTANT**: `TimeReference` is an enum accessed from the `mj` object, NOT from `maneuver_planner`.

**Example**:
```python
# CORRECT - Access TimeReference from mj
circ_op = mj.maneuver_planner.operation_circularize
circ_op.time_selector.time_reference = mj.TimeReference.apoapsis  # ✓ CORRECT
nodes = circ_op.make_nodes()

# WRONG - Do NOT access from maneuver_planner
circ_op.time_selector.time_reference = mj.maneuver_planner.TimeReference.apoapsis  # ✗ WRONG
```

**Available TimeReference values**:
- `mj.TimeReference.altitude` - At the selected circularize_altitude
- `mj.TimeReference.apoapsis` - At the next apoapsis
- `mj.TimeReference.periapsis` - At the next periapsis
- `mj.TimeReference.computed` - At the optimum time (most common for transfers)
- `mj.TimeReference.closest_approach` - At the closest approach to target
- `mj.TimeReference.eq_ascending` - At the equatorial ascending node
- `mj.TimeReference.eq_descending` - At the equatorial descending node
---
### `SmartASS`
Advanced attitude/autopilot system for orienting spacecraft.
**Attributes:**
- `interface_mode: SmartASSInterfaceMode (r/w)`
- `autopilot_mode: SmartASSAutopilotMode (r/w)`
- `force_yaw: bool (r/w)`
- `force_pitch: bool (r/w)`
- `force_roll: bool (r/w)`
- `surface_heading: float (r/w)`
- `surface_pitch: float (r/w)`
- `surface_roll: float (r/w)`
- `surface_vel_yaw: float (r/w)`
- ... (full set as in source)
- `advanced_reference: AttitudeReference (r/w)`
- `advanced_direction: Direction (r/w)`
**Methods:**
- `update(reset_pid: bool)` — Apply orientation changes (optionally reset PID loop).
#### Enums:
- `SmartASSInterfaceMode:` orbital, surface, target, advanced, automatic
- `SmartASSAutopilotMode:` See extensive full list, e.g. off, kill_rot, node, prograde, retrograde, surface, target_plus/minus, advanced, etc.
- `AttitudeReference:` inertial, orbit, orbit_horizontal, surface_north, etc.
- `Direction:` forward, back, up, down, right, left
---
### `Translatron`, `ThrustController`, `StagingController`, `RCSController`, `DeployableController`
Each controller has a set of relevant attributes and methods to enable AI control over rocket propulsion, staging, RCS control, part deployment, and fine-tuned velocity management. Provide detailed attribute/method reference as per the full source above.
---
## Error Handling
All methods that produce/plan nodes can throw:
- `OperationException` — If operation parameters invalid (e.g., target not set)
- `MJServiceException` — Internal error in MechJeb service
## Full Attribute and Method Details
For each controller and operation, refer to its detailed reference section above. Use all class docstrings and attribute descriptions as given to maximize accuracy in mission coding.
