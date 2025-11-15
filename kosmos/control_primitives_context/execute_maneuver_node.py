# Execute the first planned maneuver: execute_maneuver_node(conn);
# Execute specific node with high precision: execute_maneuver_node(conn, node, 0.1);
async def execute_maneuver_node(conn, node=None, tolerance=1.0):
    vessel = conn.space_center.active_vessel
    control = vessel.control
    
    if node is None:
        node = control.nodes[0]  # Use first node
    
    # Calculate burn time
    burn_time = calculate_burn_time(vessel, node.delta_v)
    burn_start = node.ut - (burn_time / 2)
    
    # Warp to maneuver
    conn.space_center.warp_to(burn_start - 5)
    
    # Orient to maneuver direction
    control.sas = True
    control.sas_mode = conn.space_center.SASMode.maneuver
    await asyncio.sleep(3)  # Wait for orientation
    
    # Execute burn
    control.throttle = 1.0
    while node.remaining_delta_v > tolerance:
        if node.remaining_delta_v < 10:
            control.throttle = 0.1  # Fine control
        await asyncio.sleep(0.1)
    
    control.throttle = 0.0
    node.remove()