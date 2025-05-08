import numpy as np
import matplotlib.pyplot as plt

# --- Cumulative trapezoidal integration ---
def cumtrapz_manual(y, x):
    cum_integral = np.zeros_like(y)
    for i in range(1, len(x)):
        dx = x[i] - x[i-1]
        cum_integral[i] = cum_integral[i-1] + 0.5 * (y[i] + y[i-1]) * dx
    return cum_integral

def plot_shear_force_by_section(x_val, x_sections, shear_force, t, ax):
    # Convert x_sections to numpy array if it's not already
    x_sections = np.array(x_sections)
    idx = np.argmin(np.abs(x_sections - x_val))
    
    ax.plot(t, shear_force[idx, :])
    ax.set_title(f'Shear Force vs Time at Section x = {x_sections[idx]:.2f} m')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Shear Force (N)')
    ax.grid(True)
    ax.set_facecolor('#f8f9fa')

def plot_shear_force_by_time(t_val, t, x_sections, shear_force, ax):
    # Convert x_sections to numpy array if it's not already
    x_sections = np.array(x_sections)
    idx = np.argmin(np.abs(t - t_val))
    
    ax.plot(x_sections, shear_force[:, idx])
    ax.set_title(f'Shear Force vs Section at Time t = {t[idx]:.2f} s')
    ax.set_xlabel('Section Position x (m)')
    ax.set_ylabel('Shear Force (N)')
    ax.grid(True)
    ax.set_facecolor('#f8f9fa')

def plot_bending_moment_by_section(x_val, x_sections, bending_moment, t, ax):
    # Convert x_sections to numpy array if it's not already
    x_sections = np.array(x_sections)
    idx = np.argmin(np.abs(x_sections - x_val))
    
    ax.plot(t, bending_moment[idx, :])
    ax.set_title(f'Bending Moment vs Time at Section x = {x_sections[idx]:.2f} m')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Bending Moment (Nm)')
    ax.grid(True)
    ax.set_facecolor('#f8f9fa')

def plot_bending_moment_by_time(t_val, t, x_sections, bending_moment, ax):
    # Convert x_sections to numpy array if it's not already
    x_sections = np.array(x_sections)
    idx = np.argmin(np.abs(t - t_val))
    
    ax.plot(x_sections, bending_moment[:, idx])
    ax.set_title(f'Bending Moment vs Section at Time t = {t[idx]:.2f} s')
    ax.set_xlabel('Section Position x (m)')
    ax.set_ylabel('Bending Moment (Nm)')
    ax.grid(True)
    ax.set_facecolor('#f8f9fa')
