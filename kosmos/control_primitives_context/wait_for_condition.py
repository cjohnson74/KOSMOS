# Wait until apoapsis: wait_for_condition(conn, lambda v: v.orbit.time_to_apoapsis < 60);
# Wait for specific altitude: wait_for_condition(conn, lambda v: v.flight().mean_altitude > 70000);
async def wait_for_condition(conn, condition_func, timeout=300):
    vessel = conn.space_center.active_vessel
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if condition_func(vessel):
            return True
        await asyncio.sleep(1)
    
    return False  # Timeout