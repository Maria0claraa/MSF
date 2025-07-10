import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros fixos do sistema ---
m = 1.0  # kg
k = 1.0  # N/m
alpha = 0.002 # N/m^2 (atenção: valor é N/m^2, mas a Ep é alpha*x^4, então a unidade de alpha na Ep é J/m^4. O problema dá 0.002 N/m^2. Isto pode ser uma inconsistência ou mal-entendido na unidade. Assumindo que o alpha dado é o alpha da FORÇA como em Fx = -k x - 4*alpha*x^3 para Ep = 0.5*k*x^2 + alpha*x^4.
# MAS, a força dada é Fx = -k x (1 + 2*alpha*x^2) = -k*x - 2*k*alpha*x^3
# Se Fx = - d(Ep)/dx, e Ep = 0.5*k*x^2 + 0.5*k*alpha*x^4
# Então d(Ep)/dx = k*x + 2*k*alpha*x^3
# Portanto, a força deve ser Fx = -k*x - 2*k*alpha*x^3
# Comparando com Fx = -k x(1+2*alpha x^2) = -k*x - 2*k*alpha*x^3
# As expressões são consistentes. O alpha dado (0.002 N/m^2) é o alpha usado na expressão da força e energia potencial.

b = 0.05 # kg/s
F0 = 7.5 # N
wf = 1.0 # rad/s

# --- Função de Aceleração (Oscilador Quártico Forçado e Amortecido) ---
def acceleration_quartic_forced_damped(x, vx, t):
    # Aceleração baseada na força Fx = -k*x*(1 + 2*alpha*x^2) - b*vx + F0*cos(wf*t)
    return (-k * x * (1 + 2 * alpha * x**2) - b * vx + F0 * np.cos(wf * t)) / m

# --- Função de Energia Potencial (para calcular energia mecânica) ---
def potential_energy_quartic(x_val):
    return 0.5 * k * x_val**2 * (1 + alpha * x_val**2) # Ep = 0.5*k*x^2 + 0.5*k*alpha*x^4

# --- Função de Simulação (Euler-Cromer) ---
def simulate_oscillator_quartic(x0, vx0, dt, t_total):
    t_values = []
    x_values = []
    vx_values = []
    energy_values = []

    t = 0.0
    x = x0
    vx = vx0

    t_values.append(t)
    x_values.append(x)
    vx_values.append(vx)
    energy_values.append(0.5 * m * vx**2 + potential_energy_quartic(x))

    while t <= t_total:
        ax = acceleration_quartic_forced_damped(x, vx, t)
        vx = vx + ax * dt
        x = x + vx * dt
        t = t + dt

        t_values.append(t)
        x_values.append(x)
        vx_values.append(vx)
        energy_values.append(0.5 * m * vx**2 + potential_energy_quartic(x))
    
    return t_values, x_values, vx_values, energy_values

# --- ALÍNEA a) ---
print("--- Alínea a) ---")
x0_a = 3.0 # m
vx0_a = 0.0 # m/s
dt_a_1 = 0.0001
dt_a_2 = 0.00001 # Para testar a confiança
t_total_a = 200.0 # s (tempo suficiente para atingir o regime estacionário)

# Simulação com dt_a_1
t_a1, x_a1, vx_a1, Em_a1 = simulate_oscillator_quartic(x0_a, vx0_a, dt_a_1, t_total_a)
# Simulação com dt_a_2
t_a2, x_a2, vx_a2, Em_a2 = simulate_oscillator_quartic(x0_a, vx0_a, dt_a_2, t_total_a)

plt.figure(figsize=(10, 6))
plt.plot(t_a1, x_a1, label=f'dt={dt_a_1}')
plt.plot(t_a2, x_a2, label=f'dt={dt_a_2}', linestyle='--') # Plotar com linha tracejada para sobrepor
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Quártico Forçado (Alínea a)')
plt.grid(True)
plt.show()

# Verificar confiança
print(f"Posição final (dt={dt_a_1}): {x_a1[-1]:.3f} m")
print(f"Posição final (dt={dt_a_2}): {x_a2[-1]:.3f} m")
print(f"Diferença nas posições finais: {abs(x_a1[-1] - x_a2[-1]):.3e} m")

if abs(x_a1[-1] - x_a2[-1]) < 1e-2: # Pequena tolerância
    print("Temos confiança no resultado. A lei do movimento obtida por dois passos temporais diferentes é a mesma (ou muito próxima).")
else:
    print("Os resultados com diferentes passos de tempo não são suficientemente próximos, o que pode indicar falta de confiança ou necessidade de 'dt' ainda menor.")


# --- ALÍNEA b) ---
print("\n--- Alínea b) ---")
# Regime estacionário: ignorar a parte inicial (transiente)
# O tempo de relaxamento é 2m/b = 40s. Vamos pegar os últimos ~100s da simulação.
steady_state_start_time = 100.0 # s
steady_state_index = np.where(np.array(t_a1) >= steady_state_start_time)[0][0]

x_steady_b = x_a1[steady_state_index:]
t_steady_b = t_a1[steady_state_index:]

# Amplitude: valor máximo absoluto na parte estacionária
amplitude_b = np.max(np.abs(x_steady_b))
print(f"Amplitude do movimento no regime estacionário (alínea b): {amplitude_b:.3f} m") # Solução: 13.791 m

# Período: como não é harmónico simples, o período numérico é mais complexo.
# Vamos encontrar os picos e calcular a média dos períodos.
peak_times_b = []
for i in range(1, len(x_steady_b) - 1):
    if x_steady_b[i] > x_steady_b[i-1] and x_steady_b[i] > x_steady_b[i+1]:
        peak_times_b.append(t_steady_b[i])

if len(peak_times_b) >= 2:
    periods_b = np.diff(peak_times_b)
    periodo_b = np.mean(periods_b)
    print(f"Período do movimento no regime estacionário (alínea b): {periodo_b:.3f} s") # Solução: 6.283 s
else:
    print("Não foi possível determinar o período numericamente com precisão suficiente (poucos picos encontrados).")


# --- ALÍNEA c) ---
print("\n--- Alínea c) ---")
x0_c = -2.0 # m
vx0_c = -4.0 # m/s
dt_c_1 = 0.0001
dt_c_2 = 0.00001 # Para testar a confiança
t_total_c = 200.0 # s

# Simulação com dt_c_1
t_c1, x_c1, vx_c1, Em_c1 = simulate_oscillator_quartic(x0_c, vx0_c, dt_c_1, t_total_c)
# Simulação com dt_c_2
t_c2, x_c2, vx_c2, Em_c2 = simulate_oscillator_quartic(x0_c, vx0_c, dt_c_2, t_total_c)

plt.figure(figsize=(10, 6))
plt.plot(t_c1, x_c1, label=f'dt={dt_c_1}')
plt.plot(t_c2, x_c2, label=f'dt={dt_c_2}', linestyle='--')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Quártico Forçado (Alínea c)')
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
# Regime estacionário
steady_state_start_index_d = int(len(x_c1) * 0.5) # Começar a analisar a partir da metade

x_steady_d = x_c1[steady_state_start_index_d:]
t_steady_d = t_c1[steady_state_start_index_d:]

# Amplitude: valor máximo absoluto na parte estacionária
amplitude_d = np.max(np.abs(x_steady_d))
print(f"Amplitude do movimento no regime estacionário (alínea d): {amplitude_d:.3f} m") # Solução: 13.791 m

# Período
peak_times_d = []
for i in range(1, len(x_steady_d) - 1):
    if x_steady_d[i] > x_steady_d[i-1] and x_steady_d[i] > x_steady_d[i+1]:
        peak_times_d.append(t_steady_d[i])

if len(peak_times_d) >= 2:
    periods_d = np.diff(peak_times_d)
    periodo_d = np.mean(periods_d)
    print(f"Período do movimento no regime estacionário (alínea d): {periodo_d:.3f} s") # Solução: 6.283 s
else:
    print("Não foi possível determinar o período numericamente com precisão suficiente (poucos picos encontrados).")

# Confirmação de que as amplitudes e períodos são os mesmos para as alíneas b) e d)
if abs(amplitude_b - amplitude_d) < 1e-2 and abs(periodo_b - periodo_d) < 1e-2:
    print("A amplitude e o período no regime estacionário são os mesmos para ambas as condições iniciais, o que é consistente com a teoria para sistemas não caóticos.")


# --- ALÍNEA e) ---
print("\n--- Alínea e) ---")
# Usar os resultados de t_a1 e Em_a1 da alínea a) para plotar a energia mecânica
plt.figure(figsize=(10, 6))
plt.plot(t_a1, Em_a1, label='Energia Mecânica')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia Mecânica (J)')
plt.title('Energia Mecânica do Oscilador Quártico Forçado e Amortecido')
plt.grid(True)
plt.legend()
plt.show()

print("A energia mecânica NÃO É constante ao longo do tempo.")
print("O sistema recebe energia realizada pela força externa e dissipa energia devido à resistência do meio.")
print("No regime estacionário, a energia mecânica média mantém-se constante, mas oscila devido às flutuações da potência da força externa e do amortecimento.")