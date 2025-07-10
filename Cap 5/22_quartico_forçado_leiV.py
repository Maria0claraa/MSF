import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros fixos do sistema ---
m = 1.0  # kg
k = 1.0  # N/m (não usado diretamente na força se Ep = alpha*x^4, mas pode estar implícito)
# Atenção: a Ep é dada como alpha*x^4 e a Força como -4*alpha*x^3. Isso é consistente.
# O k=1 N/m no problema não é usado na força nem na Ep, parece ser um distrator,
# ou então refere-se a um oscilador harmónico subjacente para comparação de frequências, mas não é explícito.
# Vamos seguir as equações dadas: Fx = -4*alpha*x^3.
alpha = 0.25 # N/m^2 (ou J/m^4 se considerarmos Ep)
b = 0.05 # kg/s
F0 = 7.5 # N
wf = 1.0 # rad/s

# --- Função da Aceleração (dvx/dt) para RK4 ---
def acceleration_quartic_forced_damped_chaotic(x, vx, t):
    # Fx = -4*alpha*x^3 - b*vx + F0*cos(wf*t)
    return (-4 * alpha * x**3 - b * vx + F0 * np.cos(wf * t)) / m

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
def simulate_oscillator_rk4_chaotic(x0, vx0, dt, t_total):
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
        x, vx = rk4_step(x, vx, t, dt, acceleration_quartic_forced_damped_chaotic)
        t = t + dt

        t_values.append(t)
        x_values.append(x)
        vx_values.append(vx)
    
    return t_values, x_values, vx_values

# --- Condições Iniciais para o Problema ---
x0_base = 3.000 # m
vx0 = 0.0 # m/s

# Variações nas condições iniciais
delta_x = 0.001 # m

x0_case1 = x0_base
x0_case2 = x0_base + delta_x
x0_case3 = x0_base - delta_x # Opcional: para ver a divergência de ambos os lados

# Parâmetros de simulação
dt_sim = 0.00001 # Passo de tempo muito pequeno para alta precisão
t_total_sim = 80.0 # s (tempo suficiente para observar a divergência, como na solução)

print(f"Simulando com x0 = {x0_case1:.3f} m...")
t_vals1, x_vals1, vx_vals1 = simulate_oscillator_rk4_chaotic(x0_case1, vx0, dt_sim, t_total_sim)

print(f"Simulando com x0 = {x0_case2:.3f} m...")
t_vals2, x_vals2, vx_vals2 = simulate_oscillator_rk4_chaotic(x0_case2, vx0, dt_sim, t_total_sim)

print(f"Simulando com x0 = {x0_case3:.3f} m...")
t_vals3, x_vals3, vx_vals3 = simulate_oscillator_rk4_chaotic(x0_case3, vx0, dt_sim, t_total_sim)


# --- Plotar as Leis do Movimento ---
plt.figure(figsize=(10, 6))
plt.plot(t_vals1, x_vals1, label=f'x0={x0_case1:.3f} m')
plt.plot(t_vals2, x_vals2, label=f'x0={x0_case2:.3f} m', linestyle='--')
plt.plot(t_vals3, x_vals3, label=f'x0={x0_case3:.3f} m', linestyle=':') # Linha pontilhada para o terceiro caso
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Divergência das Trajetórias para Oscilador Quártico Caótico')
plt.grid(True)
plt.legend()
plt.show()

# --- Identificar o Instante de Divergência ---
# Vamos procurar o ponto em que a diferença entre as trajetórias excede um certo limiar.
# Este limiar pode ser a diferença inicial (delta_x) multiplicada por um fator,
# ou uma fração da amplitude típica do movimento.
# A amplitude aparente no gráfico é de cerca de 3m. Um limiar de 0.1m ou 0.2m já indica divergência significativa.

# Calcular a diferença absoluta entre as duas trajetórias
# Garantir que os arrays têm o mesmo comprimento (se t_total for ajustado para eles)
min_len = min(len(x_vals1), len(x_vals2))
diff_vals_abs = np.abs(np.array(x_vals1[:min_len]) - np.array(x_vals2[:min_len]))
times_for_diff = np.array(t_vals1[:min_len])

# Plotar a diferença para visualizar
plt.figure(figsize=(10, 4))
plt.plot(times_for_diff, diff_vals_abs, label='Diferença Absoluta entre x0=3.000 e x0=3.001')
plt.xlabel('Tempo (s)')
plt.ylabel('Diferença |x1-x2| (m)')
plt.title('Diferença entre Trajetórias com Condições Iniciais Próximas')
plt.grid(True)
plt.yscale('log') # Escala logarítmica para ver crescimento exponencial da diferença
plt.legend()
plt.show()


# Encontrar o instante em que a diferença excede um limiar
# O limiar pode ser algo como 10x a diferença inicial, ou 1% da amplitude máxima do movimento.
# A amplitude é de aproximadamente 3m (ver gráficos do problema 21). Vamos usar 0.1m como limiar.
divergence_threshold = 0.1 # m (ajustar conforme a amplitude típica do movimento)

divergence_time = None
for i, diff in enumerate(diff_vals_abs):
    if diff > divergence_threshold:
        divergence_time = times_for_diff[i]
        break

if divergence_time is not None:
    print(f"\nAs trajetórias divergem significativamente (diferença > {divergence_threshold} m) por volta de t = {divergence_time:.1f} s.")
    print("A partir deste instante, a lei do movimento deixa de poder ser calculada univocamente devido à sensibilidade às condições iniciais (caos).")
else:
    print(f"\nAs trajetórias não divergiram acima do limiar de {divergence_threshold} m dentro do tempo de simulação de {t_total_sim} s.")

print("\n(A solução do PDF indica que a divergência ocorre até ~73 s).")