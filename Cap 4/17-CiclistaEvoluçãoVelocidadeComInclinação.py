import numpy as np
import matplotlib.pyplot as plt

# --- Dados do problema ---
P_cv = 0.4                    # Potência em cavalos-vapor
P = P_cv * 735.5              # Potência em Watts
v0 = 1.0                      # Velocidade inicial (m/s)
m = 80.0                      # Massa do ciclista + bicicleta (kg)
k = 0.25                      # Constante de resistência do ar (N·s²/m²)
g = 9.81                      # Aceleração gravítica (m/s²)
theta_deg = 5                # Inclinação da colina em graus
theta_rad = np.radians(theta_deg)

# --- Integração com método de Euler-Cromer ---
dt = 0.001
t_max = 1000
n = int(t_max / dt)

t = np.zeros(n)
v = np.zeros(n)
x = np.zeros(n)

v[0] = v0

for i in range(n - 1):
    if v[i] <= 0:
        a = 0
    else:
        # Força propulsora - resistência do ar - componente do peso na subida
        a = (P / (m * v[i])) - (k / m) * v[i]**2 - g * np.sin(theta_rad)
    v[i + 1] = v[i] + a * dt
    x[i + 1] = x[i] + v[i + 1] * dt
    t[i + 1] = t[i] + dt

# --- (a) Tempo para percorrer 2 km ---
idx_2km = np.argmax(x >= 2000)
t_2km = t[idx_2km]
minutos = int(t_2km // 60)
segundos = t_2km % 60

# --- (b) Velocidade terminal (média dos últimos valores)
v_terminal = np.mean(v[-1000:])

# --- Resultados ---
print(f"(a) Tempo para percorrer 2 km: {t_2km:.1f} s ≈ {minutos} min {segundos:.1f} s")
print(f"(b) Velocidade terminal: {v_terminal:.2f} m/s")

# --- Gráfico da velocidade ---
plt.plot(t, v, label="Velocidade (m/s)", color='orange')
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (m/s)")
plt.title("Velocidade do ciclista subindo colina de 5°")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
