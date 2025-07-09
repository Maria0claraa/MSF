import numpy as np
import matplotlib.pyplot as plt

# Constantes
k = 1  # N/m
m = 1  # kg
omega = np.sqrt(k / m)

# Condições iniciais
x = 4.0
v = 0.0

# Tempo
dt = 0.01
t_max = 20
n = int(t_max / dt)
tempos = np.linspace(0, t_max, n)
xs = []
vs = []

# Euler-Cromer
for t in tempos:
    a = -k * x / m
    v += a * dt
    x += v * dt
    xs.append(x)
    vs.append(v)

# Soluções analíticas
x_analitico = 4 * np.cos(tempos)
v_analitico = -4 * np.sin(tempos)

# Gráficos
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(tempos, vs, label='Velocidade (numérica)')
plt.plot(tempos, v_analitico, '--', label='Velocidade (analítica)')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(tempos, xs, label='Posição (numérica)')
plt.plot(tempos, x_analitico, '--', label='Posição (analítica)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
