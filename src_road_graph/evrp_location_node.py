class LocationNode():

    # Constructor Method for a Location Node
    def __init__(self, _latitude: float, _longitude: float, _name: str = '', rating: float|None = None) -> None:
        self.demand: float = rating
        self.latitude: float = _latitude
        self.longitude: float = _longitude
        self.label: str = _name
        self.id: str = None
        self.journeys: list[tuple[str, float]] = []
        self.time_slot: tuple[int, int] = [0, 0]

    def set_time_slot(self, start_time: int, end_time: int) -> None:
        self.time_slot = (start_time, end_time)

    def __repr__(self) -> str:
        return f"{self.label}\t@\t{self.latitude}, {self.longitude}"

    def set_id(self, typ: str, number: int) -> None:
        self.id = typ + str(number)

