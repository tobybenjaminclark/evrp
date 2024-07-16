from typing import Tuple, List, Any

from evrp_route_step import RouteStep, parse_step
from src_energy_model.emodel_basso import *
from evrp_route_utils import *
from evrp_turning_calculations import *
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
from scipy.interpolate import interp1d
import logging
import timeit
import os
from datetime import datetime

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)

# Generate the log file name based on the current date and time
current_time = datetime.now().strftime('%d%B%Y%H%M')
log_file_name = f"EVRPLog-{current_time}.log"
log_file_path = os.path.join('logs', log_file_name)

# Configure logging to write to a file in logs/
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file_path)
                    ])

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
        self.superpolyline = [point for step in self.steps for point in step.polyline]
        self.distances = [approximate_distance_from_polyline(self.superpolyline[0:n]) for n in range(0, len(self.superpolyline))]

        # Timing each method and logging the results
        self.log_method_time(self.calculate_altitude_sampling, "calculate_altitude_sampling")
        self.log_method_time(self.calculate_speed_series, "calculate_speed_series")
        self.log_method_time(self.calculate_route_turning_speed, "calculate_route_turning_speed")
        self.log_method_time(self.calculate_seconds_speeds, "calculate_seconds_speeds")
        self.log_method_time(self.calculate_energy_consumption, "calculate_energy_consumption")

        self.plot_route_data()

    def log_method_time(self, method, method_name):
        execution_time = timeit.timeit(method, number=1)
        logging.info(f"{method_name:<30}: {execution_time:.6f} seconds")

    def calculate_altitude_sampling(self, pad_size: int = 40):

        # Derive altitude series, and cumulative distances from this super-polyline (and step data)
        altitude_series = [altitude for step in self.steps for point, altitude in step.locdata]
        if len(distances := [approximate_distance_from_polyline(self.superpolyline[0:n]) for n in range(0, len(self.superpolyline))]) > pad_size: pad_size = len(distances)

        # Linearly interpolate the data series
        interpolated_altitudes = interp1d(distances, altitude_series, kind='linear', fill_value="extrapolate")

        # List Comprehension to perform a rolling window of size `pad_size`
        smooth_altitudes = [np.average(list(filter(lambda v: not(np.isnan(v) or np.isinf(v)), [interpolated_altitudes(a) for a in range(int(d - (pad_size // 2)), int(d + (pad_size // 2)), pad_size // 20)]))) for d in distances]

        # Provide altitude series as a linear interpolation of this rolling window.
        self.altitude_series = interp1d(distances, smooth_altitudes, kind='linear', fill_value="extrapolate")

    def plot_altitude_series(self, axis):

        # Synthesise a super-polyline for the whole route from the polylines of each constituent step.self.altitude_series
        discrete_altitude_sampling = [altitude for step in self.steps for point, altitude in step.locdata]

        # Calculate the widths for each bar (visualisation, the sample is at the left-most point on each bar)
        widths = [self.distances[i + 1] - self.distances[i] if i < len(self.distances) - 1 else 1 for i in range(len(self.distances))]

        # Plot Altitude vs Distance on the first subplot (altitude series over distance)
        axis.set_title(f'Altitude vs Distance (Average Sampling Rate of {round(max(self.distances) / len(self.distances), 2)}m)')
        axis.set_xlabel('Distance into Route (meters)')
        axis.set_ylabel('Altitude (meters)')

        # Ensure the x-axis and y-axis start at 0 and cover the full range of distances and (discrete) altitudes
        axis.set_xlim(0, max(self.distances))
        axis.set_ylim(min(discrete_altitude_sampling), max(discrete_altitude_sampling))

        # Initialize the pastel color generator
        color_gen = bright_colors_generator()

        # Iterate through each step and plot bars with corresponding colors
        for i, step in enumerate(self.steps):
            start_idx = sum(len(s.polyline) for s in self.steps[:i])
            end_idx = start_idx + len(step.polyline)
            color = next(color_gen)

            # Plot the altitude data for this step as bars
            axis.bar(self.distances[start_idx:end_idx], discrete_altitude_sampling[start_idx:end_idx],
                    width=widths[start_idx:end_idx], align='edge', color=color,
                    label=f'Step {i + 1} - {step.instructions}')

        # Plot the smoothed linear path (polyline) for the entire route, from calculate_altitude_series
        axis.plot(self.distances, [self.altitude_series(d) for d in self.distances], label='Smoothed Altitude Path', color='blue', linewidth=6.0)

        # Add legend and grid to the first subplot
        axis.legend()
        axis.grid(True)

        # Format the x and y axis labels to display distances and altitudes in meters
        axis.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x:.0f}m'))
        axis.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, pos: f'{y:.0f}m'))

    def calculate_speed_series(self):
        self.speed_series = [step.road_speed for step in self.steps for _ in step.polyline]

    def plot_speed_series(self, axis):

        # Plot Speed vs Distance on the second subplot (speed series over distance)
        axis.set_title('Speed vs Distance')
        axis.set_xlabel('Distance (meters)')
        axis.set_ylabel('Speed (km/h)')

        # Ensure the x-axis and y-axis start at 0 and cover the full range of distances and speeds
        axis.set_xlim(0, max(self.distances))
        axis.set_ylim(0, max(self.speed_series))

        # Initialize the pastel color generator again for the speed plot
        widths = [self.distances[i + 1] - self.distances[i] if i < len(self.distances) - 1 else 1 for i in range(len(self.distances))]
        color_gen = bright_colors_generator()

        # Iterate through each step and plot bars with corresponding colors
        for i, step in enumerate(self.steps):
            start_idx = sum(len(s.polyline) for s in self.steps[:i])
            end_idx = start_idx + len(step.polyline)
            color = next(color_gen)

            # Plot the speed data for this step as bars
            axis.bar(self.distances[start_idx:end_idx], self.speed_series[start_idx:end_idx],
                    width=widths[start_idx:end_idx], align='edge', color=color,
                    label=f'Step {i + 1} - {step.instructions}')

        # Add legend and grid to the second subplot
        axis.legend()
        axis.grid(True)

        # Format the x axis labels to display distances in meters
        axis.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x:.0f}m'))

    def plot_route_layout(self, axis):
        # Plot Route on a map in the third subplot
        axis.set_title('Route Plot')
        axis.set_xlabel('Longitude')
        axis.set_ylabel('Latitude')

        # Initialize the pastel color generator again for the route plot
        color_gen = bright_colors_generator()

        # Iterate through each step and plot segments of the polyline with corresponding colors
        for i, step in enumerate(self.steps):
            color = next(color_gen)  # Get the next pastel color
            step_latitudes = [point[0] for point in step.polyline]
            step_longitudes = [point[1] for point in step.polyline]
            axis.plot(step_longitudes, step_latitudes, marker='o', linestyle='-', color=color,
                     label=f'Step {i + 1} - {step.instructions}')

        # Label the origin at the first point of the route
        axis.text(self.steps[0].polyline[0][1], self.steps[0].polyline[0][0], self.origin.split(",")[0], fontsize=14,
                 color='black', ha='center',
                 va='bottom')

        # Label the destination at the last point of the route
        axis.text(self.steps[-1].polyline[-1][1], self.steps[-1].polyline[-1][0], self.destination.split(",")[0],
                 fontsize=14,
                 color='black', ha='center', va='bottom')

        # Set the aspect ratio of the plot to be equal
        axis.set_aspect('equal', adjustable='datalim')
        axis.legend()
        axis.grid(True)

    def plot_route_turning_speed(self, axis):
        # Plotting
        axis.set_title('Turning Speed Plots')
        axis.set_xlabel('Distance')
        axis.set_ylabel('Maximum Speed (km/h)')

        axis.set_xlim(0, max(self.distances))
        axis.set_ylim(0, max(self.acc_speed_series))
        axis.plot(self.distances, self.acc_speed_series, marker='', linestyle='-', color='green', label='Interpolated Maximum Speed (km/h)')

        # Add colors for steps
        start_idx = 0
        color_gen = bright_colors_generator()
        for i, step in enumerate(self.steps):
            end_idx = start_idx + len(step.polyline) # - 1
            axis.plot(self.distances[start_idx:end_idx], self.acc_speed_series[start_idx:end_idx], marker='o', linestyle='-', color=next(color_gen),
                     label=f'Step {i + 1}')
            start_idx = end_idx

        axis.legend()

    def calculate_route_turning_speed(self):
        max_speed_series = maximum_safe_speed(self.superpolyline, self.distances)
        self.acc_speed_series = [min(self.speed_series[i], max_speed_series[i]) for i in range(len(max_speed_series))]

    def calculate_seconds_speeds(self):
        # Parameters
        acceleration_rate = 0.82     # m/s^2
        deceleration_rate = 2.52     # m/s^2
        time_interval = 1.0          # seconds

        # Simulate the car speed
        current_speed = 1.0
        current_distance = 0.0
        interp = interp1d(self.distances, self.acc_speed_series, kind='linear', fill_value="extrapolate")

        seconds = []
        speeds = []
        distances_traveled = []

        current_second = 0
        while current_distance < self.distances[-1]:
            current_second += time_interval
            current_distance += current_speed * time_interval

            # Convert km/h to m/s
            target_speed = interp(current_distance) * (1000 / 3600)
            for x in range(int(current_distance) + 5, int(current_distance) + int(current_speed * 3.6)):
                if interp(x) < target_speed:
                    target_speed = interp(x)

            if current_speed < target_speed:
                current_speed += acceleration_rate * time_interval

                if current_speed > target_speed: current_speed = target_speed

            elif current_speed > target_speed:
                current_speed -= deceleration_rate * time_interval

                if current_speed < target_speed: current_speed = target_speed

            speeds.append(current_speed * 3.6)  # Convert m/s to km/h
            distances_traveled.append(target_speed)
            seconds.append(current_second)

            self.distances_travelled = distances_traveled
            self.seconds = seconds
            self.speeds = speeds

    def plot_real_speed_series(self, axis):

        # Plot speed
        axis.plot(self.seconds, self.speeds, label='Speed (km/h)', color='b')

        # Setup the secondary y-axis for distance
        axTwin = axis.twinx()
        axTwin.set_ylabel('Distance (m)')
        axTwin.plot(self.seconds, self.distances_travelled, label='Distance (m)', color='r')

        # Setting limits for both axes
        axis.set_ylim(0, max(self.speeds))
        axis.set_xlim(0, max(self.seconds))
        axTwin.set_ylim(0, max(self.distances_travelled))

        # Adding legends
        axis.legend(loc='upper left')
        axTwin.legend(loc='upper right')

    def calculate_energy_consumption(self):
        # sampling for gradient?
        delta_d = 10.0

        pwr_seconds = []
        pwr_pwrs = []

        interpolated_distances = interp1d(self.seconds, self.distances_travelled, kind='linear', fill_value="extrapolate")
        interpolated_speeds = interp1d(self.seconds, self.speeds, kind='linear', fill_value="extrapolate")
        interpolated_altitude = lambda dist: self.altitude_series(interpolated_distances(dist))

        for current_second in self.seconds:
            current_distance = interpolated_distances(current_second)
            current_altitude = interpolated_altitude(current_second)
            current_speed = interpolated_speeds(current_second)

            # Compute altitude at the next step
            next_distance = current_distance + delta_d
            next_altitude = self.altitude_series(next_distance)

            # Calculate the road gradient using finite differences
            gradient = (next_altitude - current_altitude) / delta_d
            gradient_degrees = math.atan(gradient) * (180 / 3.14159)

            # Calculate current speed in (m/s)
            speed_ms = current_speed * (5 / 18)

            # Compute mechanical power
            pwr = get_mechanical_power(speed_ms, gradient_degrees)

            # Print or store the result as needed
            print(f"Current Altitude: {current_altitude}, Next Altitude: {next_altitude}, Speed: {speed_ms}")
            print(f"Distance: {current_distance}, Gradient: {gradient_degrees:.2f} degrees, Power: {pwr}\n")

            if(np.isnan(pwr)):
                continue

            pwr_seconds.append(current_second)
            pwr_pwrs.append(pwr)

        total = 0
        cumulative = []
        segment = 1
        for x in pwr_pwrs:
            total = total + (x / 3600 / 1000)
            cumulative.append(total)
            # print(f"Segment {segment}, at {x:.2f} W. New total is: {total:.2f} kWh")
            segment += 1

        print(f"Total Power: {total:.2f} kWh")

        self.total = total
        self.cumulative = cumulative
        self.pwr_pwrs = pwr_pwrs
        self.pwr_seconds = pwr_seconds

    def plot_energy_consumption(self, axis):
        axis.plot(self.pwr_seconds, self.pwr_pwrs, marker='', linestyle='-', color='green', label='Mechanical Power')

        # Setup the secondary y-axis for distance
        ax6Twin = axis.twinx()
        ax6Twin.set_ylabel('Distance (m)')
        ax6Twin.plot(self.pwr_seconds, self.cumulative, label='Cumulative', color='r')

        # Setting limits for both axes
        axis.set_ylim(min(self.pwr_pwrs), max(self.pwr_pwrs))
        axis.set_xlim(0, max(self.pwr_seconds))

        ax6Twin.set_ylim(0, max(self.cumulative))

        # Adding data labels to the cumulative plot
        for i, value in enumerate(self.cumulative):
            if(i % 10 == 0): ax6Twin.annotate(f'{value:.3f} kWh', (self.pwr_seconds[i], self.cumulative[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        # Adding legends
        axis.legend(loc='upper left')
        ax6Twin.legend(loc='upper right')

    def plot_route_data(self) -> None:
        """
        Method to plot route data on a Matplotlib graph. Plots the discrete altitude sampling (over time) with a rolling
        average overlay (of length rolling_average_length). Displays the entire route (with dots at each polynode), with
        color coding for each step and visualization of angle list.
        """

        # Synthesise a super-polyline for the whole route from the polylines of each constituent step.
        superpolyline = self.superpolyline


        distances = [approximate_distance_from_polyline(self.superpolyline[0:n]) for n in range(0, len(self.superpolyline))]

        # Calculate the widths for each bar (visualisation, the sample is at the left-most point on each bar)
        widths = [distances[i + 1] - distances[i] if i < len(distances) - 1 else 1 for i in range(len(distances))]

        # Create a figure with three subplots: one for altitude vs distance, one for speed vs distance, and one for the route plot
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(70, 40))

        self.plot_altitude_series(ax1)



        speed_series = self.speed_series

        self.plot_speed_series(ax2)
        self.plot_route_layout(ax3)

        self.plot_route_turning_speed(ax4)
        self.plot_real_speed_series(ax5)
        self.plot_energy_consumption(ax6)









        # Adjust layout to prevent overlapping of subplots
        plt.tight_layout()

        # Display the plots
        plt.show()