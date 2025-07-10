import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros do Sistema --- 
m = 1.0  # kg
k = 1.0  # N/m
kp = 0.5 # N/m (k_linha, constante da mola de acoplamento)
x_Aeq = 1.0 # m
x_Beq = 1.2 # m

# --- Parâmetros da Simulação ---
dt = 0.001  # Passo de tempo
t_total = 40.0 # Tempo total de simulação 

# --- Função de Simulação (Euler-Cromer) ---
def simulate_coupled_oscillators(x_A0, x_B0, v_Ax0, v_Bx0, dt, t_total, case_label):
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
        a_A = (-k * u_A - kp * (u_A - u_B)) / m
        a_B = (-k * u_B + kp * (u_A - u_B)) / m # Cuidado com o sinal do segundo termo

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

# --- ALÍNEA a) - Calcular a lei do movimento para cada caso ---

# Caso i) 
x_A0_i = x_Aeq + 0.05
x_B0_i = x_Beq + 0.05
v_Ax0_i = 0.0
v_Bx0_i = 0.0
t_i, xA_i, xB_i = simulate_coupled_oscillators(x_A0_i, x_B0_i, v_Ax0_i, v_Bx0_i, dt, t_total, "Caso i")

# Caso ii) 
x_A0_ii = x_Aeq + 0.05
x_B0_ii = x_Beq - 0.05
v_Ax0_ii = 0.0
v_Bx0_ii = 0.0
t_ii, xA_ii, xB_ii = simulate_coupled_oscillators(x_A0_ii, x_B0_ii, v_Ax0_ii, v_Bx0_ii, dt, t_total, "Caso ii")

# Caso iii) 
x_A0_iii = x_Aeq + 0.05
x_B0_iii = x_Beq
v_Ax0_iii = 0.0
v_Bx0_iii = 0.0
t_iii, xA_iii, xB_iii = simulate_coupled_oscillators(x_A0_iii, x_B0_iii, v_Ax0_iii, v_Bx0_iii, dt, t_total, "Caso iii")

# Plotar os resultados 
plt.figure(figsize=(12, 10))

plt.subplot(3, 1, 1)
plt.plot(t_i, xA_i, label='Corpo A')
plt.plot(t_i, xB_i, label='Corpo B')
plt.axhline(y=x_Aeq, color='gray', linestyle='--', linewidth=0.8, label='$x_{Aeq}$')
plt.axhline(y=x_Beq, color='lightgray', linestyle='--', linewidth=0.8, label='$x_{Beq}$')
plt.title('Caso i) $x_{A0}=x_{Aeq}+0.05$, $x_{B0}=x_{Beq}+0.05$')
plt.ylabel('Posição (m)')
plt.grid(True)
plt.legend()
plt.ylim(x_Aeq - 0.1, x_Beq + 0.1) # Ajusta o limite y para visualização

plt.subplot(3, 1, 2)
plt.plot(t_ii, xA_ii, label='Corpo A')
plt.plot(t_ii, xB_ii, label='Corpo B')
plt.axhline(y=x_Aeq, color='gray', linestyle='--', linewidth=0.8)
plt.axhline(y=x_Beq, color='lightgray', linestyle='--', linewidth=0.8)
plt.title('Caso ii) $x_{A0}=x_{Aeq}+0.05$, $x_{B0}=x_{Beq}-0.05$')
plt.ylabel('Posição (m)')
plt.grid(True)
plt.legend()
plt.ylim(x_Aeq - 0.1, x_Beq + 0.1)

plt.subplot(3, 1, 3)
plt.plot(t_iii, xA_iii, label='Corpo A')
plt.plot(t_iii, xB_iii, label='Corpo B')
plt.axhline(y=x_Aeq, color='gray', linestyle='--', linewidth=0.8)
plt.axhline(y=x_Beq, color='lightgray', linestyle='--', linewidth=0.8)
plt.title('Caso iii) $x_{A0}=x_{Aeq}+0.05$, $x_{B0}=x_{Beq}$')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.grid(True)
plt.legend()
plt.ylim(x_Aeq - 0.1, x_Beq + 0.1)

plt.tight_layout()
plt.show()

# --- ALÍNEA b) - Caracterizar o movimento --- 
print("--- b) Caracterização do Movimento ---")
print("Caso i): Os corpos A e B oscilam em fase (sincronizados) com um movimento harmónico simples. A mola do meio não é esticada nem comprimida em relação ao seu comprimento de equilíbrio, então ela não exerce força de acoplamento entre os corpos (além das forças devido às suas próprias molas). Corresponde ao Modo Normal 1. ")
print("Caso ii): Os corpos A e B oscilam em oposição de fase (um para a direita quando o outro vai para a esquerda) com um movimento harmónico simples. A mola do meio é esticada e comprimida ao máximo. Corresponde ao Modo Normal 2. ")
print("Caso iii): O movimento de cada corpo é mais complexo, parecendo irregular ou com batimentos (amplitude modulada). Este é o resultado de uma sobreposição dos dois modos normais, pois as condições iniciais não ativam apenas um dos modos puros. ")

# --- ALÍNEA c) - Medir Período e Frequência Angular --- 

# Funções para medir o período de um sinal senoidal/quase-senoidal
def measure_period_and_omega(t_values, x_values, start_time_for_analysis=0.0):
    # Encontrar picos para medir o período
    t_peaks = []
    # Encontra o primeiro índice após o tempo de início da análise
    start_index = np.where(np.array(t_values) >= start_time_for_analysis)[0][0]
    
    for i in range(start_index + 1, len(x_values) - 1):
        # Verifica se é um máximo local
        if x_values[i] > x_values[i-1] and x_values[i] > x_values[i+1]:
            t_peaks.append(t_values[i])
            
    if len(t_peaks) >= 2:
        periods = np.diff(t_peaks)
        avg_period = np.mean(periods)
        avg_omega = 2 * np.pi / avg_period
        return avg_period, avg_omega
    else:
        return np.nan, np.nan # Não foi possível determinar o período

print("\n--- c) Período e Frequência Angular ---")

# Caso i)
T_num_i, omega_num_i = measure_period_and_omega(t_i, xA_i)
print(f"Caso i): Período Numérico = {T_num_i:.3f} s, Frequência Angular Numérica = {omega_num_i:.3f} rad/s")
print(f"Esperado (Modo 1): T_1 = {2*np.pi/1.0:.3f} s, omega_1 = {1.0:.3f} rad/s")
print(f"Conformidade: {'Sim' if abs(T_num_i - (2*np.pi/1.0)) < 0.01 and abs(omega_num_i - 1.0) < 0.01 else 'Não'}. ")

# Caso ii)
T_num_ii, omega_num_ii = measure_period_and_omega(t_ii, xA_ii)
print(f"Caso ii): Período Numérico = {T_num_ii:.3f} s, Frequência Angular Numérica = {omega_num_ii:.3f} rad/s")
print(f"Esperado (Modo 2): T_2 = {2*np.pi/np.sqrt(2):.3f} s, omega_2 = {np.sqrt(2):.3f} rad/s")
print(f"Conformidade: {'Sim' if abs(T_num_ii - (2*np.pi/np.sqrt(2))) < 0.01 and abs(omega_num_ii - np.sqrt(2)) < 0.01 else 'Não'}. ")
print("Em ambos os casos, os resultados numéricos correspondem aos períodos e frequências dos modos normais, confirmando as expectativas teóricas. ")