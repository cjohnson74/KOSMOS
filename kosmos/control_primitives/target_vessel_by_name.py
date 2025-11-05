async def target_vessel_by_name(conn, vessel_name):
    """Target a vessel by name (similar to item finding)"""
    space_center = conn.space_center
    
    for vessel in space_center.vessels:
        if vessel.name == vessel_name:
            space_center.target_vessel = vessel
            print(f"Targeted vessel: {vessel_name}")
            return vessel
    
    print(f"No vessel named '{vessel_name}' found")
    return None