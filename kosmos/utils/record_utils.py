import time
import re
from .file_utils import *
from .json_utils import *

class EventRecorder:
    def __init__(
        self,
        checkpoint_dir="checkpoint",
        resume=False,
        init_position=None,
    ):
        self.checkpoint_dir = checkpoint_dir
        self.resource_history = set()
        self.resource_vs_time = {}
        self.resource_vs_iterations = {}
        self.celestial_body_history = set()
        self.vessel_situation_history = set()
        self.init_position = init_position
        self.orbital_history = [] # Track orbital parameters over time
        self.position_hostry = [[0, 0, 0]] # 3D positions for space
        self.mission_time = 0.0 # Mission elapsed time in seconds
        self.universal_time_start = None # KSP universal time at mission start
        self.iteration = 0
        f_mkdir(self.checkpoint_dir, "events")
        if resume:
            self.resume()
        
    def record(self, telemetry, mission):
        mission = re.sub(f'[\\/:"*<>| ]', "_", mission)
        mission = mission.replace(" ", "_") + time.strftime(
            "_%Y%m%d_%H%M%S", time.localtime()
        )
        self.iteration += 1

        if not self.init_position and telemetry:
            # Initialize position from first telemetry data
            first_event = telemetry[0][1]
            if "position" in first_event:
                self.init_position = [
                    first_event["position"]["x"],
                    first_event["position"]["y"],
                    first_event["position"]["z"],
                ]

        if not self.universal_time_start and telemetry:
            # Set mission start time
            first_event = telemetry[0][1]
            if "universal_time" in first_event:
                self.universal_time_start = first_event["universal_time"]

        for event_type, event in telemetry:
            self.update_resource(event)
            self.update_orbital_state(event)
            if event_type == "observe":
                self.update_mission_time(event)

        print(
            f"Recorder message: {self.mission_time:.1f} seconds mission time\n"
            f"Recorder message: {self.iteration} iteration passed"
        )
        # Truncate mission name to avoid filename too long error
        safe_mission_name = mission.replace('\n', '_').replace(' ', '_')[:100]
        dump_json(telemetry, f_join(self.checkpoint_dir, "events", safe_mission_name))

    def resume(self, cutoff=None):
        self.resource_history = set()
        self.resource_vs_time = {}
        self.resource_vs_iterations = {}
        self.mission_time = 0.0
        self.orbital_history = []
        self.position_history = [[0, 0, 0]]
        self.celestial_body_history = set()
        self.vessel_situation_history = set()

        def get_timestamp(string):
            timestamp = "_".join(string.split("_")[-2:])
            return time.mktime(time.strptime(timestamp, "%Y%m%d_%H%M%S"))

        records = f_listdir(self.checkpoint_dir, "events")
        sorted_records = sorted(records, key=get_timestamp)

        for record in sorted_records:
            self.iteration += 1
            if cutoff and self.iteration > cutoff:
                break

            telemetry = load_json(f_join(self.checkpoint_dir, "events", record))

            if not self.init_position and telemetry:
                first_event = telemetry[0][1]
                if "position" in first_event:
                    self.init_position = [
                        first_event["position"]["x"],
                        first_event["position"]["y"],
                        first_event["position"]["z"],
                    ]

            if not self.universal_time_start and telemetry:
                first_event = telemetry[0][1]
                if "position" in first_event:
                    self.init_position = [
                        first_event["position"]["x"],
                        first_event["position"]["y"],
                        first_event["position"]["z"],
                    ]

            if not self.universal_time_start and telemetry:
                first_event = telemetry[0][1]
                if "universal_time" in first_event:
                    self.universal_time_start = first_event["universal_time"]

            for event_type, event in telemetry:
                self.update_resource(event)
                self.update_position(event)
                self.update_orbital_state(event)
                if event_type == "observe":
                    self.update_mission_time(event)

    def update_resource(self, event):
        if "resources" not in event:
            return

        resources = event["resources"]
        mission_time = event.get("mission_time", self.mission_time)
        current_body = event.get("current_body", "Unknown")
        vessel_situation = event.get("vessel_situation", "Unknown")

        current_resources = set()
        for resource_name, amount in resources.items():
            # Handle both dict and numeric amount values
            if isinstance(amount, dict):
                amount_value = amount.get('amount', 0)
            else:
                amount_value = amount
            
            if amount_value > 0.1:
                current_resources.add(resource_name)

        new_resources = current_resources - self.resource_history
        self.resource_history.update(current_resources)
        self.celestial_body_history.add(current_body)
        self.vessel_situation_history.add(vessel_situation)

        if new_resources:
            mission_time_key = self.mission_time + mission_time
            if mission_time_key not in self.resource_vs_time:
                self.resource_vs_time[mission_time_key] = []
            self.resource_vs_time[mission_time_key].extend(new_resources)

    def update_mission_time(self, event):
        if "mission_time" in event:
            self.mission_time += event["mission_time"]
        elif "universal_time" in event and self.universal_time_start:
            self.mission_time = event["universal_time"] - self.uniersal_time_start

    def update_position(self, event):
        if "position" not in event or not self.init_position:
            return

        position = [
            event["position"]["x"] - self.init_position[0],
            event["position"]["y"] - self.init_position[1],
            event["position"]["z"] - self.init_position[2],
        ]

        if self.position_history[-1] != position:
            self.position_history.append(position)

    def update_orbital_state(self, event):
        if "orbit_parameters" not in event:
            return

        orbit_data = {
            "mission_time": self.mission_time,
            "apoapsis": event["orbit_parameters"].get("apoapsis_altitude", 0),
            "periapsis": event["orbit_parameters"].get("periapsis_altitude", 0),
            "inclination": event["orbit_parameters"].get("inclination", 0),
            "eccentricity": event["orbit_parameters"].get("eccentricity", 0),
            "current_body": event.get("current_body", "Unknown"),
            "vessel_situation": event.get("vessel_situation", "Unknown"),
        }

        if (not self.orbital_history or
            abs(self.orbital_history[-1]["apoapsis"] - orbit_data["apoapsis"]) > 1000 or
            abs(self.orbital_history[-1]["periapsis"] - orbit_data["periapsis"]) > 1000 or
            self.orbital_history[-1]["current_body"] != orbit_data["current_body"]):
            self.orbital_history.append(orbit_data)

    def get_exploration_summary(self):
        return {
            "resources_discovered": len(self.resource_history),
            "celestial_bodies_visited": len(self.celestial_body_history),
            "vessel_situations_experienced": len(self.vessel_situation_history),
            "total_mission_time": self.mission_time,
            "orbital_maneuvers": len(self.orbital_history),
            "distance_traveled": self.calculate_total_distance(),
            "iterations_completed": self.iteration,
        }

    def calculate_total_distance(self):
        if len(self.position_history) < 2:
            return 0.0

        total_distance = 0.0
        for i in range(1, len(self.position_history)):
            prev_pos = self.position_history[i-1]
            curr_pos = self.position_history[i]

            distance = (
                (curr_pos[0] - prev_pos[0]) ** 2 +
                (curr_pos[1] - prev_pos[1]) ** 2 +
                (curr_pos[2] - prev_pos[2]) ** 2
            ) ** 0.5

            total_distance += distance

        return total_distance

    def get_resource_timeline(self):
        return self.resource_vs_time

    def get_orbital_progression(self):
        return self.orbital_history

    def get_visited_bodies(self):
        return list(self.vessel_situation_history)