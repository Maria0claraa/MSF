import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Para o plot 3D, opcional mas interessante

# --- Parâmetros do sistema de Lorenz ---
sigma = 10.0
b = 8.0 / 3.0
r = 28.0

# --- Condições Iniciais ---
x0 = 0.0
y0 = 1.0
z0 = 0.0

# --- Parâmetros da Simulação ---
dt = 0.001 # Passo de tempo
t_total = 60.0 # Tempo total de simulação (como na solução)

# --- Funções das Derivadas (dx/dt, dy/dt, dz/dt) ---
def lorenz_dx(x, y, z, sigma):
    return sigma * (y - x)

def lorenz_dy(x, y, z, r):
    return r * x - y - x * z

def lorenz_dz(x, y, z, b):
    return x * y - b * z

# --- Implementação do Método de Runge-Kutta de 4ª Ordem (RK4) para Lorenz ---
def rk4_step_lorenz(x, y, z, t, dt, sigma, r, b):
    # k1
    k1_x = lorenz_dx(x, y, z, sigma)
    k1_y = lorenz_dy(x, y, z, r)
    k1_z = lorenz_dz(x, y, z, b)

    # k2
    k2_x = lorenz_dx(x + k1_x * dt / 2, y + k1_y * dt / 2, z + k1_z * dt / 2, sigma)
    k2_y = lorenz_dy(x + k1_x * dt / 2, y + k1_y * dt / 2, z + k1_z * dt / 2, r)
    k2_z = lorenz_dz(x + k1_x * dt / 2, y + k1_y * dt / 2, z + k1_z * dt / 2, b)

    # k3
    k3_x = lorenz_dx(x + k2_x * dt / 2, y + k2_y * dt / 2, z + k2_z * dt / 2, sigma)
    k3_y = lorenz_dy(x + k2_x * dt / 2, y + k2_y * dt / 2, z + k2_z * dt / 2, r)
    k3_z = lorenz_dz(x + k2_x * dt / 2, y + k2_y * dt / 2, z + k2_z * dt / 2, b)

    # k4
    k4_x = lorenz_dx(x + k3_x * dt, y + k3_y * dt, z + k3_z * dt, sigma)
    k4_y = lorenz_dy(x + k3_x * dt, y + k3_y * dt, z + k3_z * dt, r)
    k4_z = lorenz_dz(x + k3_x * dt, y + k3_y * dt, z + k3_z * dt, b)

    # Atualização
    x_new = x + (k1_x + 2*k2_x + 2*k3_x + k4_x) * dt / 6
    y_new = y + (k1_y + 2*k2_y + 2*k3_y + k4_y) * dt / 6
    z_new = z + (k1_z + 2*k2_z + 2*k3_z + k4_z) * dt / 6

    return x_new, y_new, z_new

# --- Simulação principal ---
t_values = []
x_values = []
y_values = []
z_values = []

t = 0.0
x = x0
y = y0
z = z0

t_values.append(t)
x_values.append(x)
y_values.append(y)
z_values.append(z)

while t <= t_total:
    x, y, z = rk4_step_lorenz(x, y, z, t, dt, sigma, r, b)
    t = t + dt

    t_values.append(t)
    x_values.append(x)
    y_values.append(y)
    z_values.append(z)

# --- Plotar a Evolução Temporal ---
fig_time, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
axs[0].plot(t_values, x_values)
axs[0].set_ylabel('x')
axs[0].set_title('Evolução Temporal das Variáveis de Lorenz')
axs[0].grid(True)

axs[1].plot(t_values, y_values)
axs[1].set_ylabel('y')
axs[1].grid(True)

axs[2].plot(t_values, z_values)
axs[2].set_xlabel('Tempo (s)')
axs[2].set_ylabel('z')
axs[2].grid(True)

plt.tight_layout()
plt.show()


# --- Plotar o Espaço de Fase ---
fig_phase, axs_phase = plt.subplots(3, 1, figsize=(10, 12)) # Cria 3 subplots para as projeções 2D

# y vs x
axs_phase[0].plot(x_values, y_values)
axs_phase[0].set_xlabel('x')
axs_phase[0].set_ylabel('y')
axs_phase[0].set_title('Espaço de Fase: y vs x')
axs_phase[0].grid(True)

# z vs x
axs_phase[1].plot(x_values, z_values)
axs_phase[1].set_xlabel('x')
axs_phase[1].set_ylabel('z')
axs_phase[1].set_title('Espaço de Fase: z vs x')
axs_phase[1].grid(True)

# z vs y
axs_phase[2].plot(y_values, z_values)
axs_phase[2].set_xlabel('y')
axs_phase[2].set_ylabel('z')
axs_phase[2].set_title('Espaço de Fase: z vs y')
axs_phase[2].grid(True)

plt.tight_layout()
plt.show()


# Opcional: Plot 3D do Atractor de Lorenz
fig_3d = plt.figure(figsize=(8, 8))
ax_3d = fig_3d.add_subplot(111, projection='3d')
ax_3d.plot(x_values, y_values, z_values, lw=0.5)
ax_3d.set_xlabel("X Axis")
ax_3d.set_ylabel("Y Axis")
ax_3d.set_zlabel("Z Axis")
ax_3d.set_title("Atractor de Lorenz (3D)")
plt.show()

print("Simulação das Equações de Lorenz concluída. Os gráficos mostram a evolução temporal não periódica e as projeções do famoso atraktor caótico no espaço de fase.")