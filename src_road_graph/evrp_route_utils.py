from math import cos, sin, sqrt, radians, atan2
from typing import Generator

meters: type = type("meters", (), {})

# Function to chunk list into sublists of given size
def chunk_list(locations: list[tuple[float, float]], chunk_size: int = 512) -> Generator[list[tuple[float, float]], None, None]:
    for index in range(0, len(locations), chunk_size): yield locations[index : index + chunk_size]

# Convert 2 Coordinatea into a distance (in metres)
def haversine(coord1, coord2):
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6387000 * c
