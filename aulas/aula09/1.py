import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
d = 0.1               # diâmetro das esferas (m)
l = 10 * d            # comprimento das cordas (m)
m = 0.3               # massa das esferas (kg)
g = 9.8               # aceleração da gravidade (m/s²)
k = 1e7               # constante da força de contato
q = 2.0               # expoente da força de contato
N = 2                 # número de esferas

# Tempo
dt = 0.0001
t_max = 5.0
n_steps = int(t_max / dt)
t_array = np.linspace(0, t_max, n_steps)

# Condições iniciais
x = np.zeros((N, n_steps))
v = np.zeros((N, n_steps))
x[0, 0] = -5 * d
x[1, 0] = d

# Função de aceleração por contato
def acc_toque(dx, d):
    if dx < d:
        return (-k * abs(dx - d)**q) / m
    return 0.0

# Aceleração total para cada esfera
def acc_i(i, x_vec):
    a = 0
    if i > 0:
        a -= acc_toque(x_vec[i] - x_vec[i-1], d)
    if i < N - 1:
        a += acc_toque(x_vec[i+1] - x_vec[i], d)
    a -= g * (x_vec[i] - d*i) / l
    return a

# Arrays para energia e momento
momento_total = np.zeros(n_steps)
energia_total = np.zeros(n_steps)
energia_cinetica = np.zeros(n_steps)
energia_potencial = np.zeros(n_steps)

# Integração Euler-Cromer
for t in range(n_steps - 1):
    a = np.zeros(N)
    for i in range(N):
        a[i] = acc_i(i, x[:, t])
        v[i, t+1] = v[i, t] + a[i] * dt
        x[i, t+1] = x[i, t] + v[i, t+1] * dt

    # Momento e energias
    momento_total[t] = m * np.sum(v[:, t])
    energia_cinetica[t] = 0.5 * m * np.sum(v[:, t]**2)
    energia_potencial[t] = 0.5 * m * g / l * np.sum((x[:, t] - np.array([d*i for i in range(N)]))**2)
    energia_total[t] = energia_cinetica[t] + energia_potencial[t]

# Gráfico: posições das esferas
plt.figure(figsize=(10, 6))
plt.plot(t_array, x[0], label='x0(t)')
plt.plot(t_array, x[1], label='x1(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição das esferas ao longo do tempo')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Gráfico: momento total
plt.figure(figsize=(6, 4))
plt.plot(t_array, momento_total)
plt.xlabel('Tempo (s)')
plt.ylabel('Momento total (kg·m/s)')
plt.title('Momento Linear Total')
plt.grid()
plt.tight_layout()
plt.show()

# Gráfico: energia total, cinética e potencial
plt.figure(figsize=(10, 6))
plt.plot(t_array, energia_total, label='Energia Total')
plt.plot(t_array, energia_cinetica, label='Energia Cinética', linestyle='--')
plt.plot(t_array, energia_potencial, label='Energia Potencial', linestyle=':')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.title('Energias do sistema')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
