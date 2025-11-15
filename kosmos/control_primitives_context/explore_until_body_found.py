"""
Explore until find Mun in tracking station view:
target_body = await explore_until_body_found(conn, "Mun", 300, lambda: 
    "Mun" in conn.space_center.bodies and 
    can_see_body(conn.space_center.bodies["Mun"])
);

Explore until find any asteroid:
asteroid = await explore_until_body_found(conn, "asteroid", 600, lambda:
    find_nearest_asteroid(conn)
);
"""
async def explore_until_body_found(conn, target_name, max_time=300, callback=None):
    """
    target_name: str, name of celestial body to find
    max_time: number, maximum time to search in seconds  
    callback: function, custom condition check, will be called every 10 seconds
    Return: body object if found, None if timeout
    """
    start_time = time.time()
    
    # Initial check
    if callback and callback():
        return callback()
    
    # Search loop
    while time.time() - start_time < max_time:
        # Change view/orbit to search for bodies
        await change_orbital_view(conn)
        
        # Check if target found
        if target_name in conn.space_center.bodies:
            body = conn.space_center.bodies[target_name]
            return body
        
        if callback:
            result = callback()
            if result:
                return result
        
        await asyncio.sleep(10)  # Search interval
    
    return None