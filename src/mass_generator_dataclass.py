import json
from dataclasses import dataclass
from scipy.stats import truncnorm
from generator_dataclass import Generator, DepotNodeGenerator, CustomerNodeGenerator, EVChargePointNodeGenerator
from random import choice

def generate_truncated_normal_samples(min_val: float, max_val: float, n: int, std_dev: float = 3.0) -> list[float]:
    return truncnorm.rvs((min_val - (min_val + max_val) / 2) / std_dev,
                         (max_val - (min_val + max_val) / 2) / std_dev,
                         loc = (min_val + max_val) / 2,
                         scale = std_dev,
                         size = n)

@dataclass
class MultipleInstanceGenerator:

    instance_count: int

    central_locations: list[tuple[float, float]]

    minimum_customers: int
    maximum_customers: int

    minimum_chargers: int
    maximum_chargers: int

    minimum_depots: int
    maximum_depots: int

    # sampling types i.e. clustered, random clustered etc...
    time_window_generation_type: int
    customer_generation_type: int
    charger_generation_type: int
    depot_generation_type: int

    def build(self) -> list[Generator]:

        # Get a nomral distributor of customer counts.
        cust_c = generate_truncated_normal_samples(self.minimum_customers, self.maximum_customers, self.instance_count)
        cust_c = [int(max(self.minimum_customers, min(self.maximum_customers, c))) for c in cust_c]

        # Get a normal distribution of charger counts.
        charge_c = generate_truncated_normal_samples(self.minimum_chargers, self.maximum_chargers, self.instance_count)
        charge_c = [int(max(self.minimum_chargers, min(self.maximum_chargers, c))) for c in charge_c]

        # Get a normal distribution of depot counts.
        depot_c  = generate_truncated_normal_samples(self.minimum_depots, self.maximum_depots, self.instance_count)
        depot_c = [int(max(self.minimum_depots, min(self.maximum_depots, c))) for c in depot_c]

        # Get random locations
        locations = [choice(self.central_locations) for _ in range(self.instance_count)]


        print(cust_c)
        print(charge_c)
        print(depot_c)


a = MultipleInstanceGenerator(
    10,
    ["Nottingham"],
    10,
    20,
    10,
    20,
    10,
    20,
)
a.build()



def parse_mass_generator(file_path: str) -> MultipleInstanceGenerator:
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
    return MultipleInstanceGenerator(
        instance_count=instance_count,
        central_locations=central_locations,
        minimum_customers=minimum_customers,
        maximum_customers=maximum_customers,
        minimum_chargers=minimum_chargers,
        minimum_depots=minimum_depots
    )
