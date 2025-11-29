import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# -----------------------------
# Parameters
# -----------------------------
m = 30.0        # mass [kg]
g = 9.81        # gravity [m/s^2]
L0 = 2.0        # natural rope length [m]
k = 10000.0     # spring stiffness [N/m]
c = 200.0       # damping coefficient [N·s/m]

# -----------------------------
# Equations of motion
# y = [theta, theta_dot, x, x_dot]
# -----------------------------


def swing_eom(t, y):
    theta, theta_dot, x, x_dot = y

    r = L0 + x  # instantaneous rope length

    # Avoid division by zero if r becomes too small
    if r < 1e-6:
        r = 1e-6

    # Equations
    theta_ddot = (-g * np.sin(theta) - 2.0 * x_dot * theta_dot) / r
    x_ddot = g * np.cos(theta) - (k/m) * x - (c/m) * x_dot + r * theta_dot**2

    return [theta_dot, theta_ddot, x_dot, x_ddot]


# -----------------------------
# Initial conditions
# -----------------------------
theta0 = 0.3         # initial angle [rad] ~ 17 deg
theta_dot0 = 0.0     # initial angular velocity [rad/s]
x0 = 0.0             # initial rope extension [m]
x_dot0 = 0.0         # initial extension rate [m/s]

y0 = [theta0, theta_dot0, x0, x_dot0]

# -----------------------------
# Time span for simulation
# -----------------------------
t_start = 0.0
t_end = 20.0       # simulate 20 seconds
t_eval = np.linspace(t_start, t_end, 4000)  # output times

# -----------------------------
# Solve ODE
# -----------------------------
sol = solve_ivp(
    swing_eom,
    (t_start, t_end),
    y0,
    t_eval=t_eval,
    method="RK45",
    rtol=1e-8,
    atol=1e-8
)

t = sol.t
theta = sol.y[0]
theta_dot = sol.y[1]
x = sol.y[2]
x_dot = sol.y[3]

# -----------------------------
# Compute trajectory in Cartesian coordinates
# -----------------------------
r = L0 + x
x_cart = r * np.sin(theta)
y_cart = -r * np.cos(theta)

# -----------------------------
# Plot results
# -----------------------------

plt.figure(figsize=(10, 6))
plt.plot(t, theta)
plt.xlabel("Time [s]")
plt.ylabel("Angle θ [rad]")
plt.title("Swing Angle vs Time")
plt.grid(True)

plt.figure(figsize=(10, 6))
plt.plot(t, x * 1000)  # mm for visibility
plt.xlabel("Time [s]")
plt.ylabel("Rope Extension x [mm]")
plt.title("Rope Extension vs Time")
plt.grid(True)

plt.figure(figsize=(6, 6))
plt.plot(x_cart, y_cart)
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Trajectory of the Mass")
plt.axis("equal")
plt.grid(True)

plt.show()


# no (3)
