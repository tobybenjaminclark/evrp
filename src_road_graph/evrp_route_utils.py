from math import cos, sin, sqrt, radians, atan2
from geopy.distance import distance
from shapely.geometry import Point, LineString

# Type to denote meters (avoiding unit confusion).
meters: type = type("meters", (), {})


def haversine(_point_one: float, _point_two: float, earth_radius: meters = 6_387_000) -> meters:
    """
    The haversine formula determines the great-circle distance between two points on a sphere given their longitudes and
    latitudes, (See https://w.wiki/4Aj7). This is used to determine the distance between points in a polyline, when
    approximating the total distance of a route.

    :param _point_one:      Langitude & Longitude of the first point.
    :param _point_two:      Langitude & Longitude of the second point.
    :param earth_radius:    Radius of the earth in meters. (Assumed to be 6,387,000)
    :return:                Distance between the two points in meters.
    """

    lat1, lon1 = map(radians, _point_one)
    lat2, lon2 = map(radians, _point_two)
    a = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return earth_radius * (2 * atan2(sqrt(a), sqrt(1 - a)))


def approximate_distance_from_polyline(polyline = None) -> meters:
    """
    This method approximates the total length of a polyline, and is used to validate the correctness of the polyline
    against the total distance the Directions API provides. It uses the haversine function to calculate the result.

    :return:    Cumulative Distance between all points in the parameterized polyline.
    """

    if polyline == None: raise ValueError
    return sum([haversine(polyline[i], polyline[i + 1]) for i in range(len(polyline) - 1)])

def interpolate_polyline(points):
    if len(points) < 2:
        raise ValueError("Input polyline must contain at least two points.")

    interpolated_points = []
    total_distance = 0.0

    # Iterate through each pair of consecutive points
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]

        # Calculate the distance between the current pair of points
        segment_distance = distance(start, end).meters

        # If the segment distance is less than 1 meter, skip interpolation
        if segment_distance < 1:
            interpolated_points.append(start)
            total_distance += segment_distance
            continue

        # Calculate the number of segments needed to achieve 1 meter apart
        num_interpolations = int(segment_distance)

        # Calculate the latitude and longitude step sizes
        lat_step = (end[0] - start[0]) / (num_interpolations + 1)
        lon_step = (end[1] - start[1]) / (num_interpolations + 1)

        # Interpolate points between start and end
        for j in range(1, num_interpolations + 1):
            interpolated_lat = start[0] + j * lat_step
            interpolated_lon = start[1] + j * lon_step
            interpolated_points.append((interpolated_lat, interpolated_lon))

        # Add the end point of the segment
        interpolated_points.append(end)

        # Update total distance with the segment distance
        total_distance += segment_distance

    return interpolated_points