# Dock with targeted vessel: dock_with_target(conn);
# Slow precision docking: dock_with_target(conn, 25, 0.2);
async def dock_with_target(conn, approach_distance=50, final_speed=0.5):
    vessel = conn.space_center.active_vessel
    control = vessel.control
    target = conn.space_center.target_vessel
    
    # Enable RCS for fine control
    control.rcs = True
    control.sas = True
    control.sas_mode = conn.space_center.SASMode.target
    
    # Close approach phase
    while get_distance_to_target(vessel, target) > approach_distance:
        distance = get_distance_to_target(vessel, target)
        
        if distance > 1000:
            control.throttle = 0.1
        elif distance > 100:
            control.throttle = 0.05
        else:
            control.throttle = 0.01
        
        await asyncio.sleep(0.5)
    
    control.throttle = 0.0
    
    # Final docking approach
    docking_port = find_available_docking_port(vessel)
    target_port = find_available_docking_port(target)
    
    await perform_final_docking_approach(vessel, target, final_speed)
