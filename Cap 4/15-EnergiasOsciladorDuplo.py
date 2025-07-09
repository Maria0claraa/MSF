import numpy as np
import matplotlib.pyplot as plt

# Constantes do problema
k = 1.0       # Constante elástica (N/m)
m = 1.0       # Massa (kg)
x0 = 2.0      # Ponto de equilíbrio (m)
dt = 0.001    # Passo de tempo
t_max = 20.0  # Tempo total de simulação
n = int(t_max / dt)

# Energia potencial do oscilador duplo
def energia_potencial(x):
    return 0.5 * k * (np.abs(x) - x0)**2

# Força derivada da energia potencial
def forca(x):
    if x >= 0:
        return -k * (x - x0)
    else:
        return k * (-x - x0)

# Simulação do movimento via Euler-Cromer
def simular_movimento(E_total):
    x = np.sqrt(2 * E_total / k) + x0  # posição inicial máxima
    v = 0.0
    x_list = []
    t_list = []

    for i in range(n):
        t = i * dt
        F = forca(x)
        a = F / m
        v += a * dt
        x += v * dt
        x_list.append(x)
        t_list.append(t)

    x_array = np.array(x_list)
    t_array = np.array(t_list)
    A = (np.max(x_array) - np.min(x_array)) / 2

    # Estimar frequência pelas passagens pelo ponto médio
    x_mean = (np.max(x_array) + np.min(x_array)) / 2
    zero_crossings = np.where(np.diff(np.signbit(x_array - x_mean)))[0]
    if len(zero_crossings) > 1:
        periods = np.diff(t_array[zero_crossings])
        freq = 1 / (2 * np.mean(periods))  # 2 cruzamentos por ciclo
    else:
        freq = 0

    return t_array, x_array, A, freq

# a) Gráfico da energia potencial
x_vals = np.linspace(-5, 5, 1000)
U_vals = energia_potencial(x_vals)

# b), c), d) Simulação com diferentes energias
energias = [0.75, 1.0, 1.5]
resultados = {}
for E in energias:
    resultados[E] = simular_movimento(E)

# Plot dos resultados
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# a) Diagrama de energia potencial
axs[0, 0].plot(x_vals, U_vals, label="Energia Potencial", color='orange')
for E in energias:
    axs[0, 0].axhline(E, linestyle='--', label=f"E = {E} J")
axs[0, 0].set_title("a) Diagrama de Energia Potencial")
axs[0, 0].set_xlabel("Posição (m)")
axs[0, 0].set_ylabel("Energia Potencial (J)")
axs[0, 0].legend()

# b), c), d) Movimento para diferentes energias
for i, E in enumerate(energias):
    row, col = divmod(i+1, 2)
    t_array, x_array, A, f = resultados[E]
    axs[row, col].plot(t_array, x_array, label=f"Amplitude: {A:.2f} m, f: {f:.2f} Hz", color='orange')
    axs[row, col].set_title(f"{chr(98+i)}) Movimento para E = {E} J")
    axs[row, col].set_xlabel("Tempo (s)")
    axs[row, col].set_ylabel("Posição (m)")
    axs[row, col].legend()

plt.tight_layout()
plt.show()
