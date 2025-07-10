import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros do Sistema ---
m = 1.0  # kg 
k = 1.0  # N/m 
kp = 0.5 # N/m (k_linha) 
b = 0.05 # kg/s 
F0 = 0.005 # N 
x_Aeq = 1.0 # m 
x_Beq = 1.2 # m 

# --- Função de Simulação (Euler-Cromer) ---
def simulate_damped_forced_coupled_oscillators(x_A0, x_B0, v_Ax0, v_Bx0, wf_current, dt, t_total):
    t_values = []
    xA_values = []
    xB_values = []
    
    # Converter posições iniciais para desvios
    u_A = x_A0 - x_Aeq
    u_B = x_B0 - x_Beq
    
    v_A = v_Ax0
    v_B = v_Bx0
    t = 0.0

    t_values.append(t)
    xA_values.append(u_A + x_Aeq) # Armazenar posição absoluta
    xB_values.append(u_B + x_Beq)

    while t <= t_total:
        # Calcular acelerações 
        a_A = (-k * u_A - kp * (u_A - u_B) - b * v_A + F0 * np.cos(wf_current * t)) / m
        a_B = (-k * u_B + kp * (u_A - u_B) - b * v_B) / m 

        # Atualizar velocidades
        v_A = v_A + a_A * dt
        v_B = v_B + a_B * dt

        # Atualizar posições (desvios)
        u_A = u_A + v_A * dt
        u_B = u_B + v_B * dt

        # Atualizar tempo
        t = t + dt

        t_values.append(t)
        xA_values.append(u_A + x_Aeq) # Armazenar posição absoluta
        xB_values.append(u_B + x_Beq)
        
    return t_values, xA_values, xB_values

# --- ALÍNEA a) - Calcular a lei do movimento ---
print("--- a) Lei do Movimento ---")

# Condições iniciais para alínea a) 
x_A0_a = x_Aeq + 0.05
x_B0_a = x_Beq + 0.05
v_Ax0_a = 0.0
v_Bx0_a = 0.0
wf_a = 1.0 # rad/s 
dt_a = 0.001
t_total_a = 150.0 # s 

t_a, xA_a, xB_a = simulate_damped_forced_coupled_oscillators(
    x_A0_a, x_B0_a, v_Ax0_a, v_Bx0_a, wf_a, dt_a, t_total_a
)

plt.figure(figsize=(10, 6))
plt.plot(t_a, xA_a, label='Corpo A')
plt.plot(t_a, xB_a, label='Corpo B')
plt.axhline(y=x_Aeq, color='gray', linestyle='--', linewidth=0.8, label='$x_{Aeq}$')
plt.axhline(y=x_Beq, color='lightgray', linestyle='--', linewidth=0.8, label='$x_{Beq}$')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title(f'Lei do Movimento para $\omega_f$ = {wf_a} rad/s')
plt.grid(True)
plt.legend()
plt.ylim(x_Aeq - 0.08, x_Beq + 0.08) # Ajusta o limite y para visualização
plt.show()

# --- ALÍNEA b) - Amplitude em função de $\omega_f$ ---
print("\n--- b) Amplitude em função de $\omega_f$ ---")

wf_values_b = np.linspace(0.0, 2.5, 100) # Gama de $\omega_f$ de 0 a 2.5 rad/s 
amplitudes_A = []
amplitudes_B = []

# Parâmetros de simulação para cada ponto do gráfico de amplitude
# Tempo total deve ser suficiente para o regime estacionário. O tempo de decaimento (2m/b) = 40s.
# Então, 150-200s é razoável para a simulação, e pegar a última parte para medir a amplitude.
t_total_b_sim = 250.0 # s
dt_b_sim = 0.001

# Definir o ponto de início da medição da amplitude no regime estacionário
steady_state_start_time = 150.0 # s (para garantir que o transiente já decaiu)

for current_wf in wf_values_b:
    # Simular o sistema para a frequência atual (com as mesmas CI da alínea a) 
    t_sim, xA_sim, xB_sim = simulate_damped_forced_coupled_oscillators(
        x_A0_a, x_B0_a, v_Ax0_a, v_Bx0_a, current_wf, dt_b_sim, t_total_b_sim
    )
    
    # Encontrar o índice de início para o regime estacionário
    steady_state_idx = np.where(np.array(t_sim) >= steady_state_start_time)[0]
    if len(steady_state_idx) == 0:
        # Caso o tempo de simulação seja muito curto para o tempo de início do regime estacionário
        # usar a última parte dos dados
        steady_state_idx = int(len(xA_sim) * 0.7)
    else:
        steady_state_idx = steady_state_idx[0]

    # Medir a amplitude no regime estacionário 
    amp_A_current = np.max(np.abs(np.array(xA_sim[steady_state_idx:]) - x_Aeq))
    amp_B_current = np.max(np.abs(np.array(xB_sim[steady_state_idx:]) - x_Beq))
    
    amplitudes_A.append(amp_A_current)
    amplitudes_B.append(amp_B_current)

plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.plot(wf_values_b, amplitudes_A, label='Amplitude Corpo A')
plt.axvline(x=1.0, color='r', linestyle='--', linewidth=0.8, label='$\omega_1 = 1.0$ rad/s')
plt.axvline(x=np.sqrt(2), color='g', linestyle='--', linewidth=0.8, label='$\omega_2 = \sqrt{2} \approx 1.414$ rad/s')
plt.ylabel('Amplitude (m)')
plt.title('Amplitude de Oscilação vs. Frequência de Forçamento')
plt.grid(True)
plt.legend()
plt.ylim(0, 0.015) # Ajustar para melhor visualização

plt.subplot(2, 1, 2)
plt.plot(wf_values_b, amplitudes_B, label='Amplitude Corpo B')
plt.axhline(y=x_Beq, color='lightgray', linestyle='--', linewidth=0.8)
plt.axvline(x=1.0, color='r', linestyle='--', linewidth=0.8)
plt.axvline(x=np.sqrt(2), color='g', linestyle='--', linewidth=0.8)
plt.xlabel('Frequência de Forçamento $\omega_f$ (rad/s)')
plt.ylabel('Amplitude (m)')
plt.grid(True)
plt.legend()
plt.ylim(0, 0.015)

plt.tight_layout()
plt.show()

print("--- O que se observa (Alínea b) ---") # 
print("O sistema exibe ressonância nos dois corpos. Observam-se picos de amplitude quando a frequência da força externa ($\omega_f$) se aproxima das frequências dos modos normais do sistema, ou seja, $\omega_1 = 1.0 \text{ rad/s}$ e $\omega_2 = \sqrt{2} \approx 1.414 \text{ rad/s}$.") [cite: 38]
print("Isto é um fenómeno clássico de ressonância em osciladores acoplados forçados.") [cite: 38]
print("Para o corpo B, a amplitude é menor quando a frequência é perto de $\omega_1$.") # Custom observation
print("Para o corpo A, a amplitude é maior quando a frequência é perto de $\omega_1$.") # Custom observation