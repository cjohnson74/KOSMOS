# Land on current body: land_vessel(conn);
# Land on Mun with specific touchdown speed: land_vessel(conn, "Mun", True, 2.0);
async def land_vessel(conn, target_body=None, deploy_gear=True, target_speed=5.0):
    vessel = conn.space_center.active_vessel
    control = vessel.control
    
    if target_body is None:
        target_body = vessel.orbit.body
    
    # Deorbit burn if needed
    if vessel.orbit.periapsis_altitude > 0:
        await execute_deorbit_burn(vessel)
    
    # Deploy parachutes in atmosphere
    if target_body.has_atmosphere:
        await deploy_parachutes_when_safe(vessel)
    
    # Powered descent
    while vessel.situation.name != 'landed':
        altitude = vessel.flight().surface_altitude
        vertical_speed = vessel.flight().vertical_speed
        
        # Deploy landing gear
        if altitude < 1000 and deploy_gear:
            control.gear = True
        
        # Suicide burn calculation
        if altitude < 500 and vertical_speed < -target_speed:
            control.sas = True
            control.sas_mode = conn.space_center.SASMode.retrograde
            control.throttle = calculate_landing_throttle(vertical_speed, target_speed)
        
        await asyncio.sleep(0.1)
    
    control.throttle = 0.0