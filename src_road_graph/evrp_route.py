from evrp_route_step import RouteStep, parse_step
from evrp_route_utils import meters, approximate_distance_from_polyline
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt


def pastel_colors_generator():
    pastel_colors = ['#FFB6C1', '#FFDAB9', '#B0E0E6', '#98FB98', '#FFA07A',
                     '#FFAEB9', '#FFC0CB', '#FFD700', '#FFDEAD', '#FFE4B5',
                     '#FFE4C4', '#FFE4E1', '#FFEBCD', '#FFEFD5', '#FFF0F5',
                     '#FFF5EE', '#FFF8DC', '#FFFACD', '#FFFAF0', '#FFFAFA',
                     '#F0FFF0', '#F5FFFA', '#FAEBD7', '#FAF0E6', '#FAFAD2',
                     '#FDF5E6', '#FF6347', '#FF69B4', '#FF7F50', '#FF8247',
                     '#FF8C00', '#FFA500', '#FFB5C5', '#FFD700', '#FFDAB9',
                     '#FFDEAD', '#FFE4B5', '#FFE4C4', '#FFE4E1', '#FFEBCD',
                     '#FFEFD5', '#FFEFDB', '#FFF0F5', '#FFF5EE', '#FFF8DC',
                     '#FFFACD', '#FFFAF0', '#FFFAFA', '#FFFF00', '#FFFFE0',
                     '#FFFFF0', '#FFFFFF']

    index = 0
    while True:
        yield pastel_colors[index % len(pastel_colors)]
        index += 1


class Route():
    def __init__(self, response: dict):
        print(response)
        self.steps: list[RouteStep] = list(map(parse_step, [step for route in response['routes'] for leg in route['legs'] for step in leg['steps']]))
        for step in self.steps:
            print(str(step) + "\n")

        self.plot_altitude_distance_series()

    def plot_altitude_distance_series(self) -> None:
        # Generate a Polyline of coordinates representing the entire route.
        polyline = [point for step in self.steps for point in step.polyline]

        # Derive altitude series and cumulative distances from this polyline (and step data)
        altitude_series = [(point, altitude)[1] for step in self.steps for point, altitude in step.locdata]
        distances = [approximate_distance_from_polyline(polyline[0:n]) for n in range(0, len(polyline))]

        # Calculate the widths for each bar
        widths = [distances[i + 1] - distances[i] if i < len(distances) - 1 else 1 for i in range(len(distances))]

        plt.figure(figsize=(30, 15))

        # Initialize the pastel color generator
        color_gen = pastel_colors_generator()

        # Iterate through each step and plot bars with corresponding colors
        for i, step in enumerate(self.steps):
            start_idx = sum(len(s.polyline) for s in self.steps[:i])  # Start index for current step
            end_idx = start_idx + len(step.polyline)  # End index for current step
            color = next(color_gen)  # Get the next pastel color

            plt.bar(distances[start_idx:end_idx], altitude_series[start_idx:end_idx],
                    width=widths[start_idx:end_idx], align='edge', color=color,
                    label=f'Step {i + 1} - {self.steps[i].instructions}')  # Adjust label as needed

        # Plot the linear path (polyline) for the entire route
        plt.plot(distances, altitude_series, label='Linear Path', color='red')

        plt.xlabel('Distance (meters)')
        plt.ylabel('Altitude (meters)')
        plt.title(f'Altitude vs Distance (Average Sampling Rate of {round(max(distances) / len(distances), 1)}m)')
        plt.legend()
        plt.grid(True)

        plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:.0f}m'))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, pos: f'{y:.0f}m'))

        plt.tight_layout()
        plt.show()