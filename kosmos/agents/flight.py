import ast
import os
import re
import time
import json

import kosmos.utils as U
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langsmith import traceable

from kosmos.prompts import load_prompt

class FlightAgent:
    def __init__(
        self,
        model_name="claude-haiku-4-5-20251001",
        temperature=0,
        request_timeout=300,
        checkpoint_dir="checkpoint",
        chat_log=True,
        execution_error=True,
    ):
        self.checkpoint_dir = checkpoint_dir
        self.chat_log = chat_log
        self.execution_error = execution_error
        U.f_mkdir(f"{checkpoint_dir}/action")
        self.llm = ChatAnthropic(
            model=model_name,
            temperature=temperature,
            timeout=request_timeout,
            api_key=os.getenv("ANTHROPIC"),
        )
        print(f"🔍 DEBUG: FlightAgent initialized with model={model_name}, temp={temperature}, timeout={request_timeout}")

    def get_vessel_telemetry(self, env=None):
        """Render vessel observation using actual KSP telemetry"""
        if env and hasattr(env, 'get_vessel_telemetry'):
            try:
                telemetry = env.get_vessel_telemetry()
                return {
                    "vessel_name": telemetry.get("vessel_name", "Unknown"),
                    "situation": telemetry.get("vessel_situation", "Unknown"),
                    "altitude": telemetry.get("altitude", 0),
                    "mission_status": "Active"
                }
            except Exception as e:
                print(f"Warning: Could not get vessel telemetry: {e}")
        
        # Fallback to basic observation
        return {
            "vessel_name": "Retriever A1",
            "situation": "In Flight",
            "altitude": 0,
            "mission_status": "Active"
        }

    def construct_system_message(self, maneuvers=[]):
        print(f"🔍 DEBUG: FlightAgent constructing system message with {len(maneuvers)} maneuvers")
        system_template = load_prompt("flight_template")
        # Load MechJeb documentation
        mechjeb_docs = load_prompt("mechjeb_readmellm")
        # Load kRPC documentation
        krpc_docs = load_prompt("krpc_readmellm")
        # TODO: Add control primitives later - for now using maneuvers only
        programs = "\n\n".join(maneuvers)
        response_format = load_prompt("flight_response_format")
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_template
        )
        system_message = system_message_prompt.format(
            mechjeb_docs=mechjeb_docs, krpc_docs=krpc_docs, programs=programs, response_format=response_format
        )
        assert isinstance(system_message, SystemMessage)
        print(f"🔍 DEBUG: FlightAgent system message constructed, length={len(system_message.content)} chars")
        return system_message

    def construct_human_message(self, *, events, code="", task="", context="", audit=""):
        print(f"🔍 DEBUG: FlightAgent constructing human message - task='{task[:50]}...', context='{context[:50]}...', audit='{audit[:50]}...'")
        chat_messages = []
        error_messages = []
        
        # Handle both observe and error events
        last_event = events[-1]
        if isinstance(last_event, tuple) and len(last_event) > 1:
            event_type, event = last_event
        else:
            event_type, event = "observe", last_event
            
        if event_type == "error":
            print(f"🔍 DEBUG: FlightAgent detected error event: {event.get('execution_error', 'Unknown error')}")
            
        # Extract error events and chat messages from events
        for evt_tuple in events:
            try:
                if isinstance(evt_tuple, tuple) and len(evt_tuple) > 1:
                    evt_type, evt_data = evt_tuple
                else:
                    evt_type, evt_data = "observe", evt_tuple
                
                if evt_type == "error" and isinstance(evt_data, dict):
                    error_msg = evt_data.get('execution_error', 'Unknown error')
                    error_type = evt_data.get('exception_type', 'Exception')
                    error_messages.append(f"{error_type}: {error_msg}")
                elif evt_type == "onChat" and isinstance(evt_data, dict) and "onChat" in evt_data:
                    chat_messages.append(evt_data["onChat"])
            except (TypeError, AttributeError, KeyError) as e:
                print(f"🔍 DEBUG: Error processing event: {e}")
                continue

        observation = ""

        # PRIORITY: Show errors and audit critique prominently at the top
        if error_messages:
            observation += "=" * 80 + "\n"
            observation += "🚨 EXECUTION ERRORS - ACTION REQUIRED 🚨\n"
            observation += "=" * 80 + "\n\n"
            for i, error_msg in enumerate(error_messages, 1):
                observation += f"ERROR {i}: {error_msg}\n\n"
            observation += "=" * 80 + "\n\n"
        
        # Show audit critique prominently right after errors (or at top if no errors)
        if audit:
            observation += "=" * 80 + "\n"
            observation += "📋 AUDIT AGENT CRITIQUE & GUIDANCE 📋\n"
            observation += "=" * 80 + "\n\n"
            observation += f"{audit}\n\n"
            observation += "=" * 80 + "\n\n"
        elif error_messages:
            # If there were errors but no audit yet, note that
            observation += "⚠️  Note: Audit Agent is analyzing the errors above. Please wait for critique.\n\n"
            observation += "=" * 80 + "\n\n"

        if code:
            observation += f"Code from the last round:\n{code}\n\n"
        else:
            observation += f"Code from the last round: No code in the first round\n\n"
        
        if self.execution_error:
            if error_messages:
                # Errors already shown above, just add a note
                observation += f"Execution status: ERRORS occurred (see above)\n\n"
            else:
                observation += f"Execution status: No execution errors\n\n"

        if self.chat_log:
            if chat_messages:
                chat_log = "\n".join(chat_messages)
                observation += f"Chat log: {chat_log}\n\n"
            else:
                observation += f"Chat log: None\n\n"

        # Add game telemetry to the observation
        # Try to get telemetry from the last observe event, or from error event if it contains telemetry
        telemetry = None
        telemetry_event = None
        
        # Look for the last observe event
        for event_tuple in reversed(events):
            if isinstance(event_tuple, tuple) and len(event_tuple) > 1:
                evt_type, evt_data = event_tuple
            else:
                evt_type, evt_data = "observe", event_tuple
            
            if evt_type == "observe" and isinstance(evt_data, dict):
                telemetry = evt_data
                telemetry_event = event_tuple
                break
            elif evt_type == "error" and isinstance(evt_data, dict) and 'vessel_status' in evt_data:
                # Error events may contain telemetry data
                telemetry = evt_data
                telemetry_event = event_tuple
                break
        
        if telemetry:
            comprehensive = telemetry.get('comprehensive_telemetry', {})
            
            observation += f"Vessel Telemetry:\n"
            observation += f"  Vessel: {telemetry.get('vessel_name', 'Unknown')} ({telemetry.get('vessel_type', 'Unknown')})\n"
            observation += f"  Situation: {telemetry.get('vessel_situation', 'Unknown')}\n"
            observation += f"  Mission Time: {telemetry.get('mission_time', 0):.1f}s\n"
            observation += f"  Current Body: {telemetry.get('current_body', 'Unknown')}\n"
            
            # Position and velocity (use comprehensive data if available)
            if 'position' in telemetry:
                pos = telemetry['position']
                observation += f"  Position: ({pos.get('x', 0):.1f}, {pos.get('y', 0):.1f}, {pos.get('z', 0):.1f})\n"
            
            if 'velocity' in telemetry:
                vel = telemetry['velocity']
                observation += f"  Velocity: ({vel.get('x', 0):.1f}, {vel.get('y', 0):.1f}, {vel.get('z', 0):.1f})\n"
            
            # Altitude and speed (use comprehensive data if available)
            altitude = telemetry.get('altitude', 0)
            if comprehensive.get('altitude_location', {}).get('mean_altitude'):
                altitude = comprehensive['altitude_location']['mean_altitude']
            observation += f"  Altitude: {altitude:.1f}m"
            if comprehensive.get('altitude_location', {}).get('surface_altitude') is not None:
                observation += f" (Surface: {comprehensive['altitude_location']['surface_altitude']:.1f}m)"
            observation += "\n"
            
            speed = telemetry.get('speed', 0)
            if comprehensive.get('position_velocity', {}).get('speed'):
                speed = comprehensive['position_velocity']['speed']
            observation += f"  Speed: {speed:.1f}m/s"
            if comprehensive.get('position_velocity', {}).get('vertical_speed') is not None:
                observation += f" (Vertical: {comprehensive['position_velocity']['vertical_speed']:.1f}m/s)"
            if comprehensive.get('position_velocity', {}).get('horizontal_speed') is not None:
                observation += f" (Horizontal: {comprehensive['position_velocity']['horizontal_speed']:.1f}m/s)"
            observation += "\n"
            
            # G-Force (from comprehensive telemetry)
            g_force = telemetry.get('g_force', 0)
            if comprehensive.get('flight_dynamics', {}).get('g_force') is not None:
                g_force = comprehensive['flight_dynamics']['g_force']
            observation += f"  G-Force: {g_force:.2f}g\n"
            
            # Orbit parameters
            if 'orbit_parameters' in telemetry:
                orbit = telemetry['orbit_parameters']
                observation += f"  Orbit: Apoapsis {orbit.get('apoapsis_altitude', 0):.0f}m, Periapsis {orbit.get('periapsis_altitude', 0):.0f}m\n"
                observation += f"  Inclination: {orbit.get('inclination', 0):.1f}°, Eccentricity: {orbit.get('eccentricity', 0):.3f}\n"
                # Use comprehensive orbital data if available
                if comprehensive.get('orbital'):
                    orb_data = comprehensive['orbital']
                    if orb_data.get('period'):
                        observation += f"  Period: {orb_data['period']:.0f}s"
                    if orb_data.get('time_to_apoapsis') is not None:
                        observation += f", Time to Apoapsis: {orb_data['time_to_apoapsis']:.0f}s"
                    observation += "\n"
            
            # Resources (fuel, etc.) - use comprehensive data
            if 'resources' in telemetry:
                resources = telemetry['resources']
                # Also check comprehensive resources
                comp_resources = comprehensive.get('resources', {})
                all_resources = {**resources}
                for name, data in comp_resources.items():
                    if name not in all_resources:
                        all_resources[name] = {'amount': data.get('amount', 0), 'max': data.get('max', 0)}
                
                fuel_resources = {k: v for k, v in all_resources.items() 
                                if 'fuel' in k.lower() or 'oxidizer' in k.lower() or 'electric' in k.lower()}
                if fuel_resources:
                    observation += f"  Resources:\n"
                    for name, data in fuel_resources.items():
                        amount = data.get('amount', 0) if isinstance(data, dict) else 0
                        max_amount = data.get('max', 0) if isinstance(data, dict) else 0
                        percentage = (amount / max_amount * 100) if max_amount > 0 else 0
                        observation += f"    {name}: {amount:.1f}/{max_amount:.1f} ({percentage:.1f}%)\n"
            
            # Vessel status - use comprehensive data
            if 'vessel_status' in telemetry:
                status = telemetry['vessel_status']
                basic_vessel = comprehensive.get('basic_vessel', {})
                performance = comprehensive.get('performance', {})
                
                mass = status.get('mass', basic_vessel.get('mass', 0))
                observation += f"  Mass: {mass:.1f}t"
                if basic_vessel.get('dry_mass'):
                    observation += f" (Dry: {basic_vessel['dry_mass']:.1f}t)"
                observation += "\n"
                
                thrust = status.get('thrust', performance.get('thrust', 0))
                max_thrust = status.get('max_thrust', performance.get('max_thrust', 0))
                observation += f"  Thrust: {thrust:.1f}N (Available: {max_thrust:.1f}N)\n"
                
                if performance.get('specific_impulse'):
                    observation += f"  ISP: {performance['specific_impulse']:.1f}s\n"
                
                if 'control_state' in status:
                    control = status['control_state']
                    # Use comprehensive control data if available
                    comp_control = comprehensive.get('control', {})
                    observation += f"  Control: Throttle {comp_control.get('throttle', control.get('throttle', 0)):.2f}"
                    observation += f", SAS {comp_control.get('sas', control.get('sas', False))}"
                    observation += f", RCS {comp_control.get('rcs', control.get('rcs', False))}\n"
                    
                    if comp_control.get('gear') is not None:
                        observation += f"  Gear: {comp_control['gear']}"
                    if comp_control.get('lights') is not None:
                        observation += f", Lights: {comp_control['lights']}"
                    if comp_control.get('brakes') is not None:
                        observation += f", Brakes: {comp_control['brakes']}"
                    observation += "\n"
            
            # Orientation data from comprehensive telemetry
            orientation = comprehensive.get('orientation', {})
            if orientation:
                observation += f"  Orientation: Heading {orientation.get('heading', 0):.1f}°, "
                observation += f"Pitch {orientation.get('pitch', 0):.1f}°, "
                observation += f"Roll {orientation.get('roll', 0):.1f}°\n"
            
            # Autopilot status from comprehensive telemetry
            autopilot = comprehensive.get('autopilot', {})
            if autopilot.get('engaged'):
                observation += f"  Autopilot: Engaged, Error: {autopilot.get('error', 0):.2f}°\n"
                if autopilot.get('target_pitch') is not None:
                    observation += f"    Target Pitch: {autopilot['target_pitch']:.1f}°, "
                if autopilot.get('target_heading') is not None:
                    observation += f"Target Heading: {autopilot['target_heading']:.1f}°\n"
            
            # MechJeb status
            if 'mechjeb_status' in telemetry:
                mj = telemetry['mechjeb_status']
                if mj.get('api_ready'):
                    observation += f"  MechJeb: API Ready, Status: {mj.get('ascent_status', 'Unknown')}\n"
            
            # MechJeb comprehensive data
            mechjeb = comprehensive.get('mechjeb', {})
            if mechjeb.get('available') and mechjeb.get('api_ready'):
                if mechjeb.get('ascent_autopilot', {}).get('enabled'):
                    ascent = mechjeb['ascent_autopilot']
                    observation += f"  MechJeb Ascent: {ascent.get('status', 'Unknown')}, "
                    observation += f"Target Alt: {ascent.get('desired_orbit_altitude', 0):.0f}m\n"
            
            # Staging info
            if 'part_status' in telemetry:
                parts = telemetry['part_status']
                observation += f"  Parts: {parts.get('part_count', 0)} total, Stage {parts.get('current_stage', 0)}"
                if parts.get('stage_count'):
                    observation += f" ({parts['stage_count']} parts)"
                observation += "\n"
            
            # Nearby vessels
            if 'nearby_vessels' in telemetry and telemetry['nearby_vessels']:
                observation += f"  Nearby Vessels:\n"
                for vessel in telemetry['nearby_vessels'][:3]:  # Show top 3
                    observation += f"    {vessel.get('name', 'Unknown')}: {vessel.get('distance', 0):.0f}m ({vessel.get('situation', 'Unknown')})\n"
            
            # Execution time
            if 'execution_time' in telemetry:
                observation += f"  Execution Time: {telemetry.get('execution_time', 0):.3f}s\n"
            
            observation += "\n"
        else:
            # No telemetry available (shouldn't happen normally, but handle gracefully)
            observation += "Vessel Telemetry: No telemetry data available\n\n"

        observation += f"Task: {task}\n\n"

        if context:
            observation += f"Context: {context}\n\n"
        else:
            observation += f"Context: None\n\n"
        
        # Add reminder about errors/critique if present (already shown above, but include summary)
        if error_messages or audit:
            observation += "=" * 80 + "\n"
            observation += "📌 REMINDER: Review the errors and critique above, then fix your code accordingly.\n"
            observation += "=" * 80 + "\n\n"

        print(f"🔍 DEBUG: FlightAgent human message constructed, length={len(observation)} chars")
        return HumanMessage(content=observation)

    @traceable(name="flight_agent")
    def call_llm(self, messages):
        print(f"🔍 DEBUG: FlightAgent calling LLM with {len(messages)} messages")
        print(f"🔍 DEBUG: FlightAgent system message preview: {messages[0].content[:200]}...")
        print(f"🔍 DEBUG: FlightAgent human message preview: {messages[1].content[:200]}...")
        
        try:
            response = self.llm.invoke(messages)
            print(f"🔍 DEBUG: FlightAgent LLM response received, length={len(response.content)} chars")
            print(f"🔍 DEBUG: FlightAgent LLM response preview: {response.content[:300]}...")
            return response
        except Exception as e:
            print(f"🔍 ERROR: FlightAgent LLM call failed: {e}")
            raise

    def process_ai_message(self, message):
        print(f"🔍 DEBUG: FlightAgent processing AI message, length={len(message.content)} chars")
        assert isinstance(message, AIMessage)

        retry = 3
        error = None
        while retry > 0:
            try:
                print(f"🔍 DEBUG: FlightAgent parsing attempt {4-retry}, extracting code from message")
                code_pattern = re.compile(r"```(?:python|py)(.*?)```", re.DOTALL)
                code = "\n".join(code_pattern.findall(message.content))
                print(f"🔍 DEBUG: FlightAgent extracted code length: {len(code)} chars")
                if code:
                    print(f"🔍 DEBUG: FlightAgent code preview: {code[:200]}...")
                else:
                    print("🔍 WARNING: FlightAgent no code found in message")
                
                parsed = ast.parse(code)
                functions = []
                assert len(parsed.body) > 0, "No functions found"
                print(f"🔍 DEBUG: FlightAgent found {len(parsed.body)} AST nodes")
                
                for node in parsed.body:
                    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        continue
                    
                    node_type = "AsyncFunctionDef" if isinstance(node, ast.AsyncFunctionDef) else "FunctionDef"
                    
                    # Extract function parameters
                    params = []
                    for arg in node.args.args:
                        params.append(arg.arg)
                    
                    # Get function source code (simplified - in practice you might want to use ast.unparse)
                    functions.append({
                        "name": node.name,
                        "type": node_type,
                        "body": ast.unparse(node),
                        "params": params,
                    })
                
                # Find the last function (prefer regular functions over async)
                main_function = None
                for function in reversed(functions):
                    if function["type"] == "FunctionDef":
                        main_function = function
                        break
                
                # If no regular function found, look for async function
                if main_function is None:
                    for function in reversed(functions):
                        if function["type"] == "AsyncFunctionDef":
                            main_function = function
                            break
                
                print(f"🔍 DEBUG: FlightAgent found {len(functions)} functions, main_function: {main_function['name'] if main_function else 'None'}")
                
                assert (
                    main_function is not None
                ), "No function found. Your code must contain at least one function."
                
                # Functions can have any parameters - they'll use the execution context directly
                program_code = "\n\n".join(function["body"] for function in functions)
                # Call the function with the correct parameters based on what it expects
                if len(main_function['params']) == 1:
                    if main_function['params'][0] == 'mech_jeb':
                        exec_code = f"{main_function['name']}(mech_jeb)"
                    else:
                        exec_code = f"{main_function['name']}(conn)"
                elif len(main_function['params']) == 2:
                    if 'mech_jeb' in main_function['params']:
                        if main_function['params'] == ['conn', 'mech_jeb']:
                            exec_code = f"{main_function['name']}(conn, mech_jeb)"
                        elif main_function['params'] == ['mech_jeb', 'vessel']:
                            exec_code = f"{main_function['name']}(mech_jeb, vessel)"
                        else:
                            exec_code = f"{main_function['name']}(conn, vessel)"
                    else:
                        exec_code = f"{main_function['name']}(conn, vessel)"
                elif len(main_function['params']) == 3:
                    exec_code = f"{main_function['name']}(conn, vessel, mech_jeb)"
                else:
                    # Default to conn, vessel for backward compatibility
                    exec_code = f"{main_function['name']}(conn, vessel)"
                
                print(f"🔍 DEBUG: FlightAgent successfully parsed code - program_name: {main_function['name']}, exec_code: {exec_code}")
                
                return {
                    "program_code": program_code,
                    "program_name": main_function["name"],
                    "exec_code": exec_code,
                }
            except Exception as e:
                retry -= 1
                error = e
                print(f"🔍 ERROR: FlightAgent parsing failed (attempt {4-retry}): {e}")
                time.sleep(1)
        print(f"🔍 ERROR: FlightAgent failed to parse after all retries: {error}")
        return f"Error parsing action response (before program execution): {error}"

    def update_vessel_memory(self, vessel_status):
        print(f"🔍 DEBUG: FlightAgent updating vessel memory with status keys: {list(vessel_status.keys()) if vessel_status else 'None'}")
        # This method is called from kosmos.py but not implemented yet
        # Placeholder for future vessel memory functionality
        pass

    def render_vessel_observation(self, events=None):
        """Render vessel observation from telemetry events."""
        print("🔍 DEBUG: FlightAgent rendering vessel observation")
        
        if not events:
            return "No telemetry available"
        
        try:
            # Get the latest telemetry event
            last_event = events[-1]
            if isinstance(last_event, tuple) and len(last_event) > 1:
                event_type, event = last_event
            else:
                event_type, event = "observe", last_event
            
            # Check if event is None or not a dict
            if event is None:
                return "No telemetry data available"
                
            if not isinstance(event, dict):
                return f"Invalid telemetry data type: {type(event).__name__}"
            
            if event_type != "observe":
                return f"Event type: {event_type} (not observing)"
            
            # Extract comprehensive telemetry if available (safely)
            comprehensive = event.get("comprehensive_telemetry") if isinstance(event, dict) else {}
            if comprehensive is None:
                comprehensive = {}
        except (IndexError, TypeError, AttributeError) as e:
            print(f"🔍 DEBUG: Error extracting telemetry from events: {e}")
            return f"Error extracting telemetry: {type(e).__name__}"
        
        # Build a summary of key vessel state
        observation_parts = []
        
        # Basic vessel info
        vessel_name = event.get("vessel_name", "Unknown")
        situation = event.get("vessel_situation", "Unknown")
        observation_parts.append(f"Vessel: {vessel_name} ({situation})")
        
        # Position and motion (with null checks)
        if 'position' in event and isinstance(event.get('position'), dict):
            pos = event['position']
            observation_parts.append(f"Position: ({pos.get('x', 0):.1f}, {pos.get('y', 0):.1f}, {pos.get('z', 0):.1f})")
        
        if 'velocity' in event and isinstance(event.get('velocity'), dict):
            vel = event['velocity']
            observation_parts.append(f"Velocity: ({vel.get('x', 0):.1f}, {vel.get('y', 0):.1f}, {vel.get('z', 0):.1f})")
        
        observation_parts.append(f"Altitude: {event.get('altitude', 0):.1f}m, Speed: {event.get('speed', 0):.1f}m/s")
        
        # Orbital state (with null checks)
        orbit_params = event.get('orbit_parameters')
        if orbit_params and isinstance(orbit_params, dict):
            observation_parts.append(f"Orbit: Ap {orbit_params.get('apoapsis_altitude', 0):.0f}m, Pe {orbit_params.get('periapsis_altitude', 0):.0f}m")
        
        # Control state (with null checks)
        vessel_status = event.get('vessel_status')
        if vessel_status and isinstance(vessel_status, dict):
            control_state = vessel_status.get('control_state')
            if control_state and isinstance(control_state, dict):
                observation_parts.append(f"Control: Throttle {control_state.get('throttle', 0):.2f}, SAS {control_state.get('sas', False)}, RCS {control_state.get('rcs', False)}")
        
        # MechJeb status if available (with null checks)
        mechjeb_status = event.get('mechjeb_status')
        if mechjeb_status and isinstance(mechjeb_status, dict):
            if mechjeb_status.get('api_ready', False):
                observation_parts.append(f"MechJeb: API Ready, Status: {mechjeb_status.get('ascent_status', 'Unknown')}")
        
        # Resources summary (with null checks)
        resources = event.get('resources')
        if resources and isinstance(resources, dict):
            fuel_info = []
            for name in ['LiquidFuel', 'Oxidizer', 'ElectricCharge']:
                if name in resources:
                    resource_data = resources[name]
                    if isinstance(resource_data, dict):
                        amt = resource_data.get('amount', 0)
                        max_amt = resource_data.get('max', 0)
                        if max_amt > 0:
                            pct = (amt / max_amt) * 100
                            fuel_info.append(f"{name}: {pct:.1f}%")
            if fuel_info:
                observation_parts.append(f"Resources: {', '.join(fuel_info)}")
        
        return "\n".join(observation_parts)

    def summarize_telemetry_log(self, telemetry):
        print(f"🔍 DEBUG: FlightAgent summarizing telemetry log with {len(telemetry)} events")
        # This method is called from kosmos.py but not implemented yet
        # Placeholder for future telemetry summarization
        return "Telemetry summary placeholder"

    def summarize_chatlog(self, events):
        chatlog = set()
        for event_type, event in events:
            if event_type == "onChat":
                chatlog.add(event["onChat"])
        return "I also need " + ", ".join(chatlog) + "." if chatlog else ""