from math import cos

GRAVITATIONAL_CONSTANT: float = 9.8

# Calculate Rolling Resistance using fᵣ = cᵣ * m * g * cos(α)
def calculate_fᵣ(m: float, cᵣ: float, g: float) -> float:
    return cᵣ * m * GRAVITATIONAL_CONSTANT * cos(g)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
