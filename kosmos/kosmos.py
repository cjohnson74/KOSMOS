import copy
import json
import os
from pickle import FALSE
import time
from typing import Dict

import kosmos.utils as U
from kosmos.utils.debug_utils import create_debug_logger
from .env import KSPEnv

from .agents import FlightAgent, AuditAgent, MissionControlAgent, ManeuverAgent

class Kosmos:
    def __init__(
        self,
        krpc_address: str = "127.0.0.1",
        krpc_rpc_port: int = 50000,
        krpc_stream_port: int = 50001,
        openai_api_key: str = None,
        anthropic_api_key: str = None,
        env_wait_time: float = 1.0,
        env_request_timeout: float = 120,
        max_iterations: int = 160,
        reset_vessel_if_failed: bool = False,
        initial_mission: str = None,
        flight_agent_model_name: str = "claude-haiku-4-5-20251001",
        flight_agent_temperature: float = 0,
        flight_agent_task_max_retries: int = 4,
        flight_agent_show_telemetry_log: bool = True,
        flight_agent_show_execution_error: bool = True,
        mission_control_agent_model_name: str = "gpt-4o",
        mission_control_agent_temperature: float = 0,
        mission_control_agent_qa_model_name: str = "gpt-3.5-turbo",
        mission_control_agent_qa_temperature: float = 0,
        mission_control_agent_warm_up: Dict[str, int] = None,
        mission_control_agent_core_resources: str = r"LiquidFule|Oxidizer|MonoPropellant|EletricCharge|SolidFuel",
        mission_control_agent_mode: str = "auto",
        audit_agent_model_name: str = "gpt-4o",
        audit_agent_temperature: float = 0,
        audit_agent_mode: str = "auto",
        maneuver_agent_model_name: str = "gpt-3.5-turbo",
        maneuver_agent_temperature: float = 0,
        maneuver_agent_retrieval_top_k: int = 5,
        openai_api_request_timeout: int = 300,
        checkpoint_dir: str = "checkpoint",
        maneuver_library_dir: str = None,
        resume: bool = False,
    ):
        # Initialize the environment
        print("🔍 DEBUG: Initializing KSPEnv...")
        self.env = KSPEnv(
            krpc_address=krpc_address,
            krpc_rpc_port=krpc_rpc_port,
            krpc_stream_port=krpc_stream_port,
        )
        print("🔍 DEBUG: KSPEnv initialized")
        self.env_wait_time = env_wait_time
        self.reset_vessel_if_failed = reset_vessel_if_failed
        self.max_iterations = max_iterations

        self.initial_mission = initial_mission

        if openai_api_key:
            os.environ["OPENAI"] = openai_api_key
        else:
            print("⚠️  WARNING: No OpenAI API key provided. Set OPENAI_API_KEY environment variable.")
        
        if anthropic_api_key:
            os.environ["ANTHROPIC"] = anthropic_api_key
        else:
            print("⚠️  WARNING: No Anthropic API key provided. Set ANTHROPIC_API_KEY environment variable.")
            
        print("🔍 DEBUG: Initializing FlightAgent...")
        self.flight_agent = FlightAgent(
            model_name=flight_agent_model_name,
            temperature=flight_agent_temperature,
            request_timeout=openai_api_request_timeout,
            checkpoint_dir=checkpoint_dir,
            chat_log=flight_agent_show_telemetry_log,
            execution_error=flight_agent_show_execution_error,
        )
        print("🔍 DEBUG: FlightAgent initialized")
        self.flight_agent_task_max_retries = flight_agent_task_max_retries

        print("🔍 DEBUG: Initializing MissionControlAgent...")
        self.mission_control_agent = MissionControlAgent(
            model_name=mission_control_agent_model_name,
            temperature=mission_control_agent_temperature,
            qa_model_name=mission_control_agent_qa_model_name,
            qa_temperature=mission_control_agent_qa_temperature,
            request_timout=openai_api_request_timeout,
            ckpt_dir=checkpoint_dir,
            resume=resume,
            mode=mission_control_agent_mode,
            warm_up=mission_control_agent_warm_up,
            core_resources=mission_control_agent_core_resources,
        )
        print("🔍 DEBUG: MissionControlAgent initialized")

        print("🔍 DEBUG: Initializing AuditAgent...")
        self.audit_agent = AuditAgent(
            model_name=audit_agent_model_name,
            temperature=audit_agent_temperature,
            request_timeout=openai_api_request_timeout,
            mode=audit_agent_mode,
        )
        print("🔍 DEBUG: AuditAgent initialized")

        print("🔍 DEBUG: Initializing ManeuverAgent...")
        self.maneuver_agent = ManeuverAgent(
            model_name=maneuver_agent_model_name,
            temperature=maneuver_agent_temperature,
            top_k_vals=maneuver_agent_retrieval_top_k,
            timeout_period=openai_api_request_timeout,
            checkpoint_dir=checkpoint_dir,
            resume=1 if resume or maneuver_library_dir else 0,
        )
        print("🔍 DEBUG: ManeuverAgent initialized")

        self.recorder = U.EventRecorder(checkpoint_dir=checkpoint_dir)
        self.resume = resume
        
        # Initialize debug logger
        self.debug_logger = create_debug_logger("Kosmos")

        # init variables for mission rollout
        self.flight_agent_rollout_num_iterations = -1
        self.context = ""
        self.messages = None
        self.conversations = []
        self.last_events = None

    def reset(self, mission, context="", reset_env=True):
        self.flight_agent_rollout_num_iterations = 0
        self.mission = mission
        self.context = context
        if reset_env:
            self.env.reset(
                options={
                    "mode": "soft",
                    "wait_time": self.env_wait_time,
                }
            )

        # Set time warp and game settings
        telemetry = self.env.step(
            "conn.space_center.rails_warp_factor = 0\n"
            + "conn.space_center.physics_warp_factor = 0\n"
            + "print('Time warp disabled, ready for operations')"
        )

        maneuvers = self.maneuver_agent.getManeuvers(query=self.context)
        print(
            f"Render Flight Agent system message with {len(maneuvers)} skills"
        )
        system_message = self.flight_agent.construct_system_message(maneuvers=maneuvers)
        human_message = self.flight_agent.construct_human_message(
            events=telemetry, code="", task=self.mission, context=context, audit=""
        )
        self.messages = [system_message, human_message]
        assert len(self.messages) == 2
        self.conversations = []
        return self.messages

    def close(self):
        self.env.close()

    def step(self):
        self.debug_logger.debug(f"Step method called, iteration: {self.flight_agent_rollout_num_iterations}")
        if self.flight_agent_rollout_num_iterations < 0:
            raise ValueError("Agent must be reset before stepping")
        
        self.debug_logger.debug("Calling FlightAgent LLM")
        # Add delay to prevent rate limiting
        time.sleep(2)
        ai_message = self.flight_agent.call_llm(self.messages)
        self.debug_logger.debug(f"Flight Agent response received, length: {len(ai_message.content)}")
        
        self.conversations.append(
            (self.messages[0].content, self.messages[1].content, ai_message.content)
        )
        parsed_result = self.flight_agent.process_ai_message(message=ai_message)
        success = False
        if isinstance(parsed_result, dict):
            self.debug_logger.debug("Code parsed successfully, executing in environment")
            code = parsed_result["program_code"] + "\n" + parsed_result["exec_code"]
            
            print(f"🔍 DEBUG: Kosmos executing code:")
            print(f"🔍 DEBUG: Program code:\n{parsed_result['program_code']}")
            print(f"🔍 DEBUG: Exec code: {parsed_result['exec_code']}")
            print(f"🔍 DEBUG: Full code to execute:\n{code}")
            
            telemetry = self.env.step(
                code,
                programs=self.maneuver_agent.programs,
            )
            self.recorder.record(telemetry, self.mission)
            self.flight_agent.update_vessel_memory(telemetry[-1][1]["vessel_status"])
            
            self.debug_logger.debug(f"Calling Audit Agent for mission: {self.mission}")
            # Add delay to prevent rate limiting
            time.sleep(1)
            success, audit = self.audit_agent.check_mission_success(
                events=telemetry,
                task=self.mission,
                context=self.context,
                vessel_observation=self.flight_agent.render_vessel_observation(events=telemetry),
                max_retries=5,
            )
            self.debug_logger.info(f"Audit Agent Result: Success={success}, Critique='{audit[:100]}...'")

            if self.reset_vessel_if_failed and not success:
                vessel_state = []
                for event_type, event in telemetry:
                    if event_type == "onSave" and "vessel_modified" in event:
                        vessel_state.append(event["vessel_state"])
                if vessel_state:
                    new_telemetry = self.env.step(
                        f"revert_vessel_state(conn, vessel, {U.json_dumps(vessel_state[-1])})",
                        programs=self.maneuver_agent.programs,
                    )
                    telemetry[-1][1]["vessel_status"] = new_telemetry[-1][1]["vessel_status"]
                    telemetry[-1][1]["orbit_parameters"] = new_telemetry[-1][1]["orbit_parameters"]

            new_maneuvers = self.maneuver_agent.getManeuvers(
                query=self.context
                + "\n\n"
                + self.flight_agent.summarize_telemetry_log(telemetry)
            )
            system_message = self.flight_agent.construct_system_message(maneuvers=new_maneuvers)
            human_message = self.flight_agent.construct_human_message(
                events=telemetry,
                code=parsed_result["program_code"],
                task=self.mission,
                context=self.context,
                audit=audit,
            )
            self.last_events = copy.deepcopy(telemetry)
            self.messages = [system_message, human_message]
        else:
            assert isinstance(parsed_result, str)
            self.recorder.record([], self.mission)
            print(f"{parsed_result} Trying again!")
        assert len(self.messages) == 2
        self.flight_agent_rollout_num_iterations += 1
        done = (
            self.flight_agent_rollout_num_iterations >= self.flight_agent_task_max_retries
            or success
        )
        info = {
            "mission": self.mission,
            "success": success,
            "conversations": self.conversations,
        }
        if success:
            assert (
                "program_code" in parsed_result and "program_name" in parsed_result
            ), "program and program_name must be returned when success"
            info["program_code"] = parsed_result["program_code"]
            info["program_name"] = parsed_result["program_name"]
        else:
            print(
                f"Flight Agent human message\n{self.messages[-1].content}"
            )
        return self.messages, 0, done, info

    def rollout(self, *, mission, context, reset_env=FALSE):
        print(f"🔍 DEBUG: Rollout started for mission: {mission[:50]}...")
        self.reset(mission=mission, context=context, reset_env=reset_env)
        print(f"🔍 DEBUG: Reset completed, starting step loop...")
        step_count = 0
        while True:
            step_count += 1
            print(f"🔍 DEBUG: Rollout step {step_count}")
            messages, reward, done, info = self.step()
            print(f"🔍 DEBUG: Step {step_count} completed, done: {done}")
            if done:
                print(f"🔍 DEBUG: Rollout finished after {step_count} steps")
                break
        return messages, reward, done, info

    def learn(self, reset_env=True, initial_mission=None):
        print("🔍 DEBUG: Kosmos.learn() called")
        # Use the provided initial_mission if given, otherwise use the one from constructor
        if initial_mission is not None:
            self.initial_mission = initial_mission
            print(f"🔍 DEBUG: Using provided initial_mission: {initial_mission[:100]}...")
        elif self.initial_mission:
            print(f"🔍 DEBUG: Using constructor initial_mission: {self.initial_mission[:100]}...")
        else:
            print("🔍 DEBUG: No initial_mission provided")
        
        # Always use soft reset to avoid disrupting active vessel
        # Soft mode continues with whatever vessel is currently active in KSP
        print(f"🔍 DEBUG: Performing soft reset (keeping current vessel state)")
        self.env.reset(
            options={
                "mode": "soft",
                "wait_time": self.env_wait_time,
            }
        )
        self.resume = True
        self.last_events = self.env.step("")

        print("🔍 DEBUG: Starting main mission loop...")
        while True:
            print(f"🔍 DEBUG: Loop iteration {self.recorder.iteration}, max: {self.max_iterations}")
            if self.recorder.iteration > self.max_iterations:
                print("Mission iteration limit reached")
                break
            
            print(f"\033[35m🎯 Calling Mission Control Agent (Progress: {self.mission_control_agent.progress})\033[0m")
            mission, context = self.mission_control_agent.propose_next_mission(
                telemetry=self.last_events,
                vessel_observation=self.flight_agent.get_vessel_telemetry(env=self.env),
                max_retries=5,
                initial_mission=self.initial_mission,
            )
            print(f"\033[35m🎯 Mission Control Agent Result: Mission='{mission}', Context='{context[:100]}...'\033[0m")
            print(
                f"Starting mission {mission} for at most {self.flight_agent_task_max_retries} times"
            )
            try:
                print(f"🔍 DEBUG: Calling rollout for mission: {mission[:50]}...")
                messages, reward, done, info = self.rollout(
                    mission=mission,
                    context=context,
                    reset_env=reset_env,
                )
                print(f"🔍 DEBUG: Rollout completed, success: {info.get('success', 'unknown')}")
            except Exception as e:
                # Enhanced error debugging
                print(f"\033[31m{'='*70}")
                print(f"🔍 EXCEPTION CAUGHT IN LEARN()")
                print(f"Exception type: {type(e).__name__}")
                print(f"Exception module: {type(e).__module__}")
                print(f"Exception str: {str(e)}")
                print(f"Exception repr: {repr(e)}")
                if hasattr(e, 'args'):
                    print(f"Exception args: {e.args}")
                print(f"{'='*70}\033[0m")
                
                import traceback
                print("\033[31mFull traceback:\033[0m")
                traceback.print_exc()
                
                time.sleep(3) # wait for kRPC connection to stabilize
                info = {
                    "mission": mission,
                    "success": False,
                }
                # Safely access telemetry data
                last_telemetry_data = {}
                if self.last_events and len(self.last_events) > 0:
                    try:
                        last_event = self.last_events[-1]
                        # Handle different event structures
                        if isinstance(last_event, tuple) and len(last_event) > 1:
                            event_data = last_event[1]
                            last_telemetry_data = event_data if isinstance(event_data, dict) else {}
                        elif isinstance(last_event, dict):
                            last_telemetry_data = last_event
                    except (IndexError, TypeError, AttributeError) as te:
                        print(f"🔍 DEBUG: Error extracting telemetry from last_events: {te}")
                        last_telemetry_data = {}
                
                # Ensure all values are dicts, not None
                vessel_status = last_telemetry_data.get("vessel_status") if isinstance(last_telemetry_data, dict) else {}
                resources = last_telemetry_data.get("resources") if isinstance(last_telemetry_data, dict) else {}
                position = last_telemetry_data.get("position") if isinstance(last_telemetry_data, dict) else {}
                
                # Convert None to empty dict
                if not isinstance(vessel_status, dict):
                    vessel_status = {}
                if not isinstance(resources, dict):
                    resources = {}
                if not isinstance(position, dict):
                    position = {}
                
                self.last_events = self.env.reset(
                    options={
                        "mode": "soft",
                        "wait_time": self.env_wait_time,
                        "vessel_status": vessel_status,
                        "resources": resources,
                        "position": position,
                    }
                )
                print("Your last mission rollout terminated due to error:")
                print(f"{e}")

            if info["success"]:
                # Convert the info dict to the format expected by add_new_maneuver
                maneuver_data = {
                    "code_function_name": info["program_name"],
                    "code_function_body": info["program_code"]
                }
                self.maneuver_agent.add_new_maneuver(maneuver_data)

            print(f"\033[33m📊 Updating Mission Control Progress: Success={info['success']}\033[0m")
            self.mission_control_agent.update_exploration_progress(info)
            print(f"\033[33m📊 Mission Control Progress After Update: {self.mission_control_agent.progress}\033[0m")
            print(
                f"Completed missions: {', '.join(self.mission_control_agent.completed_missions)}"
            )
            print(
                f"Failed missions: {', '.join(self.mission_control_agent.failed_missions)}"
            )
        return {
            "completed_missions": self.mission_control_agent.completed_missions,
            "failed_missions": self.mission_control_agent.failed_missions,
            "maneuvers": self.maneuver_agent.availablemaneuvers,
        }

    def decompose_mission(self, mission):
        if not self.last_events:
            self.last_events = self.env.reset(
                options={
                    "mode": "hard",
                    "wait_time": self.env_wait_time,
                }
            )
        return self.mission_control_agent.decompose_mission(mission, self.last_events)

    def inference(self, mission=None, sub_missions=[], reset_mode="hard", reset_env=True):
        if not mission and not sub_missions:
            raise ValueError("Either mission or sub_missions must be provided")
        if not sub_missions:
            sub_missions = self.decompose_mission(mission)
        self.env.reset(
            options={
                "mode": reset_mode,
                "wait_time": self.env_wait_time,
            }
        )
        self.mission_control_agent.completed_missions = []
        self.mission_control_agent.failed_missions = []
        self.last_events = self.env.step("")
        while self.mission_control_agent.progress < len(sub_missions):
            next_mission = sub_missions[self.mission_control_agent.progress]
            context = self.mission_control_agent.get_mission_context(next_mission)
            print(
                f"Starting mission {next_mission} for at most {self.flight_agent_task_max_retries} times"
            )
            messages, reward, done, info = self.rollout(
                mission=next_mission,
                context=context,
                reset_env=reset_env,
            )
            self.mission_control_agent.update_exploration_progress(info)
            print(
                f"Completed missions: {', '.join(self.mission_control_agent.completed_missions)}"
            )
            print(
                f"Failed missions: {', '.join(self.mission_control_agent.failed_missions)}"
            )