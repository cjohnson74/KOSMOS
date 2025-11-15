# Transfer all available fuel from external tank to main tank: transfer_fuel(conn, "External Tank", "Main Tank");
# Transfer specific amount: transfer_fuel(conn, "Booster Tank", "Core Tank", "LiquidFuel", 500);
async def transfer_fuel(conn, from_tank_name, to_tank_name, fuel_type="LiquidFuel", amount=None):
    vessel = conn.space_center.active_vessel
    
    # Find source and destination parts
    source_part = find_part_by_name(vessel, from_tank_name)
    dest_part = find_part_by_name(vessel, to_tank_name)
    
    if not source_part or not dest_part:
        return False
    
    # Calculate transfer amount if not specified
    if amount is None:
        available = source_part.resources.amount(fuel_type)
        capacity = dest_part.resources.max(fuel_type) - dest_part.resources.amount(fuel_type)
        amount = min(available, capacity)
    
    # Perform transfer using resource transfer API
    await perform_resource_transfer(source_part, dest_part, fuel_type, amount)
    return True