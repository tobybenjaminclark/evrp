from evrp_route_step import RouteStep, parse_step
from evrp_route_utils import meters, approximate_distance_from_polyline
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

class Route():
    def __init__(self, response: dict):
        print(response)
        self.steps: list[RouteStep] = list(map(parse_step, [step for route in response['routes'] for leg in route['legs'] for step in leg['steps']]))
        for step in self.steps:
            print(str(step) + "\n")

        self.plot_altitude_distance_series()

    def plot_altitude_distance_series(self) -> None:

        polyline = []
        locdata = []
        for step in self.steps:
            polyline.extend(step.polyline)
            locdata.extend(step.locdata)

        print(polyline)
        print(locdata)

        altitudes: list[meters] = [y for x, y in locdata]
        distances: list[meters] = [approximate_distance_from_polyline(polyline[0:n]) for n in range(0, len(polyline))]

        plt.figure(figsize=(10, 5))
        plt.plot(distances, altitudes, label='Altitude over Distance', color='blue')
        plt.xlabel('Distance (meters)')
        plt.ylabel('Altitude (meters)')
        plt.title('Altitude vs Distance')
        plt.legend()
        plt.grid(True)

        ax = plt.gca()
        ax.set_aspect('equal', adjustable='datalim')

        # Optional: format the tick labels to show meters with proper unit
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:.0f}m'))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, pos: f'{y:.0f}m'))

        plt.show()