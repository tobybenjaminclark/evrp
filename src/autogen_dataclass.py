from dataclasses import dataclass
from generator_dataclass import Generator, DepotNodeGenerator, CustomerNodeGenerator, EVChargePointNodeGenerator

def generate_customers_random(count: int) -> list[CustomerNodeGenerator]:
    return []

def generate_customers_clustered(count: int) -> list[CustomerNodeGenerator]:
    return []

def generate_customers_realistic(count: int, centre: tuple[float, float]) -> list[CustomerNodeGenerator]:
    return []

def generate_customers(customer_sampling: str, customer_count: int, centre: tuple[float, float]) -> list[CustomerNodeGenerator]:
    match customer_sampling:
        case "R":
            return generate_customers_random(customer_count)
        case "C":
            return generate_customers_clustered(customer_count)
        case "RL":
            return generate_customers_realistic(customer_count, centre)
        case "R_C":
            random_count = customer_count // 2
            clustered_count = customer_count - random_count
            return generate_customers_random(random_count) + generate_customers_clustered(clustered_count)
        case "R_RL":
            random_count = customer_count // 2
            realistic_count = customer_count - random_count
            return generate_customers_random(random_count) + generate_customers_realistic(realistic_count, centre)
        case "C_RL":
            clustered_count = customer_count // 2
            realistic_count = customer_count - clustered_count
            return generate_customers_clustered(clustered_count) + generate_customers_realistic(realistic_count, centre)
        case "R_C_RL":
            random_count = customer_count // 3
            clustered_count = (customer_count - random_count) // 2
            realistic_count = customer_count - random_count - clustered_count
            return generate_customers_random(random_count) + generate_customers_clustered(clustered_count) + generate_customers_realistic(realistic_count, centre)
        case _:
            raise Exception("Customer sampling does not match any of predefined constants.")

@dataclass
class AutoGenerator:

    customer_count: int
    depot_count: int
    charger_count: int

    central_location: tuple[float, float]
    range: int

    # Sampling Types
    customer_sampling: str
    depot_sampling: str
    charger_sampling: str

    # Time Window Sampling
    time_window_gen: str
    time_window_type: str

    def build(self) -> Generator:
        pass