async def land_vessel(conn, target_body=None, deploy_gear=True, target_speed=5.0):
    """
    Land vessel on surface (similar to placeItem - precise positioning)
    """
    global _land_fail_count
    
    vessel = conn.space_center.active_vessel
    control = vessel.control
    
    if target_body is None:
        target_body = vessel.orbit.body
    
    try:
        # Pre-landing checks
        if vessel.situation.name == 'landed':
            print("Vessel is already landed")
            return True
        
        # Deorbit burn (simplified)
        if vessel.orbit.periapsis_altitude > 0:
            print("Executing deorbit burn...")
            control.sas = True
            control.sas_mode = conn.space_center.SASMode.retrograde
            control.throttle = 1.0
            
            # Burn until periapsis is negative
            while vessel.orbit.periapsis_altitude > -10000:
                time.sleep(0.1)
            
            control.throttle = 0.0
        
        # Descent phase
        print("Beginning descent...")
        altitude_stream = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
        speed_stream = conn.add_stream(getattr, vessel.flight(), 'speed')
        vertical_speed_stream = conn.add_stream(getattr, vessel.flight(), 'vertical_speed')
        
        # Deploy parachutes if available and in atmosphere
        if target_body.has_atmosphere and vessel.parts.parachutes:
            for parachute in vessel.parts.parachutes:
                if parachute.can_deploy:
                    parachute.deploy()
                    print("Parachutes deployed")
        
        # Powered landing phase
        gear_deployed = False
        
        while vessel.situation.name != 'landed':
            altitude = altitude_stream()
            speed = speed_stream()
            vertical_speed = vertical_speed_stream()
            
            # Deploy landing gear
            if altitude < 1000 and not gear_deployed and deploy_gear:
                control.gear = True
                gear_deployed = True
                print("Landing gear deployed")
            
            # Suicide burn calculation (simplified)
            if altitude < 500 and vertical_speed < -10:
                control.sas = True
                control.sas_mode = conn.space_center.SASMode.retrograde
                
                # Calculate throttle needed
                if vertical_speed < -target_speed:
                    control.throttle = min(1.0, abs(vertical_speed) / 20)
                else:
                    control.throttle = 0.0
            
            time.sleep(0.1)
        
        control.throttle = 0.0
        print(f"Landing successful! Touchdown speed: {speed:.1f} m/s")
        return True
        
    except Exception as err:
        control.throttle = 0.0
        print(f"Landing failed: {err}")
        _land_fail_count += 1
        if _land_fail_count > 3:
            raise Exception("Landing failed too many times")
        return False