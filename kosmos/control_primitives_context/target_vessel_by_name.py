# Target space station: target_vessel_by_name(conn, "Space Station Alpha");
async def target_vessel_by_name(conn, vessel_name):
    space_center = conn.space_center
    
    for vessel in space_center.vessels:
        if vessel.name == vessel_name:
            space_center.target_vessel = vessel
            return vessel
    
    return None