async def launch_vessel(conn, target_apoapsis=100000, target_inclination=0):
    """
    Launch vessel to specified orbit
    Similar to craftItem - executes a complex sequence with error handling
    """
    global _stage_fail_count
    
    if target_apoapsis < 70000:
        raise ValueError("target_apoapsis must be at least 70000m for stable orbit")
    
    vessel = conn.space_center.active_vessel
    control = vessel.control
    
    try:
        # Pre-launch checks
        if vessel.situation.name != 'pre_launch':
            raise ValueError("Vessel must be on launchpad to launch")
        
        # Initial staging and launch
        conn.space_center.physics_warp_factor = 1
        control.sas = True
        control.rcs = False
        control.throttle = 1.0
        
        # Launch!
        control.activate_next_stage()
        
        # Monitor ascent
        altitude_stream = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
        apoapsis_stream = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
        
        # Simple gravity turn
        vessel.auto_pilot.engage()
        vessel.auto_pilot.target_pitch_and_heading(90, 90)
        
        turn_start_altitude = 250
        turn_end_altitude = 45000
        
        while apoapsis_stream() < target_apoapsis:
            altitude = altitude_stream()
            
            # Execute gravity turn
            if turn_start_altitude < altitude < turn_end_altitude:
                turn_progress = (altitude - turn_start_altitude) / (turn_end_altitude - turn_start_altitude)
                target_pitch = 90 - (turn_progress * 90)
                vessel.auto_pilot.target_pitch_and_heading(target_pitch, 90)
            
            # Check for staging opportunities
            if should_stage(vessel):
                control.activate_next_stage()
                time.sleep(1)
            
            time.sleep(0.1)
        
        control.throttle = 0.0
        print(f"Target apoapsis of {target_apoapsis}m reached")
        
        # Coast to apoapsis for circularization
        while vessel.orbit.time_to_apoapsis > 60:
            time.sleep(1)
        
        # Circularization burn
        control.throttle = 1.0
        periapsis_stream = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
        
        while periapsis_stream() < target_apoapsis * 0.9:
            time.sleep(0.1)
        
        control.throttle = 0.0
        vessel.auto_pilot.disengage()
        
        print(f"Successfully reached orbit: {vessel.orbit.apoapsis_altitude:.0f} x {vessel.orbit.periapsis_altitude:.0f}m")
        return True
        
    except Exception as err:
        control.throttle = 0.0
        if vessel.auto_pilot.engaged:
            vessel.auto_pilot.disengage()
        print(f"Launch failed: {err}")
        _stage_fail_count += 1
        if _stage_fail_count > 3:
            raise Exception("Launch failed too many times, check vessel design")
        return False