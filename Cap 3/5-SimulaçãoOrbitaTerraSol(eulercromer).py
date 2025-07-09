import numpy as np
import matplotlib.pyplot as plt

# === CONSTANTES ===
G = 4 * np.pi**2  # AU^3 / (ano^2 * massa solar)

# Condições iniciais
r = np.array([1.0, 0.0])         # posição inicial (AU)
v = np.array([0.0, 2 * np.pi])   # vel. inicial (AU/ano)

dt = 0.001  # passo de tempo (anos)
n_steps = int(1 / dt * 10)  # simular 10 anos

# Armazenar trajetória
trajetoria = [r.copy()]

# === MÉTODO DE EULER-CROMER ===
r = np.array([1.0, 0.0])
v = np.array([0.0, 2 * np.pi])
trajetoria_ec = [r.copy()]

for _ in range(n_steps):
    distancia = np.linalg.norm(r)
    a = -G * r / distancia**3
    v += a * dt       # atualiza primeiro a velocidade
    r += v * dt       # depois a posição
    trajetoria_ec.append(r.copy())

trajetoria_ec = np.array(trajetoria_ec)

# === GRÁFICO ===
plt.figure(figsize=(6,6))
plt.plot(trajetoria_ec[:, 0], trajetoria_ec[:, 1], label='Euler-Cromer')
plt.plot(0, 0, 'yo', label='Sol')
plt.xlabel('x (AU)')
plt.ylabel('y (AU)')
plt.title('Órbita da Terra (Euler-Cromer)')
plt.legend()
plt.grid(True)
plt.axis("equal")
plt.show()
