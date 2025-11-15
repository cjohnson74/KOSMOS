# Launch to 100km orbit: launch_vessel(conn, 100000);
# Launch to polar orbit: launch_vessel(conn, 120000, 90);
async def launch_vessel(conn, target_apoapsis=100000, target_inclination=0):
    vessel = conn.space_center.active_vessel
    control = vessel.control
    
    # Pre-launch setup
    control.sas = True
    control.throttle = 1.0
    control.activate_next_stage()  # Launch!
    
    # Execute gravity turn
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    
    # Monitor ascent and stage as needed
    while vessel.orbit.apoapsis_altitude < target_apoapsis:
        altitude = vessel.flight().mean_altitude
        if altitude > 250:  # Start gravity turn
            turn_progress = min(1.0, (altitude - 250) / 45000)
            pitch = 90 - (turn_progress * 90)
            vessel.auto_pilot.target_pitch_and_heading(pitch, 90)
        
        if should_stage(vessel):
            control.activate_next_stage()
        
        await asyncio.sleep(0.1)
    
    # Circularization burn
    control.throttle = 0.0
    await wait_for_apoapsis(vessel, 60)
    await circularize_orbit(vessel)