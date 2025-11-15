def calculate_burn_time(vessel, delta_v):
    """Calculate time needed for burn"""
    isp = vessel.specific_impulse * 9.82
    mass = vessel.mass
    thrust = vessel.available_thrust
    return mass * isp * (1 - math.exp(-delta_v / isp)) / thrust