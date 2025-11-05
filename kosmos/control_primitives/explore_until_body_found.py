async def explore_until_body_found(conn, target_body_name, max_time=3600):
    """
    Explore space until target body is found (similar to exploreUntil)
    """
    space_center = conn.space_center
    vessel = space_center.active_vessel
    
    # Check if we can already see the target
    if target_body_name in space_center.bodies:
        target_body = space_center.bodies[target_body_name]
        print(f"Found {target_body_name}")
        return target_body
    
    start_time = time.time()
    
    print(f"Exploring space to find {target_body_name}...")
    
    # Simple exploration - change orbital plane and look around
    while time.time() - start_time < max_time:
        # In real implementation, this would use proper orbital mechanics
        # to search for celestial bodies
        
        # Check if we found the target
        if target_body_name in space_center.bodies:
            target_body = space_center.bodies[target_body_name]
            print(f"Found {target_body_name} after {time.time() - start_time:.1f} seconds")
            return target_body
        
        time.sleep(10)  # Search interval
    
    print(f"Could not find {target_body_name} within {max_time} seconds")
    return None