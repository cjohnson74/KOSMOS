# Navigation functions for spacecraft movement
await set_vessel_target_position(vessel, x, y, z)  # Move vessel to specific coordinates
await approach_target(vessel, target, distance)    # Get within specified distance of target
await maintain_formation(vessel, target, offset)   # Maintain relative position to target
await orbit_target(vessel, target, altitude)       # Enter orbit around target body
await intercept_trajectory(vessel, target)         # Calculate and execute intercept

# Vessel state functions  
vessel_at_position(vessel, x, y, z, tolerance)     # Check if vessel is at position
get_vessel_distance_to(vessel, target)             # Get distance to target
is_in_orbit(vessel, body)                          # Check if vessel is orbiting body
has_clear_trajectory(vessel, target)               # Check for collision-free path

# Vessel control functions
await orient_vessel(vessel, direction)             # Point vessel in specific direction  
await set_vessel_throttle(vessel, throttle)        # Set engine throttle (0.0 to 1.0)
await activate_vessel_stage(vessel)                # Trigger next stage
await deploy_vessel_component(vessel, component)   # Deploy solar panels, antennas, etc.
await retract_vessel_component(vessel, component)  # Retract deployed components

# Resource and system functions
await activate_vessel_system(vessel, system_name)  # Turn on/off vessel systems
await check_vessel_resources(vessel)               # Check fuel, power, life support
await repair_vessel_component(vessel, part)        # Attempt repairs on damaged parts
await transfer_crew(vessel, source, destination)   # Move crew between parts/vessels