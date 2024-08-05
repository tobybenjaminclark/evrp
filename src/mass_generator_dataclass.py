import json
from dataclasses import dataclass


@dataclass
class MultipleInstanceGenerator:
    instance_count: int
    central_locations: list[tuple[float, float]]
    minimum_customers: int
    minimum_chargers: int
    minimum_depots: int


def parse_mass_generator(file_path: str) -> MultipleInstanceGenerator:
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract data from the JSON content
    instance_count = data.get('instance_count')
    central_locations = [(loc['latitude'], loc['longitude']) for loc in data.get('central_locations', [])]
    minimum_customers = data.get('minimum_customers')
    minimum_chargers = data.get('minimum_chargers')
    minimum_depots = data.get('minimum_depots')

    # Create an instance of MultipleInstanceGenerator
    return MultipleInstanceGenerator(
        instance_count=instance_count,
        central_locations=central_locations,
        minimum_customers=minimum_customers,
        minimum_chargers=minimum_chargers,
        minimum_depots=minimum_depots
    )
