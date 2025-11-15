# Deploy all solar panels: deploy_component(conn, "solar_panels");
# Deploy landing gear: deploy_component(conn, "landing_gear");  
# Deploy specific antenna: deploy_component(conn, "antenna", part_name="High Gain Antenna");
async def deploy_component(conn, component_type, part_name=None):
    vessel = conn.space_center.active_vessel
    
    deployed_count = 0
    
    for part in vessel.parts.all:
        # Check if this part matches what we want to deploy
        should_deploy = False
        
        if component_type == "solar_panels" and part.solar_panel:
            should_deploy = True
            part.solar_panel.deployed = True
            
        elif component_type == "landing_gear" and part.landing_gear:
            should_deploy = True
            part.landing_gear.deployed = True
            
        elif component_type == "antenna" and part.antenna:
            if part_name is None or part.title == part_name:
                should_deploy = True
                part.antenna.deployed = True
                
        elif component_type == "parachute" and part.parachute:
            if part.parachute.can_deploy:
                should_deploy = True
                part.parachute.deploy()
        
        if should_deploy:
            deployed_count += 1
    
    return deployed_count > 0