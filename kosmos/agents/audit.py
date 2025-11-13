import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from kosmos.prompts import load_prompt
from kosmos.utils import fix_and_parse_json

class AuditAgent:
    def __init__(
        self,
        model_name="gpt-3.5-turbo",
        temperature=0,
        request_timeout=120,
        mode="auto",
    ):
        print(f"🔍 DEBUG: AuditAgent initializing with model={model_name}, mode={mode}")
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timeout,
            openai_api_key=os.getenv("OPENAI")
        )
        assert mode in ["auto", "manual"]
        self.mode = mode
        print(f"🔍 DEBUG: AuditAgent initialized successfully")

    def render_system_message(self):
        # Load MechJeb documentation only
        mechjeb_docs = load_prompt("mechjeb_readmellm")
        system_message = SystemMessage(content=load_prompt("audit").format(mechjeb_docs=mechjeb_docs))
        return system_message

    def render_human_message(self, *, events, task, context, vessel_observation):
        print(f"🔍 DEBUG: AuditAgent rendering human message for task: '{task[:50]}...'")
        print(f"🔍 DEBUG: AuditAgent processing {len(events)} events")
        
        # Handle both observe and error events
        try:
            last_event = events[-1]
            if isinstance(last_event, tuple) and len(last_event) > 1:
                event_type, event = last_event
            else:
                event_type, event = "observe", last_event
            
            # Check if event is None
            if event is None:
                return HumanMessage(content=f"ERROR: No telemetry data available\n\nTask: {task}\n\nContext: {context or 'None'}\n\n")
            
            if not isinstance(event, dict):
                return HumanMessage(content=f"ERROR: Invalid telemetry data type: {type(event).__name__}\n\nTask: {task}\n\nContext: {context or 'None'}\n\n")
        except (IndexError, TypeError, AttributeError) as e:
            print(f"🔍 DEBUG: Error extracting event from events: {e}")
            return HumanMessage(content=f"ERROR: Failed to extract telemetry from events: {type(e).__name__}\n\nTask: {task}\n\nContext: {context or 'None'}\n\n")
            
        # Check for error events and provide feedback instead of returning None
        error_events = []
        for evt_tuple in events:
            try:
                if isinstance(evt_tuple, tuple) and len(evt_tuple) > 1:
                    evt_type, evt_data = evt_tuple
                else:
                    evt_type, evt_data = "observe", evt_tuple
                
                if evt_type == "error" and evt_data is not None:
                    if isinstance(evt_data, dict):
                        error_events.append(evt_data)
                        error_msg = evt_data.get('execution_error', 'Unknown error') if isinstance(evt_data, dict) else 'Unknown error'
                        print(f"\033[31mAudit Agent: Error occurred - {error_msg}\033[0m")
            except (TypeError, AttributeError) as e:
                print(f"🔍 DEBUG: Error processing event in error detection: {e}")
                continue
        
        # If there are errors, create a special error-focused observation
        if error_events:
            observation = f"ERROR ANALYSIS:\n\n"
            for i, error_event in enumerate(error_events):
                error_msg = error_event.get('execution_error', 'Unknown error')
                error_type = error_event.get('exception_type', 'Unknown')
                observation += f"Error {i+1}: {error_type} - {error_msg}\n\n"
            
            observation += f"Task: {task}\n\n"
            if context:
                observation += f"Context: {context}\n\n"
            else:
                observation += f"Context: None\n\n"
            
            observation += "Please analyze these errors and provide guidance on how to fix them.\n"
            
            print(f"🔍 DEBUG: AuditAgent error analysis message constructed, length={len(observation)} chars")
            print(f"\033[31m****Audit Agent error analysis message****\n{observation}\033[0m")
            return HumanMessage(content=observation)

        # Extract comprehensive telemetry if available (safely)
        comprehensive = event.get("comprehensive_telemetry") if isinstance(event, dict) else {}
        if comprehensive is None:
            comprehensive = {}
        
        # Extract key telemetry data (use comprehensive data when available)
        current_body = event.get("current_body", "Unknown")
        mission_time = event.get("mission_time", 0)
        vessel_situation = event.get("vessel_situation", "Unknown")
        
        # Altitude - use comprehensive data if available
        altitude = event.get("altitude", 0)
        if comprehensive.get('altitude_location', {}).get('mean_altitude') is not None:
            altitude = comprehensive['altitude_location']['mean_altitude']
        surface_altitude = event.get("surface_altitude", 0)
        if comprehensive.get('altitude_location', {}).get('surface_altitude') is not None:
            surface_altitude = comprehensive['altitude_location']['surface_altitude']
        
        # Speed - use comprehensive data if available
        speed = event.get("speed", 0)
        if comprehensive.get('position_velocity', {}).get('speed') is not None:
            speed = comprehensive['position_velocity']['speed']
        vertical_speed = event.get("vertical_speed", 0)
        if comprehensive.get('position_velocity', {}).get('vertical_speed') is not None:
            vertical_speed = comprehensive['position_velocity']['vertical_speed']
        horizontal_speed = event.get("horizontal_speed", 0)
        if comprehensive.get('position_velocity', {}).get('horizontal_speed') is not None:
            horizontal_speed = comprehensive['position_velocity']['horizontal_speed']
        
        # Orbital parameters - use comprehensive data if available
        orbit_params = event.get("orbit_parameters", {})
        comp_orbital = comprehensive.get('orbital', {})
        
        apoapsis = orbit_params.get("apoapsis_altitude", comp_orbital.get("apoapsis_altitude", 0))
        periapsis = orbit_params.get("periapsis_altitude", comp_orbital.get("periapsis_altitude", 0))
        inclination = orbit_params.get("inclination", comp_orbital.get("inclination", 0))
        eccentricity = orbit_params.get("eccentricity", comp_orbital.get("eccentricity", 0))
        period = orbit_params.get("period", comp_orbital.get("period", 0))
        time_to_apoapsis = orbit_params.get("time_to_apoapsis", comp_orbital.get("time_to_apoapsis", 0))
        time_to_periapsis = orbit_params.get("time_to_periapsis", comp_orbital.get("time_to_periapsis", 0))
        
        # Resources - merge with comprehensive data
        resources = event.get("resources", {})
        comp_resources = comprehensive.get('resources', {})
        all_resources = {**resources}
        for name, data in comp_resources.items():
            if name not in all_resources:
                all_resources[name] = {'amount': data.get('amount', 0), 'max': data.get('max', 0)}
        
        liquid_fuel = all_resources.get("LiquidFuel", {}).get("amount", 0)
        oxidizer = all_resources.get("Oxidizer", {}).get("amount", 0)
        monoprop = all_resources.get("MonoPropellant", {}).get("amount", 0)
        electric_charge = all_resources.get("ElectricCharge", {}).get("amount", 0)
        
        # Position and velocity
        position = event.get("position", {"x": 0, "y": 0, "z": 0})
        velocity = event.get("velocity", {"x": 0, "y": 0, "z": 0})
        
        # Control state - use comprehensive data if available
        control_state = event.get("control_state", {})
        if not control_state:
            control_state = event.get("vessel_status", {}).get("control_state", {})
        comp_control = comprehensive.get('control', {})
        
        throttle = comp_control.get("throttle", control_state.get("throttle", 0))
        sas = comp_control.get("sas", control_state.get("sas", False))
        rcs = comp_control.get("rcs", control_state.get("rcs", False))
        gear = comp_control.get("gear", control_state.get("gear", False))
        
        # Vessel status - use comprehensive data
        vessel_status = event.get("vessel_status", {})
        basic_vessel = comprehensive.get('basic_vessel', {})
        performance = comprehensive.get('performance', {})
        
        mass = vessel_status.get("mass", basic_vessel.get("mass", 0))
        dry_mass = vessel_status.get("dry_mass", basic_vessel.get("dry_mass", 0))
        thrust = vessel_status.get("thrust", performance.get("thrust", 0))
        max_thrust = vessel_status.get("max_thrust", performance.get("max_thrust", 0))
        isp = vessel_status.get("specific_impulse", performance.get("specific_impulse", 0))
        
        # Orientation - from comprehensive telemetry
        orientation = comprehensive.get('orientation', {})
        heading = orientation.get('heading', 0)
        pitch = orientation.get('pitch', 0)
        roll = orientation.get('roll', 0)
        
        # Autopilot status
        autopilot = comprehensive.get('autopilot', {})
        autopilot_engaged = autopilot.get('engaged', False)
        autopilot_error = autopilot.get('error', 0)
        
        # MechJeb status
        mechjeb_status = event.get("mechjeb_status", {})
        mechjeb = comprehensive.get('mechjeb', {})
        mechjeb_available = mechjeb.get('available', False) or mechjeb_status.get('api_ready', False)
        mechjeb_api_ready = mechjeb.get('api_ready', False) or mechjeb_status.get('api_ready', False)
        
        # Additional comprehensive telemetry data
        aerodynamics = comprehensive.get('aerodynamics', {})
        flight_dynamics = comprehensive.get('flight_dynamics', {})
        reference_vectors = comprehensive.get('reference_vectors', {})
        torque = comprehensive.get('torque', {})
        
        # G-force from comprehensive telemetry
        g_force = flight_dynamics.get('g_force', 0)
        
        # Aerodynamics data
        drag_raw = aerodynamics.get('drag', 0)
        lift_raw = aerodynamics.get('lift', 0)
        mach = aerodynamics.get('mach', 0)
        atmosphere_density = aerodynamics.get('atmosphere_density', 0)
        
        # Convert drag/lift to magnitude if they're vectors (tuples)
        if isinstance(drag_raw, tuple) and len(drag_raw) == 3:
            drag = (drag_raw[0]**2 + drag_raw[1]**2 + drag_raw[2]**2)**0.5
        else:
            drag = float(drag_raw) if drag_raw else 0
        
        if isinstance(lift_raw, tuple) and len(lift_raw) == 3:
            lift = (lift_raw[0]**2 + lift_raw[1]**2 + lift_raw[2]**2)**0.5
        else:
            lift = float(lift_raw) if lift_raw else 0
        
        # Reference vectors for navigation
        prograde = reference_vectors.get('prograde')
        retrograde = reference_vectors.get('retrograde')
        
        # Torque capabilities
        available_torque = torque.get('available_torque')
        available_thrust = torque.get('available_thrust', 0)
        
        # Part status details
        part_status = event.get("part_status", {})
        part_count = part_status.get("part_count", 0)
        current_stage = part_status.get("current_stage", 0)
        
        # Build comprehensive observation
        observation = ""
        observation += f"=== VESSEL STATUS ===\n"
        observation += f"Current body: {current_body}\n"
        observation += f"Mission time: {mission_time:.1f}s\n"
        observation += f"Vessel situation: {vessel_situation}\n\n"
        
        observation += f"=== POSITION & MOTION ===\n"
        observation += f"Altitude: {altitude:.0f}m (Surface: {surface_altitude:.0f}m)\n"
        observation += f"Speed: {speed:.1f}m/s (Vertical: {vertical_speed:.1f}m/s, Horizontal: {horizontal_speed:.1f}m/s)\n"
        observation += f"Position: x={position['x']:.1f}, y={position['y']:.1f}, z={position['z']:.1f}\n"
        observation += f"Velocity: x={velocity['x']:.1f}, y={velocity['y']:.1f}, z={velocity['z']:.1f}\n"
        observation += f"G-Force: {g_force:.2f}g\n\n"
        observation += f"=== ORBITAL STATE ===\n"
        observation += f"Apoapsis: {apoapsis:.0f}m, Periapsis: {periapsis:.0f}m\n"
        observation += f"Inclination: {inclination:.1f}°, Eccentricity: {eccentricity:.3f}\n"
        if period > 0:
            observation += f"Orbital Period: {period:.0f}s\n"
        if time_to_apoapsis > 0:
            observation += f"Time to Apoapsis: {time_to_apoapsis:.0f}s\n"
        if time_to_periapsis > 0:
            observation += f"Time to Periapsis: {time_to_periapsis:.0f}s\n"
        if prograde:
            observation += f"Prograde vector: ({prograde[0]:.3f}, {prograde[1]:.3f}, {prograde[2]:.3f})\n"
        if retrograde:
            observation += f"Retrograde vector: ({retrograde[0]:.3f}, {retrograde[1]:.3f}, {retrograde[2]:.3f})\n"
        observation += "\n"
        
        observation += f"=== RESOURCES ===\n"
        observation += f"LiquidFuel: {liquid_fuel:.1f}"
        if all_resources.get("LiquidFuel", {}).get("max", 0) > 0:
            fuel_max = all_resources["LiquidFuel"]["max"]
            fuel_pct = (liquid_fuel / fuel_max * 100) if fuel_max > 0 else 0
            observation += f"/{fuel_max:.1f} ({fuel_pct:.1f}%)"
        observation += f"\n"
        
        observation += f"Oxidizer: {oxidizer:.1f}"
        if all_resources.get("Oxidizer", {}).get("max", 0) > 0:
            ox_max = all_resources["Oxidizer"]["max"]
            ox_pct = (oxidizer / ox_max * 100) if ox_max > 0 else 0
            observation += f"/{ox_max:.1f} ({ox_pct:.1f}%)"
        observation += f"\n"
        
        if monoprop > 0:
            observation += f"MonoPropellant: {monoprop:.1f}"
            if all_resources.get("MonoPropellant", {}).get("max", 0) > 0:
                mono_max = all_resources["MonoPropellant"]["max"]
                mono_pct = (monoprop / mono_max * 100) if mono_max > 0 else 0
                observation += f"/{mono_max:.1f} ({mono_pct:.1f}%)"
            observation += f"\n"
        
        observation += f"ElectricCharge: {electric_charge:.1f}"
        if all_resources.get("ElectricCharge", {}).get("max", 0) > 0:
            ec_max = all_resources["ElectricCharge"]["max"]
            ec_pct = (electric_charge / ec_max * 100) if ec_max > 0 else 0
            observation += f"/{ec_max:.1f} ({ec_pct:.1f}%)"
        observation += f"\n\n"
        
        observation += f"=== VESSEL PROPERTIES ===\n"
        observation += f"Mass: {mass:.1f}t (Dry: {dry_mass:.1f}t)\n"
        observation += f"Thrust: {thrust:.1f}N (Max: {max_thrust:.1f}N)"
        if available_thrust > 0:
            observation += f" (Available: {available_thrust:.1f}N)"
        if isp > 0:
            observation += f"\nSpecific Impulse (ISP): {isp:.1f}s"
        observation += f"\n"
        if available_torque:
            try:
                # Check if available_torque is a valid 3D vector
                if len(available_torque) == 3 and all(isinstance(x, (int, float)) for x in available_torque):
                    torque_mag = (available_torque[0]**2 + available_torque[1]**2 + available_torque[2]**2)**0.5
                    observation += f"Available Torque: {torque_mag:.2f} N⋅m\n"
            except (TypeError, ValueError):
                pass  # Skip torque display if format is unexpected
        observation += f"Parts: {part_count} total, Current Stage: {current_stage}\n\n"
        
        observation += f"=== AERODYNAMICS ===\n"
        observation += f"Drag: {drag:.1f}N, Lift: {lift:.1f}N\n"
        if mach > 0:
            observation += f"Mach: {mach:.2f}\n"
        if atmosphere_density > 0:
            observation += f"Atmosphere Density: {atmosphere_density:.4f} kg/m³\n"
        observation += "\n"
        
        observation += f"=== ORIENTATION & CONTROL ===\n"
        observation += f"Heading: {heading:.1f}°, Pitch: {pitch:.1f}°, Roll: {roll:.1f}°\n"
        observation += f"Throttle: {throttle:.2f}, SAS: {sas}, RCS: {rcs}, Gear: {gear}\n"
        if comp_control.get('lights') is not None:
            observation += f"Lights: {comp_control['lights']}, Brakes: {comp_control.get('brakes', False)}\n"
        observation += "\n"
        
        if autopilot_engaged:
            observation += f"Autopilot: Engaged, Error: {autopilot_error:.2f}°\n"
            if autopilot.get('target_pitch') is not None:
                observation += f"  Target Pitch: {autopilot['target_pitch']:.1f}°\n"
            if autopilot.get('target_heading') is not None:
                observation += f"  Target Heading: {autopilot['target_heading']:.1f}°\n"
            observation += "\n"
        
        if mechjeb_available and mechjeb_api_ready:
            observation += f"MechJeb: Available and API Ready\n"
            if mechjeb.get('ascent_autopilot', {}).get('enabled'):
                ascent = mechjeb['ascent_autopilot']
                observation += f"  Ascent Autopilot: {ascent.get('status', 'Unknown')}\n"
            if mechjeb.get('landing_autopilot', {}).get('enabled'):
                landing = mechjeb['landing_autopilot']
                observation += f"  Landing Autopilot: {landing.get('status', 'Unknown')}\n"
            if mechjeb.get('docking_autopilot', {}).get('enabled'):
                docking = mechjeb['docking_autopilot']
                observation += f"  Docking Autopilot: {docking.get('status', 'Unknown')}\n"
            observation += "\n"
        
        observation += f"Vessel Observation (from Flight Agent):\n{vessel_observation}\n\n"
        observation += f"Task: {task}\n\n"
        if context:
            observation += f"Context: {context}\n\n"
        else:
            observation += f"Context: None\n\n"

        print(f"🔍 DEBUG: AuditAgent human message constructed, length={len(observation)} chars")
        print(f"\033[31m****Audit Agent human message****\n{observation}\033[0m")
        return HumanMessage(content=observation)


    def human_check_success(self):  # Human checks the audit results
        confirmed = False
        success = False
        critique = ""
        while not confirmed:
            success_input = input("Was the audit successful? (y/n): ")
            success = success_input.lower() == "y"
            critique = input("Enter your critique or reasoning for the outcome: ")
            print(f"Success: {success}\nCritique: {critique}")
            confirm = input("Confirm your choices? (y/n): ")
            confirmed = confirm.lower() in ["y", ""]
        return success, critique


    def ai_check_success(self, messages, max_retries=5): # AI checks the audit results
        if max_retries == 0:
            print("\033[31mFailed to parse AuditAgent response. Update your prompt for better JSON outputs.\033[0m")
            return False, ""
        response = self.llm.invoke(messages).content
        print(f"\033[31mAuditAgent AI message\n{response}\033[0m")
        try:
            parsed = fix_and_parse_json(response)  # Ensure this parses {"success": bool, "critique": str}
            assert isinstance(parsed["success"], bool)
            critique = parsed.get("critique", "")
            return parsed["success"], critique
        except Exception as e:
            print(f"\033[31mParse error: {e}. Retrying.\033[0m")
            return self.ai_check_success(messages, max_retries - 1)

    def ai_check_mission_success(self, messages, max_retries=5):
        print(f"🔍 DEBUG: AuditAgent checking mission success (retries left: {max_retries})")
        if max_retries == 0:
            print(
                "\033[31mFailed to parse Audit Agent response. Consider updating your prompt.\033[0m"
            )
            return False, "No critique available - parsing failed"

        if messages[1] is None:
            print(f"🔍 ERROR: AuditAgent no human message provided")
            return False, "No critique available - no human message"

        print(f"🔍 DEBUG: AuditAgent calling LLM with {len(messages)} messages")
        audit = self.llm.invoke(messages).content
        print(f"🔍 DEBUG: AuditAgent LLM response length: {len(audit)} chars")
        print(f"🔍 DEBUG: AuditAgent LLM response type: {type(audit)}")
        print(f"🔍 DEBUG: AuditAgent LLM response repr preview: {repr(audit[:200])}")
        print(f"\033[31m****Audit Agent ai message****\n{audit}\033[0m")
        
        try:
            print(f"🔍 DEBUG: AuditAgent parsing JSON response")
            print(f"🔍 DEBUG: Raw response preview: {repr(audit[:200])}")  # Show raw bytes for debugging
            response = fix_and_parse_json(audit)
            print(f"\033[33mDebug - Parsed response: {response}\033[0m")
            
            # Validate response structure with detailed error messages
            if not isinstance(response, dict):
                raise ValueError(f"Response is not a dict, got {type(response).__name__}: {response}")
            
            if "success" not in response:
                raise ValueError(f"Response missing 'success' key. Available keys: {list(response.keys())}")
            
            if response["success"] not in [True, False]:
                raise ValueError(f"Invalid success value: {response['success']} (type: {type(response['success']).__name__})")
            
            # Handle missing or null critique
            critique = response.get("critique", "")
            if critique is None or critique == "" or critique == "null":
                critique = "No specific critique provided"
            
            # Validate reasoning is present (optional but good to check)
            reasoning = response.get("reasoning", "")
            if not reasoning:
                print(f"🔍 WARNING: No reasoning provided in audit response")
            
            print(f"🔍 DEBUG: AuditAgent success={response['success']}, critique='{critique[:100]}...'")
            print(f"\033[33mDebug - Final critique: '{critique}'\033[0m")
            return response["success"], critique
        except Exception as e:
            print(f"🔍 ERROR: AuditAgent parsing failed: {type(e).__name__}: {e}")
            print(f"\033[31mError parsing audit response: {e}\033[0m")
            # ALWAYS print full response for debugging (not just on final retry)
            print(f"\033[31m{'='*70}")
            print(f"Full LLM response that failed to parse:")
            print(f"Length: {len(audit)} chars")
            print(f"Type: {type(audit)}")
            print(f"Content:\n{audit}")
            print(f"{'='*70}\033[0m")
            
            if max_retries > 0:
                print(f"\033[33mRetrying... ({max_retries} attempts remaining)\033[0m")
                return self.ai_check_mission_success(
                    messages=messages,
                    max_retries=max_retries - 1,
                )
            else:
                print(f"\033[31m❌ All retries exhausted. Returning failure.\033[0m")
                return False, f"Parsing failed after all retries: {str(e)[:200]}"

    def check_mission_success(
        self, *, events, task, context, vessel_observation, max_retries=5
    ):
        print(f"\033[31m🔍 Audit Agent: Checking mission success for task: {task}\033[0m")
        human_message = self.render_human_message(
            events=events,
            task=task,
            context=context,
            vessel_observation=vessel_observation,
        )

        messages = [
            self.render_system_message(),
            human_message,
        ]

        if self.mode == "manual":
            return self.human_check_success()
        elif self.mode == "auto":
            return self.ai_check_mission_success(
                messages=messages, max_retries=max_retries
            )
        else:
            raise ValueError(f"Invalid audit agent mode: {self.mode}")