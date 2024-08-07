import json
from dataclasses import dataclass
from scipy.stats import truncnorm
from generator_dataclass import Generator, DepotNodeGenerator, CustomerNodeGenerator, EVChargePointNodeGenerator
from random import choice, shuffle
from autogen_dataclass import *

proportion_mappings = ["R", "C", "RL", "R_C", "R_RL", "C_RL", "R_C_RL"]
tw_proportion_mappings = ["R", "S"]
tw_type_mappings = ["NARROW", "MODERATE", "WIDE"]

def generate_truncated_normal_samples(min_val: float, max_val: float, n: int, std_dev: float = 3.0) -> list[float]:
    return truncnorm.rvs((min_val - (min_val + max_val) / 2) / std_dev,
                         (max_val - (min_val + max_val) / 2) / std_dev,
                         loc = (min_val + max_val) / 2,
                         scale = std_dev,
                         size = n)


def validate_proportions(proportions):
    total = sum(proportions.values())
    return total == 100


def generate_list(proportions, n):
    # Validate proportions
    if not validate_proportions(proportions): raise ValueError("Proportions must add up to 100.")

    # Create a list based on the proportions
    elements = []
    for key, proportion in proportions.items():
        count = int(n * proportion / 100)
        elements.extend([key] * count)

    # Adjust the list to ensure it has exactly n elements (handle rounding issues)
    while len(elements) < n: elements.append(choice(list(proportions.keys())))
    while len(elements) > n: elements.pop()

    shuffle(elements)  # Shuffle to ensure randomness
    return elements

@dataclass
class MultipleAutoInstanceGenerator:

    instance_count: int
    central_locations: list[tuple[float, float]]
    range: int

    minimum_customers: int
    maximum_customers: int
    minimum_chargers: int
    maximum_chargers: int
    minimum_depots: int
    maximum_depots: int

    # Sampling Types
    cgen_p: list[float]
    dgen_p: list[float]
    egen_p: list[float]

    # Time Window Sampling
    twgen_p: list[float]
    twtyp_p: list[float]

    def build(self) -> list[Generator]:

        # Get a nomral distributor of customer counts.
        cust_c = generate_truncated_normal_samples(self.minimum_customers, self.maximum_customers, self.instance_count)
        cust_c = [int(max(self.minimum_customers, min(self.maximum_customers, c))) for c in cust_c]

        # Get a normal distribution of charger counts.
        charge_c = generate_truncated_normal_samples(self.minimum_chargers, self.maximum_chargers, self.instance_count)
        charge_c = [int(max(self.minimum_chargers, min(self.maximum_chargers, c))) for c in charge_c]

        # Get a normal distribution of depot counts, and locations
        depot_c  = generate_truncated_normal_samples(self.minimum_depots, self.maximum_depots, self.instance_count)
        depot_c = [int(max(self.minimum_depots, min(self.maximum_depots, c))) for c in depot_c]
        locations = [choice(self.central_locations) for _ in range(self.instance_count)]
        ranges = [self.range for _ in range(self.instance_count)]

        # Generate Sampling Proportions, for Customers, Depots & Chargers
        mk_map = lambda p: generate_list(dict(zip(proportion_mappings, p)), self.instance_count)
        cgen_p, dgen_p, egen_p = mk_map(self.cgen_p), mk_map(self.dgen_p), mk_map(self.egen_p)

        # Generate Sampling Proportions for Time Windows
        twtyp_p = generate_list(dict(zip(tw_type_mappings, self.twtyp_p)), self.instance_count)
        twgen_p = generate_list(dict(zip(tw_proportion_mappings, self.twgen_p)), self.instance_count)

        instance_params = zip(cust_c, charge_c, depot_c, locations, ranges, cgen_p, dgen_p, egen_p, twgen_p, twtyp_p)
        autogens = [AutoGenerator(*i) for i in instance_params]

        for a in autogens: print(a)

a = MultipleAutoInstanceGenerator(
    10,
    [(-1, 1)],
    4000,
    10,
    20,
    10,
    20,
    10,
    20,
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 100.0],
    [100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [50.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [50.0, 50.0],
    [30.0, 70.0, 0.0]
)
a.build()



def parse_mass_generator(file_path: str) -> MultipleAutoInstanceGenerator:
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract data from the JSON content
    instance_count = data.get('instance_count')
    central_locations = [(loc['latitude'], loc['longitude']) for loc in data.get('central_locations', [])]
    minimum_customers = data.get('minimum_customers')
    maximum_customers = data.get('maximum_customers')
    minimum_chargers = data.get('minimum_chargers')
    minimum_depots = data.get('minimum_depots')

    # Create an instance of MultipleInstanceGenerator
    return MultipleAutoInstanceGenerator(
        instance_count=instance_count,
        central_locations=central_locations,
        minimum_customers=minimum_customers,
        maximum_customers=maximum_customers,
        minimum_chargers=minimum_chargers,
        minimum_depots=minimum_depots
    )
