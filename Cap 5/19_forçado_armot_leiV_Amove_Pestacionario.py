import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros fixos do sistema ---
m = 1.0  # kg 
k = 1.0  # N/m 
b = 0.16 # kg/s 
F0 = 2.0 # N 

# Frequência natural do oscilador
omega_0 = np.sqrt(k / m)
print(f"Frequência natural do oscilador (omega_0): {omega_0:.3f} rad/s")

# --- Função de Aceleração (Oscilador Forçado e Amortecido) ---
def acceleration_forced_damped(x, vx, t, wf_current):
    return -k / m * x - b / m * vx + F0 / m * np.cos(wf_current * t)

# --- Função de Simulação (Euler-Cromer) ---
def simulate_oscillator_forced(x0, vx0, dt, t_total, wf_current):
    t_values = []
    x_values = []
    vx_values = []

    t = 0.0
    x = x0
    vx = vx0

    t_values.append(t)
    x_values.append(x)
    vx_values.append(vx)

    while t <= t_total:
        ax = acceleration_forced_damped(x, vx, t, wf_current)
        vx = vx + ax * dt
        x = x + vx * dt
        t = t + dt

        t_values.append(t)
        x_values.append(x)
        vx_values.append(vx)
    
    return t_values, x_values, vx_values

# --- ALÍNEA a) ---
print("--- Alínea a) ---")
wf_alinea_a = 2.0 # rad/s 
x0_a = 4.0 # m 
vx0_a = 0.0 # m/s 
dt_a = 0.001
t_total_a = 100.0 # s (Tempo para atingir regime estacionário)

t_a, x_a, vx_a = simulate_oscillator_forced(x0_a, vx0_a, dt_a, t_total_a, wf_alinea_a)

plt.figure(figsize=(10, 6))
plt.plot(t_a, x_a, label='x(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title(f'Lei do Movimento (wf={wf_alinea_a} rad/s)')
plt.grid(True)
plt.legend()
plt.show()

# --- ALÍNEA b) ---
print("\n--- Alínea b) ---")
# Para o regime estacionário, vamos analisar os últimos N segundos da simulação
steady_state_start_time = 60.0 # s (após 60s o transiente deve ter decaído bem)
steady_state_index = np.where(np.array(t_a) >= steady_state_start_time)[0][0]

x_steady_b = x_a[steady_state_index:]

# Amplitude no regime estacionário: valor máximo absoluto na parte estacionária
amplitude_b = np.max(np.abs(x_steady_b))
print(f"Amplitude no regime estacionário: {amplitude_b:.4f} m") # Solução: 0.6648 m

# Período no regime estacionário:
periodo_b = 2 * np.pi / wf_alinea_a
print(f"Período no regime estacionário: {periodo_b:.3f} s")


# --- ALÍNEA c) ---
print("\n--- Alínea c) ---")

# Define a gama de frequências para o gráfico
wf_values_c = np.linspace(0.2, 2.0, 50) # 50 pontos de 0.2 a 2.0 rad/s
amplitudes_c = []

# Parâmetros de simulação para o cálculo da amplitude vs wf (pode ser mais curto)
t_total_c_sim = 150.0 # Tempo de simulação para cada wf para atingir o regime estacionário
dt_c_sim = 0.001

for current_wf in wf_values_c:
    # Condições iniciais para cada simulação (não afetam a amplitude no regime estacionário)
    x0_c = 0.0 # Pode-se usar 0.0 para não ter um transiente muito grande se não for preciso
    vx0_c = 0.0
    
    # Simula o oscilador para a frequência atual
    t_c, x_c, vx_c = simulate_oscillator_forced(x0_c, vx0_c, dt_c_sim, t_total_c_sim, current_wf)
    
    # Encontra a amplitude no regime estacionário (últimos 30% dos dados para garantir regime estável)
    steady_state_start_index_c = int(len(x_c) * 0.7) # Começar nos últimos 30%
    amplitude_c_current = np.max(np.abs(x_c[steady_state_start_index_c:]))
    amplitudes_c.append(amplitude_c_current)

# Plotar a amplitude em função de wf
plt.figure(figsize=(10, 6))
plt.plot(wf_values_c, amplitudes_c, marker='o', linestyle='-', markersize=4, label='Amplitude Numérica')

# Opcional: Adicionar a curva de amplitude teórica para comparação
# Fórmula da amplitude: A(wf) = (F0/m) / sqrt((wf^2 - omega_0^2)^2 + (b*wf/m)^2) 
amplitude_teorica_c = []
for current_wf in wf_values_c:
    denom = np.sqrt((current_wf**2 - omega_0**2)**2 + ((b * current_wf) / m)**2)
    amp_theor = (F0 / m) / denom
    amplitude_teorica_c.append(amp_theor)

plt.plot(wf_values_c, amplitude_teorica_c, 'r--', label='Amplitude Teórica')


plt.xlabel('Frequência da Força Externa $\omega_f$ (rad/s)')
plt.ylabel('Amplitude (m)')
plt.title('Amplitude do Movimento em Função da Frequência da Força Externa')
plt.grid(True)
plt.legend()
plt.show()