def should_stage(vessel):
    """Check if vessel should stage (similar to recipe validation in craftItem)"""
    # Check if current stage engines are out of fuel
    resources = vessel.resources_in_decouple_stage(vessel.control.current_stage, cumulative=False)
    
    # If we have SRBs and they're empty, stage
    if resources.max('SolidFuel') > 0 and resources.amount('SolidFuel') < 0.1:
        return True
    
    # If liquid fuel engines are empty, stage
    if (resources.max('LiquidFuel') > 0 and resources.amount('LiquidFuel') < 0.1 and
        resources.max('Oxidizer') > 0 and resources.amount('Oxidizer') < 0.1):
        return True
    
    return False