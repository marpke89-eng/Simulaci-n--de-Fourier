import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONTENEDOR DE CONFIGURACIÓN GLOBAL
# =============================================================================
Fs = 1000          # Frecuencia de muestreo (Hz) - 1000 muestras por segundo
T = 1 / Fs         # Período de muestreo (s)
L = 2000           # Longitud de la señal (Número de muestras)
t = np.arange(-L//2, L//2) * T  # Vector de tiempo centrado en cero (-1s a +1s)

# Vector de frecuencias para graficar el espectro centrado (fftshift)
frequencies = np.fft.fftshift(np.fft.fftfreq(L, T))

def calcular_espectro(signal):
    """Calcula la FFT centrada y normalizada en magnitud."""
    X_fft = np.fft.fft(signal)
    X_shifted = np.fft.fftshift(X_fft)
    # Normalizamos por la longitud L para que la magnitud guarde relación física
    magnitud = np.abs(X_shifted) / L 
    fase = np.angle(X_shifted)
    return magnitud, fase

# =============================================================================
# SEÑAL 1: PULSO RECTANGULAR & PROPIEDAD DE ESCALAMIENTO
# =============================================================================
# Pulso original (Ancho de 0.2 segundos)
pulso_original = np.where(np.abs(t) <= 0.1, 1.0, 0.0)
mag_pulso, _ = calcular_espectro(pulso_original)

# Propiedad de Escalamiento: Pulso más angosto en tiempo (Ancho 0.05 segundos)
# Al comprimir en tiempo, se debe expandir en frecuencia (y bajar su amplitud)
pulso_angosto = np.where(np.abs(t) <= 0.025, 1.0, 0.0)
mag_angosto, _ = calcular_espectro(pulso_angosto)

# =============================================================================
# SEÑAL 2: FUNCIÓN SENOIDAL & PROPIEDAD DE DESPLAZAMIENTO EN FRECUENCIA
# =============================================================================
f1 = 50   # Frecuencia de la primera onda (50 Hz)
f2 = 120  # Frecuencia de la segunda onda (120 Hz)

# Seno puro (50 Hz)
seno_puro = np.sin(2 * np.pi * f1 * t)
mag_seno, _ = calcular_espectro(seno_puro)

# Linealidad: Suma de dos componentes senoidales (50Hz + 120Hz)
senal_compuesta = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t)
mag_compuesta, _ = calcular_espectro(senal_compuesta)

# =============================================================================
# VISUALIZACIÓN DE RESULTADOS
# =============================================================================
plt.figure(figsize=(12, 10))

# Gráfica 1: Pulso Rectangular (Tiempo)
plt.subplot(3, 2, 1)
plt.plot(t, pulso_original, 'b', label='Ancho original')
plt.plot(t, pulso_angosto, 'r--', label='Comprimido')
plt.title('Señales en el Dominio del Tiempo (Pulso Rectangular)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.xlim([-0.5, 0.5])
plt.grid(True)
plt.legend()

# Gráfica 2: Espectro del Pulso (Frecuencia -> Función Sinc)
plt.subplot(3, 2, 2)
plt.plot(frequencies, mag_pulso, 'b', label='Espectro Original')
plt.plot(frequencies, mag_angosto, 'r--', label='Espectro Expandido')
plt.title('Dominio de la Frecuencia (Espectro Sinc)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.xlim([-50, 50])
plt.grid(True)
plt.legend()

# Gráfica 3: Seno Puro (Tiempo)
plt.subplot(3, 2, 3)
plt.plot(t, seno_puro, 'g')
plt.title('Señal Senoidal Pura (50 Hz)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.xlim([0, 0.1]) # Zoom para apreciar los ciclos
plt.grid(True)

# Gráfica 4: Espectro de Seno Puro (Frecuencia -> Impulsos)
plt.subplot(3, 2, 4)
plt.plot(frequencies, mag_seno, 'g')
plt.title('Espectro del Seno Puro (Deltas de Dirac a ±50 Hz)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.xlim([-150, 150])
plt.grid(True)

# Gráfica 5: Senal Compuesta (Tiempo)
plt.subplot(3, 2, 5)
plt.plot(t, senal_compuesta, 'm')
plt.title('Señal Compuesta (Linealidad: 50 Hz + 120 Hz)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.xlim([0, 0.1])
plt.grid(True)

# Gráfica 6: Espectro Combinado (Frecuencia)
plt.subplot(3, 2, 6)
plt.plot(frequencies, mag_compuesta, 'm')
plt.title('Espectro Combinado (Dos picos diferenciados)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.xlim([-150, 150])
plt.savefig('/Users/Admin/Desktop/graficas_fourier.png', dpi=300)

plt.show()
plt.grid(True)

plt.tight_layout()
plt.show()

