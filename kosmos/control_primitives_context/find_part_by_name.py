def find_part_by_name(vessel, part_name):
    """Find vessel part by name"""
    for part in vessel.parts.all:
        if part.title == part_name or part.name == part_name:
            return part
    return None