import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros do sistema ---
m = 1.0   # kg
k = 1.0   # N/m
alpha = -0.01 # N/m^2

# --- Função para calcular a aceleração ---
def acceleration(x, m_val, k_val, alpha_val):
    return (-k_val * x - 3 * alpha_val * x**2) / m_val

# --- Função para calcular a energia potencial ---
def potential_energy(x, k_val, alpha_val):
    return 0.5 * k_val * x**2 + alpha_val * x**3

# --- Função para simular o movimento com Euler-Cromer ---
def simulate_oscillator(x0, vx0, dt, t_total, m_val, k_val, alpha_val):
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
    energy_values.append(0.5 * m_val * vx**2 + potential_energy(x, k_val, alpha_val))

    while t <= t_total:
        ax = acceleration(x, m_val, k_val, alpha_val)
        vx = vx + ax * dt
        x = x + vx * dt
        t = t + dt

        t_values.append(t)
        x_values.append(x)
        vx_values.append(vx)
        energy_values.append(0.5 * m_val * vx**2 + potential_energy(x, k_val, alpha_val))
    
    return np.array(t_values), np.array(x_values), np.array(vx_values), np.array(energy_values)

# --- ALÍNEA a) ---
print("--- ALÍNEA a) ---")
x_plot = np.linspace(-5, 5, 500) # Intervalo de x para o gráfico
Ep_plot = potential_energy(x_plot, k, alpha)

plt.figure(figsize=(8, 6))
plt.plot(x_plot, Ep_plot, label='Energia Potencial $E_p(x)$')
plt.xlabel('Posição (m)')
plt.ylabel('Energia Potencial (J)')
plt.title('Diagrama de Energia Potencial do Oscilador Cúbico')
plt.grid(True)
plt.ylim(0, 20) # Ajustar limites y conforme a solução gráfica
plt.show()

# Análise do movimento para E_total < 1 J
# Pelo gráfico, vê-se que para x > 0 existe uma barreira de potencial.
# O valor do pico da barreira (derivada primeira = 0)
# d(Ep)/dx = k*x + 3*alpha*x^2 = x * (k + 3*alpha*x) = 0
# x = 0 (mínimo local) ou k + 3*alpha*x = 0 => x = -k / (3*alpha)
x_barreira = -k / (3 * alpha)
Ep_barreira = potential_energy(x_barreira, k, alpha)
print(f"Ponto da barreira de potencial em x = {x_barreira:.3f} m")
print(f"Valor da barreira de potencial Ep = {Ep_barreira:.3f} J")

if Ep_barreira > 1.0:
    print("Quando a energia total for menor que 1 J, o movimento será periódico (confinado no poço de potencial).")
else:
    print("Para energia total menor que 1 J, o movimento pode não ser confinado.")

# --- ALÍNEA b) ---
print("\n--- ALÍNEA b) ---")
x0_b = 1.3 # m
vx0_b = 0.0 # m/s
dt = 0.0001 # dt para maior precisão em sistemas não lineares
t_total = 40.0 # s

t_b, x_b, vx_b, Em_b = simulate_oscillator(x0_b, vx0_b, dt, t_total, m, k, alpha)

plt.figure(figsize=(10, 6))
plt.plot(t_b, x_b, label=f'x(t) para x0={x0_b} m')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Cúbico (b)')
plt.grid(True)
plt.legend()
plt.show()

Em_total_b = Em_b[0] # Energia mecânica inicial
print(f"Energia mecânica para x0={x0_b} m: {Em_total_b:.3f} J")

# Limites do movimento
x_min_b = np.min(x_b)
x_max_b = np.max(x_b)
print(f"Limites do movimento para x0={x0_b} m: [{x_min_b:.3f} m, {x_max_b:.3f} m]")

# Cálculo do período (aproximado, por picos)
# Encontrar picos/vales para calcular o período
peak_indices = []
for i in range(1, len(x_b) - 1):
    if (x_b[i] > x_b[i-1] and x_b[i] > x_b[i+1]) or (x_b[i] < x_b[i-1] and x_b[i] < x_b[i+1]):
        peak_indices.append(i)

# Filtrar para ter apenas os picos de um lado (ex: os máximos)
# Ou mais robusto: contar as passagens por zero com velocidade num determinado sentido
# Para este tipo de gráfico, é fácil ver os picos
# Vamos pegar no tempo entre os primeiros picos de amplitude
if len(peak_indices) > 2:
    T_b_values = np.diff(t_b[peak_indices])
    T_b_avg = np.mean(T_b_values)
    f_b = 1 / T_b_avg
    print(f"Período do movimento para x0={x0_b} m: {T_b_avg:.3f} s")
    print(f"Frequência do movimento para x0={x0_b} m: {f_b:.3f} Hz")
else:
    print("Não foi possível calcular o período/frequência com precisão suficiente (poucas oscilações).")

# --- ALÍNEA c) ---
print("\n--- ALÍNEA c) ---")
x0_c = 2.9 # m
vx0_c = 0.0 # m/s
dt = 0.0001 # dt para maior precisão em sistemas não lineares
t_total = 40.0 # s

t_c, x_c, vx_c, Em_c = simulate_oscillator(x0_c, vx0_c, dt, t_total, m, k, alpha)

plt.figure(figsize=(10, 6))
plt.plot(t_c, x_c, label=f'x(t) para x0={x0_c} m')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento do Oscilador Cúbico (c)')
plt.grid(True)
plt.legend()
plt.show()

Em_total_c = Em_c[0] # Energia mecânica inicial
print(f"Energia mecânica para x0={x0_c} m: {Em_total_c:.3f} J")

# Limites do movimento
x_min_c = np.min(x_c)
x_max_c = np.max(x_c)
print(f"Limites do movimento para x0={x0_c} m: [{x_min_c:.3f} m, {x_max_c:.3f} m]")

# Cálculo do período (aproximado, por picos)
peak_indices_c = []
for i in range(1, len(x_c) - 1):
    if (x_c[i] > x_c[i-1] and x_c[i] > x_c[i+1]) or (x_c[i] < x_c[i-1] and x_c[i] < x_c[i+1]):
        peak_indices_c.append(i)

if len(peak_indices_c) > 2:
    T_c_values = np.diff(t_c[peak_indices_c])
    T_c_avg = np.mean(T_c_values)
    f_c = 1 / T_c_avg
    print(f"Período do movimento para x0={x0_c} m: {T_c_avg:.3f} s")
    print(f"Frequência do movimento para x0={x0_c} m: {f_c:.3f} Hz")
else:
    print("Não foi possível calcular o período/frequência com precisão suficiente (poucas oscilações).")