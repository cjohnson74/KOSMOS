# kRPC and kRPC.MechJeb ReadMe.LLM

The following is the full ReadMe.LLM for the kRPC library and its MechJeb extension:

## ReadMe.LLM

### context_description
The context will be for the kRPC library and kRPC.MechJeb extension. kRPC allows you to control Kerbal Space Program from scripts running outside of the game using Remote Procedure Calls. It provides client libraries for many popular languages including C#, C++, C, Java, Lua, Python, and Ruby. kRPC.MechJeb extends this functionality by providing remote procedures to interact with MechJeb 2 autopilots. The context is organized into numbered sections using XML tags, with each section containing a description, code snippets, and use case examples.

## context_1

### context_1_description
The kRPC SpaceCenter service provides the core functionality for controlling Kerbal Space Program from external scripts. It includes vessel control, flight data access, resource management, maneuver node planning, and camera control. This service exposes most of KSP's API for interacting with rockets, celestial bodies, and game state management.

### context_1_code_snippet

```python
import krpc

# Connect to the kRPC server
conn = krpc.connect(name='Flight Controller')

# Get the SpaceCenter service
space_center = conn.space_center

# Get the active vessel
vessel = space_center.active_vessel

# Control systems
control = vessel.control
autopilot = vessel.auto_pilot
flight = vessel.flight()
orbit = vessel.orbit

# Basic vessel properties
print(f"Vessel name: {vessel.name}")
print(f"Mass: {vessel.mass} kg")
print(f"Dry mass: {vessel.dry_mass} kg")

# Flight telemetry
print(f"Altitude: {flight.mean_altitude:.2f} m")
print(f"Speed: {flight.speed:.2f} m/s")
print(f"Vertical speed: {flight.vertical_speed:.2f} m/s")

# Orbital information
print(f"Apoapsis: {orbit.apoapsis_altitude:.2f} m")
print(f"Periapsis: {orbit.periapsis_altitude:.2f} m")
print(f"Inclination: {orbit.inclination:.2f} degrees")

# Vessel control
control.throttle = 1.0  # Full throttle
control.activate_next_stage()  # Stage separation
control.sas = True  # Enable SAS
control.rcs = True  # Enable RCS

# Autopilot control
autopilot.engage()
autopilot.target_pitch_and_heading(45, 90)  # 45 degrees pitch, 90 degrees heading
autopilot.wait()

# Resource management
for resource in vessel.resources.all:
    print(f"{resource.name}: {resource.amount:.2f}/{resource.max:.2f}")

# Maneuver nodes
ut = space_center.ut + 3600  # 1 hour from now
node = control.add_node(ut, prograde=1000)  # Add 1000 m/s prograde burn

# Camera control
camera = space_center.camera
camera.mode = space_center.CameraMode.free
camera.pitch = 0
camera.heading = 90
camera.distance = 150

# Parts and staging
for stage in vessel.control.current_stage:
    print(f"Stage {stage}")
    
for part in vessel.parts.all:
    if part.engine:
        print(f"Engine: {part.title}, Thrust: {part.engine.thrust}")
```

### context_1_examples

```python
"""
Simple orbital insertion script using kRPC
Launches a rocket and performs a basic gravity turn to orbit
"""
import krpc
import time
import math

# Connect to kRPC
conn = krpc.connect(name='Launch Controller')
vessel = conn.space_center.active_vessel

# Set up data streams for efficient monitoring
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

# Launch parameters
target_altitude = 100000  # 100km orbit
turn_start_altitude = 250
turn_end_altitude = 45000
target_heading = 90  # East

print('Launch!')
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, target_heading)

# Main ascent loop
srbs_separated = False
turn_angle = 0

while apoapsis() < target_altitude:
    # Gravity turn
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
        frac = ((altitude() - turn_start_altitude) / 
                (turn_end_altitude - turn_start_altitude))
        new_turn_angle = frac * 90
        if abs(new_turn_angle - turn_angle) > 0.5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, target_heading)

    # Separate SRBs when empty
    if not srbs_separated:
        if srb_fuel() < 0.1:
            vessel.control.activate_next_stage()
            srbs_separated = True
            print('SRBs separated')

    time.sleep(0.1)

print('Apoapsis reached')
vessel.control.throttle = 0.0

# Wait until approaching apoapsis
print('Coasting to apoapsis')
while vessel.orbit.time_to_apoapsis > 75:
    time.sleep(1)

# Execute circularization burn
print('Circularization burn')
vessel.control.throttle = 1.0
while vessel.orbit.periapsis_altitude < target_altitude * 0.9:
    time.sleep(0.1)

vessel.control.throttle = 0.0
vessel.auto_pilot.disengage()
print('Launch complete!')
```

## context_2

### context_2_description
The kRPC.MechJeb service provides programmatic access to MechJeb 2 autopilots and systems. This extension allows external scripts to configure and control MechJeb's various autopilots including ascent guidance, landing autopilot, docking autopilot, and maneuver execution. It exposes MechJeb's sophisticated flight control algorithms through a simple API.

### context_2_code_snippet

```python
import krpc

# Connect to kRPC with MechJeb extension
conn = krpc.connect(name='MechJeb Controller')
vessel = conn.space_center.active_vessel
mj = conn.mech_jeb

# Check if MechJeb is available
print(f"MechJeb available: {mj.available}")

# Ascent Autopilot
ascent = mj.ascent_autopilot
ascent.enabled = True
ascent.desired_orbit_altitude = 100000  # 100km
ascent.desired_inclination = 0  # Equatorial orbit
ascent.force_roll = True
ascent.vertical_roll = 0
ascent.turn_roll = 0

# Ascent guidance settings
classic = ascent.ascent_path_classic
classic.turn_start_altitude = 500
classic.turn_start_velocity = 100
classic.turn_end_altitude = 60000
classic.turn_end_angle = 0
classic.turn_shape_percentage = 40

# Landing Autopilot
landing = mj.landing_autopilot
landing.enabled = True
landing.touchdown_speed = 0.5  # m/s
landing.deploy_parachutes = True
landing.deploy_landing_gear = True

# Set landing target
target = conn.space_center.target_body.surface_position(
    latitude=-0.0972, longitude=-74.5577  # KSC coordinates
)
landing.land_at_position_target(target)

# Docking Autopilot
docking = mj.docking_autopilot
docking.enabled = True
docking.speed_limit = 1.0  # m/s approach speed

# Maneuver Planner
maneuver_planner = mj.maneuver_planner
# Plan Hohmann transfer
hohmann = maneuver_planner.operation_hohmann
hohmann.make_nodes(target_body=conn.space_center.bodies['Mun'])

# Node Executor
node_executor = mj.node_executor
node_executor.enabled = True
node_executor.tolerance = 0.1  # m/s delta-v tolerance

# Smart A.S.S. (Attitude Control)
smart_ass = mj.smart_ass
smart_ass.autopilot_mode = mj.SmartASSAutopilotMode.prograde
smart_ass.update()

# Thrust Controller
thrust = mj.thrust_controller
thrust.twr_controller = True
thrust.target_twr = 1.5  # Target thrust-to-weight ratio

# Staging Controller
staging = mj.staging_controller
staging.enabled = True
staging.auto_stage_pre_delay = 0.5
staging.auto_stage_post_delay = 1.0

# Warp Controller
warp = mj.warp_controller
warp.warp_to_next_sol()  # Warp to next sphere of influence
```

### context_2_examples

```python
"""
Automated mission to Mun using kRPC.MechJeb
Performs launch, transfer, landing, and return
"""
import krpc
import time

def wait_for_autopilot(autopilot, timeout=300):
    """Wait for autopilot to complete with timeout"""
    start_time = time.time()
    while autopilot.enabled and (time.time() - start_time) < timeout:
        time.sleep(1)
    return not autopilot.enabled

# Connect to game
conn = krpc.connect(name='Mun Mission Controller')
vessel = conn.space_center.active_vessel
sc = conn.space_center
mj = conn.mech_jeb

print("=== MUN MISSION CONTROLLER ===")
print(f"Controlling vessel: {vessel.name}")

# === LAUNCH PHASE ===
print("\n1. LAUNCH TO PARKING ORBIT")
ascent = mj.ascent_autopilot
ascent.desired_orbit_altitude = 100000
ascent.desired_inclination = 0
ascent.ascent_path_index = mj.AscentPathType.classic

# Configure classic ascent path
classic = ascent.ascent_path_classic
classic.turn_start_altitude = 250
classic.turn_start_velocity = 100
classic.turn_end_altitude = 45000
classic.turn_shape_percentage = 40

# Enable staging and launch
staging = mj.staging_controller
staging.enabled = True
ascent.enabled = True

print("Launching...")
wait_for_autopilot(ascent, timeout=600)
print("Parking orbit achieved")

# === TRANSFER PHASE ===
print("\n2. TRANSFER TO MUN")
maneuver = mj.maneuver_planner

# Plan Hohmann transfer to Mun
hohmann = maneuver.operation_hohmann
mun = sc.bodies['Mun']
hohmann.make_nodes(mun)

# Execute the maneuver
node_exec = mj.node_executor
node_exec.tolerance = 1.0
node_exec.enabled = True

print("Executing transfer burn...")
wait_for_autopilot(node_exec, timeout=300)
print("Transfer burn complete")

# Warp to Mun SOI
warp = mj.warp_controller
print("Warping to Mun sphere of influence...")
warp.warp_to_soi_change()

# === MUN ORBIT INSERTION ===
print("\n3. MUN ORBIT INSERTION")
# Plan circularization at Mun periapsis
circularize = maneuver.operation_circularize
circularize.make_nodes()

node_exec.enabled = True
print("Executing orbit insertion...")
wait_for_autopilot(node_exec, timeout=300)
print("Mun orbit achieved")

# === LANDING PHASE ===
print("\n4. LANDING ON MUN")
landing = mj.landing_autopilot
landing.enabled = True
landing.touchdown_speed = 2.0
landing.deploy_landing_gear = True

# Choose landing site (East Crater)
landing.land_somewhere = True
print("Beginning descent...")
wait_for_autopilot(landing, timeout=600)
print("Landed on Mun!")

# === SAMPLE COLLECTION SIMULATION ===
print("\n5. SURFACE OPERATIONS")
print("Collecting samples... (simulated)")
time.sleep(10)

# === RETURN PHASE ===
print("\n6. RETURN TO KERBIN")
# Launch from Mun surface
ascent.desired_orbit_altitude = 15000  # Low Mun orbit
ascent.enabled = True
wait_for_autopilot(ascent, timeout=300)
print("Launched from Mun surface")

# Plan return to Kerbin
kerbin = sc.bodies['Kerbin']
hohmann.make_nodes(kerbin)
node_exec.enabled = True
wait_for_autopilot(node_exec, timeout=300)
print("Return trajectory set")

# Warp to Kerbin SOI
warp.warp_to_soi_change()

# === ATMOSPHERIC ENTRY ===
print("\n7. ATMOSPHERIC ENTRY")
# Configure for atmospheric entry
smart_ass = mj.smart_ass
smart_ass.autopilot_mode = mj.SmartASSAutopilotMode.retrograde
smart_ass.update()

# Deploy parachutes when safe
print("Deploying parachutes...")
vessel.control.activate_next_stage()

print("\n=== MISSION COMPLETE ===")
print("Welcome back to Kerbin!")
```

```python
"""
Rendezvous and docking script using kRPC.MechJeb
Automatically rendezvous with and dock to a target vessel
"""
import krpc
import time

conn = krpc.connect(name='Docking Controller')
vessel = conn.space_center.active_vessel
sc = conn.space_center
mj = conn.mech_jeb

# Verify we have a target
if not sc.target_vessel:
    print("ERROR: No target vessel selected!")
    exit(1)

target = sc.target_vessel
print(f"Docking {vessel.name} with {target.name}")

# === PHASE 1: RENDEZVOUS ===
print("\n1. PLANNING RENDEZVOUS")
maneuver = mj.maneuver_planner

# Plan Hohmann transfer to target
rendezvous = maneuver.operation_hohmann_transfer
rendezvous.make_nodes()

# Execute approach burn
node_exec = mj.node_executor
node_exec.tolerance = 0.5
node_exec.enabled = True

print("Executing approach burn...")
while node_exec.enabled:
    time.sleep(1)

# === PHASE 2: CLOSE APPROACH ===
print("\n2. FINE APPROACH")
# Get within 100m using Smart A.S.S.
smart_ass = mj.smart_ass
smart_ass.autopilot_mode = mj.SmartASSAutopilotMode.target
smart_ass.update()

# Thrust towards target until close
thrust = mj.thrust_controller
vessel.control.rcs = True

while vessel.orbital_reference_frame.position(target).magnitude > 100:
    distance = vessel.orbital_reference_frame.position(target).magnitude
    
    if distance > 1000:
        vessel.control.throttle = 0.1
    elif distance > 100:
        vessel.control.throttle = 0.05
    else:
        vessel.control.throttle = 0.0
    
    time.sleep(0.5)

vessel.control.throttle = 0.0
print("Close approach achieved")

# === PHASE 3: DOCKING ===
print("\n3. AUTOMATED DOCKING")
docking = mj.docking_autopilot
docking.speed_limit = 0.2  # Very slow approach
docking.roll_reference = mj.DockingAutopilotRollReference.off
docking.enabled = True

print("Docking in progress...")
while docking.enabled:
    status = docking.status
    print(f"Docking status: {status}")
    time.sleep(2)

if vessel.control.rcs:
    vessel.control.rcs = False

print("\n=== DOCKING COMPLETE ===")
print(f"{vessel.name} successfully docked with {target.name}")
```

## context_3

### context_3_description
Advanced kRPC utilities provide helper functions and classes for common spaceflight operations. These utilities handle coordinate transformations, orbital mechanics calculations, vessel state monitoring, and automated mission sequencing. They serve as building blocks for complex automated missions and can be combined with both basic kRPC and MechJeb functionality.

### context_3_code_snippet

```python
import krpc
import time
import math
from collections import namedtuple

class VesselMonitor:
    """Monitor vessel telemetry with data streams for efficiency"""
    
    def __init__(self, connection, vessel):
        self.conn = connection
        self.vessel = vessel
        self._setup_streams()
    
    def _setup_streams(self):
        """Set up data streams for efficient monitoring"""
        self.ut = self.conn.add_stream(getattr, self.conn.space_center, 'ut')
        self.altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'mean_altitude')
        self.speed = self.conn.add_stream(getattr, self.vessel.flight(), 'speed')
        self.vertical_speed = self.conn.add_stream(getattr, self.vessel.flight(), 'vertical_speed')
        self.apoapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
        self.periapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
        self.inclination = self.conn.add_stream(getattr, self.vessel.orbit, 'inclination')
        
    def get_telemetry(self):
        """Get current telemetry snapshot"""
        Telemetry = namedtuple('Telemetry', [
            'time', 'altitude', 'speed', 'vertical_speed', 
            'apoapsis', 'periapsis', 'inclination'
        ])
        return Telemetry(
            self.ut(), self.altitude(), self.speed(), self.vertical_speed(),
            self.apoapsis(), self.periapsis(), math.degrees(self.inclination())
        )

class OrbitalMechanics:
    """Utility functions for orbital mechanics calculations"""
    
    @staticmethod
    def hohmann_delta_v(r1, r2, mu):
        """Calculate delta-v required for Hohmann transfer"""
        v1 = math.sqrt(mu / r1)  # Circular velocity at r1
        v2 = math.sqrt(mu / r2)  # Circular velocity at r2
        
        # Transfer ellipse parameters
        a_transfer = (r1 + r2) / 2
        v_transfer_1 = math.sqrt(mu * (2/r1 - 1/a_transfer))
        v_transfer_2 = math.sqrt(mu * (2/r2 - 1/a_transfer))
        
        dv1 = abs(v_transfer_1 - v1)  # Departure burn
        dv2 = abs(v2 - v_transfer_2)  # Arrival burn
        
        return dv1, dv2, dv1 + dv2
    
    @staticmethod
    def time_to_phase_angle(current_angle, target_angle, angular_velocity):
        """Calculate time until target phase angle is reached"""
        angle_diff = (target_angle - current_angle) % 360
        if angle_diff > 180:
            angle_diff -= 360
        return abs(angle_diff / math.degrees(angular_velocity))

class MissionController:
    """High-level mission sequencing and control"""
    
    def __init__(self, connection):
        self.conn = connection
        self.vessel = connection.space_center.active_vessel
        self.monitor = VesselMonitor(connection, self.vessel)
        
        # Try to initialize MechJeb if available
        try:
            self.mj = connection.mech_jeb
            self.has_mechjeb = True
            print("MechJeb integration enabled")
        except:
            self.has_mechjeb = False
            print("Operating without MechJeb")
    
    def launch_to_orbit(self, target_altitude=100000, target_inclination=0):
        """Launch vessel to specified orbit"""
        if self.has_mechjeb:
            return self._launch_with_mechjeb(target_altitude, target_inclination)
        else:
            return self._launch_manual(target_altitude, target_inclination)
    
    def _launch_with_mechjeb(self, altitude, inclination):
        """Launch using MechJeb autopilot"""
        ascent = self.mj.ascent_autopilot
        ascent.desired_orbit_altitude = altitude
        ascent.desired_inclination = inclination
        ascent.enabled = True
        
        # Enable staging
        self.mj.staging_controller.enabled = True
        
        # Wait for completion
        while ascent.enabled:
            telem = self.monitor.get_telemetry()
            print(f"Alt: {telem.altitude:.0f}m, Speed: {telem.speed:.0f}m/s, "
                  f"Ap: {telem.apoapsis:.0f}m")
            time.sleep(5)
        
        return True
    
    def _launch_manual(self, altitude, inclination):
        """Manual launch implementation"""
        vessel = self.vessel
        
        # Launch
        vessel.control.activate_next_stage()
        vessel.auto_pilot.engage()
        vessel.auto_pilot.target_pitch_and_heading(90, 90)
        
        # Simple gravity turn
        turn_start = 250
        turn_end = 45000
        
        while self.monitor.apoapsis() < altitude:
            alt = self.monitor.altitude()
            
            # Gravity turn logic
            if turn_start < alt < turn_end:
                progress = (alt - turn_start) / (turn_end - turn_start)
                pitch = 90 - (progress * 90)
                vessel.auto_pilot.target_pitch_and_heading(pitch, 90)
            
            time.sleep(0.5)
        
        vessel.control.throttle = 0.0
        
        # Coast to apoapsis and circularize
        while vessel.orbit.time_to_apoapsis > 60:
            time.sleep(1)
        
        vessel.control.throttle = 1.0
        while self.monitor.periapsis() < altitude * 0.9:
            time.sleep(0.1)
        
        vessel.control.throttle = 0.0
        vessel.auto_pilot.disengage()
        
        return True
    
    def transfer_to_body(self, target_body_name):
        """Execute interplanetary transfer"""
        target_body = self.conn.space_center.bodies[target_body_name]
        
        if self.has_mechjeb:
            # Use MechJeb maneuver planner
            planner = self.mj.maneuver_planner
            hohmann = planner.operation_hohmann
            hohmann.make_nodes(target_body)
            
            # Execute with node executor
            executor = self.mj.node_executor
            executor.tolerance = 1.0
            executor.enabled = True
            
            while executor.enabled:
                time.sleep(1)
            
            print(f"Transfer to {target_body_name} complete")
        else:
            print("Manual transfer planning not implemented")
            return False
        
        return True
    
    def autonomous_docking(self, target_vessel):
        """Perform autonomous docking with target vessel"""
        if not self.has_mechjeb:
            print("Autonomous docking requires MechJeb")
            return False
        
        # Set target
        self.conn.space_center.target_vessel = target_vessel
        
        # Use MechJeb docking autopilot
        docking = self.mj.docking_autopilot
        docking.speed_limit = 0.5
        docking.enabled = True
        
        print(f"Docking with {target_vessel.name}...")
        
        while docking.enabled:
            time.sleep(2)
            print(f"Docking status: {docking.status}")
        
        print("Docking complete!")
        return True
```

### context_3_examples

```python
"""
Complete automated mission example using the mission controller
Demonstrates multi-phase mission with error handling and telemetry
"""
import krpc
import time
from mission_controller import MissionController, OrbitalMechanics

def main():
    # Connect to KSP
    print("Connecting to Kerbal Space Program...")
    conn = krpc.connect(name='Automated Mission Controller')
    
    # Initialize mission controller
    mission = MissionController(conn)
    print(f"Mission controller initialized for {mission.vessel.name}")
    
    try:
        # Phase 1: Launch to Low Kerbin Orbit
        print("\n=== PHASE 1: LAUNCH TO ORBIT ===")
        success = mission.launch_to_orbit(
            target_altitude=100000,
            target_inclination=0
        )
        
        if not success:
            print("Launch failed!")
            return
        
        print("Successfully reached orbit")
        telem = mission.monitor.get_telemetry()
        print(f"Final orbit: {telem.apoapsis:.0f} x {telem.periapsis:.0f} km")
        
        # Phase 2: Wait for optimal transfer window (simplified)
        print("\n=== PHASE 2: TRANSFER WINDOW ===")
        print("Calculating optimal transfer window to Mun...")
        
        # In a real mission, this would calculate proper phase angles
        time.sleep(5)  # Simulated calculation time
        
        # Phase 3: Execute transfer
        print("\n=== PHASE 3: INTERPLANETARY TRANSFER ===")
        success = mission.transfer_to_body('Mun')
        
        if not success:
            print("Transfer planning failed!")
            return
        
        # Phase 4: Monitor transfer progress
        print("\n=== PHASE 4: CRUISE PHASE ===")
        print("Transfer burn complete. Monitoring trajectory...")
        
        # Wait until we're in Mun's SOI
        mun = conn.space_center.bodies['Mun']
        while mission.vessel.orbit.body.name != 'Mun':
            time.sleep(10)
            distance = mission.vessel.orbit.body.position(mun, 
                       mission.vessel.orbit.body.reference_frame).magnitude
            print(f"Distance to Mun: {distance/1000:.0f} km")
        
        print("Entered Mun sphere of influence!")
        
        # Phase 5: Orbit insertion
        print("\n=== PHASE 5: ORBIT INSERTION ===")
        if mission.has_mechjeb:
            # Use MechJeb for circularization
            planner = mission.mj.maneuver_planner
            circularize = planner.operation_circularize
            circularize.make_nodes()
            
            executor = mission.mj.node_executor
            executor.enabled = True
            
            while executor.enabled:
                time.sleep(1)
            
            print("Mun orbit achieved!")
        
        # Phase 6: Landing (if equipped)
        print("\n=== PHASE 6: SURFACE OPERATIONS ===")
        if mission.has_mechjeb and has_landing_capability(mission.vessel):
            landing = mission.mj.landing_autopilot
            landing.enabled = True
            landing.touchdown_speed = 2.0
            landing.land_somewhere = True
            
            print("Beginning automated landing...")
            while landing.enabled:
                altitude = mission.monitor.altitude()
                print(f"Descent altitude: {altitude:.0f} m")
                time.sleep(5)
            
            print("Landed successfully!")
            
            # Simulate surface operations
            print("Conducting surface experiments...")
            time.sleep(30)
        
        print("\n=== MISSION COMPLETE ===")
        print("All objectives achieved successfully!")
        
    except Exception as e:
        print(f"Mission error: {e}")
        # Emergency procedures
        mission.vessel.control.throttle = 0.0
        if mission.vessel.auto_pilot.enabled:
            mission.vessel.auto_pilot.disengage()

def has_landing_capability(vessel):
    """Check if vessel has landing gear or parachutes"""
    for part in vessel.parts.all:
        if part.parachute or part.landing_gear:
            return True
    return False

if __name__ == "__main__":
    main()
```