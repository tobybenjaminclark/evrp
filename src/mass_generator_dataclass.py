from dataclasses import dataclass

@dataclass
class mass_generator():

    instance_count: int
    central_locations: list[tuple[float, float]]
    minimum_customers: int
    minimum_chargers: int
    minimum_depots: int
