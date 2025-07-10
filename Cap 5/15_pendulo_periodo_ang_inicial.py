import numpy as np
import matplotlib.pyplot as plt

def solve_pendulum(initial_angle_deg, g, L, dt, t_total):
    """
    Resolve a equação do pêndulo não linear usando Euler-Cromer.
    Calcula o período do movimento.
    """
    theta0 = np.radians(initial_angle_deg) # Converter para radianos
    omega0 = 0.0 # rad/s 

    t_values = []
    theta_values = []
    omega_values = []

    t = 0.0
    theta = theta0
    omega = omega0

    t_values.append(t)
    theta_values.append(theta)
    omega_values.append(omega)

    # Variáveis para cálculo do período
    zero_crossings_times = []
    prev_theta = theta0

    while t <= t_total:
        # Calcular aceleração angular
        alpha = -g / L * np.sin(theta) # Equação não linear 

        # Atualizar velocidade angular
        omega = omega + alpha * dt

        # Atualizar posição angular
        theta = theta + omega * dt

        # Atualizar tempo
        t = t + dt

        t_values.append(t)
        theta_values.append(theta)
        omega_values.append(omega)

        # Detectar cruzamentos por zero (passagens pela posição de equilíbrio)
        # Procuramos passagens de positivo para negativo (ou vice-versa)
        if (prev_theta >= 0 and theta < 0) or (prev_theta < 0 and theta >= 0):
            zero_crossings_times.append(t)
        prev_theta = theta

    # Calcular o período a partir dos cruzamentos por zero
    periods = []
    # Precisamos de 4 cruzamentos para ter um período completo (por exemplo, 0 -> max -> 0 -> min -> 0)
    # ou 2 cruzamentos na mesma direção (ex: 0 crescente -> 0 crescente)
    # Uma forma mais robusta é usar picos, mas cruzamentos por zero funcionam se bem tratados
    
    # Para simplicidade e seguindo o padrão de obter 2 * pi / omega para SHM, vamos adaptar para não linear
    # A maneira mais fiável é medir o tempo entre dois picos consecutivos (amplitude máxima)
    # ou entre a primeira passagem por zero (com velocidade positiva) e a próxima passagem por zero
    # com velocidade positiva.
    
    # Uma forma mais simples, para um sistema que parte do repouso no ângulo máximo:
    # O primeiro retorno ao ângulo máximo (depois de uma oscilação completa) dará o período.
    # No entanto, detectar o ângulo exato numericamente pode ser complicado.
    # Alternativa: o tempo entre 2 passagens pela posição de equilíbrio com a MESMA velocidade (sinal e aprox. magnitude)
    
    # Melhor abordagem para o período: identificar o primeiro pico (ou quase pico) após o início
    # e o segundo pico (uma oscilação depois).
    
    # Método mais simples: encontrar os tempos em que theta_values está no máximo (ou mínimo)
    # Dado que começa em theta_max e omega=0, o primeiro retorno a theta_max marcará o período
    peak_times = []
    for i in range(1, len(theta_values) - 1):
        if (theta_values[i] > theta_values[i-1] and theta_values[i] > theta_values[i+1]) or \
           (theta_values[i] < theta_values[i-1] and theta_values[i] < theta_values[i+1]):
            # Encontrou um pico ou vale (máximo ou mínimo local)
            # Se a condição inicial é um máximo, o próximo máximo é um período.
            # Se a condição inicial é um mínimo, o próximo mínimo é um período.
            # Para o pêndulo, os picos são os ângulos extremos.
            # Como começa em theta_max com velocidade zero, o próximo theta_max será 1 período.
            if len(peak_times) == 0 and abs(theta_values[i] - theta0) < np.radians(0.1): # Encontra o primeiro pico após o início
                 peak_times.append(t_values[i])
            elif len(peak_times) > 0 and abs(theta_values[i] - theta0) < np.radians(0.1): # Encontra outros picos que retornam à amplitude inicial
                peak_times.append(t_values[i])
                
    if len(peak_times) >= 2:
        # Calcular o período médio entre os picos
        periods = np.diff(peak_times)
        avg_period = np.mean(periods)
    else:
        avg_period = np.nan # Não foi possível determinar o período

    return t_values, theta_values, avg_period


# --- Parâmetros comuns ---
g = 9.8  # m/s^2
L = 1.0  # m 
dt = 0.0001 # Passo de tempo pequeno para precisão
t_total = 10.0 # Tempo total de simulação para ver várias oscilações

# --- Executar para cada ângulo inicial e imprimir o período ---
angles_deg = [5, 10, 20, 30] # 
solutions = {}

for angle_deg in angles_deg:
    t_vals, theta_vals, period = solve_pendulum(angle_deg, g, L, dt, t_total)
    solutions[angle_deg] = {'t': t_vals, 'theta': theta_vals, 'period': period}
    print(f"Ângulo Inicial: {angle_deg}° -> Período: {period:.4f} s") # 4 algarismos de precisão

# Opcional: Plotar alguns gráficos para visualização
plt.figure(figsize=(10, 6))
for angle_deg in angles_deg:
    plt.plot(solutions[angle_deg]['t'], np.degrees(solutions[angle_deg]['theta']),
             label=f'theta(t) for {angle_deg}°')
plt.xlabel('Tempo (s)')
plt.ylabel('Ângulo (graus)')
plt.title('Lei do Movimento do Pêndulo Não Linear')
plt.grid(True)
plt.legend()
plt.show()

# As soluções do PDF para comparação:
# a) 5°: 2.008 s 
# b) 10°: 2.011 s 
# c) 20°: 2.022 s 
# d) 30°: 2.042 s