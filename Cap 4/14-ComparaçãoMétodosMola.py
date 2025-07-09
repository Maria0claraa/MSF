import numpy as np
import matplotlib.pyplot as plt

k = 1.0     # constante elástica (N/m)
m = 1.0     # massa (kg)
x0 = 4.0    # posição inicial (m)
v0 = 0.0    # velocidade inicial (m/s)
dt = 0.01   # passo de tempo (s)
t_total = 5.0  # tempo total (s)

# Cálculo da energia total
Ep = 0.5 * k * x0**2      # energia potencial
Ec = 0.5 * m * v0**2      # energia cinética
E_total = Ep + Ec         # energia total
print(f"Energia total do sistema: {E_total:.2f} J")

# Preparar arrays de tempo
n = int(t_total / dt)  #número de passos
t_vals = np.linspace(0, t_total, n)

# Inicializações para Euler
x_euler = np.zeros(n)
v_euler = np.zeros(n)
E_euler = np.zeros(n)

# Inicializações para Euler-Cromer
x_ec = np.zeros(n)
v_ec = np.zeros(n)
E_ec = np.zeros(n)

# Condições iniciais
x_euler[0] = x0
v_euler[0] = v0
E_euler[0] = 0.5 * k * x0**2 + 0.5 * m * v0**2

x_ec[0] = x0
v_ec[0] = v0
E_ec[0] = 0.5 * k * x0**2 + 0.5 * m * v0**2

# Loop de integração
for i in range(1, n):
    # ----- Método de Euler -----
    a_e = -k/m * x_euler[i-1]
    x_euler[i] = x_euler[i-1] + v_euler[i-1] * dt
    v_euler[i] = v_euler[i-1] + a_e * dt
    E_euler[i] = 0.5 * k * x_euler[i]**2 + 0.5 * m * v_euler[i]**2

    # ----- Método de Euler-Cromer -----
    a_ec = -k/m * x_ec[i-1]
    v_ec[i] = v_ec[i-1] + a_ec * dt
    x_ec[i] = x_ec[i-1] + v_ec[i] * dt
    E_ec[i] = 0.5 * k * x_ec[i]**2 + 0.5 * m * v_ec[i]**2

fig, axs = plt.subplots(1, 2, figsize=(12, 4))
# Euler
axs[0].plot(t_vals, E_euler, label="Euler", color='darkred')
axs[0].set_title("Energia total, Método de Euler, dt = 0.01")
axs[0].set_xlabel("t (s)")
axs[0].set_ylabel("Energia total (J)")
axs[0].grid(True)
# Euler-Cromer
axs[1].plot(t_vals, E_ec, label="Euler-Cromer", color='navy')
axs[1].set_title("Energia total, Método de Euler-Cromer, dt = 0.01")
axs[1].set_xlabel("t (s)")
axs[1].set_ylabel("Energia total (J)")
axs[1].grid(True)

plt.tight_layout()
plt.show()
