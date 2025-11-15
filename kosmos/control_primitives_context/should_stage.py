def should_stage(vessel):
    """Check if vessel should stage based on fuel levels"""
    current_stage = vessel.control.current_stage
    resources = vessel.resources_in_decouple_stage(current_stage, cumulative=False)
    
    # Check SRB fuel
    if resources.max('SolidFuel') > 0 and resources.amount('SolidFuel') < 0.1:
        return True
    
    # Check liquid fuel  
    if (resources.max('LiquidFuel') > 0 and resources.amount('LiquidFuel') < 0.1 and
        resources.max('Oxidizer') > 0 and resources.amount('Oxidizer') < 0.1):
        return True
    
    return False