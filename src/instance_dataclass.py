from dataclasses import dataclass
import csv


@dataclass
class CustomerInstance():
    """ Class representing an output instance for a `customer` node in an EVRP Benchmark. """

    demand: float
    start_time: int
    end_time: int
    id: str
    journeys_energy: list[tuple[str, float]]
    journeys_time: list[tuple[str, int]]



@dataclass
class DepotInstance():
    """ Class representing an output instance for a `depot` node in an EVRP Benchmark. """

    id: str
    journeys_energy: list[tuple[str, float]]
    journeys_time: list[tuple[str, int]]



@dataclass
class EVChargeInstance:
    """ Class representing an output instance for a `charger` node in an EVRP Benchmark. """

    charge_rate: float
    id: str
    journeys_energy: list[tuple[str, float]]
    journeys_time: list[tuple[str, int]]



@dataclass
class Instance():
    """ Class representing an output instance for in an EVRP Benchmark. """

    customers: list[CustomerInstance]
    depots: list[DepotInstance]
    chargers: list[EVChargeInstance]
    generator: "Generator"

    def write(self, file_path: str = ""):

        nodes = self.customers +  self.depots +  self.chargers
        node_ids = [node.id for node in nodes]

        # Create an initial matrix with infinite values, except for the diagonal
        matrix = {node_id: {nid: 0 if nid == node_id else float('inf') for nid in node_ids} for node_id in node_ids}
        time_matrix = {node_id: {nid: 0 if nid == node_id else float('inf') for nid in node_ids} for node_id in
                       node_ids}

        # Populate matrices with energy consumption and time taken
        for node in nodes:
            for dest_id, energy in node.journeys_energy:
                matrix[node.id][dest_id] = energy
            for dest_id, time_taken in node.journeys_time:
                time_matrix[node.id][dest_id] = time_taken

        # Initialize the location matrix with demand values
        location_matrix = {node.id: {'demand': 0, 'start_of_slot': 0, 'end_of_slot': 0} for node in self.customers}
        for cnode in self.customers:
            location_matrix[cnode.id]['demand'] = cnode.demand
            location_matrix[cnode.id]['start_of_slot'] = cnode.start_time
            location_matrix[cnode.id]['end_of_slot'] = cnode.end_time

        # Write to CSV
        csvfile = open(file_path + self.generator.instance_id + ".csv", 'w', newline='')

        writer = csv.writer(csvfile)

        # Write customer demands
        writer.writerow(['Customer Demand'])
        writer.writerow(['Node ID', 'Demand', 'Start of Time Slot', 'End of Time Slot'])
        for node_id in location_matrix.keys():
            writer.writerow([node_id, location_matrix[node_id]['demand'], location_matrix[node_id]['start_of_slot'],
                             location_matrix[node_id]['end_of_slot']])

        # Write EC matrix header
        writer.writerow([])  # Empty line for separation
        writer.writerow(['EC Matrix'])
        writer.writerow([''] + node_ids)  # Header row
        for node_id in node_ids:
            row = [node_id] + [matrix[node_id][nid] for nid in node_ids]
            writer.writerow(row)

        # Write time matrix header
        writer.writerow([])  # Empty line for separation
        writer.writerow(['Time Matrix'])
        writer.writerow([''] + node_ids)  # Header row
        for node_id in node_ids:
            row = [node_id] + [time_matrix[node_id][nid] for nid in node_ids]
            writer.writerow(row)

        csvfile.close()



