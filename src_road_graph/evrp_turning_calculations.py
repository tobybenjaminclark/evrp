import numpy as np
from statistics import median
from itertools import product
from constants import *



# Function to convert degrees to radians
def deg_to_rad(deg) -> float: return deg * np.pi / 180.0



# Function to convert latitude and longitude to Cartesian coordinates
def lat_lon_to_cartesian(lat, lon, R):
    lat, lon = deg_to_rad(lat), deg_to_rad(lon)
    return np.array([R * np.cos(lat) * np.cos(lon), R * np.cos(lat) * np.sin(lon), R * np.sin(lat)])



# Function to calculate the radius of the arc from three coordinates
def calculate_radius(lat1: float, lon1: float, lat2: float, lon2: float, lat3: float, lon3: float) -> float:
    p1, p2, p3 = lat_lon_to_cartesian(lat1, lon1, R), lat_lon_to_cartesian(lat2, lon2, R), lat_lon_to_cartesian(lat3, lon3, R)

    # Calculate the lengths of the sides of the triangle formed by p1, p2, and p3 and the semi-perimeter (s)
    a, b, c = np.linalg.norm(p2 - p3), np.linalg.norm(p1 - p3), np.linalg.norm(p1 - p2)
    s = (a + b + c) / 2

    # Calculate the area of the triangle using Heron's formula and the circumradius & convert to metres
    area = np.sqrt(s * (s - a) * (s - b) * (s - c))
    return ((a * b * c) / (4 * area) if (4 * area) != 0 else 0) * 1000



# Function to calculate maximum speed in a turn
def max_speed(lat1: float, lon1: float, lat2: float, lon2: float, lat3: float, lon3: float, gravity: float = g, friction_coefficient: float = mu) -> float:
    return np.sqrt(calculate_radius(lat1, lon1, lat2, lon2, lat3, lon3) * friction_coefficient * gravity)



# Find safe speed for a polyline
def maximum_safe_speed(polyline: list[tuple[float, float]], arcs_per_side: int = 20, max_speeds: list[float] = []) -> list[float]:
    """
    This function determines the (theoretical) maximum safe driving speed, for every point in the line, considering the
    curvature (calculated aross multiple surrounding points, arcs_per_side). This calculation is based on the centrifrugal
    force.

    :polyline:      List of tuples representing the points (lang, long) on the polyline.
    :arcs_per_side: The number of points to consider on either side of the current point for curvature calculation.
    """

    for i in range(1, len(polyline) - 1, 1):
        pre_c = [polyline[i + _i] for _i in filter(lambda v: v != 0 and (i + v) >= 0 and (i + v) < len(polyline), range(-arcs_per_side, 0))]
        post_c = [polyline[i + _i] for _i in filter(lambda v: v != 0 and (i + v) >= 0 and (i + v) < len(polyline), range(0, arcs_per_side))]
        max_speeds.append(median([max_speed(*p1, polyline[i][0], polyline[i][1], *p2) * 3.6 for (p1, p2) in list(product(pre_c, post_c))]))
    return list(filter(lambda v: float(v), max_speeds + [max_speeds[len(max_speeds) - 1]] + [max_speeds[len(max_speeds) - 1]]))