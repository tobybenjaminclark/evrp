class LocationNode():

    # Constructor Method for a Location Node
    def __init__(self, _latitude: float, _longitude: float, _name: str = '') -> None:
        self.latitude: float = _latitude
        self.longitude: float = _longitude
        self.label: str = _name
        self.id: str = None
        self.journeys: list[tuple[str, float]] = []

    def __repr__(self) -> str:
        return f"{self.label}\t@\t{self.latitude}, {self.longitude}"

    def set_id(self, typ: str, number: int) -> None:
        self.id = typ + str(number)

