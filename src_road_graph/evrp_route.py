from typing import Tuple, List, Any

from evrp_route_step import RouteStep, parse_step
from evrp_route_utils import meters, approximate_distance_from_polyline
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from scipy.interpolate import interp1d

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
        color coding for each step.

        :return:    None
        """

        # Generate a Polyline of coordinates representing the entire route
        polyline = [point for step in self.steps for point in step.polyline]

        # Derive altitude series and cumulative distances from this polyline (and step data)
        altitude_series = [altitude for step in self.steps for point, altitude in step.locdata]
        distances: tuple[list[Any], list[Any]] = [approximate_distance_from_polyline(polyline[0:n]) for n in range(0, len(polyline))]

        # Perform linear interpolation
        f_interp = interp1d(distances, altitude_series, kind='linear')

        # Create a new set of distances for the smoothed line (with higher resolution)
        smoothed_distances = np.linspace(distances[0], distances[-1], num=len(distances) * 10)
        smoothed_altitudes = f_interp(smoothed_distances)

        # Apply a rolling average to further smooth the data
        rolling_window = rolling_average_length  # 30 meters rolling average
        smoothed_altitudes_rolling = np.convolve(smoothed_altitudes, np.ones(rolling_window) / rolling_window, mode='same')

        # Calculate the widths for each bar
        widths = [distances[i + 1] - distances[i] if i < len(distances) - 1 else 1 for i in range(len(distances))]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 20))  # Add one more axis for the heatmap

        # Plot Altitude vs Distance on the first subplot
        ax1.set_title(f'Altitude vs Distance (Average Sampling Rate of {round(max(distances) / len(distances), 1)}m)')
        ax1.set_xlabel('Distance (meters)')
        ax1.set_ylabel('Altitude (meters)')

        # Ensure axis starts at (0, 0)
        ax1.set_xlim(0, max(distances))
        ax1.set_ylim(min(altitude_series), max(altitude_series))

        # Initialize the pastel color generator
        color_gen = bright_colors_generator()

        # Iterate through each step and plot bars with corresponding colors
        for i, step in enumerate(self.steps):
            start_idx = sum(len(s.polyline) for s in self.steps[:i])  # Start index for current step
            end_idx = start_idx + len(step.polyline)  # End index for current step
            color = next(color_gen)  # Get the next pastel color

            ax1.bar(distances[start_idx:end_idx], altitude_series[start_idx:end_idx],
                    width=widths[start_idx:end_idx], align='edge', color=color,
                    label=f'Step {i + 1} - {self.steps[i].instructions}')

        # Plot the linear path (polyline) for the entire route
        ax1.plot(smoothed_distances[::10], smoothed_altitudes_rolling[::10], label='Smoothed Linear Path', color='blue')

        ax1.legend()
        ax1.grid(True)

        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x:.0f}m'))
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'{y:.0f}m'))

        # Plot Route on a map in the second subplot
        ax2.set_title('Route Plot')
        ax2.set_xlabel('Longitude')
        ax2.set_ylabel('Latitude')

        # Initialize the pastel color generator again for the route plot
        color_gen = bright_colors_generator()

        # Iterate through each step and plot segments of the polyline with corresponding colors
        for i, step in enumerate(self.steps):
            color = next(color_gen)  # Get the next pastel color
            step_latitudes = [point[0] for point in step.polyline]
            step_longitudes = [point[1] for point in step.polyline]
            ax2.plot(step_longitudes, step_latitudes, marker='o', linestyle='-', color=color,
                     label=f'Step {i + 1} - {self.steps[i].instructions}')

        # Label the origin at the first point
        origin_latitude = self.steps[0].polyline[0][0]
        origin_longitude = self.steps[0].polyline[0][1]
        ax2.text(origin_longitude, origin_latitude, self.origin.split(",")[0], fontsize=14, color='black', ha='center', va='bottom')

        # Label the destination at the last point
        destination_latitude = self.steps[-1].polyline[-1][0]
        destination_longitude = self.steps[-1].polyline[-1][1]
        ax2.text(destination_longitude, destination_latitude, self.destination.split(",")[0], fontsize=14, color='black', ha='center', va='bottom')

        ax2.set_aspect('equal', adjustable='datalim')
        ax2.legend()
        ax2.grid(True)


        plt.tight_layout()
        plt.show()