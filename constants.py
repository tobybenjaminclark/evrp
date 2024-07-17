# Constants
g = 9.81  # Acceleration due to gravity in m/s^2
mu = 0.3  # Coefficient of friction (example value, adjust as needed)
R = 6371.0  # Earth's radius in kilometers


# mechanical power is
# m * a * v(t) + m * g * v(t) * sin theta(t) + m * g * v(t) * cr * cos * theta(t) + 0.5 * cd * A * p * v(t)^3

cr = 0.0064         # rolling resistance, from basso
cd = 0.7            # air drag , basso
A = 8.0             # vehicle frontal area (in metres squared) , basso
p = 1.2             # air density in kg/m^3

# m is vehicle mass
# a is instantaneous vehicle acceleration
# v, v(t) is vehicle speed
# theta is road angle (in degrees)

import re
print(bool(re.match(r'[+-]?([0-9]*[.])?[0-9]+', "0")))
print(bool(re.match(r'[+-]?([0-9]*[.])?[0-9]+', "312314123.4234232423")))