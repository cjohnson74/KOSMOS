def find_available_docking_port(vessel):
    """Find ready docking port on vessel"""
    for port in vessel.parts.docking_ports:
        if port.state.name == 'ready':
            return port
    return None