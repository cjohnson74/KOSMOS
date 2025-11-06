async def execute_maneuver_node(conn, node=None, tolerance=1.0):
    """
    Execute a maneuver node (similar to smeltItem - complex process with validation)
    """
    global _burn_fail_count
    
    vessel = conn.space_center.active_vessel
    control = vessel.control
    
    if node is None:
        if not control.nodes:
            print("No maneuver nodes to execute")
            return False
        node = control.nodes[0]
    
    try:
        # Calculate burn time
        isp = vessel.specific_impulse * 9.82  # Convert to m/s
        mass = vessel.mass
        delta_v = node.delta_v
        burn_time = mass * isp * (1 - math.exp(-delta_v / isp)) / vessel.available_thrust
        
        # Wait until burn time
        burn_ut = node.ut - (burn_time / 2)
        lead_time = 5  # Start orienting 5 seconds early
        
        # Warp to maneuver time
        conn.space_center.warp_to(burn_ut - lead_time)
        
        # Orient to maneuver
        control.sas = True
        control.sas_mode = conn.space_center.SASMode.maneuver
        
        # Wait for orientation
        time.sleep(3)
        
        # Execute burn
        remaining_delta_v = node.remaining_delta_v
        control.throttle = 1.0
        
        while remaining_delta_v > tolerance:
            remaining_delta_v = node.remaining_delta_v
            
            # Throttle down as we approach target
            if remaining_delta_v < 10:
                control.throttle = 0.1
            elif remaining_delta_v < 50:
                control.throttle = 0.5
            
            time.sleep(0.1)
        
        control.throttle = 0.0
        node.remove()
        
        print(f"Maneuver executed successfully, {remaining_delta_v:.1f} m/s remaining")
        return True
        
    except Exception as err:
        control.throttle = 0.0
        print(f"Maneuver execution failed: {err}")
        _burn_fail_count += 1
        if _burn_fail_count > 5:
            raise Exception("Maneuver execution failed too many times")
        return False