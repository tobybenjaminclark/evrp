from math import cos, sin
from typing import TypeAlias

# Type Alias for units
Kilowatt: TypeAlias = float
Kilogram: TypeAlias = float

# Φd : Efficiency Parameter (motor mode)
# Φr : Efficiency Parameter (generator mode)
Φd: float = 1.184692
Φr: float = 0.846055

# φd : Efficiency Parameter (for discharging)
# φr : Efficiency Parameter (for recuperation)
φd: float = 1.112434
φr: float = 0.928465

GRAVITATIONAL_CONSTANT: float = 9.8

# Calculate Rolling Resistance using fᵣ = cᵣ * m * g * cos(α)
def calculate_rolling_resistance(mass: Kilogram, friction_coefficient: float, gradient: float) -> float:
    return friction_coefficient * mass * GRAVITATIONAL_CONSTANT * cos(gradient)

# Calculate aerodynamic resistance
def calculate_air_resistance(speed: float, drag_coefficient: float, air_density: float, frontal_area: float) -> float:
    return (1 / 2) * air_density * frontal_area * drag_coefficient * (speed ** 2)

# Calculate total mechanical power needed
def calculate_total_mechanical_power(mass: Kilogram, acceleration: float, drag_coefficient: float, air_density: float, frontal_area: float, speed: float, gradient: float, friction_coefficient: float) -> float:
    return (mass * acceleration + calculate_air_resistance(speed, drag_coefficient, air_density, frontal_area) + mass * GRAVITATIONAL_CONSTANT * sin(gradient) + calculate_rolling_resistance(mass, friction_coefficient, gradient)) * speed

# Calculate electric power required
def calculate_electric_power(mechanical_power: Kilowatt) -> Kilowatt | ValueError:
    return (Φd * mechanical_power if mechanical_power in range(0,100) else (Φr * mechanical_power if mechanical_power in range(-100, 0) else ValueError))

# Calculate battery power required
def calculate_battery_power(electric_power: Kilowatt) -> Kilowatt:
    return (φd * electric_power if electric_power >= 0 else φr * electric_power)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
