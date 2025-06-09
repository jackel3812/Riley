"""
RILEY - Physics Module

This module provides advanced physics calculations and simulations including:
- Classical mechanics
- Thermodynamics
- Electromagnetism
- Quantum physics
- Relativity
- Fluid dynamics
"""

import logging
import math
import numpy as np
import sympy as sp
from sympy import symbols, solve, integrate, diff, simplify
import matplotlib.pyplot as plt
from io import BytesIO
import base64

logger = logging.getLogger(__name__)

# Physical constants
GRAVITATIONAL_CONSTANT = 6.67430e-11  # N⋅m²/kg²
SPEED_OF_LIGHT = 299792458  # m/s
PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
ELEMENTARY_CHARGE = 1.602176634e-19  # C
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m
VACUUM_PERMEABILITY = 1.25663706212e-6  # H/m
ELECTRON_MASS = 9.1093837015e-31  # kg
PROTON_MASS = 1.67262192369e-27  # kg
NEUTRON_MASS = 1.67492749804e-27  # kg
AVOGADRO_NUMBER = 6.02214076e23  # mol⁻¹
UNIVERSAL_GAS_CONSTANT = 8.31446261815324  # J/(mol⋅K)
EARTH_GRAVITY = 9.80665  # m/s²
EARTH_MASS = 5.972e24  # kg
EARTH_RADIUS = 6.371e6  # m

class PhysicsEngine:
    """Advanced physics calculations and simulations engine."""
    
    def __init__(self):
        """Initialize the physics engine."""
        logger.info("Initializing Physics Engine")
        self.constants = {
            "G": GRAVITATIONAL_CONSTANT,
            "c": SPEED_OF_LIGHT,
            "h": PLANCK_CONSTANT,
            "k_B": BOLTZMANN_CONSTANT,
            "e": ELEMENTARY_CHARGE,
            "epsilon_0": VACUUM_PERMITTIVITY,
            "mu_0": VACUUM_PERMEABILITY,
            "m_e": ELECTRON_MASS,
            "m_p": PROTON_MASS,
            "m_n": NEUTRON_MASS,
            "N_A": AVOGADRO_NUMBER,
            "R": UNIVERSAL_GAS_CONSTANT,
            "g": EARTH_GRAVITY,
            "M_earth": EARTH_MASS,
            "R_earth": EARTH_RADIUS
        }
    
    # Classical Mechanics
    def calculate_projectile_motion(self, initial_velocity, launch_angle_degrees, initial_height=0):
        """Calculate projectile motion parameters.
        
        Args:
            initial_velocity: Initial velocity in m/s
            launch_angle_degrees: Launch angle in degrees
            initial_height: Initial height in meters (default: 0)
            
        Returns:
            Dictionary with projectile motion parameters
        """
        try:
            # Convert angle to radians
            launch_angle = math.radians(launch_angle_degrees)
            
            # Initial velocity components
            v0x = initial_velocity * math.cos(launch_angle)
            v0y = initial_velocity * math.sin(launch_angle)
            
            # Time of flight
            if initial_height == 0:
                time_of_flight = 2 * v0y / EARTH_GRAVITY
            else:
                # Quadratic formula for time when y = 0
                a = -0.5 * EARTH_GRAVITY
                b = v0y
                c = initial_height
                discriminant = b**2 - 4*a*c
                
                if discriminant < 0:
                    # Projectile never hits the ground
                    time_of_flight = None
                else:
                    # Take the positive solution
                    time_of_flight = (-b + math.sqrt(discriminant)) / (2*a)
            
            # Range (horizontal distance)
            if time_of_flight is not None:
                horizontal_range = v0x * time_of_flight
            else:
                horizontal_range = None
            
            # Maximum height
            max_height = initial_height + v0y**2 / (2 * EARTH_GRAVITY)
            
            # Time to reach maximum height
            time_to_max_height = v0y / EARTH_GRAVITY
            
            # Generate trajectory data for plotting
            if time_of_flight is not None:
                time_points = np.linspace(0, time_of_flight, 100)
            else:
                # If projectile never hits ground, use a reasonable time range
                time_points = np.linspace(0, 2 * time_to_max_height, 100)
            
            x_positions = v0x * time_points
            y_positions = initial_height + v0y * time_points - 0.5 * EARTH_GRAVITY * time_points**2
            
            # Create plot
            plt.figure(figsize=(10, 6))
            plt.plot(x_positions, y_positions)
            plt.title("Projectile Motion Trajectory")
            plt.xlabel("Distance (m)")
            plt.ylabel("Height (m)")
            plt.grid(True)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            
            # Mark important points
            plt.plot(0, initial_height, 'go', label="Launch Point")
            
            if time_of_flight is not None:
                plt.plot(horizontal_range, 0, 'ro', label="Landing Point")
            
            # Mark maximum height point
            max_height_x = v0x * time_to_max_height
            plt.plot(max_height_x, max_height, 'bo', label="Maximum Height")
            
            plt.legend()
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "initial_velocity": initial_velocity,
                "launch_angle_degrees": launch_angle_degrees,
                "initial_height": initial_height,
                "horizontal_range": horizontal_range,
                "max_height": max_height,
                "time_of_flight": time_of_flight,
                "time_to_max_height": time_to_max_height,
                "trajectory_plot": {
                    "data": plot_data,
                    "format": "base64_png"
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating projectile motion: {e}")
            return {"error": f"Could not calculate projectile motion: {e}"}
    
    def calculate_orbital_motion(self, central_mass, orbit_radius, orbital_type="circular"):
        """Calculate orbital motion parameters.
        
        Args:
            central_mass: Mass of the central body in kg
            orbit_radius: Orbit radius in meters
            orbital_type: Type of orbit (default: "circular")
            
        Returns:
            Dictionary with orbital motion parameters
        """
        try:
            # Calculate orbital velocity for circular orbit
            orbital_velocity = math.sqrt(GRAVITATIONAL_CONSTANT * central_mass / orbit_radius)
            
            # Calculate orbital period
            orbital_period = 2 * math.pi * orbit_radius / orbital_velocity
            
            # Calculate orbital energy
            orbital_energy = -GRAVITATIONAL_CONSTANT * central_mass / (2 * orbit_radius)
            
            # Calculate angular momentum per unit mass
            angular_momentum = orbital_velocity * orbit_radius
            
            # Escape velocity for comparison
            escape_velocity = math.sqrt(2 * GRAVITATIONAL_CONSTANT * central_mass / orbit_radius)
            
            return {
                "central_mass": central_mass,
                "orbit_radius": orbit_radius,
                "orbital_type": orbital_type,
                "orbital_velocity": orbital_velocity,
                "orbital_period": orbital_period,
                "orbital_energy": orbital_energy,
                "angular_momentum": angular_momentum,
                "escape_velocity": escape_velocity
            }
            
        except Exception as e:
            logger.error(f"Error calculating orbital motion: {e}")
            return {"error": f"Could not calculate orbital motion: {e}"}
    
    def analyze_simple_harmonic_motion(self, mass, spring_constant, initial_displacement, initial_velocity=0, damping_coefficient=0):
        """Analyze simple harmonic motion.
        
        Args:
            mass: Mass in kg
            spring_constant: Spring constant in N/m
            initial_displacement: Initial displacement in meters
            initial_velocity: Initial velocity in m/s (default: 0)
            damping_coefficient: Damping coefficient in kg/s (default: 0)
            
        Returns:
            Dictionary with simple harmonic motion analysis
        """
        try:
            # Natural angular frequency
            natural_frequency = math.sqrt(spring_constant / mass)
            
            # Damping ratio
            damping_ratio = damping_coefficient / (2 * mass * natural_frequency)
            
            # Damped angular frequency
            if damping_ratio < 1:  # Underdamped
                damped_frequency = natural_frequency * math.sqrt(1 - damping_ratio**2)
            else:
                damped_frequency = 0
            
            # Period
            if damped_frequency > 0:
                period = 2 * math.pi / damped_frequency
            else:
                period = float('inf')
            
            # Classification of damping
            if damping_ratio == 0:
                damping_type = "Undamped"
            elif damping_ratio < 1:
                damping_type = "Underdamped"
            elif damping_ratio == 1:
                damping_type = "Critically damped"
            else:
                damping_type = "Overdamped"
            
            # Generate motion data for plotting
            time_points = np.linspace(0, 10 * (2 * math.pi / natural_frequency) if period != float('inf') else 5 * (2 * math.pi / natural_frequency), 1000)
            displacements = []
            
            if damping_ratio == 0:  # Undamped
                for t in time_points:
                    x = initial_displacement * math.cos(natural_frequency * t) + (initial_velocity / natural_frequency) * math.sin(natural_frequency * t)
                    displacements.append(x)
            elif damping_ratio < 1:  # Underdamped
                for t in time_points:
                    exp_term = math.exp(-damping_ratio * natural_frequency * t)
                    cos_term = math.cos(damped_frequency * t)
                    sin_term = math.sin(damped_frequency * t)
                    
                    x = exp_term * (initial_displacement * cos_term + 
                                  ((initial_velocity + damping_ratio * natural_frequency * initial_displacement) / damped_frequency) * sin_term)
                    displacements.append(x)
            elif damping_ratio == 1:  # Critically damped
                for t in time_points:
                    x = (initial_displacement + (initial_velocity + natural_frequency * initial_displacement) * t) * math.exp(-natural_frequency * t)
                    displacements.append(x)
            else:  # Overdamped
                r1 = -natural_frequency * (damping_ratio + math.sqrt(damping_ratio**2 - 1))
                r2 = -natural_frequency * (damping_ratio - math.sqrt(damping_ratio**2 - 1))
                for t in time_points:
                    c1 = (initial_velocity - r2 * initial_displacement) / (r1 - r2)
                    c2 = (r1 * initial_displacement - initial_velocity) / (r1 - r2)
                    x = c1 * math.exp(r1 * t) + c2 * math.exp(r2 * t)
                    displacements.append(x)
            
            # Create plot
            plt.figure(figsize=(10, 6))
            plt.plot(time_points, displacements)
            plt.title(f"Simple Harmonic Motion - {damping_type}")
            plt.xlabel("Time (s)")
            plt.ylabel("Displacement (m)")
            plt.grid(True)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "mass": mass,
                "spring_constant": spring_constant,
                "initial_displacement": initial_displacement,
                "initial_velocity": initial_velocity,
                "damping_coefficient": damping_coefficient,
                "natural_frequency": natural_frequency,
                "damping_ratio": damping_ratio,
                "damped_frequency": damped_frequency,
                "period": period,
                "damping_type": damping_type,
                "motion_plot": {
                    "data": plot_data,
                    "format": "base64_png"
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing simple harmonic motion: {e}")
            return {"error": f"Could not analyze simple harmonic motion: {e}"}
    
    # Thermodynamics
    def calculate_thermodynamic_process(self, process_type, initial_state, final_value, parameter="volume"):
        """Calculate thermodynamic process parameters.
        
        Args:
            process_type: Type of thermodynamic process (isochoric, isobaric, isothermal, adiabatic)
            initial_state: Dictionary with initial P, V, T values
            final_value: Final value of the varying parameter
            parameter: Parameter being varied (volume, pressure, temperature) (default: "volume")
            
        Returns:
            Dictionary with thermodynamic process parameters
        """
        try:
            # Extract initial values
            initial_pressure = initial_state.get("pressure", 0)  # Pa
            initial_volume = initial_state.get("volume", 0)  # m³
            initial_temperature = initial_state.get("temperature", 0)  # K
            gas_constant = initial_state.get("gas_constant", UNIVERSAL_GAS_CONSTANT)  # J/(mol·K)
            moles = initial_state.get("moles", 1)  # mol
            gamma = initial_state.get("gamma", 1.4)  # Heat capacity ratio, default for diatomic gas
            
            # Calculate the missing initial value if not provided
            if initial_pressure == 0 and initial_volume != 0 and initial_temperature != 0:
                initial_pressure = moles * gas_constant * initial_temperature / initial_volume
            elif initial_volume == 0 and initial_pressure != 0 and initial_temperature != 0:
                initial_volume = moles * gas_constant * initial_temperature / initial_pressure
            elif initial_temperature == 0 and initial_pressure != 0 and initial_volume != 0:
                initial_temperature = initial_pressure * initial_volume / (moles * gas_constant)
            
            # Calculate final state based on process type
            final_state = {
                "pressure": initial_pressure,
                "volume": initial_volume,
                "temperature": initial_temperature
            }
            
            work_done = 0
            heat_transferred = 0
            change_in_internal_energy = 0
            
            if process_type.lower() == "isochoric":  # Constant volume
                final_state["volume"] = initial_volume
                
                if parameter.lower() == "pressure":
                    final_state["pressure"] = final_value
                    final_state["temperature"] = final_value * initial_volume / (moles * gas_constant)
                elif parameter.lower() == "temperature":
                    final_state["temperature"] = final_value
                    final_state["pressure"] = moles * gas_constant * final_value / initial_volume
                
                # Calculate energy changes
                work_done = 0  # No work in isochoric process
                change_in_internal_energy = (3/2) * moles * gas_constant * (final_state["temperature"] - initial_temperature)
                heat_transferred = change_in_internal_energy
                
            elif process_type.lower() == "isobaric":  # Constant pressure
                final_state["pressure"] = initial_pressure
                
                if parameter.lower() == "volume":
                    final_state["volume"] = final_value
                    final_state["temperature"] = final_value * initial_pressure / (moles * gas_constant)
                elif parameter.lower() == "temperature":
                    final_state["temperature"] = final_value
                    final_state["volume"] = moles * gas_constant * final_value / initial_pressure
                
                # Calculate energy changes
                work_done = initial_pressure * (final_state["volume"] - initial_volume)
                change_in_internal_energy = (3/2) * moles * gas_constant * (final_state["temperature"] - initial_temperature)
                heat_transferred = change_in_internal_energy + work_done
                
            elif process_type.lower() == "isothermal":  # Constant temperature
                final_state["temperature"] = initial_temperature
                
                if parameter.lower() == "volume":
                    final_state["volume"] = final_value
                    final_state["pressure"] = moles * gas_constant * initial_temperature / final_value
                elif parameter.lower() == "pressure":
                    final_state["pressure"] = final_value
                    final_state["volume"] = moles * gas_constant * initial_temperature / final_value
                
                # Calculate energy changes
                work_done = moles * gas_constant * initial_temperature * math.log(final_state["volume"] / initial_volume)
                change_in_internal_energy = 0  # No change in internal energy in isothermal process
                heat_transferred = work_done
                
            elif process_type.lower() == "adiabatic":  # No heat transfer
                if parameter.lower() == "volume":
                    final_state["volume"] = final_value
                    final_state["pressure"] = initial_pressure * (initial_volume / final_value)**gamma
                    final_state["temperature"] = initial_temperature * (initial_volume / final_value)**(gamma - 1)
                elif parameter.lower() == "pressure":
                    final_state["pressure"] = final_value
                    final_state["volume"] = initial_volume * (initial_pressure / final_value)**(1/gamma)
                    final_state["temperature"] = initial_temperature * (final_value / initial_pressure)**((gamma - 1)/gamma)
                elif parameter.lower() == "temperature":
                    final_state["temperature"] = final_value
                    final_state["volume"] = initial_volume * (initial_temperature / final_value)**(1/(gamma - 1))
                    final_state["pressure"] = initial_pressure * (initial_temperature / final_value)**(gamma/(gamma - 1))
                
                # Calculate energy changes
                work_done = (moles * gas_constant * (final_state["temperature"] - initial_temperature)) / (1 - gamma)
                change_in_internal_energy = (3/2) * moles * gas_constant * (final_state["temperature"] - initial_temperature)
                heat_transferred = 0  # No heat transfer in adiabatic process
            
            # Generate P-V diagram
            if process_type.lower() in ["isochoric", "isobaric", "isothermal", "adiabatic"]:
                if process_type.lower() == "isochoric":
                    # Constant volume line
                    volumes = [initial_volume] * 100
                    pressures = np.linspace(min(initial_pressure, final_state["pressure"]), 
                                           max(initial_pressure, final_state["pressure"]), 100)
                elif process_type.lower() == "isobaric":
                    # Constant pressure line
                    pressures = [initial_pressure] * 100
                    volumes = np.linspace(min(initial_volume, final_state["volume"]), 
                                         max(initial_volume, final_state["volume"]), 100)
                elif process_type.lower() == "isothermal":
                    # P*V = constant curve
                    volumes = np.linspace(min(initial_volume, final_state["volume"]), 
                                         max(initial_volume, final_state["volume"]), 100)
                    pressures = [moles * gas_constant * initial_temperature / v for v in volumes]
                elif process_type.lower() == "adiabatic":
                    # P*V^gamma = constant curve
                    volumes = np.linspace(min(initial_volume, final_state["volume"]), 
                                         max(initial_volume, final_state["volume"]), 100)
                    pressures = [initial_pressure * (initial_volume / v)**gamma for v in volumes]
                
                # Create plot
                plt.figure(figsize=(10, 6))
                plt.plot(volumes, pressures)
                plt.title(f"P-V Diagram for {process_type.capitalize()} Process")
                plt.xlabel("Volume (m³)")
                plt.ylabel("Pressure (Pa)")
                plt.grid(True)
                
                # Mark initial and final states
                plt.plot(initial_volume, initial_pressure, 'go', label="Initial State")
                plt.plot(final_state["volume"], final_state["pressure"], 'ro', label="Final State")
                plt.legend()
                
                # Save plot to base64 for display
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                buffer.seek(0)
                plot_data = base64.b64encode(buffer.read()).decode('utf-8')
                
                # Add plot to results
                diagram = {
                    "data": plot_data,
                    "format": "base64_png"
                }
            else:
                diagram = None
            
            return {
                "process_type": process_type,
                "initial_state": {
                    "pressure": initial_pressure,
                    "volume": initial_volume,
                    "temperature": initial_temperature
                },
                "final_state": final_state,
                "work_done": work_done,  # Joules
                "heat_transferred": heat_transferred,  # Joules
                "change_in_internal_energy": change_in_internal_energy,  # Joules
                "pv_diagram": diagram
            }
            
        except Exception as e:
            logger.error(f"Error calculating thermodynamic process: {e}")
            return {"error": f"Could not calculate thermodynamic process: {e}"}
    
    def analyze_heat_engine(self, hot_reservoir_temp, cold_reservoir_temp, engine_type="carnot"):
        """Analyze heat engine efficiency and performance.
        
        Args:
            hot_reservoir_temp: Hot reservoir temperature in Kelvin
            cold_reservoir_temp: Cold reservoir temperature in Kelvin
            engine_type: Type of heat engine (default: "carnot")
            
        Returns:
            Dictionary with heat engine analysis
        """
        try:
            # Calculate maximum (Carnot) efficiency
            carnot_efficiency = 1 - (cold_reservoir_temp / hot_reservoir_temp)
            
            # Calculate actual efficiency based on engine type
            if engine_type.lower() == "carnot":
                actual_efficiency = carnot_efficiency
                engine_name = "Carnot Engine"
            elif engine_type.lower() == "otto":
                # Otto cycle (gasoline engine) - need compression ratio
                compression_ratio = 8  # Typical value
                specific_heat_ratio = 1.4  # For diatomic gas
                actual_efficiency = 1 - (1 / (compression_ratio**(specific_heat_ratio - 1)))
                engine_name = "Otto Cycle Engine (Gasoline)"
            elif engine_type.lower() == "diesel":
                # Diesel cycle - need compression ratio and cutoff ratio
                compression_ratio = 18  # Typical value
                cutoff_ratio = 2  # Typical value
                specific_heat_ratio = 1.4  # For diatomic gas
                actual_efficiency = 1 - (1 / (compression_ratio**(specific_heat_ratio - 1))) * (
                    (cutoff_ratio**specific_heat_ratio - 1) / 
                    (specific_heat_ratio * (cutoff_ratio - 1))
                )
                engine_name = "Diesel Cycle Engine"
            elif engine_type.lower() == "brayton":
                # Brayton cycle (gas turbine) - need pressure ratio
                pressure_ratio = 10  # Typical value
                specific_heat_ratio = 1.4  # For diatomic gas
                actual_efficiency = 1 - (1 / (pressure_ratio**((specific_heat_ratio - 1) / specific_heat_ratio)))
                engine_name = "Brayton Cycle Engine (Gas Turbine)"
            elif engine_type.lower() == "rankine":
                # Rankine cycle (steam turbine) - simplified approximation
                actual_efficiency = 0.6 * carnot_efficiency  # Rough approximation
                engine_name = "Rankine Cycle Engine (Steam Turbine)"
            else:
                actual_efficiency = 0.7 * carnot_efficiency  # Generic approximation
                engine_name = "Generic Heat Engine"
            
            # For 1 J of work output, calculate heat input required
            work_output = 1  # J
            heat_input = work_output / actual_efficiency  # J
            heat_rejected = heat_input - work_output  # J
            
            # Calculate power output for 1 kg/s of working fluid (rough approximation)
            specific_heat = 1000  # J/(kg·K) (approximation)
            mass_flow_rate = 1  # kg/s
            power_output = mass_flow_rate * specific_heat * (hot_reservoir_temp - cold_reservoir_temp) * actual_efficiency  # W
            
            return {
                "engine_type": engine_type,
                "engine_name": engine_name,
                "hot_reservoir_temp": hot_reservoir_temp,
                "cold_reservoir_temp": cold_reservoir_temp,
                "carnot_efficiency": carnot_efficiency,
                "actual_efficiency": actual_efficiency,
                "work_output_per_heat_input": actual_efficiency,  # J/J
                "heat_input_for_unit_work": heat_input,  # J
                "heat_rejected_for_unit_work": heat_rejected,  # J
                "approximate_power_output": power_output  # W
            }
            
        except Exception as e:
            logger.error(f"Error analyzing heat engine: {e}")
            return {"error": f"Could not analyze heat engine: {e}"}
    
    # Electromagnetism
    def calculate_electric_field(self, charge_configuration, point):
        """Calculate electric field at a point due to a configuration of charges.
        
        Args:
            charge_configuration: List of dictionaries with charge and position
            point: Position where to calculate the field
            
        Returns:
            Dictionary with electric field information
        """
        try:
            # Initialize electric field components
            E_x, E_y, E_z = 0, 0, 0
            
            # Calculate contribution from each charge
            for charge in charge_configuration:
                q = charge.get("charge", 0)  # Coulombs
                pos = charge.get("position", [0, 0, 0])  # [x, y, z] in meters
                
                # Vector from charge to point
                r_x = point[0] - pos[0]
                r_y = point[1] - pos[1]
                r_z = point[2] - pos[2]
                
                # Distance from charge to point
                r = math.sqrt(r_x**2 + r_y**2 + r_z**2)
                
                if r > 0:  # Avoid division by zero
                    # Calculate electric field contribution (Coulomb's law)
                    k = 1 / (4 * math.pi * VACUUM_PERMITTIVITY)
                    E_magnitude = k * q / r**2
                    
                    # Electric field components
                    E_x += E_magnitude * r_x / r
                    E_y += E_magnitude * r_y / r
                    E_z += E_magnitude * r_z / r
            
            # Calculate total electric field magnitude
            E_magnitude = math.sqrt(E_x**2 + E_y**2 + E_z**2)
            
            return {
                "point": point,
                "electric_field": {
                    "x": E_x,
                    "y": E_y,
                    "z": E_z,
                    "magnitude": E_magnitude
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating electric field: {e}")
            return {"error": f"Could not calculate electric field: {e}"}
    
    def calculate_magnetic_field(self, current_configuration, point):
        """Calculate magnetic field at a point due to a configuration of currents.
        
        Args:
            current_configuration: List of dictionaries with current and path
            point: Position where to calculate the field
            
        Returns:
            Dictionary with magnetic field information
        """
        try:
            # Initialize magnetic field components
            B_x, B_y, B_z = 0, 0, 0
            
            # Calculate contribution from each current element
            for current_element in current_configuration:
                current_type = current_element.get("type", "straight_wire")
                current = current_element.get("current", 0)  # Amperes
                
                if current_type == "straight_wire":
                    # Straight wire segment
                    start = current_element.get("start", [0, 0, 0])  # [x, y, z] in meters
                    end = current_element.get("end", [0, 0, 1])  # [x, y, z] in meters
                    
                    # Calculate magnetic field using Biot-Savart law for a straight wire segment
                    # Vector along the wire
                    dl_x = end[0] - start[0]
                    dl_y = end[1] - start[1]
                    dl_z = end[2] - start[2]
                    wire_length = math.sqrt(dl_x**2 + dl_y**2 + dl_z**2)
                    
                    # Unit vector along the wire
                    dl_x /= wire_length
                    dl_y /= wire_length
                    dl_z /= wire_length
                    
                    # Minimum distance from point to wire
                    # First, find parameter t for the closest point on the line
                    t = ((point[0] - start[0]) * dl_x + 
                         (point[1] - start[1]) * dl_y + 
                         (point[2] - start[2]) * dl_z)
                    
                    # Clamp t to wire segment
                    t = max(0, min(wire_length, t))
                    
                    # Closest point on the wire
                    closest_x = start[0] + t * dl_x
                    closest_y = start[1] + t * dl_y
                    closest_z = start[2] + t * dl_z
                    
                    # Distance from point to closest point on wire
                    r_x = point[0] - closest_x
                    r_y = point[1] - closest_y
                    r_z = point[2] - closest_z
                    r = math.sqrt(r_x**2 + r_y**2 + r_z**2)
                    
                    if r > 0:  # Avoid division by zero
                        # Calculate B-field using Biot-Savart law approximation
                        mu_0 = VACUUM_PERMEABILITY
                        B_magnitude = (mu_0 * current) / (2 * math.pi * r)
                        
                        # Cross product of dl and r
                        cross_x = dl_y * r_z - dl_z * r_y
                        cross_y = dl_z * r_x - dl_x * r_z
                        cross_z = dl_x * r_y - dl_y * r_x
                        
                        # Normalize the cross product
                        cross_magnitude = math.sqrt(cross_x**2 + cross_y**2 + cross_z**2)
                        if cross_magnitude > 0:
                            cross_x /= cross_magnitude
                            cross_y /= cross_magnitude
                            cross_z /= cross_magnitude
                            
                            # Magnetic field components
                            B_x += B_magnitude * cross_x
                            B_y += B_magnitude * cross_y
                            B_z += B_magnitude * cross_z
                
                elif current_type == "circular_loop":
                    # Circular current loop
                    center = current_element.get("center", [0, 0, 0])  # [x, y, z] in meters
                    radius = current_element.get("radius", 1)  # meters
                    normal = current_element.get("normal", [0, 0, 1])  # Direction of loop's normal
                    
                    # Normalize the normal vector
                    normal_magnitude = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
                    if normal_magnitude > 0:
                        normal = [normal[0]/normal_magnitude, normal[1]/normal_magnitude, normal[2]/normal_magnitude]
                    
                    # Relative position from loop center to point
                    r_x = point[0] - center[0]
                    r_y = point[1] - center[1]
                    r_z = point[2] - center[2]
                    
                    # Distance from center
                    r = math.sqrt(r_x**2 + r_y**2 + r_z**2)
                    
                    # Projection along normal axis
                    z = r_x * normal[0] + r_y * normal[1] + r_z * normal[2]
                    
                    # Radial distance in plane of loop
                    rho = math.sqrt(r**2 - z**2)
                    
                    # Calculate magnetic field - only valid on the axis of the loop
                    if abs(rho) < 1e-10:  # Point is on the axis
                        mu_0 = VACUUM_PERMEABILITY
                        # Magnetic field magnitude on axis of loop
                        B_magnitude = (mu_0 * current * radius**2) / (2 * (radius**2 + z**2)**(3/2))
                        
                        # Field points along the normal direction
                        B_x += B_magnitude * normal[0]
                        B_y += B_magnitude * normal[1]
                        B_z += B_magnitude * normal[2]
                    else:
                        # Off-axis calculation requires elliptic integrals
                        # Simplified approximation used here
                        mu_0 = VACUUM_PERMEABILITY
                        
                        # Approximate radial and axial components
                        k = math.sqrt(4 * radius * rho / ((radius + rho)**2 + z**2))
                        
                        # First degree elliptic integral approximation
                        K = math.pi/2 * (1 + k**2/4 + 9*k**4/64)
                        
                        # Second degree elliptic integral approximation
                        E = math.pi/2 * (1 - k**2/4 - 3*k**4/64)
                        
                        # Prefactor
                        prefactor = mu_0 * current / (2 * math.pi * math.sqrt((radius + rho)**2 + z**2))
                        
                        # Radial and axial components
                        B_z_component = prefactor * (K + E * (radius**2 - rho**2 - z**2) / ((radius - rho)**2 + z**2))
                        B_rho_component = prefactor * z / rho * (E * (radius**2 + rho**2 + z**2) / ((radius - rho)**2 + z**2) - K)
                        
                        # Now need to convert back to Cartesian coordinates
                        # First get unit vector in rho direction
                        r_in_plane = [r_x - z*normal[0], r_y - z*normal[1], r_z - z*normal[2]]
                        rho_magnitude = math.sqrt(sum(x**2 for x in r_in_plane))
                        
                        if rho_magnitude > 0:
                            rho_unit = [x/rho_magnitude for x in r_in_plane]
                            
                            # Now add contributions
                            B_x += B_z_component * normal[0] + B_rho_component * rho_unit[0]
                            B_y += B_z_component * normal[1] + B_rho_component * rho_unit[1]
                            B_z += B_z_component * normal[2] + B_rho_component * rho_unit[2]
                
                elif current_type == "solenoid":
                    # Solenoid (long coil)
                    center = current_element.get("center", [0, 0, 0])  # [x, y, z] in meters
                    radius = current_element.get("radius", 0.1)  # meters
                    length = current_element.get("length", 1)  # meters
                    turns = current_element.get("turns", 100)  # number of turns
                    axis = current_element.get("axis", [0, 0, 1])  # Direction of solenoid axis
                    
                    # Normalize the axis vector
                    axis_magnitude = math.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)
                    if axis_magnitude > 0:
                        axis = [axis[0]/axis_magnitude, axis[1]/axis_magnitude, axis[2]/axis_magnitude]
                    
                    # Relative position from solenoid center to point
                    r_x = point[0] - center[0]
                    r_y = point[1] - center[1]
                    r_z = point[2] - center[2]
                    
                    # Projection along solenoid axis
                    z = r_x * axis[0] + r_y * axis[1] + r_z * axis[2]
                    
                    # Vector from axis to point
                    r_perp = [r_x - z * axis[0], r_y - z * axis[1], r_z - z * axis[2]]
                    rho = math.sqrt(sum(x**2 for x in r_perp))
                    
                    # Calculate magnetic field
                    mu_0 = VACUUM_PERMEABILITY
                    n = turns / length  # Turns per unit length
                    
                    if abs(z) > length/2:
                        # Point is outside the solenoid along axis
                        # Magnetic field falls off rapidly
                        # Very rough approximation
                        B_magnitude = 0.1 * mu_0 * n * current * (length/2) / abs(z)
                    elif rho < radius:
                        # Point is inside the solenoid
                        B_magnitude = mu_0 * n * current
                    else:
                        # Point is outside the solenoid radially
                        # Field drops off approximately as 1/r²
                        B_magnitude = mu_0 * n * current * (radius / rho)**2
                    
                    # Field is along the axis direction
                    B_x += B_magnitude * axis[0]
                    B_y += B_magnitude * axis[1]
                    B_z += B_magnitude * axis[2]
            
            # Calculate total magnetic field magnitude
            B_magnitude = math.sqrt(B_x**2 + B_y**2 + B_z**2)
            
            return {
                "point": point,
                "magnetic_field": {
                    "x": B_x,
                    "y": B_y,
                    "z": B_z,
                    "magnitude": B_magnitude
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating magnetic field: {e}")
            return {"error": f"Could not calculate magnetic field: {e}"}
    
    def analyze_circuit(self, circuit_elements):
        """Analyze a simple electrical circuit.
        
        Args:
            circuit_elements: List of dictionaries with circuit elements
            
        Returns:
            Dictionary with circuit analysis
        """
        try:
            # Extract circuit parameters
            voltage_sources = []
            resistors = []
            capacitors = []
            inductors = []
            
            for element in circuit_elements:
                element_type = element.get("type", "")
                value = element.get("value", 0)
                
                if element_type.lower() == "voltage_source":
                    voltage_sources.append(value)  # Volts
                elif element_type.lower() == "resistor":
                    resistors.append(value)  # Ohms
                elif element_type.lower() == "capacitor":
                    capacitors.append(value)  # Farads
                elif element_type.lower() == "inductor":
                    inductors.append(value)  # Henries
            
            # Simple series circuit analysis
            # Total voltage
            total_voltage = sum(voltage_sources)
            
            # Total resistance
            total_resistance = sum(resistors)
            
            # Total current
            if total_resistance > 0:
                total_current = total_voltage / total_resistance
            else:
                total_current = float('inf')
            
            # Power dissipated
            power_dissipated = total_voltage * total_current
            
            # Voltage across each resistor
            resistor_voltages = [total_current * r for r in resistors]
            
            # Time constant for RC circuit
            if resistors and capacitors:
                rc_time_constant = total_resistance * sum(capacitors)
            else:
                rc_time_constant = None
            
            # Time constant for RL circuit
            if resistors and inductors:
                rl_time_constant = sum(inductors) / total_resistance
            else:
                rl_time_constant = None
            
            # Resonant frequency for RLC circuit
            if capacitors and inductors:
                resonant_frequency = 1 / (2 * math.pi * math.sqrt(sum(inductors) * sum(capacitors)))
            else:
                resonant_frequency = None
            
            return {
                "circuit_type": "Series Circuit",
                "total_voltage": total_voltage,
                "total_resistance": total_resistance,
                "total_current": total_current,
                "power_dissipated": power_dissipated,
                "resistor_voltages": resistor_voltages,
                "rc_time_constant": rc_time_constant,
                "rl_time_constant": rl_time_constant,
                "resonant_frequency": resonant_frequency
            }
            
        except Exception as e:
            logger.error(f"Error analyzing circuit: {e}")
            return {"error": f"Could not analyze circuit: {e}"}
    
    # Quantum Physics
    def quantum_particle_in_box(self, box_length, energy_levels=5):
        """Calculate energy levels and wavefunctions for a particle in a box.
        
        Args:
            box_length: Length of the box in meters
            energy_levels: Number of energy levels to calculate (default: 5)
            
        Returns:
            Dictionary with quantum particle in a box analysis
        """
        try:
            # Planck's constant
            h = PLANCK_CONSTANT
            h_bar = h / (2 * math.pi)
            
            # Particle mass (electron mass)
            m = ELECTRON_MASS
            
            # Calculate energy levels
            energies = []
            for n in range(1, energy_levels + 1):
                # E_n = (n²π²ħ²)/(2mL²)
                energy = (n**2 * math.pi**2 * h_bar**2) / (2 * m * box_length**2)
                energies.append({
                    "level": n,
                    "energy": energy,  # Joules
                    "energy_ev": energy / ELEMENTARY_CHARGE  # eV
                })
            
            # Generate wavefunction data for plotting
            x_points = np.linspace(0, box_length, 100)
            wavefunctions = []
            
            for n in range(1, energy_levels + 1):
                # ψ_n(x) = sqrt(2/L) * sin(nπx/L)
                amplitude = math.sqrt(2 / box_length)
                psi_values = [amplitude * math.sin(n * math.pi * x / box_length) for x in x_points]
                
                wavefunctions.append({
                    "level": n,
                    "x_values": x_points.tolist(),
                    "psi_values": psi_values
                })
            
            # Create plot
            plt.figure(figsize=(12, 8))
            
            # Plot wavefunctions
            for n in range(min(energy_levels, 5)):  # Only plot the first 5 for clarity
                level_data = wavefunctions[n]
                energy_val = energies[n]["energy_ev"]
                
                # Scale and shift the wavefunction for visualization
                scaled_psi = np.array(level_data["psi_values"]) + energy_val
                
                plt.plot(level_data["x_values"], scaled_psi, label=f"n={n+1}")
                
                # Draw the energy level line
                plt.hlines(y=energy_val, xmin=0, xmax=box_length, linestyles='dashed', alpha=0.5)
            
            plt.title("Particle in a Box: Energy Levels and Wavefunctions")
            plt.xlabel("Position (m)")
            plt.ylabel("Energy (eV) / Wavefunction (scaled)")
            plt.grid(True)
            plt.legend()
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "box_length": box_length,
                "particle_mass": m,
                "energy_levels": energies,
                "wavefunctions": wavefunctions,
                "plot": {
                    "data": plot_data,
                    "format": "base64_png"
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating quantum particle in a box: {e}")
            return {"error": f"Could not calculate quantum particle in a box: {e}"}
    
    def hydrogen_atom_energies(self, principal_quantum_numbers=None):
        """Calculate hydrogen atom energy levels and properties.
        
        Args:
            principal_quantum_numbers: List of principal quantum numbers to analyze
            
        Returns:
            Dictionary with hydrogen atom energy levels
        """
        try:
            # If quantum numbers not specified, use 1-5
            if principal_quantum_numbers is None:
                principal_quantum_numbers = list(range(1, 6))
            
            # Constants
            h = PLANCK_CONSTANT
            h_bar = h / (2 * math.pi)
            m_e = ELECTRON_MASS
            e = ELEMENTARY_CHARGE
            epsilon_0 = VACUUM_PERMITTIVITY
            alpha = e**2 / (4 * math.pi * epsilon_0 * h_bar * SPEED_OF_LIGHT)  # Fine structure constant
            
            # Rydberg energy
            rydberg_energy = m_e * e**4 / (8 * epsilon_0**2 * h**2)  # Joules
            rydberg_energy_ev = rydberg_energy / e  # eV
            
            # Bohr radius
            a_0 = 4 * math.pi * epsilon_0 * h_bar**2 / (m_e * e**2)  # meters
            
            # Calculate energy levels
            energy_levels = []
            for n in principal_quantum_numbers:
                # Energy: E_n = -R/n²
                energy = -rydberg_energy / n**2  # Joules
                energy_ev = energy / e  # eV
                
                # Orbital radius: r_n = n²a₀
                orbital_radius = n**2 * a_0  # meters
                
                # Possible l values (angular momentum)
                l_values = list(range(n))
                
                # Count of states in this energy level
                state_count = sum(2 * (2 * l + 1) for l in l_values)
                
                energy_levels.append({
                    "principal_quantum_number": n,
                    "energy": energy,  # Joules
                    "energy_ev": energy_ev,  # eV
                    "orbital_radius": orbital_radius,  # meters
                    "allowed_l_values": l_values,
                    "state_count": state_count
                })
            
            # Create energy level diagram
            plt.figure(figsize=(10, 8))
            
            # Plot energy levels
            for level in energy_levels:
                n = level["principal_quantum_number"]
                energy_ev = level["energy_ev"]
                
                # Draw energy level line
                plt.hlines(y=energy_ev, xmin=0.2, xmax=0.8, linewidth=2)
                
                # Label the energy level
                plt.text(0.85, energy_ev, f"n={n}", verticalalignment='center')
                plt.text(0.1, energy_ev, f"{energy_ev:.2f} eV", verticalalignment='center')
            
            plt.title("Hydrogen Atom Energy Levels")
            plt.ylabel("Energy (eV)")
            plt.grid(True, axis='y')
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.xlim(0, 1)
            plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "rydberg_energy": rydberg_energy,  # Joules
                "rydberg_energy_ev": rydberg_energy_ev,  # eV
                "bohr_radius": a_0,  # meters
                "fine_structure_constant": alpha,  # dimensionless
                "energy_levels": energy_levels,
                "energy_level_diagram": {
                    "data": plot_data,
                    "format": "base64_png"
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating hydrogen atom energies: {e}")
            return {"error": f"Could not calculate hydrogen atom energies: {e}"}
    
    def quantum_tunneling(self, barrier_height_ev, barrier_width, particle_energy_ev):
        """Calculate quantum tunneling probability.
        
        Args:
            barrier_height_ev: Height of potential barrier in eV
            barrier_width: Width of potential barrier in meters
            particle_energy_ev: Energy of particle in eV
            
        Returns:
            Dictionary with quantum tunneling analysis
        """
        try:
            # Convert energies to Joules
            barrier_height = barrier_height_ev * ELEMENTARY_CHARGE  # J
            particle_energy = particle_energy_ev * ELEMENTARY_CHARGE  # J
            
            # Check if energy is less than barrier height (tunneling condition)
            if particle_energy >= barrier_height:
                tunneling_probability = 1.0
                tunneling_mode = "Above barrier"
            else:
                # Planck's constant
                h = PLANCK_CONSTANT
                h_bar = h / (2 * math.pi)
                
                # Particle mass (electron mass)
                m = ELECTRON_MASS
                
                # Wave number inside barrier
                k = math.sqrt(2 * m * (barrier_height - particle_energy)) / h_bar
                
                # Tunneling probability (simplified WKB approximation)
                exponent = -2 * k * barrier_width
                tunneling_probability = math.exp(exponent)
                tunneling_mode = "Tunneling"
            
            # Generate tunneling probability vs. energy data
            energy_range = np.linspace(0.2 * barrier_height_ev, 1.5 * barrier_height_ev, 100)
            probability_values = []
            
            for E in energy_range:
                E_joules = E * ELEMENTARY_CHARGE
                
                if E_joules >= barrier_height:
                    probability_values.append(1.0)
                else:
                    k = math.sqrt(2 * ELECTRON_MASS * (barrier_height - E_joules)) / (h_bar)
                    prob = math.exp(-2 * k * barrier_width)
                    probability_values.append(prob)
            
            # Create plot
            plt.figure(figsize=(10, 6))
            plt.semilogy(energy_range, probability_values)
            plt.axvline(x=barrier_height_ev, color='r', linestyle='--', label="Barrier Height")
            plt.axvline(x=particle_energy_ev, color='g', linestyle='--', label="Particle Energy")
            
            plt.title("Quantum Tunneling Probability vs. Energy")
            plt.xlabel("Energy (eV)")
            plt.ylabel("Tunneling Probability")
            plt.grid(True)
            plt.legend()
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            # Plot potential barrier and wavefunction
            plt.figure(figsize=(10, 6))
            
            # Define x range (distance)
            x_range = np.linspace(-2e-9, 4e-9, 1000)  # in meters
            barrier_start = 0
            barrier_end = barrier_width
            
            # Define potential
            potential = np.zeros_like(x_range)
            potential[(x_range >= barrier_start) & (x_range <= barrier_end)] = barrier_height_ev
            
            # Plot potential barrier
            plt.plot(x_range * 1e9, potential, 'k-', label="Potential")
            
            # Plot particle energy
            plt.axhline(y=particle_energy_ev, color='g', linestyle='--', label="Particle Energy")
            
            # Simulate wavefunction (very simplified)
            k1 = math.sqrt(2 * ELECTRON_MASS * particle_energy) / h_bar  # Wave number outside barrier
            
            wavefunction = np.zeros_like(x_range)
            for i, x in enumerate(x_range):
                if x < barrier_start:
                    # Incoming and reflected waves
                    wavefunction[i] = math.cos(k1 * x) + 0.2 * particle_energy_ev * math.sin(k1 * (2*barrier_start - x))
                elif x > barrier_end:
                    # Transmitted wave (scaled by transmission amplitude)
                    wavefunction[i] = math.sqrt(tunneling_probability) * math.cos(k1 * (x - barrier_width))
                else:
                    # Inside barrier (exponentially decaying)
                    if particle_energy < barrier_height:
                        k2 = math.sqrt(2 * ELECTRON_MASS * (barrier_height - particle_energy)) / h_bar
                        amplitude = math.exp(-k2 * (x - barrier_start))
                    else:
                        k2 = math.sqrt(2 * ELECTRON_MASS * (particle_energy - barrier_height)) / h_bar
                        amplitude = 0.4 * math.cos(k2 * (x - barrier_start))
                    
                    wavefunction[i] = amplitude
            
            # Scale and shift wavefunction for visualization
            wavefunction = 0.2 * particle_energy_ev * wavefunction + 0.3 * particle_energy_ev
            
            # Plot wavefunction
            plt.plot(x_range * 1e9, wavefunction, 'b-', label="Wavefunction (schematic)")
            
            plt.title("Quantum Tunneling: Potential Barrier and Wavefunction")
            plt.xlabel("Position (nm)")
            plt.ylabel("Energy (eV)")
            plt.grid(True)
            plt.legend()
            
            # Save wavefunction plot to base64
            buffer2 = BytesIO()
            plt.savefig(buffer2, format='png')
            plt.close()
            buffer2.seek(0)
            wavefunction_plot_data = base64.b64encode(buffer2.read()).decode('utf-8')
            
            return {
                "barrier_height_ev": barrier_height_ev,
                "barrier_width": barrier_width,
                "particle_energy_ev": particle_energy_ev,
                "tunneling_probability": tunneling_probability,
                "tunneling_mode": tunneling_mode,
                "probability_plot": {
                    "data": plot_data,
                    "format": "base64_png"
                },
                "wavefunction_plot": {
                    "data": wavefunction_plot_data,
                    "format": "base64_png"
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating quantum tunneling: {e}")
            return {"error": f"Could not calculate quantum tunneling: {e}"}
    
    # Relativity
    def relativistic_effects(self, velocity, mass_rest=ELECTRON_MASS, distance=None):
        """Calculate relativistic effects at a given velocity.
        
        Args:
            velocity: Velocity in m/s
            mass_rest: Rest mass in kg (default: electron mass)
            distance: Distance for length contraction calculation (optional)
            
        Returns:
            Dictionary with relativistic effects
        """
        try:
            # Speed of light
            c = SPEED_OF_LIGHT
            
            # Velocity as fraction of c
            beta = velocity / c
            
            if abs(beta) >= 1:
                return {
                    "error": "Velocity must be less than the speed of light"
                }
            
            # Lorentz factor
            gamma = 1 / math.sqrt(1 - beta**2)
            
            # Time dilation
            # If t_0 is 1 second in rest frame
            t_0 = 1  # s
            t_dilated = gamma * t_0  # s
            
            # Mass increase
            mass_relativistic = gamma * mass_rest  # kg
            
            # Length contraction
            if distance is not None:
                length_contracted = distance / gamma  # m
            else:
                length_contracted = None
            
            # Relativistic energy
            energy_rest = mass_rest * c**2  # J
            energy_relativistic = mass_relativistic * c**2  # J
            energy_kinetic = energy_relativistic - energy_rest  # J
            
            # Convert energies to more convenient units
            energy_rest_ev = energy_rest / ELEMENTARY_CHARGE  # eV
            energy_relativistic_ev = energy_relativistic / ELEMENTARY_CHARGE  # eV
            energy_kinetic_ev = energy_kinetic / ELEMENTARY_CHARGE  # eV
            
            # For MeV scale
            if energy_rest_ev > 1e6:
                energy_rest_mev = energy_rest_ev / 1e6
                energy_relativistic_mev = energy_relativistic_ev / 1e6
                energy_kinetic_mev = energy_kinetic_ev / 1e6
                energy_unit = "MeV"
                rest_energy = energy_rest_mev
                total_energy = energy_relativistic_mev
                kinetic_energy = energy_kinetic_mev
            else:
                energy_unit = "eV"
                rest_energy = energy_rest_ev
                total_energy = energy_relativistic_ev
                kinetic_energy = energy_kinetic_ev
            
            # Generate plot data for various relativistic effects vs. velocity
            beta_range = np.linspace(0, 0.9999, 100)
            gamma_values = [1 / math.sqrt(1 - b**2) for b in beta_range]
            
            # Create plot
            plt.figure(figsize=(10, 6))
            
            # Plot gamma factor
            plt.plot(beta_range, gamma_values, 'b-', label="Lorentz Factor (γ)")
            
            # Mark the current velocity
            plt.axvline(x=beta, color='r', linestyle='--', label=f"v = {beta:.4f}c")
            current_gamma = 1 / math.sqrt(1 - beta**2)
            plt.plot(beta, current_gamma, 'ro')
            
            plt.title("Relativistic Effects vs. Velocity")
            plt.xlabel("Velocity (fraction of c)")
            plt.ylabel("Lorentz Factor (γ)")
            plt.grid(True)
            plt.legend()
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "velocity": velocity,  # m/s
                "velocity_fraction_c": beta,  # dimensionless
                "lorentz_factor": gamma,  # dimensionless
                "time_dilation": {
                    "t_0": t_0,  # s
                    "t_dilated": t_dilated  # s
                },
                "mass": {
                    "rest_mass": mass_rest,  # kg
                    "relativistic_mass": mass_relativistic  # kg
                },
                "length_contraction": length_contracted,  # m (if distance provided)
                "energy": {
                    "rest_energy": rest_energy,  # In specified units
                    "relativistic_energy": total_energy,  # In specified units
                    "kinetic_energy": kinetic_energy,  # In specified units
                    "unit": energy_unit
                },
                "plot": {
                    "data": plot_data,
                    "format": "base64_png"
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating relativistic effects: {e}")
            return {"error": f"Could not calculate relativistic effects: {e}"}
    
    def gravitational_time_dilation(self, radius, mass=EARTH_MASS):
        """Calculate gravitational time dilation at a given radius from a massive object.
        
        Args:
            radius: Distance from center of mass (m)
            mass: Mass of the object (kg) (default: Earth mass)
            
        Returns:
            Dictionary with gravitational time dilation
        """
        try:
            # Gravitational constant
            G = GRAVITATIONAL_CONSTANT
            
            # Speed of light
            c = SPEED_OF_LIGHT
            
            # Schwarzschild radius
            r_s = 2 * G * mass / c**2
            
            # Check if radius is greater than Schwarzschild radius
            if radius <= r_s:
                return {
                    "error": "Radius must be greater than the Schwarzschild radius (event horizon)"
                }
            
            # Time dilation factor
            time_dilation_factor = 1 / math.sqrt(1 - r_s / radius)
            
            # If t_0 is 1 second in flat spacetime
            t_0 = 1  # s
            t_dilated = time_dilation_factor * t_0  # s
            
            # Calculate time dilation for various scenarios
            time_dilation_gps = 1 / math.sqrt(1 - r_s / (EARTH_RADIUS + 20200000))  # GPS satellites (~20,200 km)
            time_dilation_iss = 1 / math.sqrt(1 - r_s / (EARTH_RADIUS + 408000))  # ISS (~408 km)
            
            # Generate plot data for time dilation vs. distance
            if mass == EARTH_MASS:
                # For Earth, plot from surface to high orbit
                r_values = np.linspace(EARTH_RADIUS, EARTH_RADIUS + 40000000, 100)  # From Earth surface to ~40,000 km
                label_x = "Height above Earth (km)"
                x_values = [(r - EARTH_RADIUS) / 1000 for r in r_values]  # Convert to km above surface
            else:
                # For other masses, plot from just outside event horizon
                r_values = np.linspace(r_s * 1.01, r_s * 10, 100)
                label_x = "Distance from center (Schwarzschild radii)"
                x_values = [r / r_s for r in r_values]
            
            dilation_values = [1 / math.sqrt(1 - r_s / r) for r in r_values]
            
            # Create plot
            plt.figure(figsize=(10, 6))
            plt.plot(x_values, dilation_values)
            
            # Mark the current radius
            if mass == EARTH_MASS:
                x_current = (radius - EARTH_RADIUS) / 1000  # km above surface
            else:
                x_current = radius / r_s  # Schwarzschild radii
            
            plt.axvline(x=x_current, color='r', linestyle='--', label=f"r = {x_current:.2f}")
            plt.plot(x_current, time_dilation_factor, 'ro')
            
            plt.title("Gravitational Time Dilation vs. Distance")
            plt.xlabel(label_x)
            plt.ylabel("Time Dilation Factor")
            plt.grid(True)
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            return {
                "mass": mass,  # kg
                "radius": radius,  # m
                "schwarzschild_radius": r_s,  # m
                "time_dilation_factor": time_dilation_factor,  # dimensionless
                "time_dilation": {
                    "t_0": t_0,  # s
                    "t_dilated": t_dilated  # s
                },
                "references": {
                    "gps_satellites": time_dilation_gps,  # dimensionless
                    "iss": time_dilation_iss  # dimensionless
                },
                "practical_impact": {
                    "seconds_per_day": (time_dilation_factor - 1) * 86400  # s/day
                },
                "plot": {
                    "data": plot_data,
                    "format": "base64_png"
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating gravitational time dilation: {e}")
            return {"error": f"Could not calculate gravitational time dilation: {e}"}
    
    # Fluid Dynamics
    def analyze_fluid_flow(self, pipe_diameter, flow_rate=None, pressure_drop=None, fluid_density=1000, fluid_viscosity=0.001):
        """Analyze fluid flow in a pipe.
        
        Args:
            pipe_diameter: Diameter of the pipe in meters
            flow_rate: Volumetric flow rate in m³/s (optional)
            pressure_drop: Pressure drop over a pipe length in Pa (optional)
            fluid_density: Density of the fluid in kg/m³ (default: water)
            fluid_viscosity: Dynamic viscosity of the fluid in Pa·s (default: water)
            
        Returns:
            Dictionary with fluid flow analysis
        """
        try:
            # Pipe geometry
            pipe_radius = pipe_diameter / 2  # m
            pipe_area = math.pi * pipe_radius**2  # m²
            pipe_length = 1.0  # m (default value for calculations)
            
            # If both flow_rate and pressure_drop are provided, adjust pipe_length
            if flow_rate is not None and pressure_drop is not None:
                # Hagen-Poiseuille equation: L = (π·r⁴·ΔP) / (8·η·Q)
                pipe_length = (math.pi * pipe_radius**4 * pressure_drop) / (8 * fluid_viscosity * flow_rate)
            
            # Calculate missing parameter
            if flow_rate is None and pressure_drop is not None:
                # Hagen-Poiseuille equation: Q = (π·r⁴·ΔP) / (8·η·L)
                flow_rate = (math.pi * pipe_radius**4 * pressure_drop) / (8 * fluid_viscosity * pipe_length)
            elif pressure_drop is None and flow_rate is not None:
                # Hagen-Poiseuille equation: ΔP = (8·η·L·Q) / (π·r⁴)
                pressure_drop = (8 * fluid_viscosity * pipe_length * flow_rate) / (math.pi * pipe_radius**4)
            
            # Calculate flow velocity
            if flow_rate is not None:
                flow_velocity = flow_rate / pipe_area  # m/s
            else:
                flow_velocity = None
            
            # Calculate Reynolds number
            if flow_velocity is not None:
                reynolds_number = (fluid_density * flow_velocity * pipe_diameter) / fluid_viscosity
                
                # Determine flow regime
                if reynolds_number < 2300:
                    flow_regime = "Laminar"
                elif reynolds_number < 4000:
                    flow_regime = "Transitional"
                else:
                    flow_regime = "Turbulent"
                
                # Calculate friction factor
                if reynolds_number < 2300:
                    # Laminar flow: f = 64/Re
                    friction_factor = 64 / reynolds_number
                else:
                    # Turbulent flow: Use Swamee-Jain approximation of Colebrook-White equation
                    pipe_roughness = 0.000015  # m (assumed value for drawn pipe)
                    relative_roughness = pipe_roughness / pipe_diameter
                    friction_factor = 0.25 / (math.log10(relative_roughness/3.7 + 5.74/(reynolds_number**0.9)))**2
                
                # Calculate pressure drop using Darcy-Weisbach equation
                darcy_weisbach_pressure_drop = (friction_factor * pipe_length * fluid_density * flow_velocity**2) / (2 * pipe_diameter)
                
                # Calculate head loss
                head_loss = darcy_weisbach_pressure_drop / (fluid_density * 9.81)  # m
                
                # Calculate power loss
                power_loss = flow_rate * darcy_weisbach_pressure_drop  # W
            else:
                reynolds_number = None
                flow_regime = None
                friction_factor = None
                darcy_weisbach_pressure_drop = None
                head_loss = None
                power_loss = None
            
            # Generate velocity profile for laminar flow
            if flow_regime == "Laminar" and flow_velocity is not None:
                # Radial positions
                r_values = np.linspace(0, pipe_radius, 50)
                
                # Velocity profile for laminar flow: v(r) = v_max * (1 - (r/R)²)
                v_max = 2 * flow_velocity  # Maximum velocity at center
                velocity_profile = [v_max * (1 - (r/pipe_radius)**2) for r in r_values]
                
                # Create plot
                plt.figure(figsize=(10, 6))
                plt.plot(r_values, velocity_profile)
                plt.plot([0, pipe_radius], [flow_velocity, flow_velocity], 'r--', label="Average Velocity")
                
                plt.title("Laminar Flow Velocity Profile")
                plt.xlabel("Radial Position (m)")
                plt.ylabel("Velocity (m/s)")
                plt.grid(True)
                plt.legend()
                
                # Save plot to base64 for display
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                buffer.seek(0)
                profile_plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            else:
                profile_plot_data = None
            
            return {
                "pipe_geometry": {
                    "diameter": pipe_diameter,  # m
                    "radius": pipe_radius,  # m
                    "area": pipe_area,  # m²
                    "length": pipe_length  # m
                },
                "fluid_properties": {
                    "density": fluid_density,  # kg/m³
                    "viscosity": fluid_viscosity  # Pa·s
                },
                "flow_characteristics": {
                    "flow_rate": flow_rate,  # m³/s
                    "flow_velocity": flow_velocity,  # m/s
                    "pressure_drop": pressure_drop,  # Pa
                    "reynolds_number": reynolds_number,
                    "flow_regime": flow_regime,
                    "friction_factor": friction_factor,
                    "head_loss": head_loss,  # m
                    "power_loss": power_loss  # W
                },
                "velocity_profile_plot": {
                    "data": profile_plot_data,
                    "format": "base64_png"
                } if profile_plot_data else None
            }
            
        except Exception as e:
            logger.error(f"Error analyzing fluid flow: {e}")
            return {"error": f"Could not analyze fluid flow: {e}"}

# Initialize the physics engine
physics_engine = PhysicsEngine()

def get_physics_engine():
    """Get the global physics engine instance."""
    global physics_engine
    return physics_engine