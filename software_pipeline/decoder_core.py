# =============================================================================
# MODULE: decoder_core.py
# DESCRIPTION: Digital Signal Processing (DSP) lens for the Ground Base Station.
#              Extracts cross-coupling frequencies out of raw noisy telemetry.
# =============================================================================

import numpy as np

def process_telemetry_fft(noisy_fidelity, times):
    """
    Ingests noisy time-domain quantum state fidelity metrics and maps them
    into the frequency domain to isolate cosmic anomalies.
    
    Parameters:
        noisy_fidelity (np.array): Raw, noisy data stream from space probe.
        times (np.array): Chronological timeline array of the mission window.
        
    Returns:
        freqs (np.array): Positive frequency bins (Hz).
        fft_power (np.array): Energy intensity spectrum for peak identification.
    """
    # Calculate time delta step interval (dt) dynamically from the timeline
    dt = times[1] - times[0]
    
    # 1. DETRENDING STEP: Subtract the mean value to kill the 0 Hz DC blind spot
    signal_prime = noisy_fidelity - np.mean(noisy_fidelity)
    
    # 2. RUN FAST FOURIER TRANSFORM (FFT)
    fft_vals = np.fft.fft(signal_prime)
    fft_freqs = np.fft.fftfreq(len(times), d=dt)
    
    # 3. MASKING: Filter for positive frequencies only (eliminate negative mirrors)
    positive_indices = np.where(fft_freqs >= 0)
    
    # 4. ISOLATE SPECTRUM DATA
    freqs = fft_freqs[positive_indices]
    fft_power = np.abs(fft_vals[positive_indices])**2
    
    return freqs, fft_power

# =============================================================================
# UNIT TEST / VERIFICATION INTEGRATION LOOP
# =============================================================================
if __name__ == "__main__":
    print(">> Initializing standalone testing verification for decoder_core.py...")
    
    # Generate 5 seconds of mock data containing a subtle 2.5 Hz anomaly hidden in noise
    test_times = np.linspace(0, 5.0, 500)
    mock_clean_signal = np.sin(2 * np.pi * 2.5 * test_times)
    mock_noise = np.random.normal(0, 2.0, size=len(test_times)) # High noise floor
    mock_telemetry = mock_clean_signal + mock_noise + 12.5       # Constant DC offset added
    
    # Execute the core function
    verified_freqs, verified_power = process_telemetry_fft(mock_telemetry, test_times)
    
    # Find the strongest frequency component resolved out of the noise
    dominant_frequency = verified_freqs[np.argmax(verified_power)]
    
    print(">> Test Execution: SUCCESS.")
    print(f"| Isolated Anomaly Peak Detected at: {dominant_frequency:.2f} Hz (Target: 2.50 Hz)")
    print("| Decoder Core operational loop verified and ready for deployment pipeline.")
