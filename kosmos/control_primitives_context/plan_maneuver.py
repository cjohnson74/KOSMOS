# Plan Hohmann transfer to Mun: plan_maneuver(conn, "hohmann_transfer", target_body="Mun");
# Plan orbit circularization: plan_maneuver(conn, "circularize");
async def plan_maneuver(conn, maneuver_type, **kwargs):
    vessel = conn.space_center.active_vessel
    
    if maneuver_type == "hohmann_transfer":
        target_body = kwargs.get("target_body")
        node = calculate_hohmann_transfer(vessel, target_body)
        
    elif maneuver_type == "circularize":
        node = calculate_circularization_burn(vessel)
        
    elif maneuver_type == "plane_change":
        target_inclination = kwargs.get("inclination", 0)
        node = calculate_plane_change(vessel, target_inclination)
    
    # Add the calculated node to the flight plan
    control = vessel.control
    control.add_node(node.ut, node.prograde, node.normal, node.radial)
    
    return node