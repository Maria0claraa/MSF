import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange
from scipy.stats import linregress

# --- Parâmetros do sistema ---
m = 0.25 # kg
k = 1.0  # N/m
b = 0.1  # kg/s

# --- Condições Iniciais ---
x0 = 0.4 # m
vx0 = 0.0 # m/s

# --- Parâmetros da simulação ---
dt = 0.0001 # Passo de tempo (pequeno para precisão nos picos)
t_total = 20.0 # s

# --- Função de Aceleração ---
def acceleration_damped(x, vx):
    return -k / m * x - b / m * vx

# --- Simulação (Euler-Cromer) ---
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
    ax = acceleration_damped(x, vx)
    vx = vx + ax * dt
    x = x + vx * dt
    t = t + dt

    t_values.append(t)
    x_values.append(x)
    vx_values.append(vx)

# --- ALÍNEA a) ---
print("--- Alínea a) ---")
plt.figure(figsize=(10, 6))
plt.plot(t_values, x_values, label='x(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Harmónico Amortecido')
plt.grid(True)
plt.legend()
plt.show()

# --- ALÍNEA b) ---
print("\n--- Alínea b) ---")
peak_times = []
peak_amplitudes = []

# Encontrar índices dos máximos e mínimos locais
for i in range(1, len(x_values) - 1):
    # Condição para máximo local
    if x_values[i] > x_values[i-1] and x_values[i] > x_values[i+1]:
        # Interpolação de Lagrange para o máximo
        if i > 0 and i < len(x_values) - 1: # Garantir que temos 3 pontos
            x_interp = np.array([t_values[i-1], t_values[i], t_values[i+1]])
            y_interp = np.array([x_values[i-1], x_values[i], x_values[i+1]])
            
            # Polinómio de Lagrange (grau 2)
            poly = lagrange(x_interp, y_interp)
            
            # Derivada do polinómio de grau 2 é 2ax + b. Onde a derivada é zero, temos o extremo.
            # Se poly = c2*x^2 + c1*x + c0, então derivada = 2*c2*x + c1.
            # x_vertex = -c1 / (2*c2)
            coeffs = poly.coeffs
            if len(coeffs) == 3 and coeffs[0] != 0: # Para um polinómio de grau 2
                t_peak = -coeffs[1] / (2 * coeffs[0])
                amplitude_peak = poly(t_peak)
                peak_times.append(t_peak)
                peak_amplitudes.append(amplitude_peak)
            elif len(coeffs) == 2: # Caso a interpolação retorne grau 1 (muito raro num pico)
                 t_peak = t_values[i] # Apenas usa o ponto original
                 amplitude_peak = x_values[i]
                 peak_times.append(t_peak)
                 peak_amplitudes.append(amplitude_peak)


    # Condição para mínimo local
    elif x_values[i] < x_values[i-1] and x_values[i] < x_values[i+1]:
        # Interpolação de Lagrange para o mínimo
        if i > 0 and i < len(x_values) - 1:
            x_interp = np.array([t_values[i-1], t_values[i], t_values[i+1]])
            y_interp = np.array([x_values[i-1], x_values[i], x_values[i+1]])

            poly = lagrange(x_interp, y_interp)

            coeffs = poly.coeffs
            if len(coeffs) == 3 and coeffs[0] != 0:
                t_min = -coeffs[1] / (2 * coeffs[0])
                amplitude_min = poly(t_min)
                peak_times.append(t_min)
                peak_amplitudes.append(amplitude_min)
            elif len(coeffs) == 2:
                t_min = t_values[i]
                amplitude_min = x_values[i]
                peak_times.append(t_min)
                peak_amplitudes.append(amplitude_min)

# Ordenar os picos e vales pelo tempo
sorted_peaks_and_vals = sorted(zip(peak_times, peak_amplitudes), key=lambda item: item[0])
peak_times_sorted, peak_amplitudes_sorted = zip(*sorted_peaks_and_vals)

print("Tempos e Amplitudes dos Máximos/Mínimos Locais:")
for t_p, amp_p in sorted_peaks_and_vals:
    print(f"Tempo: {t_p:.4f} s, Amplitude: {amp_p:.6f} m")

# --- ALÍNEA c) ---
print("\n--- Alínea c) ---")

# Filtrar para amplitudes absolutas para o log plot, e apenas as primeiras para o declínio exponencial
# A primeira "amplitude" é x0. As seguintes são os picos e vales.
# Vamos pegar apenas os picos de amplitude (que é o envelope superior)
# Ou, de forma mais geral, o valor absoluto de todos os extremos.

# Como a oscilação começa em x=0.4m (positivo), o primeiro extremo é um máximo.
# Os próximos são um mínimo, depois um máximo, etc.
# Queremos a sequência de amplitudes (magnitude dos extremos).
amplitudes_envelope = [abs(amp) for amp in peak_amplitudes_sorted]
times_envelope = list(peak_times_sorted)

# Remove o primeiro ponto (t=0) se já não for um pico detetado
if times_envelope[0] > 0.001: # Se o primeiro ponto de t_values não foi um pico
    amplitudes_envelope.insert(0, abs(x_values[0]))
    times_envelope.insert(0, t_values[0])


log_amplitudes = np.log(amplitudes_envelope)

plt.figure(figsize=(10, 6))
plt.plot(times_envelope, log_amplitudes, 'o', label='log(Amplitude) numérico')

# Ajuste linear
slope, intercept, r_value, p_value, std_err = linregress(times_envelope, log_amplitudes)
plt.plot(times_envelope, intercept + slope * np.array(times_envelope), 'r-', label=f'Ajuste Linear: y = {slope:.4f}x + {intercept:.4f}')

plt.xlabel('Tempo (s)')
plt.ylabel('log(Amplitude (m))')
plt.title('Logaritmo das Amplitudes vs. Tempo')
plt.grid(True)
plt.legend()
plt.show()

print(f"Declive do Ajuste Linear: {slope:.9f} s^-1") # Aumentar casas decimais para precisão
print(f"Erro Padrão do Declive: {std_err:.9f} s^-1")

# Comparação com a teoria
# A amplitude teórica é A(t) = A0 * exp(- (b / 2m) * t)
# Então, log(A(t)) = log(A0) - (b / 2m) * t
# O declive teórico esperado é -b / (2m)
declive_teorico = -b / (2 * m)
print(f"Declive Teórico Esperado: {declive_teorico:.9f} s^-1")

# Conclusão sobre a concordância
print(f"Diferença entre o declive numérico e teórico: {abs(slope - declive_teorico):.9f} s^-1")
# Verifica se o valor esperado está dentro do intervalo do declive_numerico +/- std_err
# Se (slope - std_err) <= declive_teorico <= (slope + std_err)
if (slope - std_err <= declive_teorico <= slope + std_err):
    print("O declive numérico CONCORDA com o declive teórico dentro do erro padrão.")
else:
    print("O declive numérico NÃO CONCORDA com o declive teórico dentro do erro padrão.")
    print("No entanto, a diferença é pequena e pode ser considerada razoável dependendo da precisão exigida.")