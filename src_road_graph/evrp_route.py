from typing import Tuple, List, Any

from evrp_route_step import RouteStep, parse_step
from evrp_route_utils import meters, approximate_distance_from_polyline, haversine
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from scipy.interpolate import interp1d
import math
import statistics


def calculate_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formula used is from:
    https://www.movable-type.co.uk/scripts/latlong.html
    """
    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])
    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -π to +π so we need to normalize the result to a compass bearing
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def angle_difference(angle1, angle2):
    return (360 - abs(angle1 - angle2)) if abs(angle1 - angle2) > 180 else abs(angle1 - angle2)

def construct_bearing_list(polyline):
    bearing_prev: float = calculate_bearing(polyline[0], polyline[1])
    bearings = []
    for index in range(0, len(polyline) - 1):
        point_one, point_two = polyline[index], polyline[index + 1]
        bearing = calculate_bearing(point_one, point_two)

        bearings.append(angle_difference(bearing, bearing_prev))
        bearing_prev = bearing
    return bearings + [0]




def maximum_safe_speed(radius, friction_coefficient = 0.7, gravity = 9.8):
    """
    Calculate the maximum safe speed a car can make a turn.

    Parameters:
    radius (float): Radius of the turn in meters.
    friction_coefficient (float): Coefficient of friction between the tires and the road.
    gravity (float): Acceleration due to gravity in m/s^2. Default is 9.8 m/s^2.

    Returns:
    float: Maximum safe speed in km/h.
    """
    radius = max(radius, 1.0)
    speed_m_per_s = math.sqrt(friction_coefficient * gravity * radius)
    speed_km_per_h = speed_m_per_s * 3.6
    return speed_km_per_h



def bright_colors_generator():
    less_bright_colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']

    index = 0
    while True:
        yield less_bright_colors[index % len(less_bright_colors)]
        index += 1


class Route():


    def __init__(self, response: dict, _origin: str, _destination: str):
        self.origin = _origin
        self.destination = _destination
        self.steps: list[RouteStep] = list(map(parse_step, [step for route in response['routes'] for leg in route['legs'] for step in leg['steps']]))
        for step in self.steps:
            print(str(step) + "\n")

        self.plot_route_data()

    def plot_route_data(self, rolling_average_length: int = 30) -> None:
        """
        Method to plot route data on a Matplotlib graph. Plots the discrete altitude sampling (over time) with a rolling
        average overlay (of length rolling_average_length). Displays the entire route (with dots at each polynode), with
        color coding for each step and visualization of angle list.
        """

        # Synthesise a super-polyline for the whole route from the polylines of each constituent step.
        superpolyline = [point for step in self.steps for point in step.polyline]
        angle_list = construct_bearing_list(superpolyline)

        print(f"Generated {len(angle_list)} bearings for a polyline of length {len(superpolyline)}")

        # Derive altitude series, speed series, and cumulative distances from this super-polyline (and step data)
        altitude_series = [altitude for step in self.steps for point, altitude in step.locdata]
        speed_series = [step.road_speed for step in self.steps for _ in step.polyline]
        distances = [approximate_distance_from_polyline(superpolyline[0:n]) for n in range(0, len(superpolyline))]

        # Perform linear interpolation (filling in gaps between samples linearly)
        f_interp = interp1d(distances, altitude_series, kind='linear')

        # Create a new set of distances for the smoothed line (with higher resolution)
        smoothed_distances = np.linspace(distances[0], distances[-1], num=len(distances) * 10)
        smoothed_altitudes = f_interp(smoothed_distances)

        # Apply a rolling average to further smooth the data, according to the rolling average length.
        rolling_window = rolling_average_length
        smoothed_altitudes_rolling = np.convolve(smoothed_altitudes, np.ones(rolling_window) / rolling_window, mode='same')

        # Calculate the widths for each bar (visualisation, the sample is at the left-most point on each bar)
        widths = [distances[i + 1] - distances[i] if i < len(distances) - 1 else 1 for i in range(len(distances))]

        # Create a figure with three subplots: one for altitude vs distance, one for speed vs distance, and one for the route plot
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(70, 60))

        # Plot Altitude vs Distance on the first subplot (altitude series over distance)
        ax1.set_title(f'Altitude vs Distance (Average Sampling Rate of {round(max(distances) / len(distances), 1)}m)')
        ax1.set_xlabel('Distance (meters)')
        ax1.set_ylabel('Altitude (meters)')

        # Ensure the x-axis and y-axis start at 0 and cover the full range of distances and altitudes
        ax1.set_xlim(0, max(distances))
        ax1.set_ylim(min(altitude_series), max(altitude_series))

        # Initialize the pastel color generator
        color_gen = bright_colors_generator()

        # Iterate through each step and plot bars with corresponding colors
        for i, step in enumerate(self.steps):
            start_idx = sum(len(s.polyline) for s in self.steps[:i])
            end_idx = start_idx + len(step.polyline)
            color = next(color_gen)

            # Plot the altitude data for this step as bars
            ax1.bar(distances[start_idx:end_idx], altitude_series[start_idx:end_idx],
                    width=widths[start_idx:end_idx], align='edge', color=color,
                    label=f'Step {i + 1} - {step.instructions}')

        # Plot the smoothed linear path (polyline) for the entire route
        ax1.plot(smoothed_distances[::10], smoothed_altitudes_rolling[::10], label='Smoothed Linear Path', color='blue')

        # Add legend and grid to the first subplot
        ax1.legend()
        ax1.legend()
        ax1.grid(True)

        # Format the x and y axis labels to display distances and altitudes in meters
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x:.0f}m'))
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'{y:.0f}m'))

        # Plot Speed vs Distance on the second subplot (speed series over distance)
        ax2.set_title('Speed vs Distance')
        ax2.set_xlabel('Distance (meters)')
        ax2.set_ylabel('Speed (km/h)')

        # Ensure the x-axis and y-axis start at 0 and cover the full range of distances and speeds
        ax2.set_xlim(0, max(distances))
        ax2.set_ylim(0, max(speed_series))

        # Initialize the pastel color generator again for the speed plot
        color_gen = bright_colors_generator()

        # Iterate through each step and plot bars with corresponding colors
        for i, step in enumerate(self.steps):
            start_idx = sum(len(s.polyline) for s in self.steps[:i])
            end_idx = start_idx + len(step.polyline)
            color = next(color_gen)

            # Plot the speed data for this step as bars
            ax2.bar(distances[start_idx:end_idx], speed_series[start_idx:end_idx],
                    width=widths[start_idx:end_idx], align='edge', color=color,
                    label=f'Step {i + 1} - {step.instructions}')

        # Add legend and grid to the second subplot
        ax2.legend()
        ax2.grid(True)

        # Format the x axis labels to display distances in meters
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x:.0f}m'))

        # Plot Route on a map in the third subplot
        ax3.set_title('Route Plot')
        ax3.set_xlabel('Longitude')
        ax3.set_ylabel('Latitude')

        # Initialize the pastel color generator again for the route plot
        color_gen = bright_colors_generator()

        # Iterate through each step and plot segments of the polyline with corresponding colors
        for i, step in enumerate(self.steps):
            color = next(color_gen)  # Get the next pastel color
            step_latitudes = [point[0] for point in step.polyline]
            step_longitudes = [point[1] for point in step.polyline]
            ax3.plot(step_longitudes, step_latitudes, marker='o', linestyle='-', color=color,
                     label=f'Step {i + 1} - {step.instructions}')

        # Label the origin at the first point of the route
        ax3.text(self.steps[0].polyline[0][1], self.steps[0].polyline[0][0], self.origin.split(",")[0], fontsize=14,
                 color='black', ha='center',
                 va='bottom')

        # Label the destination at the last point of the route
        ax3.text(self.steps[-1].polyline[-1][1], self.steps[-1].polyline[-1][0], self.destination.split(",")[0],
                 fontsize=14,
                 color='black', ha='center', va='bottom')

        # Set the aspect ratio of the plot to be equal
        ax3.set_aspect('equal', adjustable='datalim')
        ax3.legend()
        ax3.grid(True)

        # Plot Angle List on the fourth subplot (ax4)
        ax4.set_title('Angle List')
        ax4.set_xlabel('Segment Index')
        ax4.set_ylabel('Angle (degrees)')
        ax4.set_xlim(0, max(distances))

        # Plot the angle list
        ax4.plot(distances, angle_list, marker='o', linestyle='-', color='green', label='Angles')
        ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x:.0f}m'))

        # Add colors for steps
        start_idx = 0
        color_gen = bright_colors_generator()
        for i, step in enumerate(self.steps):
            end_idx = start_idx + len(step.polyline) # - 1
            ax4.plot(distances[start_idx:end_idx], angle_list[start_idx:end_idx], marker='o', linestyle='-', color=next(color_gen),
                     label=f'Step {i + 1}')
            start_idx = end_idx

        # Add legend and grid to the fourth subplot
        ax4.legend()
        ax4.grid(True)

        ax5.set_title('Turning Speed Plots')
        ax5.set_xlabel('Distance')
        ax5.set_ylabel('Maximum Speed (km/h)')
        distances_adjusted = [0] + [distances[index] - distances[index - 1] for index in range(1, len(distances))]

        angle_list_nonzero = list(map(lambda v: math.radians(v) if v != 0 else math.radians(1), angle_list))
        max_speed_series = [maximum_safe_speed(distances_adjusted[i] / angle_list_nonzero[i]) for i in range(len(angle_list))]
        acc_speed_series = [min(speed_series[i], max_speed_series[i]) for i in range(len(max_speed_series))]

        ax5.set_xlim(0, max(distances))
        ax5.set_ylim(min(acc_speed_series), max(acc_speed_series))
        ax5.plot(distances, acc_speed_series, marker='o', linestyle='-', color='green', label='Maximum Speed (km/h)')

        # Adjust layout to prevent overlapping of subplots
        plt.tight_layout()

        # Display the plots
        plt.show()