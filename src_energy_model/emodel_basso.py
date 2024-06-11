from math import sin, cos

# Road Graph G_r = (V_r, A_r) (Set of Intersections and Set of links)
# To calculate the energy cost coefficients associated with the road network, G_r is preprocessed to create the cost
# graph G_c = (V_c, A_c) with V_c = V_r and each arc in A_c is composed of one or more adjacent links from A_r.
# every arc in the cost graph represents its respective cost coefficients.

# Each pair of nodes is onneted by a path P_ij formed by a set of consecutive links in the road graph.
# The customer graph is a complete and directed graph G = (V, A) with V = 0 U C U S, V subset Vc
# The depot is node 0, the set of customer nodes is C and set of harging customers by S

# So:
#   Road Graph is Gr (Graph Road)
#   Cost graph is Gc (Graph Cost)
#   Customer Graph is G

# Longitudinal Dynamics of vehicles (t is time!) [1]
#
# m * a(t) = F_t(t) - (F_g(t) + F_r(t) + F_a(t))
#
# m is the total vehicle mass (urb weight + payload)
# a(t) is the instantaneous acceleration (m/s^2)
# F_t(t) is the force generated by the powertrain/brakes
# F_g(t) is the gravity force on non-horizontal roads
# F_r(t) is rolling friction
# F_a(t) is the aerodynamic force

# The can be defined below
# F_g(t) = Gravitational Force   = m * g * sin * theta(t)
# F_r(t) = Rolling Friction      = m * g * C_r * cos * theta(t)
# F_a(t) = Aerodynamic Force     = 0.5 * C_d * A * p * v * (t)^2
#
# g is 9.81m/s^2
# theta(t) is the instantaneous road inclination angle
# C_r is rolling resistance coefficient
# C_d is the drag coefficient
# A is the frontal surface of the vehicle (m^2)
# P is the air density (kg/m^3)
# V(t) is the instantaneous speed (m/s)

# Mechanical Power Pm(t) needed to make the vehicle move, calculated by multiplying [1] by instantaneous speed.
# Pm(t) = m * a * v(t) + m * g * v(t) * sin * theta(t) + m * g * v(t) * C_r * cos * theta(t) + 0.5 * C_d * A * p * v(t)^3

def calculate_mechanical_power(m, a, v, C_r, theta, C_d, A, p, g = 9.81):
    return m * a * v + m * g * v * sin * theta + m * g * v * C_r * cos * theta + 0.5 * C_d * A * p * v^3