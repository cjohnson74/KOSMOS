async def transfer_fuel(conn, from_tank, to_tank, fuel_type='LiquidFuel', amount=None):
    """
    Transfer fuel between tanks (similar to chest operations)
    """
    vessel = conn.space_center.active_vessel
    
    try:
        # Find source and destination tanks
        source_tank = None
        dest_tank = None
        
        for part in vessel.parts.all:
            if part.name == from_tank and part.resources.amount(fuel_type) > 0:
                source_tank = part
            elif part.name == to_tank and part.resources.max(fuel_type) > 0:
                dest_tank = part
        
        if not source_tank:
            print(f"No source tank '{from_tank}' with {fuel_type} found")
            return False
        
        if not dest_tank:
            print(f"No destination tank '{to_tank}' found")
            return False
        
        # Calculate transfer amount
        if amount is None:
            available = source_tank.resources.amount(fuel_type)
            capacity = dest_tank.resources.max(fuel_type) - dest_tank.resources.amount(fuel_type)
            amount = min(available, capacity)
        
        # Perform transfer (simplified - real implementation would use proper API)
        print(f"Transferring {amount:.1f} units of {fuel_type} from {from_tank} to {to_tank}")
        
        # In real kRPC, this would use the resource transfer API
        return True
        
    except Exception as err:
        print(f"Fuel transfer failed: {err}")
        return False