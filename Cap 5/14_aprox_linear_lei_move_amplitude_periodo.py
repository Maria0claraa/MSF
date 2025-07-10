import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros do sistema ---
g = 9.8  # m/s^2
L = 0.5  # m

# --- Condições Iniciais ---
theta0 = 0.1  # rad
omega0 = 0.5  # rad/s (velocidade angular inicial)

# --- Parâmetros da simulação ---
dt = 0.001     # Passo de tempo
t_total = 4.0  # Tempo total de simulação

# --- Listas para armazenar os resultados ---
t_values = []
theta_values = []
omega_values = []

# --- Inicialização ---
t = 0.0
theta = theta0
omega = omega0

t_values.append(t)
theta_values.append(theta)
omega_values.append(omega)

# --- Loop de simulação (Método de Euler-Cromer) ---
while t <= t_total:
    # Calcular a aceleração angular no instante atual
    alpha = -g / L * theta

    # Atualizar velocidade angular usando a aceleração angular no instante atual
    omega = omega + alpha * dt

    # Atualizar posição angular usando a nova velocidade angular
    theta = theta + omega * dt

    # Atualizar o tempo
    t = t + dt

    # Armazenar os resultados
    t_values.append(t)
    theta_values.append(theta)
    omega_values.append(omega)

# --- Análise e Resultados ---

# a) Gráfico da Lei do Movimento (theta(t))
plt.figure(figsize=(10, 6))
plt.plot(t_values, theta_values, label='theta(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Ângulo (rad)')
plt.title('Lei do Movimento do Pêndulo (Aproximação Linear)')
plt.grid(True)
plt.legend()
plt.show()

# b) Amplitude e Período (a partir dos resultados numéricos)
# Para a amplitude, podes encontrar o valor máximo absoluto da posição angular
amplitude_numerica = np.max(np.abs(theta_values))
print(f"Amplitude numérica: {amplitude_numerica:.3f} rad")

# Para o período, podes encontrar o tempo entre dois picos sucessivos ou um número de oscilações
# A frequência angular natural teórica para esta aproximação é omega_0 = sqrt(g/L)
omega_teorica = np.sqrt(g / L)
periodo_teorico = 2 * np.pi / omega_teorica
print(f"Período teórico: {periodo_teorico:.3f} s")

# Para obter o período numericamente com mais precisão, podes procurar picos ou passagens por zero.
# Por exemplo, encontrar os índices onde a velocidade angular é zero e o ângulo é máximo/mínimo.
# Ou então, após um regime "estável" (aqui é sempre estável), medir a distância entre 2 picos.
# Uma forma simples de estimar numericamente: contar o número de ciclos e dividir pelo tempo total.
# Por exemplo, se observares no gráfico 2 ciclos em 3 segundos, o período é 1.5s.
# As soluções dadas (A=0.151 rad, T=1.419 s) são as que deves tentar obter.