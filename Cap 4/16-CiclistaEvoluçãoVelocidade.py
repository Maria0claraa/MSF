import numpy as np
import matplotlib.pyplot as plt

# --- Dados do problema ---
P_cv = 0.4                    # Potência em cv
P = P_cv * 735.5              # Potência em W
v0 = 1.0                      # Velocidade inicial (m/s)
m = 80.0                      # Massa do ciclista (kg)
k = 0.25                      # Constante de resistência do ar (kg/m)

# --- (a) Velocidade terminal teórica ---
v_terminal = (P / k) ** (1 / 3)
print(f"(a) Velocidade terminal: {v_terminal:.2f} m/s = {v_terminal*3.6:.2f} km/h")

# --- Integração com método de Euler ---
dt = 0.01
t_max = 500
n = int(t_max / dt)

t = np.zeros(n)
v = np.zeros(n)
x = np.zeros(n)

v[0] = v0

for i in range(n - 1):
    if v[i] <= 0:
        a = 0
    else:
        a = (P / (m * v[i])) - (k / m) * v[i]**2
    v[i + 1] = v[i] + a * dt
    x[i + 1] = x[i] + v[i + 1] * dt
    t[i + 1] = t[i] + dt

# --- (b) Tempo para atingir 90% da velocidade terminal ---
v90 = 0.9 * v_terminal
idx_90 = np.argmax(v >= v90)
t_90 = t[idx_90]
print(f"(b) Tempo para atingir 90% da velocidade terminal: {t_90:.2f} s")

# --- (c) Tempo para percorrer 2 km ---
idx_2km = np.argmax(x >= 2000)
t_2km = t[idx_2km]
minutos = int(t_2km // 60)
segundos = t_2km % 60
print(f"(c) Tempo para percorrer 2 km: {t_2km:.1f} s = {minutos} min {segundos:.1f} s")

# --- Gráfico da velocidade ---
plt.plot(t, v, label="Velocidade (m/s)")
plt.axhline(v_terminal, color='r', linestyle='--', label='Velocidade Terminal')
plt.axhline(v90, color='g', linestyle='--', label='90% Vel. Terminal')
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (m/s)")
plt.title("Evolução da velocidade do ciclista")
plt.grid()
plt.legend()
plt.show()
