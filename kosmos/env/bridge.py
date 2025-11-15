
import time
from typing import SupportsFloat, Any, Tuple, Dict
import math
import krpc

import gymnasium as gym
from gymnasium.core import ObsType
from kosmos.utils.telemetry_collector import TelemetryCollector

class KSPEnv(gym.Env):
    def __init__(
        self,
        krpc_address="127.0.0.1",
        krpc_rpc_port=50000,
        krpc_stream_port=50001,
    ):
        self.krpc_address = krpc_address
        self.krpc_rpc_port = krpc_rpc_port
        self.krpc_stream_port = krpc_stream_port

        self.conn = None
        self.vessel = None
        self.space_center = None
        self.mech_jeb = None
        self.has_reset = False
        self.reset_options = None
        self.connected = False
        self.streams = {} # Store active streams for clean
        self.telemetry_collector = None 
        self._vessel_cached_for_collector = None

    def check_connection(self):
        # Attempt to connect to KSP
        retry = 0
        max_retries = 5

        while retry < max_retries:
            try:
                if self.conn:
                    # Test existing connection
                    self.conn.krpc.current_game_scene
                    print(f"🔍 DEBUG: Existing connection found, mech_jeb={self.mech_jeb}")
                    # Check if MechJeb is available but not connected
                    if self.mech_jeb is None:
                        try:
                            print("🔍 DEBUG: Attempting to connect to MechJeb service...")
                            self.mech_jeb = self.conn.mech_jeb
                            self.telemetry_collector.mech_jeb = self.mech_jeb
                            print("✅ MechJeb service available")
                            print(f"🔍 DEBUG: MechJeb object: {self.mech_jeb}")
                        except Exception as e:
                            print(f"❌ MechJeb service not available: {e}")
                            self.mech_jeb = None
                    else:
                        print(f"🔍 DEBUG: MechJeb already connected: {self.mech_jeb}")
                        # Test MechJeb API readiness on existing connection
                        try:
                            api_ready = self.mech_jeb.api_ready
                            print(f"🔍 DEBUG: MechJeb API ready: {api_ready}")
                            if not api_ready:
                                print("⚠️ WARNING: MechJeb service connected but API not ready - may need activation in game")
                                # Try to refresh MechJeb connection
                                try:
                                    self.mech_jeb = self.conn.mech_jeb
                                    self.telemetry_collector.mech_jeb = self.mech_jeb
                                    print("🔄 DEBUG: Refreshed MechJeb connection")
                                except Exception as refresh_e:
                                    print(f"⚠️ WARNING: Could not refresh MechJeb connection: {refresh_e}")
                        except Exception as api_e:
                            print(f"⚠️ WARNING: Could not check MechJeb API readiness: {api_e}")
                            # Try to reconnect to MechJeb
                            try:
                                self.mech_jeb = self.conn.mech_jeb
                                self.telemetry_collector.mech_jeb = self.mech_jeb
                                print("🔄 DEBUG: Reconnected to MechJeb service")
                            except Exception as reconnect_e:
                                print(f"❌ ERROR: Could not reconnect to MechJeb: {reconnect_e}")
                                self.mech_jeb = None
                    return True
                else:
                    # Establish new connection
                    self.conn = krpc.connect(
                        name=f"Kosmos-{int(time.time())}",
                        address=self.krpc_address,
                        rpc_port=self.krpc_rpc_port,
                        stream_port=self.krpc_stream_port,
                    )
                    print(f"Connected to kRPC at {self.krpc_address}:{self.krpc_rpc_port}")

                    # Initialize core services
                    self.space_center = self.conn.space_center

                    # Initialize telemetry collector
                    self.telemetry_collector = TelemetryCollector(f"Kosmos-{int(time.time())}")
                    self.telemetry_collector.conn = self.conn
                    self.telemetry_collector.space_center = self.space_center

                    # Try to get MechJeb if available
                    try:
                        print("🔍 DEBUG: Attempting to connect to MechJeb service...")
                        self.mech_jeb = self.conn.mech_jeb
                        self.telemetry_collector.mech_jeb = self.mech_jeb
                        print("✅ MechJeb service available")
                        print(f"🔍 DEBUG: MechJeb object: {self.mech_jeb}")
                        
                        # Test MechJeb API readiness
                        try:
                            api_ready = self.mech_jeb.api_ready
                            print(f"🔍 DEBUG: MechJeb API ready: {api_ready}")
                            if not api_ready:
                                print("⚠️ WARNING: MechJeb service connected but API not ready - may need activation in game")
                        except Exception as api_e:
                            print(f"⚠️ WARNING: Could not check MechJeb API readiness: {api_e}")
                            
                    except Exception as e:
                        print(f"❌ MechJeb service not available: {e}")
                        self.mech_jeb = None

                    self.connected = True
                    return True
            except Exception as e:
                retry += 1
                print(f"Connection attempt {retry} failed: {e}")
                if retry < max_retries:
                    time.sleep(2 ** retry)
                else:
                    raise RuntimeError(f"Failed to connect to kRPC after {max_retries} attempts")

    def get_vessel_telemetry(self):
        if not self.connected or not self.vessel or not self.telemetry_collector:
            return {}

        try:
            # Only (re)bind vessel to telemetry collector when it changes
            if self._vessel_cached_for_collector is not self.vessel:
                self.telemetry_collector.set_vessel()
                self._vessel_cached_for_collector = self.vessel
            
            # Get AI-optimized telemetry data
            ai_data = self.telemetry_collector.get_ai_decision_data()
            
            # Convert to the format expected by the agents
            telemetry = {
                "vessel_name": ai_data.get("name", "Unknown"),
                "vessel_type": ai_data.get("situation", "Unknown"),  # Using situation as type for now
                "vessel_situation": ai_data.get("situation", "Unknown"),
                "mission_time": ai_data.get("timestamp", 0),
                "universal_time": self.space_center.ut if self.space_center else 0,
                "current_body": self.vessel.orbit.body.name if self.vessel and self.vessel.orbit else "Unknown",
            }

            # Position and velocity
            position = ai_data.get("position_surface", (0, 0, 0))
            velocity = ai_data.get("velocity_surface", (0, 0, 0))
            telemetry.update({
                "position": {
                    "x": position[0] if len(position) > 0 else 0,
                    "y": position[1] if len(position) > 1 else 0,
                    "z": position[2] if len(position) > 2 else 0,
                },
                "velocity": {
                    "x": velocity[0] if len(velocity) > 0 else 0,
                    "y": velocity[1] if len(velocity) > 1 else 0,
                    "z": velocity[2] if len(velocity) > 2 else 0,
                },
                "altitude": ai_data.get("altitude", 0),
                "surface_altitude": ai_data.get("surface_altitude", 0),
                "speed": ai_data.get("speed", 0),
                "vertical_speed": ai_data.get("vertical_speed", 0),
                "g_force": 0,  # Not in AI data, will be calculated if needed
            })

            # Override with fast streams if available to reduce RPC latency
            try:
                if "altitude" in self.streams:
                    telemetry["altitude"] = self.streams["altitude"]()
                if "speed" in self.streams:
                    telemetry["speed"] = self.streams["speed"]()
                if "vertical_speed" in self.streams:
                    telemetry["vertical_speed"] = self.streams["vertical_speed"]()
            except:
                pass

            # Orbital parameters
            telemetry["orbit_parameters"] = {
                "apoapsis_altitude": ai_data.get("apoapsis_altitude", 0),
                "periapsis_altitude": ai_data.get("periapsis_altitude", 0),
                "inclination": ai_data.get("inclination", 0),
                "eccentricity": ai_data.get("eccentricity", 0),
                "period": 0,  # Not in AI data
                "time_to_apoapsis": 0,  # Not in AI data
                "time_to_periapsis": 0,  # Not in AI data
            }

            # Resources
            resources = {}
            fuel_amount = ai_data.get("fuel_amount", 0)
            fuel_max = ai_data.get("fuel_max", 0)
            electric_charge = ai_data.get("electric_charge", 0)
            electric_charge_max = ai_data.get("electric_charge_max", 0)
            
            if fuel_max > 0:
                resources["LiquidFuel"] = {"amount": fuel_amount, "max": fuel_max}
            if electric_charge_max > 0:
                resources["ElectricCharge"] = {"amount": electric_charge, "max": electric_charge_max}
            
            telemetry["resources"] = resources

            # Vessel status
            telemetry["vessel_status"] = {
                "mass": ai_data.get("mass", 0),
                "dry_mass": 0,  # Not in AI data
                "thrust": ai_data.get("thrust", 0),
                "available_thrust": ai_data.get("max_thrust", 0),
                "max_thrust": ai_data.get("max_thrust", 0),
                "specific_impulse": 0,  # Not in AI data
                "control_state": {
                    "throttle": ai_data.get("throttle", 0),
                    "sas": ai_data.get("sas_enabled", False),
                    "rcs": ai_data.get("rcs_enabled", False),
                    "gear": ai_data.get("gear_deployed", False),
                    "lights": False,  # Not in AI data
                    "brakes": False,  # Not in AI data
                },
            }

            # Override control state with streams if available
            try:
                cs = telemetry["vessel_status"]["control_state"]
                if "throttle" in self.streams:
                    cs["throttle"] = self.streams["throttle"]()
                if "sas" in self.streams:
                    cs["sas"] = self.streams["sas"]()
            except:
                pass

            # Add MechJeb status
            telemetry["mechjeb_status"] = {
                "api_ready": False,
                "ascent_status": "Unknown"
            }
            
            # Override with streams if available
            try:
                if "mechjeb_api_ready" in self.streams:
                    telemetry["mechjeb_status"]["api_ready"] = self.streams["mechjeb_api_ready"]()
                if "ascent_status" in self.streams:
                    telemetry["mechjeb_status"]["ascent_status"] = self.streams["ascent_status"]()
            except:
                pass

            # Add maneuver intent
            try:
                api_ready = telemetry["mechjeb_status"]["api_ready"]
                if (self.mech_jeb is None) or (not api_ready):
                    telemetry["maneuver"] = {"has_node": False}
                    if self.mech_jeb is None:
                        print("🔍 DEBUG: Maneuver intent skipped - MechJeb is None")
                    else:
                        print(f"🔍 DEBUG: Maneuver intent skipped - MechJeb API ready: {api_ready}")
                else:
                    nodes = list(self.vessel.control.nodes)
                    if not nodes:
                        telemetry["maneuver"] = {"has_node": False}
                        print("🔍 DEBUG: No maneuver nodes present")
                    else:
                        node = nodes[0]

                    # timing
                    ut_now = self.space_center.ut
                    node_ut = node.ut
                    time_to_node = node_ut - ut_now

                    # delta-v components
                    dv_prograde = node.prograde 
                    dv_normal = node.normal 
                    dv_radial = node.radial

                    dv_total = getattr(node, "delta_v", None)
                    if dv_total is None:
                        dv_total = (dv_prograde ** 2 + dv_normal ** 2 + dv_radial ** 2) ** 0.5
                        print(f"🔍 DEBUG: delta_v not provided; computed from components: prograde={dv_prograde:.3f}, normal={dv_normal:.3f}, radial={dv_radial:.3f}, total={dv_total:.3f}")
                    else:
                        print(f"🔍 DEBUG: Node delta_v reported: total={dv_total:.3f}, prograde={dv_prograde:.3f}, normal={dv_normal:.3f}, radial={dv_radial:.3f}")

                    burn_time = None
                    thrust = self.vessel.available_thrust
                    isp = self.vessel.specific_impulse
                    g0 = 9.80665
                    
                    if thrust is not None and thrust > 0 and isp is not None and isp > 0 and dv_total is not None and dv_total > 0:
                        ve = isp * g0
                        if ve > 0:
                            m0 = self.vessel.mass
                            try:
                                m1 = m0 / math.exp(dv_total / ve)
                                prop_mass = max(m0 - m1, 0.0)
                                mass_flow = thrust / (isp * g0)
                                burn_time = prop_mass / mass_flow if mass_flow > 1e-9 and prop_mass >= 0 else None
                            except OverflowError as e:
                                print(f"🔍 DEBUG: Error calculating burn time (overflow): {e}")
                                burn_time = None
                        else:
                            print(f"🔍 DEBUG: Burn time not computed - thrust={thrust}, isp={isp}, dv_total={dv_total}")
                    
                    half_burn_start = (node_ut - (burn_time / 2.0)) if burn_time else None

                    telemetry["maneuver"] = {
                        "has_node": True,
                        "node_ut": node_ut,
                        "time_to_node": time_to_node,
                        "dv_total": dv_total,
                        "dv_prograde": dv_prograde,
                        "dv_normal": dv_normal,
                        "dv_radial": dv_radial,
                        "burn_time": burn_time,
                        "half_burn_start": half_burn_start,
                    }
                    print(f"🔍 DEBUG: Maneuver telemetry: has_node={telemetry['maneuver'].get('has_node')}, dv_total={telemetry['maneuver'].get('dv_total')}, burn_time={telemetry['maneuver'].get('burn_time')}, time_to_node={telemetry['maneuver'].get('time_to_node')}")
            except Exception as e:
                print(f"🔍 DEBUG: Maneuver intent block failed: {e}")
                telemetry["maneuver"] = {"has_node": False}
            
            # Add next-patch (encounter) preview
            try:
                patches = list(self.vessel.orbit.patches)
                if len(patches) < 2:
                    telemetry["next_patch"] = {"has_next_patch": False}
                    print("🔍 DEBUG: No next orbit patch available (less than 2 patches)")
                else:
                    npatch = patches[1]
                    rel_speed = None
                    try:
                        rel_speed = npatch.speed_at(npatch.periapsis)
                    except Exception:
                        pass
                    telemetry["next_patch"] = {
                        "has_next_patch": True,
                        "next_body": npatch.body.name,
                        "next_periapsis_altitude": npatch.periapsis_altitude,
                        "time_to_next_periapsis": npatch.time_to_periapsis,
                        "relative_speed_at_periapsis": rel_speed,
                    }
                    print(f"🔍 DEBUG: Next patch: body={npatch.body.name}, periapsis_alt={npatch.periapsis_altitude}, time_to_periapsis={npatch.time_to_periapsis}, rel_speed_at_pe={rel_speed}")
            except Exception as e:
                print(f"🔍 DEBUG: Next-patch preview failed: {e}")
                telemetry["next_patch"] = {"has_next_patch": False}


            try:
                telemetry["mechjeb_status"]["planner_warning"] = getattr(self.mech_jeb.maneuver_planner, "error_message", "") or ""
            except Exception as e:
                print(f"🔍 DEBUG: Could not read planner warning: {e}")
                telemetry["mechjeb_status"]["planner_warning"] = ""
            try:
                telemetry["mechjeb_status"]["executor_state"] = getattr(self.mech_jeb.node_executor, "state", None)
            except Exception as e:
                print(f"🔍 DEBUG: Could not read executor state: {e}")
                telemetry["mechjeb_status"]["executor_state"] = None
            


            # Part status
            telemetry["part_status"] = {
                "part_count": ai_data.get("part_count", 0),
                "stage_count": 0,  # Not available in AI data yet
                "current_stage": ai_data.get("current_stage", 0),
            }

            # Nearby vessels (simplified for now)
            telemetry["nearby_vessels"] = []

            # Add comprehensive telemetry if available
            try:
                if self.telemetry_collector:
                    comprehensive = self.telemetry_collector.get_comprehensive_telemetry()
                    telemetry["comprehensive_telemetry"] = comprehensive
                    print(f"🔍 DEBUG: Added comprehensive telemetry with {len(comprehensive)} categories")
            except Exception as e:
                print(f"🔍 DEBUG: Could not get comprehensive telemetry: {e}")
                telemetry["comprehensive_telemetry"] = {}

            return telemetry

        except Exception as e:
            print(f"Error getting telemetry: {e}")
            return {"error": str(e)}

    def calculate_distance(self, vessel1, vessel2):
        try:
            pos1 = vessel1.position(vessel1.orbit.body.reference_frame)
            pos2 = vessel2.position(vessel2.orbit.body.reference_frame)
            return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5
        except Exception as e:
            return float('inf')

    def step(
        self,
        code: str,
        programs: str = "",
    ) -> Tuple[ObsType, SupportsFloat, bool, bool, Dict[str, Any]]:
        if not self.has_reset:
            raise RuntimeError("Environment has not been reset yet")
        
        self.check_connection()

        # Prepare execution context
        execution_context = {
            "conn": self.conn,
            "vessel": self.vessel,
            "space_center": self.space_center,
            "print": print,
            "time": time,
            "krpc": krpc,
        }

        # Add programs to context
        if programs:
            try:
                print(f"🔍 DEBUG: KSPEnv executing programs ({len(programs)} chars)")
                print(f"🔍 DEBUG: Programs: {programs}")
                exec(programs, execution_context)
            except Exception as e:
                return [("error", {"execution_error": f"Program error: {e}"})]

        # Execute main code
        start_time = time.time()
        print(f"🔍 DEBUG: KSPEnv executing code ({len(code)} chars)")
        print(f"🔍 DEBUG: Code preview: {code[:200]}...")
        print(f"🔍 DEBUG: Execution context keys: {list(execution_context.keys())}")
        
        try:
            # Add a custom print function that shows what's happening
            def debug_print(*args, **kwargs):
                print(f"🔍 DEBUG: [KSP Code] {' '.join(str(arg) for arg in args)}")
            
            # Add debug_print to execution context
            execution_context["debug_print"] = debug_print
            
            print(f"🔍 DEBUG: KSPEnv executing code ({len(code)} chars)")
            print(f"🔍 DEBUG: Code: {code}")
            exec(code, execution_context)
            execution_time = time.time() - start_time
            print(f"🔍 DEBUG: Code execution completed in {execution_time:.3f}s")

            # Small delay to allow state to update; keep minimal for responsiveness
            time.sleep(0.05)
            
            # Get telemetry after execution
            telemetry = self.get_vessel_telemetry()
            telemetry["execution_time"] = execution_time
            print(f"🔍 DEBUG: Telemetry collected: {len(telemetry)} fields")

            return [("observe", telemetry)]
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"🔍 ERROR: Code execution failed after {execution_time:.3f}s: {e}")
            print(f"🔍 ERROR: Exception type: {type(e).__name__}")
            import traceback
            print(f"🔍 ERROR: Traceback: {traceback.format_exc()}")
            
            error_data = {
                "execution_error": str(e),
                "execution_time": execution_time,
            }
            # Still try to get telemetry even on error
            try:
                telemetry = self.get_vessel_telemetry()
                error_data.update(telemetry)
                print(f"🔍 DEBUG: Error telemetry collected: {len(telemetry)} fields")
            except Exception as te:
                print(f"🔍 ERROR: Failed to collect error telemetry: {te}")

            return [("error", error_data)]

    def reset(
        self,
        *,
        speed=None,
        options=None,
    ) -> Tuple[ObsType, Dict[str, Any]]:
        if options is None:
            options = {}

        self.reset_options = {
            "mode": options.get("mode", "hard"),
            "vessel_name": options.get("vessel_name", None),
            "wait_time": options.get("wait_time", 0.1),
            "scene": options.get("scene", "flight"),
        }

        self.check_connection()

        mode = self.reset_options["mode"]

        if mode == "hard":
            # Reset to launch pad or specific vessel
            try:
                # Switch to space center if not already there
                if self.conn.krpc.current_game_scene != self.conn.krpc.GameScene.space_center:
                    self.space_center.load_space_center()
                    time.sleep(0.2)

                # Get active vessel (should be on launch pad after space center switch)
                self.vessel = self.space_center.active_vessel

            except Exception as e:
                print(f"Hard reset failed: {e}")
                # Fallback to current active vessel
                self.vessel = self.space_center.active_vessel

        elif mode == "soft":
            # Keep current vessel and state, just refresh connection
            self.vessel = self.space_center.active_vessel

        # Wait for stabilization (short)
        time.sleep(self.reset_options["wait_time"])

        # (Re)create fast telemetry streams for current vessel
        try:
            # Clear old per-vessel streams
            for key in ["altitude", "speed", "vertical_speed", "throttle", "sas", "mechjeb_api_ready", "ascent_status"]:
                if key in self.streams:
                    try:
                        self.streams[key].remove()
                    except:
                        pass
                    del self.streams[key]

            flight = self.vessel.flight()
            self.streams["altitude"] = self.add_stream(getattr, flight, "mean_altitude")
            self.streams["speed"] = self.add_stream(getattr, flight, "speed")
            self.streams["vertical_speed"] = self.add_stream(getattr, flight, "vertical_speed")
            self.streams["throttle"] = self.add_stream(getattr, self.vessel.control, "throttle")
            self.streams["sas"] = self.add_stream(getattr, self.vessel.control, "sas")
            
            # Add MechJeb streams if available
            if self.mech_jeb:
                try:
                    self.streams["mechjeb_api_ready"] = self.add_stream(getattr, self.mech_jeb, "api_ready")
                    ascent_ap = self.mech_jeb.ascent_autopilot
                    self.streams["ascent_status"] = self.add_stream(getattr, ascent_ap, "status")
                    print("🔍 DEBUG: MechJeb streams created successfully")
                except Exception as mj_e:
                    print(f"⚠️ WARNING: Could not create MechJeb streams: {mj_e}")
                    # Try to refresh MechJeb connection and retry streams
                    try:
                        self.mech_jeb = self.conn.mech_jeb
                        self.telemetry_collector.mech_jeb = self.mech_jeb
                        self.streams["mechjeb_api_ready"] = self.add_stream(getattr, self.mech_jeb, "api_ready")
                        ascent_ap = self.mech_jeb.ascent_autopilot
                        self.streams["ascent_status"] = self.add_stream(getattr, ascent_ap, "status")
                        print("🔄 DEBUG: MechJeb streams created after refresh")
                    except Exception as retry_e:
                        print(f"❌ ERROR: Could not create MechJeb streams after refresh: {retry_e}")
        except Exception:
            pass

        initial_telemetry = self.get_vessel_telemetry()

        self.has_reset = True
        return [("observe"), initial_telemetry]

    def close(self):
        # Remove all streams
        for stream in self.streams.values():
            try:
                stream.remove()
            except:
                pass
        self.streams.clear()

        # Close kRPC connection
        if self.conn:
            try:
                self.conn.close()
                self.connected = False
                print("kRPC connection closed")
            except:
                pass

        return not self.connected

    def add_stream(self, func, *args, **kwargs):
        stream = self.conn.add_stream(func, *args, **kwargs)
        stream_id = f"{func.__name__}_{len(self.streams)}"
        self.streams[stream_id] = stream
        return stream

    def remove_stream(self, stream_id):
        if stream_id in self.streams:
            try:
                self.streams[stream_id].remove()
                del self.streams[stream_id]
            except:
                pass

    def wait_for_scene(self, target_scene, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                current_scene = self.conn.krpc.current_game_scene
                if current_scene == target_scene:
                    return True
                time.sleep(0.5)
            except:
                time.sleep(1)
        return False