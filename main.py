from math import cos, sin

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
def calculate_rolling_resistance(mass: float, friction_coefficient: float, gradient: float) -> float:
    return friction_coefficient * mass * GRAVITATIONAL_CONSTANT * cos(gradient)

# Calculate aerodynamic resistance
def calculate_air_resistance(speed: float, drag_coefficient: float, air_density: float, frontal_area: float) -> float:
    return (1 / 2) * air_density * frontal_area * drag_coefficient * (speed ** 2)

# Calculate total mechanical power needed
def calculate_total_mechanical_power(mass: float, acceleration: float, drag_coefficient: float, air_density: float, frontal_area: float, speed: float, gradient: float, friction_coefficient: float) -> float:
    return (mass * acceleration + calculate_air_resistance(speed, drag_coefficient, air_density, frontal_area) + mass * GRAVITATIONAL_CONSTANT * sin(gradient) + calculate_rolling_resistance(mass, friction_coefficient, gradient)) * speed

# Calculate electric power
def calculate_electric_power(pm: float) -> float | ValueError:
    return (Φd * pm if pm in range(0,100) else (Φr * pm if pm in range(-100, 0) else ValueError))

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
