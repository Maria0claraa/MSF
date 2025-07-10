import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros do sistema ---
m = 1.0  # kg 
k = 1.0  # N/m 

# --- Condições Iniciais ---
x0 = 4.0  # m 
vx0 = 0.0 # m/s 

# --- Parâmetros da simulação ---
dt = 0.001 # Passo de tempo (escolhe um valor adequado)
t_total = 30.0 # Tempo total de simulação (para observar várias oscilações)

# --- Listas para armazenar os resultados ---
t_values = []
x_values = []
vx_values = []
energy_values = [] # Para a alínea c)

# --- Inicialização ---
t = 0.0
x = x0
vx = vx0

t_values.append(t)
x_values.append(x)
vx_values.append(vx)

# --- Loop de simulação (Método de Euler-Cromer) ---
while t <= t_total:
    # Calcular a aceleração no instante atual
    ax = -k / m * x

    # Atualizar velocidade usando a aceleração no instante atual
    vx = vx + ax * dt

    # Atualizar posição usando a nova velocidade
    x = x + vx * dt

    # Atualizar o tempo
    t = t + dt

    # Armazenar os resultados
    t_values.append(t)
    x_values.append(x)
    vx_values.append(vx)

    # Calcular a energia mecânica para a alínea c)
    Ec = 0.5 * m * vx**2
    Ep = 0.5 * k * x**2
    Em = Ec + Ep
    energy_values.append(Em)


# --- Análise e Resultados ---

# a) Gráfico da Lei do Movimento (x(t))
plt.figure(figsize=(10, 6))
plt.plot(t_values, x_values, label='x(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Massa-Mola')
plt.grid(True)
plt.legend()
plt.show()

# b) Amplitude e Período (a partir dos resultados numéricos)
# Para a amplitude, basta olhar para o valor máximo da posição
amplitude_numerica = np.max(x_values)
print(f"Amplitude numérica: {amplitude_numerica:.3f} m")

# Para o período, podes encontrar o tempo entre dois picos sucessivos ou um número de oscilações
# Uma forma simples é usar a frequência angular natural teórica (já que é harmónico simples)
# Período teórico T = 2 * pi / omega_0
periodo_teorico = 2 * np.pi / np.sqrt(k/m)
print(f"Período teórico: {periodo_teorico:.3f} s")
# (Podes tentar extrair o período numericamente a partir do gráfico, mas para um SHM sem amortecimento é direto)


# c) Energia Mecânica
plt.figure(figsize=(10, 6))
plt.plot(t_values[:-1], energy_values, label='Energia Mecânica') # t_values[:-1] para alinhar com energy_values
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.title('Energia Mecânica do Oscilador ao Longo do Tempo')
plt.grid(True)
plt.ylim(7.9, 8.1) # Ajustar limites para ver se é constante
plt.legend()
plt.show()

# Ver se a energia é constante (comparar valores)
primeira_energia = energy_values[0]
ultima_energia = energy_values[-1]
print(f"Primeira energia mecânica: {primeira_energia:.3f} J")
print(f"Última energia mecânica: {ultima_energia:.3f} J")
# Espera-se que seja constante (ou quase) pois não há amortecimento nem força externa
# no oscilador harmónico simples.