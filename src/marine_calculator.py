import numpy as np

def calculate_shear_force_and_bending_moment(
    a33, b33, c33, a55, b55, c55, omega, Awl, M, I55, B_ML, section_positions, t
):
    rho = 1.025  # Sea water density (T/m³)
    g = 9.81     # Gravity (m/s²)

    omega_z = np.sqrt((rho * g * Awl) / (M + a33))
    omega_theta = np.sqrt((rho * g * M * B_ML) / (a55 + I55))

    G_heave = 1 / np.sqrt((1 - (omega / omega_z) ** 2) ** 2 +
                          (2 * (b33 / (2 * M * omega_z)) * (omega / omega_z)) ** 2)
    phi_heave = np.arctan2(2 * (b33 / (2 * M * omega_z)) * (omega / omega_z),
                           1 - (omega / omega_z) ** 2)

    G_pitch = 1 / np.sqrt((1 - (omega / omega_theta) ** 2) ** 2 +
                          (2 * (b55 / (2 * I55 * omega_theta)) * (omega / omega_theta)) ** 2)
    phi_pitch = np.arctan2(2 * (b55 / (2 * I55 * omega_theta)) * (omega / omega_theta),
                           1 - (omega / omega_theta) ** 2)

    x_heave = (1 / c33) * G_heave * np.cos(omega_z * t - phi_heave)
    x_pitch = (1 / c55) * G_pitch * np.cos(omega_theta * t - phi_pitch)

    dx_heave = -omega_z * (1 / c33) * G_heave * np.sin(omega_z * t - phi_heave)
    ddx_heave = -omega_z**2 * (1 / c33) * G_heave * np.cos(omega_z * t - phi_heave)

    dtheta = -omega_theta * (1 / c55) * G_pitch * np.sin(omega_theta * t - phi_pitch)
    ddtheta = -omega_theta**2 * (1 / c55) * G_pitch * np.cos(omega_theta * t - phi_pitch)

    shear_force = np.zeros((len(section_positions), len(t)))
    bending_moment = np.zeros_like(shear_force)

    section_positions = np.array(section_positions)

    for j in range(len(t)):
        z_x = x_heave[j] - section_positions * x_pitch[j]
        dz_x = dx_heave[j] - section_positions * dtheta[j]
        ddz_x = ddx_heave[j] - section_positions * ddtheta[j]
        integrand = a33 * ddz_x + b33 * dz_x + rho * g * z_x
        shear_force[:, j] = np.cumsum(integrand) * np.diff(section_positions, prepend=section_positions[0])

    for j in range(shear_force.shape[1]):
        bending_moment[:, j] = np.cumsum(shear_force[:, j]) * np.diff(section_positions, prepend=section_positions[0])

    return shear_force, bending_moment
