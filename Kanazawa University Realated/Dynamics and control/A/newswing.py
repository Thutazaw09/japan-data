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
c = 200.0       # radial damping coefficient [N·s/m]

# "Stop & swing" control parameters
swing_duration = 3.0   # seconds of free swinging
stop_duration = 2.0    # seconds of stopping/holding
cycle_duration = swing_duration + stop_duration

# Strong "controller" to stop the swing (tangential direction)
k_stop = 50.0          # angular stiffness during stop [N·m/rad approx]
c_stop = 20.0          # angular damping during stop [N·m·s/rad approx]


def mode_function(t):
    """
    Return 'swing' or 'stop' depending on time.
    One cycle = [0, swing_duration) -> swing
                [swing_duration, cycle_duration) -> stop
    and then repeat periodically.
    """
    tau = t % cycle_duration
    if tau < swing_duration:
        return "swing"
    else:
        return "stop"


# -----------------------------
# Equations of motion
# y = [theta, theta_dot, x, x_dot]
# -----------------------------
def swing_eom(t, y):
    theta, theta_dot, x, x_dot = y

    r = L0 + x  # instantaneous rope length
    if r < 1e-6:
        r = 1e-6

    # Base (free) dynamics
    theta_ddot_free = (-g * np.sin(theta) - 2.0 * x_dot * theta_dot) / r
    x_ddot = g * np.cos(theta) - (k/m) * x - (c/m) * x_dot + r * theta_dot**2

    # Determine mode: "swing" or "stop"
    mode = mode_function(t)

    if mode == "swing":
        # Free swing, no extra control
        theta_ddot = theta_ddot_free
    else:
        # Stop mode: add strong restoring + damping torque toward theta = 0
        # This is like someone actively holding/braking the swing.
        #
        # Extra tangential "control" term:
        # tau_ctrl ~ -k_stop * theta - c_stop * theta_dot
        # -> contributes as +tau_ctrl / (m * r) to tangential acceleration.
        tau_ctrl = -k_stop * theta - c_stop * theta_dot
        a_theta_ctrl = tau_ctrl / (m * r)

        theta_ddot = theta_ddot_free + a_theta_ctrl

    return [theta_dot, theta_ddot, x_dot, x_ddot]


# -----------------------------
# Initial conditions
# -----------------------------
theta0 = 0.4         # initial angle [rad]
theta_dot0 = 0.0     # initial angular velocity [rad/s]
x0 = 0.0             # initial rope extension [m]
x_dot0 = 0.0         # initial extension rate [m/s]

y0 = [theta0, theta_dot0, x0, x_dot0]

# -----------------------------
# Time span for simulation
# -----------------------------
t_start = 0.0
t_end = 30.0       # longer to see several stop/swing cycles
t_eval = np.linspace(t_start, t_end, 6000)

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
plt.figure(figsize=(10, 5))
plt.plot(t, theta)
plt.xlabel("Time [s]")
plt.ylabel("Angle θ [rad]")
plt.title("Swing Angle vs Time (Stop & Swing Alternating)")
plt.grid(True)

plt.figure(figsize=(10, 5))
plt.plot(t, x * 1000)
plt.xlabel("Time [s]")
plt.ylabel("Rope Extension x [mm]")
plt.title("Rope Extension vs Time (Stop & Swing Alternating)")
plt.grid(True)

plt.show()
