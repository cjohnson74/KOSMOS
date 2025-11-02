#!/usr/bin/env python3
"""
Comprehensive kRPC Telemetry Collector for AI Agents

This module provides a simple interface to collect all available telemetry
data from Kerbal Space Program via kRPC for AI agent decision making.
"""

import krpc
from typing import Dict, Any, Optional, Tuple
import time


class TelemetryCollector:
    """
    A comprehensive telemetry collector for KSP vessels.
    
    This class provides methods to gather all available telemetry data
    from a vessel in Kerbal Space Program, organized by category for
    easy access by AI agents.
    """
    
    def __init__(self, connection_name: str = "AI_Agent"):
        """
        Initialize the telemetry collector.
        
        Args:
            connection_name: Name for the kRPC connection
        """
        self.conn = krpc.connect(name=connection_name)
        self.space_center = self.conn.space_center
        self.vessel = None
        self.flight = None
        self.orbit = None
        self.control = None
        self.resources = None
        
    def set_vessel(self, vessel_name: Optional[str] = None):
        """
        Set the active vessel for telemetry collection.
        
        Args:
            vessel_name: Name of vessel to track. If None, uses active vessel.
        """
        if vessel_name:
            vessels = self.space_center.vessels
            self.vessel = next((v for v in vessels if v.name == vessel_name), None)
            if not self.vessel:
                raise ValueError(f"Vessel '{vessel_name}' not found")
        else:
            self.vessel = self.space_center.active_vessel
            
        if not self.vessel:
            raise ValueError("No active vessel available")
            
        # Initialize related objects
        self.flight = self.vessel.flight()
        self.orbit = self.vessel.orbit
        self.control = self.vessel.control
        self.resources = self.vessel.resources
        
    def get_basic_vessel_data(self) -> Dict[str, Any]:
        """Get basic vessel information."""
        if not self.vessel:
            return {}
            
        return {
            'name': self.vessel.name,
            'type': str(self.vessel.type),
            'situation': str(self.vessel.situation),
            'mass': self.vessel.mass,
            'dry_mass': self.vessel.dry_mass,
            'crew_count': self.vessel.crew_count,
            'crew_capacity': self.vessel.crew_capacity,
            'biome': self.vessel.biome,
            'recoverable': self.vessel.recoverable,
            'met': self.vessel.met,  # Mission Elapsed Time
        }
    
    def get_performance_data(self) -> Dict[str, Any]:
        """Get vessel performance metrics."""
        if not self.vessel:
            return {}
            
        return {
            'thrust': self.vessel.thrust,
            'max_thrust': self.vessel.max_thrust,
            'max_vacuum_thrust': self.vessel.max_vacuum_thrust,
            'specific_impulse': self.vessel.specific_impulse,
            'kerbin_sea_level_specific_impulse': self.vessel.kerbin_sea_level_specific_impulse,
            'vacuum_specific_impulse': self.vessel.vacuum_specific_impulse,
        }
    
    def get_torque_data(self) -> Dict[str, Any]:
        """Get available torque and control capabilities."""
        if not self.vessel:
            return {}
            
        return {
            'available_control_surface_torque': self.vessel.available_control_surface_torque,
            'available_engine_torque': self.vessel.available_engine_torque,
            'available_rcs_torque': self.vessel.available_rcs_torque,
            'available_reaction_wheel_torque': self.vessel.available_reaction_wheel_torque,
            'available_thrust': self.vessel.available_thrust,
            'available_torque': self.vessel.available_torque,
        }
    
    def get_position_velocity_data(self) -> Dict[str, Any]:
        """Get position and velocity information in multiple reference frames."""
        if not self.flight or not self.vessel:
            return {}
            
        # Get reference frames
        vessel_rf = self.vessel.reference_frame
        orbital_rf = self.vessel.orbital_reference_frame
        surface_rf = self.vessel.surface_reference_frame
        
        return {
            # Vessel-relative position and velocity
            'position_vessel': self.vessel.position(vessel_rf),
            'velocity_vessel': self.vessel.velocity(vessel_rf),
            
            # Orbital-relative position and velocity
            'position_orbital': self.vessel.position(orbital_rf),
            'velocity_orbital': self.vessel.velocity(orbital_rf),
            
            # Surface-relative position and velocity
            'position_surface': self.vessel.position(surface_rf),
            'velocity_surface': self.vessel.velocity(surface_rf),
            
            # Flight data (uses default reference frame)
            'speed': self.flight.speed,
            'horizontal_speed': self.flight.horizontal_speed,
            'vertical_speed': self.flight.vertical_speed,
            'equivalent_air_speed': self.flight.equivalent_air_speed,
            'true_air_speed': self.flight.true_air_speed,
            'terminal_velocity': self.flight.terminal_velocity,
        }
    
    def get_altitude_location_data(self) -> Dict[str, Any]:
        """Get altitude and location information."""
        if not self.flight:
            return {}
            
        return {
            'mean_altitude': self.flight.mean_altitude,
            'surface_altitude': self.flight.surface_altitude,
            'bedrock_altitude': self.flight.bedrock_altitude,
            'latitude': self.flight.latitude,
            'longitude': self.flight.longitude,
            'elevation': self.flight.elevation,
        }
    
    def get_aerodynamics_data(self) -> Dict[str, Any]:
        """Get aerodynamic information (stock KSP + FAR if available)."""
        if not self.flight:
            return {}
        
        # Basic aerodynamics (available in stock KSP)
        aero_data = {
            'atmosphere_density': self.flight.atmosphere_density,
            'dynamic_pressure': self.flight.dynamic_pressure,
            'static_pressure': self.flight.static_pressure,
            'static_pressure_at_msl': self.flight.static_pressure_at_msl,
            'drag': self.flight.drag,
            'lift': self.flight.lift,
            'mach': self.flight.mach,
        }
        
        # FAR-specific properties (optional - only if FAR mod is installed)
        # These will be None if FAR is not available
        try:
            aero_data['drag_coefficient'] = self.flight.drag_coefficient
        except:
            aero_data['drag_coefficient'] = None
        
        try:
            aero_data['lift_coefficient'] = self.flight.lift_coefficient
        except:
            aero_data['lift_coefficient'] = None
        
        try:
            aero_data['ballistic_coefficient'] = self.flight.ballistic_coefficient
        except:
            aero_data['ballistic_coefficient'] = None
        
        try:
            aero_data['reynolds_number'] = self.flight.reynolds_number
        except:
            aero_data['reynolds_number'] = None
        
        return aero_data
    
    def get_orientation_data(self) -> Dict[str, Any]:
        """Get vessel orientation information."""
        if not self.flight:
            return {}
            
        return {
            'heading': self.flight.heading,
            'pitch': self.flight.pitch,
            'roll': self.flight.roll,
            'direction': self.flight.direction,
            'rotation': self.flight.rotation,
            'angle_of_attack': self.flight.angle_of_attack,
            'sideslip_angle': self.flight.sideslip_angle,
        }
    
    def get_flight_dynamics_data(self) -> Dict[str, Any]:
        """Get flight dynamics information (stock KSP + FAR if available)."""
        if not self.flight:
            return {}
        
        dynamics_data = {
            'g_force': self.flight.g_force,
            'center_of_mass': self.flight.center_of_mass,
            'aerodynamic_force': self.flight.aerodynamic_force,
        }
        
        # FAR-specific properties (optional - only if FAR mod is installed)
        try:
            dynamics_data['thrust_specific_fuel_consumption'] = self.flight.thrust_specific_fuel_consumption
        except:
            dynamics_data['thrust_specific_fuel_consumption'] = None
        
        try:
            dynamics_data['stall_fraction'] = self.flight.stall_fraction
        except:
            dynamics_data['stall_fraction'] = None
        
        return dynamics_data
    
    def get_reference_vectors(self) -> Dict[str, Any]:
        """Get reference direction vectors."""
        if not self.flight:
            return {}
            
        return {
            'prograde': self.flight.prograde,
            'retrograde': self.flight.retrograde,
            'normal': self.flight.normal,
            'anti_normal': self.flight.anti_normal,
            'radial': self.flight.radial,
            'anti_radial': self.flight.anti_radial,
        }
    
    def get_reference_frame_data(self) -> Dict[str, Any]:
        """Get reference frame information and positions in different coordinate systems."""
        if not self.vessel:
            return {}
            
        # Get reference frames
        vessel_rf = self.vessel.reference_frame
        orbital_rf = self.vessel.orbital_reference_frame
        surface_rf = self.vessel.surface_reference_frame
        
        # Get positions in different reference frames
        vessel_pos = self.vessel.position(vessel_rf)
        orbital_pos = self.vessel.position(orbital_rf)
        surface_pos = self.vessel.position(surface_rf)
        
        # Get velocities in different reference frames
        vessel_vel = self.vessel.velocity(vessel_rf)
        orbital_vel = self.vessel.velocity(orbital_rf)
        surface_vel = self.vessel.velocity(surface_rf)
        
        return {
            'reference_frames': {
                'vessel': {
                    'position': vessel_pos,
                    'velocity': vessel_vel,
                    'description': 'Vessel-relative coordinates (X=right, Y=forward, Z=up)'
                },
                'orbital': {
                    'position': orbital_pos,
                    'velocity': orbital_vel,
                    'description': 'Orbital coordinates (X=anti-radial, Y=prograde, Z=normal)'
                },
                'surface': {
                    'position': surface_pos,
                    'velocity': surface_vel,
                    'description': 'Surface coordinates (X=zenith, Y=north, Z=east)'
                }
            },
            'coordinate_systems': {
                'vessel_available': vessel_rf is not None,
                'orbital_available': orbital_rf is not None,
                'surface_available': surface_rf is not None,
            }
        }
    
    def get_orbital_data(self) -> Dict[str, Any]:
        """Get orbital information."""
        if not self.orbit:
            return {}
            
        return {
            # Orbital elements
            'semi_major_axis': self.orbit.semi_major_axis,
            'semi_minor_axis': self.orbit.semi_minor_axis,
            'eccentricity': self.orbit.eccentricity,
            'inclination': self.orbit.inclination,
            'longitude_of_ascending_node': self.orbit.longitude_of_ascending_node,
            'argument_of_periapsis': self.orbit.argument_of_periapsis,
            'mean_anomaly': self.orbit.mean_anomaly,
            'eccentric_anomaly': self.orbit.eccentric_anomaly,
            'true_anomaly': self.orbit.true_anomaly,
            
            # Orbital characteristics
            'apoapsis': self.orbit.apoapsis,
            'periapsis': self.orbit.periapsis,
            'apoapsis_altitude': self.orbit.apoapsis_altitude,
            'periapsis_altitude': self.orbit.periapsis_altitude,
            'period': self.orbit.period,
            'orbital_speed': self.orbit.orbital_speed,
            'speed': self.orbit.speed,
            'radius': self.orbit.radius,
            
            # Timing
            'time_to_apoapsis': self.orbit.time_to_apoapsis,
            'time_to_periapsis': self.orbit.time_to_periapsis,
            'time_to_soi_change': self.orbit.time_to_soi_change,
            'epoch': self.orbit.epoch,
            'mean_anomaly_at_epoch': self.orbit.mean_anomaly_at_epoch,
            
            # Body information
            'body_name': self.orbit.body.name if self.orbit.body else None,
        }
    
    def get_control_data(self) -> Dict[str, Any]:
        """Get current control inputs and system status."""
        if not self.control:
            return {}
            
        return {
            # Flight controls
            'pitch': self.control.pitch,
            'yaw': self.control.yaw,
            'roll': self.control.roll,
            'throttle': self.control.throttle,
            'forward': self.control.forward,
            'up': self.control.up,
            'right': self.control.right,
            
            # System controls
            'sas': self.control.sas,
            'rcs': self.control.rcs,
            'brakes': self.control.brakes,
            'gear': self.control.gear,
            'lights': self.control.lights,
            'abort': self.control.abort,
            
            # Advanced controls
            'custom_axis01': self.control.custom_axis01,
            'custom_axis02': self.control.custom_axis02,
            'custom_axis03': self.control.custom_axis03,
            'custom_axis04': self.control.custom_axis04,
            'wheel_steering': self.control.wheel_steering,
            'wheel_throttle': self.control.wheel_throttle,
            
            # System status
            'state': str(self.control.state),
            'source': str(self.control.source),
            'current_stage': self.control.current_stage,
            'stage_lock': self.control.stage_lock,
            'sas_mode': str(self.control.sas_mode),
            'input_mode': str(self.control.input_mode),
        }
    
    def get_resource_data(self) -> Dict[str, Any]:
        """Get vessel resource information."""
        if not self.resources:
            return {}
            
        # Get all available resources
        resource_data = {}
        for resource in self.resources.names:
            res_info = {
                'amount': self.resources.amount(resource),
                'max': self.resources.max(resource),
            }
            
            # These properties may not be available for all resources or configurations
            try:
                res_info['flow_mode'] = str(self.resources.flow_mode(resource))
            except:
                res_info['flow_mode'] = None
            
            try:
                res_info['density'] = self.resources.density(resource)
            except:
                res_info['density'] = None
            
            resource_data[resource] = res_info
        
        return resource_data
    
    def get_comprehensive_telemetry(self) -> Dict[str, Any]:
        """
        Get all available telemetry data in one comprehensive dictionary.
        
        Returns:
            Dictionary containing all telemetry data organized by category
        """
        return {
            'timestamp': time.time(),
            'basic_vessel': self.get_basic_vessel_data(),
            'performance': self.get_performance_data(),
            'torque': self.get_torque_data(),
            'position_velocity': self.get_position_velocity_data(),
            'altitude_location': self.get_altitude_location_data(),
            'aerodynamics': self.get_aerodynamics_data(),
            'orientation': self.get_orientation_data(),
            'flight_dynamics': self.get_flight_dynamics_data(),
            'reference_vectors': self.get_reference_vectors(),
            'reference_frames': self.get_reference_frame_data(),
            'orbital': self.get_orbital_data(),
            'control': self.get_control_data(),
            'resources': self.get_resource_data(),
        }
    
    def get_ai_decision_data(self) -> Dict[str, Any]:
        """
        Get a simplified dataset optimized for AI decision making.
        
        This includes only the most critical data points for AI agents
        to make flight decisions.
        """
        if not self.vessel or not self.flight or not self.orbit:
            return {}
            
        return {
            'timestamp': time.time(),
            
            # Critical vessel state
            'name': self.vessel.name,
            'situation': str(self.vessel.situation),
            'mass': self.vessel.mass,
            'thrust': self.vessel.thrust,
            'max_thrust': self.vessel.max_thrust,
            
            # Position and motion (in different reference frames)
            'position_vessel': self.vessel.position(self.vessel.reference_frame),
            'velocity_vessel': self.vessel.velocity(self.vessel.reference_frame),
            'position_orbital': self.vessel.position(self.vessel.orbital_reference_frame),
            'velocity_orbital': self.vessel.velocity(self.vessel.orbital_reference_frame),
            'position_surface': self.vessel.position(self.vessel.surface_reference_frame),
            'velocity_surface': self.vessel.velocity(self.vessel.surface_reference_frame),
            'speed': self.flight.speed,
            'altitude': self.flight.mean_altitude,
            'surface_altitude': self.flight.surface_altitude,
            
            # Orientation
            'heading': self.flight.heading,
            'pitch': self.flight.pitch,
            'roll': self.flight.roll,
            
            # Orbital state
            'apoapsis_altitude': self.orbit.apoapsis_altitude,
            'periapsis_altitude': self.orbit.periapsis_altitude,
            'eccentricity': self.orbit.eccentricity,
            'inclination': self.orbit.inclination,
            'orbital_speed': self.orbit.orbital_speed,
            
            # Control inputs
            'throttle': self.control.throttle if self.control else 0,
            'pitch_input': self.control.pitch if self.control else 0,
            'yaw_input': self.control.yaw if self.control else 0,
            'roll_input': self.control.roll if self.control else 0,
            
            # System status
            'sas_enabled': self.control.sas if self.control else False,
            'rcs_enabled': self.control.rcs if self.control else False,
            'gear_deployed': self.control.gear if self.control else False,
            
            # Resources (key ones only)
            'fuel_amount': self.resources.amount('LiquidFuel') if self.resources else 0,
            'fuel_max': self.resources.max('LiquidFuel') if self.resources else 0,
            'electric_charge': self.resources.amount('ElectricCharge') if self.resources else 0,
            'electric_charge_max': self.resources.max('ElectricCharge') if self.resources else 0,
            
            # Parts information
            'part_count': len(self.vessel.parts.all) if hasattr(self.vessel, 'parts') else 0,
            'current_stage': self.vessel.control.current_stage if self.vessel.control else 0,
        }
    
    def get_reference_frame_for_mission(self, mission_type: str) -> Dict[str, Any]:
        """
        Get reference frame data optimized for specific mission types.
        
        Args:
            mission_type: Type of mission ('launch', 'orbital', 'landing', 'docking', 'surface')
            
        Returns:
            Dictionary with reference frame data relevant to the mission type
        """
        if not self.vessel:
            return {}
            
        base_data = {
            'mission_type': mission_type,
            'reference_frames_available': {
                'vessel': self.vessel.reference_frame is not None,
                'orbital': self.vessel.orbital_reference_frame is not None,
                'surface': self.vessel.surface_reference_frame is not None,
            }
        }
        
        if mission_type == 'launch':
            # For launch, we need surface and vessel reference frames
            return {
                **base_data,
                'surface_position': self.vessel.position(self.vessel.surface_reference_frame),
                'surface_velocity': self.vessel.velocity(self.vessel.surface_reference_frame),
                'vessel_position': self.vessel.position(self.vessel.reference_frame),
                'vessel_velocity': self.vessel.velocity(self.vessel.reference_frame),
                'altitude': self.flight.mean_altitude,
                'vertical_speed': self.flight.vertical_speed,
            }
            
        elif mission_type == 'orbital':
            # For orbital operations, we need orbital reference frame
            return {
                **base_data,
                'orbital_position': self.vessel.position(self.vessel.orbital_reference_frame),
                'orbital_velocity': self.vessel.velocity(self.vessel.orbital_reference_frame),
                'prograde': self.flight.prograde,
                'retrograde': self.flight.retrograde,
                'normal': self.flight.normal,
                'radial': self.flight.radial,
            }
            
        elif mission_type == 'landing':
            # For landing, we need surface reference frame
            return {
                **base_data,
                'surface_position': self.vessel.position(self.vessel.surface_reference_frame),
                'surface_velocity': self.vessel.velocity(self.vessel.surface_reference_frame),
                'surface_altitude': self.flight.surface_altitude,
                'vertical_speed': self.flight.vertical_speed,
                'horizontal_speed': self.flight.horizontal_speed,
            }
            
        elif mission_type == 'docking':
            # For docking, we need vessel reference frame
            return {
                **base_data,
                'vessel_position': self.vessel.position(self.vessel.reference_frame),
                'vessel_velocity': self.vessel.velocity(self.vessel.reference_frame),
                'vessel_orientation': {
                    'heading': self.flight.heading,
                    'pitch': self.flight.pitch,
                    'roll': self.flight.roll,
                }
            }
            
        elif mission_type == 'surface':
            # For surface operations, we need surface reference frame
            return {
                **base_data,
                'surface_position': self.vessel.position(self.vessel.surface_reference_frame),
                'surface_velocity': self.vessel.velocity(self.vessel.surface_reference_frame),
                'latitude': self.flight.latitude,
                'longitude': self.flight.longitude,
                'heading': self.flight.heading,
            }
            
        else:
            # Default: return all reference frame data
            return {
                **base_data,
                'all_reference_frames': self.get_reference_frame_data()
            }
    
    def close(self):
        """Close the kRPC connection."""
        if self.conn:
            self.conn.close()


# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the telemetry collector
    try:
        # Initialize collector
        collector = TelemetryCollector("AI_Agent_Test")
        
        # Set active vessel
        collector.set_vessel()
        
        # Get comprehensive telemetry
        print("Getting comprehensive telemetry...")
        telemetry = collector.get_comprehensive_telemetry()
        print(f"Collected {len(telemetry)} categories of data")
        
        # Get AI-optimized data
        print("\nGetting AI decision data...")
        ai_data = collector.get_ai_decision_data()
        print(f"AI data contains {len(ai_data)} key metrics")
        
        # Print some sample data
        print(f"\nVessel: {ai_data.get('name', 'Unknown')}")
        print(f"Situation: {ai_data.get('situation', 'Unknown')}")
        print(f"Altitude: {ai_data.get('altitude', 0):.1f}m")
        print(f"Speed: {ai_data.get('speed', 0):.1f}m/s")
        print(f"Throttle: {ai_data.get('throttle', 0):.2f}")
        
        # Demonstrate reference frame usage
        print("\nReference Frame Data:")
        print(f"Vessel Position: {ai_data.get('position_vessel', (0,0,0))}")
        print(f"Orbital Position: {ai_data.get('position_orbital', (0,0,0))}")
        print(f"Surface Position: {ai_data.get('position_surface', (0,0,0))}")
        
        # Demonstrate mission-specific reference frames
        print("\nMission-specific Reference Frames:")
        for mission_type in ['launch', 'orbital', 'landing', 'docking', 'surface']:
            mission_data = collector.get_reference_frame_for_mission(mission_type)
            print(f"{mission_type.capitalize()}: {len(mission_data)} data points")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Kerbal Space Program is running with kRPC mod installed")
    
    finally:
        if 'collector' in locals():
            collector.close()
