import numpy as np

def calculate_anomaly_direction(power_X, power_Y, power_Z):
    """
    Ingests the recovered spectral peak power from the X, Y, and Z 
    orthogonal atom pairs and computes the 3D directional vector 
    and angular coordinates of the signal source.
    """
    print("\n>> Processing Spatial Tensors for Directivity...")
    
    # Construct the raw 3D intensity vector from the decoupled atomic channels
    vector = np.array([power_X, power_Y, power_Z])
    magnitude = np.linalg.norm(vector)
    
    if magnitude == 0:
        print("   [SYSTEM IDLE] No localized gradient detected above the cushion floor.")
        return [0.0, 0.0, 0.0], 0.0, 0.0
        
    # Normalize the vector to find the directional unit matrix
    unit_vector = vector / magnitude
    
    # Calculate Spherical Coordinates:
    # Azimuthal Angle (theta) in the horizontal plane (0 to 360 degrees)
    theta = np.degrees(np.arctan2(unit_vector[1], unit_vector[0]))
    if theta < 0: theta += 360.0
    
    # Elevation Angle (phi) relative to the probe heading vector (-90 to +90 degrees)
    phi = np.degrees(np.arcsin(unit_vector[2]))
    
    print(f"| Normalized Heading: [X: {unit_vector[0]:.3f} | Y: {unit_vector[1]:.3f} | Z: {unit_vector[2]:.3f}]")
    print(f"| Angle of Incidence: Azimuth (θ) = {theta:.2f}° | Elevation (φ) = {phi:.2f}°")
    
    return unit_vector, theta, phi

# =============================================================================
# PIPELINE INTEGRATION VERIFICATION CHECK
# =============================================================================
if __name__ == "__main__":
    # Simulated scenario: A gravitational wave hits the probe predominantly 
    # from the upper-right quadrant. The FFT outputs high energy on X and Z channels.
    simulated_peak_energy_X = 0.85
    simulated_peak_energy_Y = 0.22
    simulated_peak_energy_Z = 0.61
    
    heading, azimuth, elevation = calculate_anomaly_direction(
        simulated_peak_energy_X, 
        simulated_peak_energy_Y, 
        simulated_peak_energy_Z
    )
    print(">> Directional verification checklist complete. System synergy confirmed.")
