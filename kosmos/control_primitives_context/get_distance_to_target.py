def get_distance_to_target(vessel, target):
    """Get distance between vessel and target"""
    vessel_pos = vessel.position(target.reference_frame)
    return math.sqrt(sum(x**2 for x in vessel_pos))