import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
g = 9.81  # Gravidade (m/s^2)
v0 = 10.0  # Velocidade inicial (m/s)
y0 = 0.0  # Posição inicial (m)
vT = 27.78  # Velocidade terminal (m/s)
m = 1.0  # Massa arbitrária (kg)
k = m * g / vT  # Coeficiente de resistência do ar

# Parâmetros numéricos
dt = 0.01  # Passo de tempo
t_max = 3.0  # Tempo máximo de simulação
N = int(t_max / dt)  # Número de passos

# Inicialização das variáveis
t_vals = np.zeros(N)
y_vals = np.zeros(N)
v_vals = np.zeros(N)

y_vals[0] = y0
v_vals[0] = v0

# Método de Euler
for i in range(N - 1):
    t_vals[i + 1] = t_vals[i] + dt
    v_vals[i + 1] = v_vals[i] - (g + (k / m) * v_vals[i]) * dt
    y_vals[i + 1] = y_vals[i] + v_vals[i] * dt

# Encontrando a altura máxima numericamente
idx_max = np.argmax(y_vals)
t_max = t_vals[idx_max]
y_max = y_vals[idx_max]

# Encontrando o instante de retorno numericamente
idx_return = np.where(y_vals < 0)[0][0]  # Primeiro índice onde y < 0
t_return = t_vals[idx_return]

# Plotando os resultados
plt.figure(figsize=(8, 5))
plt.plot(t_vals, y_vals, label="Altura (m)")
plt.axvline(t_max, color="r", linestyle="--", label=f"T_max = {t_max:.2f} s")
plt.axvline(t_return, color="g", linestyle="--", label=f"T_return = {t_return:.2f} s")
plt.xlabel("Tempo (s)")
plt.ylabel("Altura (m)")
plt.title("Movimento com resistência do ar")
plt.legend()
plt.grid()
plt.show()

# Resultados
print(f"Altura máxima: {y_max:.2f} m em {t_max:.2f} s")
print(f"Instante de retorno: {t_return:.2f} s")
 