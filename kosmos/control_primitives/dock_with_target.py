async def dock_with_target(conn, approach_distance=50, final_approach_speed=0.5):
    """
    Dock with target vessel (similar to complex multi-step operations)
    """
    global _dock_fail_count
    
    vessel = conn.space_center.active_vessel
    control = vessel.control
    space_center = conn.space_center
    
    if not space_center.target_vessel:
        print("No target vessel selected for docking")
        return False
    
    target = space_center.target_vessel
    
    try:
        # Phase 1: Close approach
        control.rcs = True
        control.sas = True
        control.sas_mode = space_center.SASMode.target
        
        # Get close to target
        while True:
            target_distance = vessel.orbital_reference_frame.position(target).magnitude
            
            if target_distance < approach_distance:
                break
            
            # Thrust toward target
            if target_distance > 1000:
                control.throttle = 0.1
            elif target_distance > 100:
                control.throttle = 0.05
            else:
                control.throttle = 0.01
            
            time.sleep(0.5)
        
        control.throttle = 0.0
        print(f"Close approach achieved: {target_distance:.1f}m")
        
        # Phase 2: Final docking approach
        control.sas_mode = space_center.SASMode.stability_assist
        
        # Find docking ports
        my_port = find_docking_port(vessel)
        target_port = find_docking_port(target)
        
        if not my_port or not target_port:
            print("Could not find docking ports on vessels")
            return False
        
        # Approach target port
        while not vessel.parts.docking_ports[0].state.name == 'docked':
            # Simple approach logic
            time.sleep(1)
            
            # In real implementation, this would use precise navigation
            # This is simplified for the primitive example
            
        print("Docking successful!")
        control.rcs = False
        return True
        
    except Exception as err:
        control.throttle = 0.0
        control.rcs = False
        print(f"Docking failed: {err}")
        _dock_fail_count += 1
        if _dock_fail_count > 3:
            raise Exception("Docking failed too many times")
        return False

def find_docking_port(vessel):
    """Find available docking port on vessel"""
    for port in vessel.parts.docking_ports:
        if port.state.name == 'ready':
            return port
    return None