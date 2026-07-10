import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, tensor, qeye, sigmaz, sigmax, ket2dm, mesolve, expect

def run_phase2_space_sensor_simulation():
    print("Initializing Phase 2: Dual Magnetic & Gravitational Space Sensor Simulation...")

    # 1. TIME VECTOR CONFIGURATION
    t_max = 5.0
    steps = 500
    times = np.linspace(0, t_max, steps)

    # 2. DEFINE THE INITIAL 4-ATOM ENTANGLED STATE (GHZ State)
    state_0 = basis(2, 0)
    state_1 = basis(2, 1)

    zero_combination = tensor(state_0, state_0, state_0, state_0)
    one_combination  = tensor(state_1, state_1, state_1, state_1)

    psi_initial = (zero_combination + one_combination).unit()
    rho_initial = ket2dm(psi_initial)

    # 3. ENVIRONMENT & SIGNAL VARIABLES
    gamma_solar_wind = 0.15  # Baseline Deep Space Noise
    B_field = 1.2            # Phase 1: Magnetic Vector
    G_anomaly = 0.8          # Phase 2: New Gravitational / Acceleration Vector

    # 4. DEFINE THE COMBINED HAMILTONIAN
    # Magnetic field alters the spin state (sigmaz)
    H_magnetic = B_field * (
        tensor(qeye(2), qeye(2), sigmaz(), qeye(2)) +
        tensor(qeye(2), qeye(2), qeye(2), sigmaz())
    )

    # Gravitational acceleration induces a kinetic state coupling (sigmax)
    # This simulates the physical displacement/stretching of the wave packet
    H_gravitational = G_anomaly * (
        tensor(qeye(2), qeye(2), sigmax(), qeye(2)) +
        tensor(qeye(2), qeye(2), qeye(2), sigmax())
    )

    # Total system Hamiltonian acting on the probe
    H_total = H_magnetic + H_gravitational

    # Environmental Noise (Dephasing)
    L_noise_atom2 = np.sqrt(gamma_solar_wind) * tensor(qeye(2), qeye(2), sigmaz(), qeye(2))
    L_noise_atom3 = np.sqrt(gamma_solar_wind) * tensor(qeye(2), qeye(2), qeye(2), sigmaz())
    collapse_operators = [L_noise_atom2, L_noise_atom3]

    # 5. EXECUTE COMPUTATION ENGINE
    result = mesolve(H_total, rho_initial, times, collapse_operators)

    # 6. POST-PROCESSING: MANUALLY COMPUTE ENTAGLEMENT FIDELITY
    fidelity_operator = ket2dm(psi_initial)
    fidelity_data = [expect(fidelity_operator, state) for state in result.states]

    # 7. DATA PLOTTING & VISUALIZATION
    plt.figure(figsize=(10, 6))
    plt.plot(times, fidelity_data, label='Combined Mag+Grav Fidelity', color='#2ca02c', linewidth=2.5)
    plt.axhline(y=0.5, color='r', linestyle='--', label='Classical Limit Threshold (0.5)')

    plt.title('Phase 2 Simulation: Dual Field Sensing (Gravity + Magnetics)', fontsize=14, fontweight='bold')
    plt.xlabel('Mission Exposure Time (Seconds)', fontsize=12)
    plt.ylabel('Quantum State Fidelity', fontsize=12)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.ylim(-0.05, 1.05)
    plt.legend(loc='upper right', fontsize=11)

    print("Phase 2 Simulation complete. Displaying data plots...")
    plt.show()

if __name__ == "__main__":
    run_phase2_space_sensor_simulation()
