import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq # Para a análise de Fourier na alínea d)

# --- Parâmetros fixos do sistema ---
m = 1.0  # kg
k = 1.0  # N/m
alpha = 1.00 # N/m^2 (o valor crítico neste problema)
b = 0.05 # kg/s
F0 = 7.5 # N
wf = 1.0 # rad/s

# --- Função da Aceleração (dvx/dt) para RK4 ---
def acceleration_quartic_forced_damped(x, vx, t):
    # Fx = -k*x*(1 + 2*alpha*x^2) - b*vx + F0*cos(wf*t)
    return (-k * x * (1 + 2 * alpha * x**2) - b * vx + F0 * np.cos(wf * t)) / m

# --- Função de Energia Potencial ---
def potential_energy_quartic(x_val):
    return 0.5 * k * x_val**2 * (1 + alpha * x_val**2)

# --- Implementação do Método de Runge-Kutta de 4ª Ordem (RK4) ---
def rk4_step(x, vx, t, dt, accel_func):
    # k1 para x e vx
    k1_vx = accel_func(x, vx, t)
    k1_x = vx

    # k2 para x e vx
    k2_vx = accel_func(x + k1_x * dt / 2, vx + k1_vx * dt / 2, t + dt / 2)
    k2_x = vx + k1_vx * dt / 2

    # k3 para x e vx
    k3_vx = accel_func(x + k2_x * dt / 2, vx + k2_vx * dt / 2, t + dt / 2)
    k3_x = vx + k2_vx * dt / 2

    # k4 para x e vx
    k4_vx = accel_func(x + k3_x * dt, vx + k3_vx * dt, t + dt)
    k4_x = vx + k3_vx * dt

    # Atualização
    x_new = x + (k1_x + 2*k2_x + 2*k3_x + k4_x) * dt / 6
    vx_new = vx + (k1_vx + 2*k2_vx + 2*k3_vx + k4_vx) * dt / 6

    return x_new, vx_new

# --- Função de Simulação com RK4 ---
def simulate_oscillator_rk4(x0, vx0, dt, t_total):
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
        x, vx = rk4_step(x, vx, t, dt, acceleration_quartic_forced_damped)
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
dt_a_1 = 0.01 # Passo de tempo maior
dt_a_2 = 0.001 # Passo de tempo menor (para confiança)
t_total_a = 100.0 # s (tempo suficiente para regime estacionário, como nas soluções)

# Simulação com dt_a_1
print(f"Simulando com dt={dt_a_1}...")
t_a1, x_a1, vx_a1, Em_a1 = simulate_oscillator_rk4(x0_a, vx0_a, dt_a_1, t_total_a)
# Simulação com dt_a_2
print(f"Simulando com dt={dt_a_2}...")
t_a2, x_a2, vx_a2, Em_a2 = simulate_oscillator_rk4(x0_a, vx0_a, dt_a_2, t_total_a)

plt.figure(figsize=(10, 6))
plt.plot(t_a1, x_a1, label=f'dt={dt_a_1}')
# Para sobrepor de forma clara, vamos plotar apenas uma parte do dt_a_2
# e talvez com um estilo de linha diferente
plt.plot(t_a2, x_a2, label=f'dt={dt_a_2}', linestyle='--')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Quártico Forçado (Alínea a)')
plt.grid(True)
plt.legend()
plt.show()

# Verificar confiança (comparar apenas a parte final do movimento)
# Ajustar para o mesmo comprimento de tempo se os t_total forem diferentes
min_len = min(len(x_a1), len(x_a2))
# Comparar a "parte estável" (últimos 10-20 segundos, por exemplo)
comparison_start_index = int(0.8 * min_len) 
diff_end = np.mean(np.abs(x_a1[comparison_start_index:min_len] - x_a2[comparison_start_index:min_len]))

print(f"Diferença média na parte final (após transiente): {diff_end:.3e} m")
if diff_end < 1e-2: # Pequena tolerância
    print("Temos confiança no resultado. As leis do movimento obtidas por dois passos temporais diferentes são a mesma (ou muito próximas).")
else:
    print("Os resultados com diferentes passos de tempo não são suficientemente próximos. Considere reduzir ainda mais o 'dt'.")

# --- ALÍNEA b) ---
print("\n--- Alínea b) ---")
# Regime estacionário: ignorar a parte inicial (transiente)
# O tempo de relaxamento é 2m/b = 40s. Vamos pegar a parte final da simulação (após uns 60s).
steady_state_start_time_b = 60.0 # s
steady_state_index_b = np.where(np.array(t_a1) >= steady_state_start_time_b)[0][0]

x_steady_b = x_a1[steady_state_index_b:]
vx_steady_b = vx_a1[steady_state_index_b:]
t_steady_b = t_a1[steady_state_index_b:]

# Limites do movimento (amplitude)
amplitude_max_b = np.max(x_steady_b)
amplitude_min_b = np.min(x_steady_b)
print(f"Limites do movimento (amplitude): Max={amplitude_max_b:.4f} m, Min={amplitude_min_b:.4f} m") # Solução: 2.1066 m e -2.3606 m

# Período: como o movimento é periódico, mas não sinusoidal simples, vamos identificar os picos
peak_times_b = []
for i in range(1, len(x_steady_b) - 1):
    if x_steady_b[i] > x_steady_b[i-1] and x_steady_b[i] > x_steady_b[i+1]:
        peak_times_b.append(t_steady_b[i])

if len(peak_times_b) >= 2:
    periods_b_list = np.diff(peak_times_b)
    periodo_b_avg = np.mean(periods_b_list)
    print(f"Período do movimento no regime estacionário (alínea b): {periodo_b_avg:.3f} s") # Solução: 12.57 s (4*pi)
else:
    print("Não foi possível determinar o período numericamente com precisão suficiente (poucos picos encontrados).")

# Gráfico no Espaço da Fase
plt.figure(figsize=(8, 8))
plt.plot(x_steady_b, vx_steady_b, label='Trajetória no Espaço da Fase')
plt.xlabel('Posição x (m)')
plt.ylabel('Velocidade vx (m/s)')
plt.title('Espaço da Fase (Regime Estacionário - Alínea b)')
plt.grid(True)
plt.legend()
plt.show()


# --- ALÍNEA c) ---
print("\n--- Alínea c) ---")
x0_c = -3.0 # m
vx0_c = -3.0 # m/s
dt_c_1 = 0.01
dt_c_2 = 0.001
t_total_c = 100.0 # s

print(f"Simulando com dt={dt_c_1}...")
t_c1, x_c1, vx_c1, Em_c1 = simulate_oscillator_rk4(x0_c, vx0_c, dt_c_1, t_total_c)
print(f"Simulando com dt={dt_c_2}...")
t_c2, x_c2, vx_c2, Em_c2 = simulate_oscillator_rk4(x0_c, vx_c2, dt_c_2, t_total_c)

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
min_len_c = min(len(x_c1), len(x_c2))
comparison_start_index_c = int(0.8 * min_len_c)
diff_end_c = np.mean(np.abs(x_c1[comparison_start_index_c:min_len_c] - x_c2[comparison_start_index_c:min_len_c]))

print(f"Diferença média na parte final (após transiente): {diff_end_c:.3e} m")
if diff_end_c < 1e-2:
    print("Temos confiança no resultado. As leis do movimento obtidas por dois passos temporais diferentes são a mesma (ou muito próximas).")
else:
    print("Os resultados com diferentes passos de tempo não são suficientemente próximos. Considere reduzir ainda mais o 'dt'.")

# --- ALÍNEA d) ---
print("\n--- Alínea d) ---")
# Regime estacionário
steady_state_start_time_d = 60.0 # s
steady_state_index_d = np.where(np.array(t_c1) >= steady_state_start_time_d)[0][0]

x_steady_d = x_c1[steady_state_index_d:]
vx_steady_d = vx_c1[steady_state_index_d:]
t_steady_d = t_c1[steady_state_index_d:]

# Limites do movimento (amplitude)
amplitude_max_d = np.max(x_steady_d)
amplitude_min_d = np.min(x_steady_d)
print(f"Limites do movimento (amplitude): Max={amplitude_max_d:.4f} m, Min={amplitude_min_d:.4f} m") # Solução: 2.3800 m e -2.3800 m

# Período
peak_times_d = []
for i in range(1, len(x_steady_d) - 1):
    if x_steady_d[i] > x_steady_d[i-1] and x_steady_d[i] > x_steady_d[i+1]:
        peak_times_d.append(t_steady_d[i])

if len(peak_times_d) >= 2:
    periods_d_list = np.diff(peak_times_d)
    periodo_d_avg = np.mean(periods_d_list)
    print(f"Período do movimento no regime estacionário (alínea d): {periodo_d_avg:.3f} s") # Solução: 18.85 s (6*pi)
else:
    print("Não foi possível determinar o período numericamente com precisão suficiente (poucos picos encontrados).")

# Gráfico no Espaço da Fase
plt.figure(figsize=(8, 8))
plt.plot(x_steady_d, vx_steady_d, label='Trajetória no Espaço da Fase')
plt.xlabel('Posição x (m)')
plt.ylabel('Velocidade vx (m/s)')
plt.title('Espaço da Fase (Regime Estacionário - Alínea d)')
plt.grid(True)
plt.legend()
plt.show()

# Análise de Fourier (simplificada, apenas para mostrar a ideia)
# Para uma análise mais robusta, pode ser necessário ajustar a janela de tempo e a duração
# Número de pontos na amostra
N_d = len(x_steady_d)
# Espaçamento da amostra
T_d_sample = t_steady_d[1] - t_steady_d[0] # dt
yf_d = fft(x_steady_d)
xf_d = fftfreq(N_d, T_d_sample)[:N_d//2] # Frequências positivas

plt.figure(figsize=(10, 6))
plt.plot(xf_d, 2.0/N_d * np.abs(yf_d[0:N_d//2]))
plt.xlabel('Frequência (Hz)')
plt.ylabel('Amplitude')
plt.title('Espectro de Frequências (Análise de Fourier - Alínea d)')
plt.grid(True)
plt.xlim(0, 0.5) # Limitar a gama de frequências para melhor visualização
plt.show()
print("Análise de Fourier realizada. O gráfico de espectro de frequências mostra as componentes de frequência presentes no movimento.")
print(f"Frequência da força externa (Hz): {wf / (2*np.pi):.3f}")
# Pode-se procurar picos no espectro que correspondam a wf ou múltiplos inteiros (harmónicas)
# ou frequências sub-harmónicas para comportamento não linear/caótico.


# --- ALÍNEA e) ---
print("\n--- Alínea e) ---")
# Energia Mecânica para a alínea a) (primeiro caso)
plt.figure(figsize=(10, 6))
plt.plot(t_a1, Em_a1, label='Energia Mecânica (Alínea a)')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia Mecânica (J)')
plt.title('Energia Mecânica do Oscilador Quártico Forçado e Amortecido (Alínea a)')
plt.grid(True)
plt.legend()
plt.show()

# Energia Mecânica para a alínea c) (segundo caso)
plt.figure(figsize=(10, 6))
plt.plot(t_c1, Em_c1, label='Energia Mecânica (Alínea c)')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia Mecânica (J)')
plt.title('Energia Mecânica do Oscilador Quártico Forçado e Amortecido (Alínea c)')
plt.grid(True)
plt.legend()
plt.show()

print("A energia mecânica NÃO É constante ao longo do tempo em ambos os casos.")
print("O sistema recebe energia da força externa e dissipa energia devido ao amortecimento.")
print("No regime estacionário, a energia média é mantida, mas a energia instantânea varia e pode ter flutuações complexas.")


# --- ALÍNEA f) ---
print("\n--- Alínea f) ---")
# Comparar regimes estacionários das alíneas b) e d)
print("Comparação dos regimes estacionários:")
print(f"  Caso (b): Limites Max={amplitude_max_b:.4f} m, Min={amplitude_min_b:.4f} m, Período={periodo_b_avg:.3f} s")
print(f"  Caso (d): Limites Max={amplitude_max_d:.4f} m, Min={amplitude_min_d:.4f} m, Período={periodo_d_avg:.3f} s")

# As soluções do PDF indicam resultados **diferentes** para as alíneas b) e d).
# b) Amplitude: [2.1066, -2.3606] m, Período: 12.57 s.
# d) Amplitude: [2.3800, -2.3800] m, Período: 18.85 s.
# Isso sugere **sensibilidade às condições iniciais** no regime estacionário.
# O movimento não é sinusoidal e o período é um múltiplo da força externa (12.57 = 4*pi, 18.85 = 6*pi aproximadamente).

print("\nCaracterização das soluções deste oscilador forçado:")
print("O sistema apresenta um comportamento transiente inicial, que decai com o tempo devido ao amortecimento.")
print("Após o transiente, o sistema atinge um regime estacionário que é periódico, mas não sinusoidal (devido à não-linearidade do termo quártico).")
print("No entanto, os **limites do movimento e o período no regime estacionário DEPENDEM das condições iniciais.**")
print("Esta dependência das condições iniciais no regime estacionário é uma característica de sistemas complexos e, em casos extremos (como o próximo problema, o problema 22), pode indicar comportamento caótico. Aqui, o sistema é periódico, mas com diferentes 'órbitas' dependendo de onde se começa.")
print("A solução não é sinusoidal e o período é um múltiplo da frequência da força externa (ou uma combinação de harmónicas), não sendo um simples oscilador harmónico forçado.")