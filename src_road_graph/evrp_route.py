from evrp_route_step import RouteStep, parse_step

class Route():
    def __init__(self, response: dict):
        print(response)
        self.steps: list[RouteStep] = map(parse_step, [step for route in response['routes'] for leg in route['legs'] for step in leg['steps']])
        for step in self.steps: print(str(step) + "\n")