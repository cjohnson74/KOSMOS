from __future__ import annotations

import os
import random
import re

import kosmos.utils as U
from kosmos.prompts import load_prompt
from kosmos.utils.json_utils import fix_and_parse_json
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_chroma import Chroma


class MissionControlAgent:
    def __init__(
        self,
        model_name="gpt-3.5-turbo",
        temperature=0,
        qa_model_name="gpt-3.5-turbo",
        qa_temperature=0,
        request_timout=120,
        ckpt_dir="ckpt",
        resume=False,
        mode="auto",
        warm_up=None,
        core_resources: str | None = None,
    ):
        print(f"🔍 DEBUG: MissionControlAgent initializing with model={model_name}, mode={mode}, resume={resume}")
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            request_timeout=request_timout,
            openai_api_key=os.getenv("OPENAI"),
        )
        self.qa_llm = ChatOpenAI(
            model_name=qa_model_name,
            temperature=qa_temperature,
            request_timeout=request_timout,
            openai_api_key=os.getenv("OPENAI"),
        )
        assert mode in [
            "auto",
            "manual",
        ], f"mode {mode} not supported"
        self.mode = mode
        self.ckpt_dir = ckpt_dir
        U.f_mkdir(f"{ckpt_dir}/mission_control/vectordb")
        if resume:
            print(f"\033[35mLoading Mission Control Agent from {ckpt_dir}/mission_control\033[0m")
            self.completed_missions = U.load_json(
                f"{ckpt_dir}/mission_control/completed_missions.json"
            )
            self.failed_missions = U.load_json(f"{ckpt_dir}/mission_control/failed_missions.json")
            self.qa_cache = U.load_json(f"{ckpt_dir}/mission_control/qa_cache.json")
            print(f"🔍 DEBUG: MissionControlAgent loaded {len(self.completed_missions)} completed, {len(self.failed_missions)} failed missions")
        else:
            self.completed_missions = []
            self.failed_missions = []
            self.qa_cache = {}
            print(f"🔍 DEBUG: MissionControlAgent starting fresh with no previous missions")
        
        # vectordb for qa cache
        self.qa_cache_questions_vectordb = Chroma(
            collection_name="qa_cache_questions_vectordb",
            embedding_function=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI")),
            persist_directory=f"{ckpt_dir}/mission_control/vectordb",
        )
        assert self.qa_cache_questions_vectordb._collection.count() == len(
            self.qa_cache
        ), (
            f"Mission Control Agent's qa cache question vectordb is not synced with qa_cache.json.\n"
            f"There are {self.qa_cache_questions_vectordb._collection.count()} questions in vectordb "
            f"but {len(self.qa_cache)} questions in qa_cache.json.\n"
            f"Did you set resume=False when initializing the agent?\n"
            f"You may need to manually delete the qa cache question vectordb directory for running from scratch.\n"
        )
        
        # Initialize warm up parameters
        if not warm_up:
            warm_up = self.default_warmup
        self.warm_up = {}
        if "optional_resources" in warm_up:
            assert core_resources is not None
            self._core_resources_regex = re.compile(core_resources)
            self.warm_up["optional_resources"] = warm_up["optional_resources"]
        else:
            self.warm_up["optional_resources"] = 0

        for key in self.mission_observations:
            self.warm_up[key] = warm_up.get(key, self.default_warmup[key])

        # Set mission-specific warm up values
        self.warm_up["vessel_status"] = 0
        self.warm_up["resources"] = 0
        self.warm_up["completed_missions"] = 0
        self.warm_up["failed_missions"] = 0

    @property
    def default_warmup(self):
        return {
            "context": 15,
            "current_body": 10,
            "mission_time": 15,
            "vessel_status": 0,
            "orbit_parameters": 10,
            "nearby_vessels": 5,
            "fuel_remaining": 15,
            "battery_charge": 15,
            "position": 0,
            "velocity": 0,
            "resources": 0,
            "optional_resources": 7,
            "part_status": 0,
            "completed_missions": 0,
            "failed_missions": 0,
        }

    @property
    def mission_observations(self):
        return [
            "context",
            "current_body",
            "mission_time",
            "vessel_status",
            "orbit_parameters",
            "nearby_vessels",
            "fuel_remaining",
            "battery_charge",
            "position",
            "velocity",
            "resources",
            "part_status",
            "completed_missions",
            "failed_missions",
        ]

    @property
    def progress(self):
        return len(self.completed_missions)

    def render_system_message(self):
        # Load the base mission control prompt
        base_prompt = load_prompt("mission_control")
        # Load kRPC documentation to help with understanding vessel capabilities
        mechjeb_docs = load_prompt("mechjeb_readmellm")
        
        # Combine the prompts
        enhanced_prompt = f"""{base_prompt}

## kRPC MechJeb API Documentation

The following kRPC MechJebAPI documentation will help you understand what operations are possible with vessels and their capabilities:

{mechjeb_docs}

## Data Validation Guidelines

When analyzing vessel telemetry data, be aware of the following:

1. **Impossible States**: If you see contradictory data (e.g., vessel in orbit but with 0 velocity, or 0 parts but still functioning), this indicates data corruption or errors.

2. **Vessel Capabilities**: Use the kRPC MechJeb documentation above to understand what operations are actually possible. For example:
   - A vessel needs parts to function
   - SAS requires electricity and control systems
   - Throttle control requires engines
   - Basic operations like "Enable SAS and set throttle" are always possible if the vessel has the required parts

3. **Error Handling**: If telemetry data appears corrupted or impossible, suggest missions that are simple and safe rather than complex operations.

4. **Mission Appropriateness**: Consider whether the requested mission is appropriate for the vessel's apparent state. Simple control operations (like enabling SAS or setting throttle) should be possible even with limited data.

Use this documentation to better understand vessel capabilities and suggest appropriate missions based on what's actually possible with the kRPC API."""
        
        system_message = SystemMessage(content=enhanced_prompt)
        assert isinstance(system_message, SystemMessage)
        return system_message

    def render_observation(self, *, telemetry, vessel_observation):
        # Handle both observe and error events
        last_event = telemetry[-1]
        if isinstance(last_event, tuple) and len(last_event) > 1:
            event_type, event = last_event
        else:
            event_type, event = "observe", last_event
            
        if event_type == "error":
            return f"Error occurred: {event.get('execution_error', 'Unknown error')}"
            
        event = last_event[1] if isinstance(last_event, tuple) and len(last_event) > 1 else last_event
        
        # Extract comprehensive telemetry if available
        comprehensive = event.get("comprehensive_telemetry", {})
        
        current_body = event.get("current_body", "Unknown")
        mission_time = event.get("mission_time", 0)
        vessel_situation = event.get("vessel_situation", "Unknown")
        
        # Position and velocity - use comprehensive data if available
        position = event.get("position", {"x": 0, "y": 0, "z": 0})
        velocity = event.get("velocity", {"x": 0, "y": 0, "z": 0})
        
        altitude = event.get("altitude", 0)
        if comprehensive.get('altitude_location', {}).get('mean_altitude') is not None:
            altitude = comprehensive['altitude_location']['mean_altitude']
        
        speed = event.get("speed", 0)
        if comprehensive.get('position_velocity', {}).get('speed') is not None:
            speed = comprehensive['position_velocity']['speed']
        
        # Orbital parameters - use comprehensive data if available
        orbit_params = event.get("orbit_parameters", {})
        comp_orbital = comprehensive.get('orbital', {})
        
        apoapsis = orbit_params.get("apoapsis_altitude", comp_orbital.get("apoapsis_altitude", 0))
        periapsis = orbit_params.get("periapsis_altitude", comp_orbital.get("periapsis_altitude", 0))
        inclination = orbit_params.get("inclination", comp_orbital.get("inclination", 0))
        eccentricity = orbit_params.get("eccentricity", comp_orbital.get("eccentricity", 0))
        
        # Resources - merge with comprehensive data
        resources = event.get("resources", {})
        comp_resources = comprehensive.get('resources', {})
        all_resources = {**resources}
        for name, data in comp_resources.items():
            if name not in all_resources:
                all_resources[name] = {'amount': data.get('amount', 0), 'max': data.get('max', 0)}
        
        vessel_status = event.get("vessel_status", {})
        part_status = event.get("part_status", {})
        nearby_vessels = event.get("nearby_vessels", [])
        
        # Calculate fuel levels - use merged resources
        liquid_fuel = all_resources.get("LiquidFuel", {}).get("amount", 0)
        oxidizer = all_resources.get("Oxidizer", {}).get("amount", 0)
        monoprop = all_resources.get("MonoPropellant", {}).get("amount", 0)
        electric_charge = all_resources.get("ElectricCharge", {}).get("amount", 0)
        
        completed_missions = (
            ", ".join(self.completed_missions) if self.completed_missions else "None"
        )
        failed_missions = ", ".join(self.failed_missions) if self.failed_missions else "None"
        
        # Filter resources for warm-up phase
        if self.progress < self.warm_up["optional_resources"]:
            filtered_resources = {}
            for resource_name, resource_data in all_resources.items():
                if self._core_resources_regex.search(resource_name) is not None:
                    filtered_resources[resource_name] = resource_data
            resources = filtered_resources
        else:
            resources = all_resources

        nearby_vessels_str = (
            ", ".join([vessel["name"] for vessel in nearby_vessels[:5]]) 
            if nearby_vessels else "None"
        )

        observation = {
            "context": "",
            "current_body": f"Current body: {current_body}\n\n",
            "mission_time": f"Mission time: {mission_time:.1f} seconds\n\n",
            "vessel_status": f"Vessel situation: {vessel_situation}\nAltitude: {altitude:.0f}m\nSpeed: {speed:.1f}m/s\n\n",
            "orbit_parameters": f"Orbital parameters: Apoapsis: {apoapsis:.0f}m, Periapsis: {periapsis:.0f}m, Inclination: {inclination:.1f}°, Eccentricity: {eccentricity:.3f}\n\n",
            "nearby_vessels": f"Nearby vessels: {nearby_vessels_str}\n\n",
            "fuel_remaining": f"Fuel remaining: LiquidFuel: {liquid_fuel:.1f}, Oxidizer: {oxidizer:.1f}\n\n",
            "battery_charge": f"Battery charge: ElectricCharge: {electric_charge:.1f}\n\n",
            "position": f"Position: x={position['x']:.1f}, y={position['y']:.1f}, z={position['z']:.1f}\n\n",
            "velocity": f"Velocity: x={velocity['x']:.1f}, y={velocity['y']:.1f}, z={velocity['z']:.1f}\n\n",
            "resources": f"Resources: {resources if resources else 'No significant resources'}\n\n",
            "part_status": f"Parts: {part_status.get('part_count', 0)} total, Stage {part_status.get('current_stage', 0)}\n\n",
            "completed_missions": f"Completed missions: {completed_missions}\n\n",
            "failed_missions": f"Failed missions that are too difficult: {failed_missions}\n\n",
        }
        return observation

    def render_human_message(self, *, telemetry, vessel_observation):
        content = ""
        observation = self.render_observation(
            telemetry=telemetry, vessel_observation=vessel_observation
        )
        
        if self.progress >= self.warm_up["context"]:
            questions, answers = self.run_qa(
                telemetry=telemetry, vessel_observation=vessel_observation
            )
            i = 1
            for question, answer in zip(questions, answers):
                if "Answer: Unknown" in answer or "language model" in answer:
                    continue
                observation["context"] += f"Question {i}: {question}\n"
                observation["context"] += f"{answer}\n\n"
                i += 1
                if i > 5:
                    break

        # Only process observation as dict if it's not a string (error case)
        if isinstance(observation, dict):
            for key in self.mission_observations:
                if self.progress >= self.warm_up[key]:
                    if self.warm_up[key] != 0:
                        should_include = random.random() < 0.8
                    else:
                        should_include = True
                    if should_include:
                        content += observation[key]
        else:
            # If observation is a string (error case), just add it
            content += str(observation)

        print(f"\033[35m****Mission Control Agent human message****\n{content}\033[0m")
        return HumanMessage(content=content)

    def propose_next_mission(self, *, telemetry, vessel_observation, max_retries=5, initial_mission=None):
        print(f"\033[33mDebug - Mission Control Progress: {self.progress}\033[0m")
        print(f"\033[33mDebug - Completed missions: {self.completed_missions}\033[0m")
        print(f"\033[33mDebug - Failed missions: {self.failed_missions}\033[0m")
        
        # Use initial mission if provided (regardless of progress)
        if self.mode == "auto" and initial_mission:
            mission = initial_mission
            # Always preserve the full initial mission as provided
            context = f"Initial mission provided. Follow these instructions exactly as given."
            print(f"\033[33mDebug - Using initial mission: {mission[:100]}...\033[0m")
            return mission, context

        # Handle resource constraints
        if telemetry and len(telemetry) > 0:
            last_event = telemetry[-1]
            if isinstance(last_event, tuple) and len(last_event) > 1:
                event = last_event[1]
            else:
                event = last_event
            resources = event.get("resources", {})
            liquid_fuel = resources.get("LiquidFuel", {}).get("amount", 0)
            electric_charge = resources.get("ElectricCharge", {}).get("amount", 0)
            
            # Low fuel warning missions
            if liquid_fuel < 100:
                mission = "Perform emergency landing"
                context = f"Liquid fuel is critically low ({liquid_fuel:.1f} units). Execute immediate landing procedures to save the crew and mission data."
                return mission, context
            
            # Low battery missions    
            if electric_charge < 50:
                mission = "Deploy solar panels and recharge"
                context = f"Electric charge is low ({electric_charge:.1f} units). Deploy solar panels or use alternate power generation to recharge batteries."
                return mission, context

        messages = [
            self.render_system_message(),
            self.render_human_message(
                telemetry=telemetry, 
                vessel_observation=vessel_observation
            ),
        ]

        if self.mode == "auto":
            print(f"\033[33mDebug - Using AI to propose next mission (Progress: {self.progress})\033[0m")
            return self.propose_next_ai_mission(messages=messages, max_retries=max_retries)
        elif self.mode == "manual":
            print(f"\033[33mDebug - Using manual mission input\033[0m")
            return self.propose_next_manual_mission()
        else:
            raise ValueError(f"Invalid mission control agent mode: {self.mode}")

    def propose_next_ai_mission(self, *, messages, max_retries=5):
        print(f"🔍 DEBUG: MissionControlAgent proposing AI mission (retries left: {max_retries})")
        if max_retries == 0:
            raise RuntimeError("Max retries reached, failed to propose AI mission.")
        
        print(f"🔍 DEBUG: MissionControlAgent calling LLM with {len(messages)} messages")
        curriculum = self.llm.invoke(messages).content
        print(f"\033[31m****Mission Control Agent AI message****\n{curriculum}\033[0m")
        
        try:
            print(f"🔍 DEBUG: MissionControlAgent parsing AI response")
            response = self.parse_ai_message(curriculum)
            assert "next_mission" in response
            print(f"🔍 DEBUG: MissionControlAgent parsed mission: {response['next_mission']}")
            
            print(f"🔍 DEBUG: MissionControlAgent getting mission context")
            context = self.get_mission_context(response["next_mission"])
            print(f"🔍 DEBUG: MissionControlAgent context length: {len(context)} chars")
            
            return response["next_mission"], context
        except Exception as e:
            print(
                f"\033[35mError parsing mission control response: {e}. Trying again!\033[0m"
            )
            return self.propose_next_ai_mission(
                messages=messages,
                max_retries=max_retries - 1,
            )

    def parse_ai_message(self, message):
        print(f"🔍 DEBUG: MissionControlAgent parsing message with {len(message)} chars")
        mission = ""
        lines = message.split("\n")
        
        # Always try to extract the full mission content after "Mission:"
        mission_started = False
        mission_lines = []
        for line in lines:
            if line.startswith("Mission:"):
                mission_started = True
                mission_content = line[8:].strip()
                if mission_content:
                    mission_lines.append(mission_content)
            elif mission_started and line.strip():
                mission_lines.append(line.strip())
            elif mission_started and not line.strip():
                # Empty line, continue collecting
                continue
            elif mission_started and line.startswith("Reasoning:"):
                # Hit next section, stop collecting
                break
        
        mission = "\n".join(mission_lines).strip()
        
        # If no mission was found with the above method, fall back to simple extraction
        if not mission:
            for line in lines:
                if line.startswith("Mission:"):
                    mission = line[8:].replace(".", "").strip()
                    print(f"🔍 DEBUG: MissionControlAgent found mission line: {line}")
                    break
        
        assert mission, "Mission not found in Mission Control Agent response"
        print(f"🔍 DEBUG: MissionControlAgent extracted mission: '{mission[:100]}...'")
        return {"next_mission": mission}

    def propose_next_manual_mission(self):
        confirmed = False
        mission, context = "", ""
        while not confirmed:
            mission = input("Enter mission: ")
            context = input("Enter context: ")
            print(f"Mission: {mission}\nContext: {context}")
            confirmed = input("Confirm? (y/n)").lower() in ["y", ""]
        return mission, context

    def update_exploration_progress(self, info):
        mission = info["mission"]
        success = info["success"]
        
        print(f"\033[35m📊 Mission Control: Updating progress for mission: {mission[:50]}... (Success: {success})\033[0m")
        
        # Skip recording certain utility missions
        if mission.startswith("Deploy solar panels") or mission.startswith("Perform emergency"):
            print(f"\033[35m📊 Mission Control: Skipping utility mission\033[0m")
            return
            
        if success:
            print(f"\033[35mCompleted mission: {mission}.\033[0m")
            self.completed_missions.append(mission)
        else:
            print(
                f"\033[35mFailed to complete mission: {mission}. Adding to failed missions.\033[0m"
            )
            self.failed_missions.append(mission)
        
        print(f"\033[35m📊 Mission Control: Progress before cleanup: {len(self.completed_missions)} completed, {len(self.failed_missions)} failed\033[0m")

        # Clean up missions and save to disk
        self.clean_up_missions()

    def clean_up_missions(self):
        updated_completed_missions = []
        updated_failed_missions = self.failed_missions
        
        # Dedup completed missions but keep order
        for mission in self.completed_missions:
            if mission not in updated_completed_missions:
                updated_completed_missions.append(mission)

        # Remove completed missions from failed missions
        for mission in updated_completed_missions:
            while mission in updated_failed_missions:
                updated_failed_missions.remove(mission)

        self.completed_missions = updated_completed_missions
        self.failed_missions = updated_failed_missions

        # Save to JSON
        U.dump_json(
            self.completed_missions, f"{self.ckpt_dir}/mission_control/completed_missions.json"
        )
        U.dump_json(self.failed_missions, f"{self.ckpt_dir}/mission_control/failed_missions.json")

    def decompose_mission(self, mission, telemetry):
        messages = [
            SystemMessage(
                content=load_prompt("mission_control_mission_decomposition"),
            ),
            self.render_human_message(telemetry=telemetry, vessel_observation=""),
            HumanMessage(content=f"Final mission: {mission}"),
        ]
        print(
            f"\033[31m****Mission Control Agent mission decomposition****\nFinal mission: {mission}\033[0m"
        )
        response = self.llm.invoke(messages).content
        print(f"\033[31m****Mission Control Agent mission decomposition****\n{response}\033[0m")
        return fix_and_parse_json(response)

    def run_qa(self, *, telemetry, vessel_observation):
        questions_new, _ = self.run_qa_step1_ask_questions(
            telemetry=telemetry, vessel_observation=vessel_observation
        )
        questions = []
        answers = []
        for question in questions_new:
            if self.qa_cache_questions_vectordb._collection.count() > 0:
                docs_and_scores = (
                    self.qa_cache_questions_vectordb.similarity_search_with_score(
                        question, k=1
                    )
                )
                if docs_and_scores and docs_and_scores[0][1] < 0.05:
                    question_cached = docs_and_scores[0][0].page_content
                    assert question_cached in self.qa_cache
                    answer_cached = self.qa_cache[question_cached]
                    questions.append(question_cached)
                    answers.append(answer_cached)
                    continue
            answer = self.run_qa_step2_answer_questions(question=question)
            assert question not in self.qa_cache
            self.qa_cache[question] = answer
            self.qa_cache_questions_vectordb.add_texts(
                texts=[question],
            )
            U.dump_json(self.qa_cache, f"{self.ckpt_dir}/mission_control/qa_cache.json")
            self.qa_cache_questions_vectordb.persist()
            questions.append(question)
            answers.append(answer)
        assert len(questions_new) == len(questions) == len(answers)
        return questions, answers

    def get_mission_context(self, mission):
        question = (
            f"How to {mission.replace('_', ' ').replace('.', '').strip().lower()}"
            f" in Kerbal Space Program?"
        )
        print(f"🔍 DEBUG: MissionControlAgent getting context for mission: '{mission}'")
        print(f"🔍 DEBUG: MissionControlAgent generated question: '{question}'")
        
        if question in self.qa_cache:
            print(f"🔍 DEBUG: MissionControlAgent found cached answer for question")
            answer = self.qa_cache[question]
        else:
            print(f"🔍 DEBUG: MissionControlAgent no cached answer, calling QA system")
            answer = self.run_qa_step2_answer_questions(question=question)
            self.qa_cache[question] = answer
            self.qa_cache_questions_vectordb.add_texts(
                texts=[question],
            )
            U.dump_json(self.qa_cache, f"{self.ckpt_dir}/mission_control/qa_cache.json")
            self.qa_cache_questions_vectordb.persist()
            print(f"🔍 DEBUG: MissionControlAgent cached new answer")
        
        context = f"Question: {question}\n{answer}"
        print(f"🔍 DEBUG: MissionControlAgent context length: {len(context)} chars")
        return context

    def render_system_message_qa_step1_ask_questions(self):
        return SystemMessage(content=load_prompt("mission_control_qa_step1_ask_questions"))

    def render_human_message_qa_step1_ask_questions(self, *, telemetry, vessel_observation):
        observation = self.render_observation(
            telemetry=telemetry, vessel_observation=vessel_observation
        )
        content = ""
        for key in self.mission_observations:
            content += observation[key]
        return HumanMessage(content=content)

    def run_qa_step1_ask_questions(self, *, telemetry, vessel_observation):
        event = telemetry[-1][1]
        current_body = event.get("current_body", "Unknown").replace("_", " ")
        
        questions = [
            f"What can I do when orbiting {current_body} in Kerbal Space Program?",
            f"What are the characteristics of {current_body} in Kerbal Space Program?",
            f"What missions are possible from {current_body} in Kerbal Space Program?",
        ]
        concepts = [current_body, current_body, current_body]
        
        messages = [
            self.render_system_message_qa_step1_ask_questions(),
            self.render_human_message_qa_step1_ask_questions(
                telemetry=telemetry, vessel_observation=vessel_observation
            ),
        ]
        qa_response = self.qa_llm(messages).content
        try:
            # Regex pattern to extract question and concept pairs
            pattern = r"Question \d+: (.+)\nConcept \d+: (.+)"
            # Extract all question and concept pairs
            pairs = re.findall(pattern, qa_response)
            # Store each question and concept in separate lists
            questions_new = [pair[0] for pair in pairs]
            concepts_new = [pair[1] for pair in pairs]
            assert len(questions_new) == len(concepts_new)
            questions.extend(questions_new)
            concepts.extend(concepts_new)
        except Exception as e:
            print(
                f"\033[35mError parsing mission control response for "
                f"QA step 1 ask questions: {e}.\033[0m"
            )
        return questions, concepts

    def render_system_message_qa_step2_answer_questions(self):
        return SystemMessage(
            content=load_prompt("mission_control_qa_step2_answer_questions")
        )

    def render_human_message_qa_step2_answer_questions(self, question):
        content = f"Question: {question}"
        return HumanMessage(content=content)

    def run_qa_step2_answer_questions(self, question):
        messages = [
            self.render_system_message_qa_step2_answer_questions(),
            self.render_human_message_qa_step2_answer_questions(question=question),
        ]
        print(f"\033[35mMission Control Agent Question: {question}\033[0m")
        qa_answer = self.qa_llm(messages).content
        print(f"\033[31mMission Control Agent {qa_answer}\033[0m")
        return qa_answer

    # def update_exploration_progress(self, info):
    #     mission = info["mission"]
    #     if mission.startswith("Deposit useless items into the chest at"):
    #         # No need to record the deposit mission
    #         return
    #     if info["success"]:
    #         print(f"\033[35mCompleted mission {mission}.\033[0m")
    #         self.completed_missions.append(mission)
    #     else:
    #         print(
    #             f"\033[35mFailed to complete mission {mission}. Skipping to next mission.\033[0m"
    #         )
    #         self.failed_missions.append(mission)

    #     # clean up missions and dump to disk
    #     self.clean_up_missions()

    # def clean_up_missions(self):
    #     updated_completed_missions = []
    #     # record repeated failed missions
    #     updated_failed_missions = self.failed_missions
    #     # dedup but keep order
    #     for mission in self.completed_missions:
    #         if mission not in updated_completed_missions:
    #             updated_completed_missions.append(mission)

    #     # remove completed missions from failed missions
    #     for mission in updated_completed_missions:
    #         while mission in updated_failed_missions:
    #             updated_failed_missions.remove(mission)

    #     self.completed_missions = updated_completed_missions
    #     self.failed_missions = updated_failed_missions

    #     # dump to json
    #     from kosmos.utils import dump_json
    #     dump_json(
    #         self.completed_missions, f"{self.ckpt_dir}/mission_control/completed_missions.json"
    #     )
    #     dump_json(self.failed_missions, f"{self.ckpt_dir}/mission_control/failed_missions.json")
