from dataclasses import dataclass, field
from typing import List, Tuple, Optional



@dataclass
class LocationNodeBase:
    """
    Base class for nodes in the Electric Vehicle Routing Problem (EVRP) representing locations.

    Attributes:
        latitude (float): The latitude of the node's location.
        longitude (float): The longitude of the node's location.
        label (str): A descriptive label for the node. Default is "Empty".
        journeys (List[Tuple[str, float]]): A list of journeys originating from this node, where each journey
                                            is represented as a tuple containing the destination node ID and the distance.
                                            Default is an empty list.
        id (Optional[str]): An optional unique identifier for the node. Default is None.
    """
    latitude: float
    longitude: float
    label: str = "Empty"
    journeys: List[Tuple[str, float]] = field(default_factory=list)
    id: Optional[str] = None



@dataclass
class CustomerNode:
    """
    Represents a customer node in the EVRP with a specific demand and time constraints.

    Attributes:
        latitude (float): The latitude of the customer location.
        longitude (float): The longitude of the customer location.
        time_slot (Tuple[int, int]): The time window during which service can be provided to the customer,
                                     represented as a tuple of start and end times (in hours).
        demand (float): The demand or required delivery quantity at this customer location.
        journeys (List[Tuple[str, float]]): A list of journeys originating from this customer node,
                                            represented as tuples of destination ID and distance. Default is an empty list.
        id (Optional[str]): An optional unique identifier for the customer node. Default is None.
        label (str): A descriptive label for the customer node. Default is "Empty".
    """
    latitude: float
    longitude: float
    time_slot: Tuple[int, int]
    demand: float
    journeys: List[Tuple[str, float]] = field(default_factory=list)
    id: Optional[str] = None
    label: str = "Empty"



@dataclass
class DepotNode:
    """
    Represents a depot node in the EVRP, typically the starting and ending point for vehicles.

    Attributes:
        latitude (float): The latitude of the depot location.
        longitude (float): The longitude of the depot location.
        label (str): A descriptive label for the depot node. Default is "Empty".
    """
    latitude: float
    longitude: float
    label: str = "Empty"



@dataclass
class EVChargeNode:
    """
    Represents an electric vehicle charging station node in the EVRP.

    Attributes:
        latitude (float): The latitude of the charging station location.
        longitude (float): The longitude of the charging station location.
        charge_rate (float): The rate at which vehicles can be charged at this station, typically in kW.
        journeys (List[Tuple[str, float]]): A list of journeys originating from this charging station node,
                                            represented as tuples of destination ID and distance. Default is an empty list.
        id (Optional[str]): An optional unique identifier for the charging station node. Default is None.
        label (str): A descriptive label for the charging station node. Default is "Empty".
    """
    latitude: float
    longitude: float
    charge_rate: float
    journeys: List[Tuple[str, float]] = field(default_factory=list)
    id: Optional[str] = None
    label: str = "Empty"
