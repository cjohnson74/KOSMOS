# Stage when current stage is empty: stage_vessel(conn);
async def stage_vessel(conn):
    vessel = conn.space_center.active_vessel
    control = vessel.control
    
    # Check if staging is safe and necessary
    if should_stage(vessel):
        control.activate_next_stage()
        await asyncio.sleep(1)  # Wait for staging to complete
        return True
    
    return False