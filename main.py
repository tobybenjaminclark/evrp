from math import cos, sin

GRAVITATIONAL_CONSTANT: float = 9.8

# Calculate Rolling Resistance using fᵣ = cᵣ * m * g * cos(α)
def calculate_rolling_resistance(mass: float, friction_coefficient: float, gradient: float) -> float:
    return friction_coefficient * mass * GRAVITATIONAL_CONSTANT * cos(gradient)

# Calculate aerodynamic resistance
def calculate_air_resistance(speed: float, drag_coefficient: float, air_density: float, frontal_area: float) -> float:
    return (1 / 2) * air_density * frontal_area * drag_coefficient * (speed ** 2)

# Calculate total mechanical power needed
def calculate_total_mechanical_power(mass: float, acceleration: float, drag_coefficient: float, air_density: float, frontal_area: float, speed: float, gradient: float, friction_coefficient: float) -> float:
    return (mass * acceleration + calculate_air_resistance(speed, drag_coefficient, air_density, frontal_area) + mass * GRAVITATIONAL_CONSTANT * sin(gradient) + calculate_rolling_resistance(mass, friction_coefficient, gradient)) * speed

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
