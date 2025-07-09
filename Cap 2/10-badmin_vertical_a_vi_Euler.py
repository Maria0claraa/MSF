import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
m = 0.058  # Massa do volante (kg)
g = 9.81  # Aceleração da gravidade (m/s^2)
vT = 6.80  # Velocidade terminal (m/s)
k = m * g / vT  # Coeficiente de resistência do ar

# Condições iniciais
v0 = 200 / 3.6  # Velocidade inicial em m/s
h = 0  # Altura inicial arbitrária

dt = 0.01  # Passo de tempo
T_max = 5  # Tempo máximo da simulação
N = int(T_max / dt)  # Número de passos

# Inicialização das listas de tempo, velocidade, aceleração e posição
t_vals = np.zeros(N)
v_vals = np.zeros(N)
a_vals = np.zeros(N)
y_vals = np.zeros(N)

# Condições iniciais
v_vals[0] = v0
y_vals[0] = h

def euler_method():
    for i in range(1, N):
        t_vals[i] = t_vals[i-1] + dt
        a_vals[i] = g - (k/m) * v_vals[i-1]  # Aceleração
        v_vals[i] = v_vals[i-1] + a_vals[i] * dt  # Velocidade
        y_vals[i] = y_vals[i-1] + v_vals[i] * dt  # Posição
        
        # Verifica quando a velocidade reduz para 50%
        if abs(v_vals[i]) <= 0.5 * v0:
            t_50 = t_vals[i]
    
    return t_50

# Executando o método de Euler
t_50 = euler_method()

# Encontrando o tempo para percorrer 4m
idx_4m = np.where(y_vals >= 4)[0][0]
t_4m = t_vals[idx_4m]

# Gráficos
plt.figure(figsize=(10, 5))

# Gráfico da aceleração
plt.subplot(1, 3, 1)
plt.plot(t_vals, a_vals, label='Aceleração (m/s²)', color='r')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s²)')
plt.legend()
plt.grid()

# Gráfico da velocidade
plt.subplot(1, 3, 2)
plt.plot(t_vals, v_vals, label='Velocidade (m/s)', color='b')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.legend()
plt.grid()

# Gráfico da posição
plt.subplot(1, 3, 3)
plt.plot(t_vals, y_vals, label='Posição (m)', color='g')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

# Resultados
print(f"Velocidade após 1s: {v_vals[int(1/dt)] * 3.6:.2f} km/h")
print(f"Tempo para reduzir a velocidade em 50%: {t_50:.2f} s")
print(f"Tempo para percorrer 4m: {t_4m:.2f} s")
