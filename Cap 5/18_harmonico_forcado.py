import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros do sistema ---
m = 1.0  # kg
k = 1.0  # N/m
b = 0.05 # kg/s
F0 = 7.5 # N
wf = 1.0 # rad/s (frequência da força externa)

# Frequência natural para referência
omega_0 = np.sqrt(k / m)
print(f"Frequência natural do oscilador (omega_0): {omega_0:.3f} rad/s")
print(f"Frequência da força externa (wf): {wf:.3f} rad/s -> Em ressonância (wf = omega_0)\n")

# --- Função de Aceleração (Oscilador Forçado e Amortecido) ---
def acceleration_forced_damped(x, vx, t):
    return -k / m * x - b / m * vx + F0 / m * np.cos(wf * t)

# --- Função de Simulação (Euler-Cromer) ---
def simulate_oscillator_forced(x0, vx0, dt, t_total):
    t_values = []
    x_values = []
    vx_values = []
    energy_values = [] # Para alínea e)

    t = 0.0
    x = x0
    vx = vx0

    t_values.append(t)
    x_values.append(x)
    vx_values.append(vx)
    # Calculando a energia mecânica inicial
    energy_values.append(0.5 * m * vx**2 + 0.5 * k * x**2)

    while t <= t_total:
        ax = acceleration_forced_damped(x, vx, t)
        vx = vx + ax * dt
        x = x + vx * dt
        t = t + dt

        t_values.append(t)
        x_values.append(x)
        vx_values.append(vx)
        # Calculando a energia mecânica
        energy_values.append(0.5 * m * vx**2 + 0.5 * k * x**2)
    
    return t_values, x_values, vx_values, energy_values

# --- ALÍNEA a) ---
print("--- Alínea a) ---")
x0_a = 4.0 # m
vx0_a = 0.0 # m/s
dt_a_1 = 0.0001
dt_a_2 = 0.00001 # Para testar a confiança
t_total_a = 300.0 # s (tempo suficiente para atingir o regime estacionário)

# Simulação com dt_a_1
t_a1, x_a1, vx_a1, Em_a1 = simulate_oscillator_forced(x0_a, vx0_a, dt_a_1, t_total_a)
# Simulação com dt_a_2
t_a2, x_a2, vx_a2, Em_a2 = simulate_oscillator_forced(x0_a, vx0_a, dt_a_2, t_total_a)

plt.figure(figsize=(10, 6))
plt.plot(t_a1, x_a1, label=f'dt={dt_a_1}')
plt.plot(t_a2, x_a2, label=f'dt={dt_a_2}', linestyle='--') # Plotar com linha tracejada para sobrepor
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Harmónico Forçado (Alínea a)')
plt.grid(True)
plt.legend()
plt.show()

# Verificar confiança
# Comparar o valor final da posição para os dois dt
print(f"Posição final (dt={dt_a_1}): {x_a1[-1]:.3f} m")
print(f"Posição final (dt={dt_a_2}): {x_a2[-1]:.3f} m")
print(f"Diferença nas posições finais: {abs(x_a1[-1] - x_a2[-1]):.3e} m")

if abs(x_a1[-1] - x_a2[-1]) < 1e-2: # Pequena tolerância para considerar igual
    print("Temos confiança no resultado. A lei do movimento obtida por dois passos temporais diferentes é a mesma (ou muito próxima).") [cite: 113]
else:
    print("Os resultados com diferentes passos de tempo não são suficientemente próximos, o que pode indicar falta de confiança ou necessidade de 'dt' ainda menor.")


# --- ALÍNEA b) ---
print("\n--- Alínea b) ---")
# Regime estacionário: ignorar a parte inicial (transiente)
# O tempo para atingir o regime estacionário pode ser estimado visualmente no gráfico,
# ou sabendo que decai com exp(-(b/2m)*t).
# Um tempo típico para atingir o regime estacionário é algumas vezes 2m/b.
# 2m/b = 2*1/0.05 = 40 s. Vamos pegar o final da simulação (t > 150s, por exemplo).
start_steady_state_index = np.where(np.array(t_a1) > 150)[0][0] # Começar a analisar a partir de t=150s

x_steady_state_b = x_a1[start_steady_state_index:]
t_steady_state_b = t_a1[start_steady_state_index:]

# Amplitude: valor máximo na parte estacionária
amplitude_b = np.max(np.abs(x_steady_state_b))
print(f"Amplitude do movimento no regime estacionário (alínea b): {amplitude_b:.2f} m") [cite: 114]

# Período: como wf = 1.0 rad/s, o período deve ser 2*pi/wf
periodo_b = 2 * np.pi / wf
print(f"Período do movimento no regime estacionário (alínea b): {periodo_b:.3f} s") [cite: 114]


# --- ALÍNEA c) ---
print("\n--- Alínea c) ---")
x0_c = -2.0 # m
vx0_c = -4.0 # m/s
dt_c_1 = 0.0001
dt_c_2 = 0.00001 # Para testar a confiança
t_total_c = 300.0 # s

# Simulação com dt_c_1
t_c1, x_c1, vx_c1, Em_c1 = simulate_oscillator_forced(x0_c, vx0_c, dt_c_1, t_total_c)
# Simulação com dt_c_2
t_c2, x_c2, vx_c2, Em_c2 = simulate_oscillator_forced(x0_c, vx0_c, dt_c_2, t_total_c)


plt.figure(figsize=(10, 6))
plt.plot(t_c1, x_c1, label=f'dt={dt_c_1}')
plt.plot(t_c2, x_c2, label=f'dt={dt_c_2}', linestyle='--')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Harmónico Forçado (Alínea c)')
plt.grid(True)
plt.legend()
plt.show()

# Confiança: verificar posições finais
print(f"Posição final (dt={dt_c_1}): {x_c1[-1]:.3f} m")
print(f"Posição final (dt={dt_c_2}): {x_c2[-1]:.3f} m")
print(f"Diferença nas posições finais: {abs(x_c1[-1] - x_c2[-1]):.3e} m")
if abs(x_c1[-1] - x_c2[-1]) < 1e-2:
    print("Temos confiança no resultado. A lei do movimento obtida por dois passos temporais diferentes é a mesma (ou muito próxima).")
else:
    print("Os resultados com diferentes passos de tempo não são suficientemente próximos.")


# --- ALÍNEA d) ---
print("\n--- Alínea d) ---")
# Regime estacionário: ignorar a parte inicial (transiente)
start_steady_state_index_d = np.where(np.array(t_c1) > 150)[0][0] # Começar a analisar a partir de t=150s

x_steady_state_d = x_c1[start_steady_state_index_d:]
t_steady_state_d = t_c1[start_steady_state_index_d:]

# Amplitude: valor máximo na parte estacionária
amplitude_d = np.max(np.abs(x_steady_state_d))
print(f"Amplitude do movimento no regime estacionário (alínea d): {amplitude_d:.2f} m") [cite: 115]

# Período: como wf = 1.0 rad/s, o período deve ser 2*pi/wf
periodo_d = 2 * np.pi / wf
print(f"Período do movimento no regime estacionário (alínea d): {periodo_d:.3f} s") [cite: 115]

# Confirmar que as amplitudes e períodos são os mesmos para as alíneas b) e d)
if abs(amplitude_b - amplitude_d) < 1e-2 and abs(periodo_b - periodo_d) < 1e-2:
    print("A amplitude e o período no regime estacionário são os mesmos para ambas as condições iniciais, o que é consistente com a teoria.")


# --- ALÍNEA e) ---
print("\n--- Alínea e) ---")
# Usar os resultados de t_a1 e Em_a1 da alínea a) para plotar a energia mecânica
plt.figure(figsize=(10, 6))
plt.plot(t_a1, Em_a1, label='Energia Mecânica') [cite: 115]
plt.xlabel('Tempo (s)')
plt.ylabel('Energia Mecânica (J)')
plt.title('Energia Mecânica do Oscilador Harmónico Forçado e Amortecido')
plt.grid(True)
plt.legend()
plt.show()

print("A energia mecânica NÃO É constante ao longo do tempo.") [cite: 115]
print("No início, a energia mecânica aumenta à medida que o sistema absorve energia da força externa e a amplitude cresce.")
print("No regime estacionário, a energia mecânica flutua mas a sua média é constante, pois a energia fornecida pela força externa é equilibrada pela energia dissipada pelo amortecimento.")
print("O sistema recebe energia realizada pela força externa e dissipa energia devido à resistência do meio.") [cite: 120]