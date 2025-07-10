import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros do Sistema ---
m = 1.0  # kg
k = 1.0  # N/m
kp = 0.5 # N/m (k_linha)

# --- Matriz do Sistema (M) para o problema de valores próprios ---
# M = [[(k+kp)/m, -kp/m, 0],
#      [-kp/m, 2*kp/m, -kp/m],
#      [0, -kp/m, (k+kp)/m]]
matrix_M = np.array([
    [(k + kp) / m, -kp / m, 0],
    [-kp / m, 2 * kp / m, -kp / m],
    [0, -kp / m, (k + kp) / m]
])

# --- ALÍNEA a) - Calcular frequências angulares dos modos normais ---
print("--- a) Frequências Angulares dos Modos Normais ---")
eigenvalues, eigenvectors = np.linalg.eig(matrix_M)

# Os valores próprios são ω^2. As frequências são a raiz quadrada.
# Arredondar para melhor legibilidade
omegas_squared = np.round(eigenvalues, 4)
omegas = np.round(np.sqrt(eigenvalues), 4)

# Os vetores próprios (colunas da matriz eigenvectors) podem estar desordenados.
# Vamos ordenar as frequências angulares (ω) por ordem crescente.
sort_indices = np.argsort(omegas)
omegas_sorted = omegas[sort_indices]
eigenvectors_sorted = eigenvectors[:, sort_indices] # Ordenar as colunas dos vetores próprios

print(f"Matriz M:\n{matrix_M}")
print(f"\nValores próprios (omega^2) ordenados: {omegas_sorted**2}")
print(f"Frequências angulares (omega) dos modos normais (rad/s) ordenadas: {omegas_sorted}")
print(f"\nVetores próprios (colunas) ordenados:\n{np.round(eigenvectors_sorted, 4)}")

# Soluções do problema: 0.707 rad/s, 1.225 rad/s, 1.414 rad/s.
# Meus resultados: [0.7071 1.2247 1.4142], que batem perfeitamente.

# --- ALÍNEA b) - Gráfico do movimento para cada modo e descrição ---

# Equilíbrio positions (assumidas, com base em problemas anteriores)
x_Aeq = 1.0 # m
x_Beq = 1.2 # m
x_Ceq = 1.4 # m

# Parâmetros de simulação para o Euler-Cromer
dt = 0.001
t_total = 80.0 # s (para ver várias oscilações)
amplitude_scaling_factor = 0.05 # m (amplitude inicial para o modo mais "estendido")

# --- Função de Simulação Euler-Cromer para 3 corpos ---
def simulate_3_coupled_oscillators(u_A0, u_B0, u_C0, v_A0, v_B0, v_C0, dt, t_total):
    t_values = []
    uA_values = []
    uB_values = []
    uC_values = []
    
    u_A, u_B, u_C = u_A0, u_B0, u_C0
    v_A, v_B, v_C = v_A0, v_B0, v_C0
    t = 0.0

    t_values.append(t)
    uA_values.append(u_A)
    uB_values.append(u_B)
    uC_values.append(u_C)

    while t <= t_total:
        # Calcular acelerações (derivadas das equações de movimento)
        a_A = (-k * u_A - kp * (u_A - u_B)) / m
        a_B = (-kp * (u_B - u_A) - kp * (u_B - u_C)) / m
        a_C = (-k * u_C - kp * (u_C - u_B)) / m

        # Atualizar velocidades
        v_A += a_A * dt
        v_B += a_B * dt
        v_C += a_C * dt

        # Atualizar posições (desvios)
        u_A += v_A * dt
        u_B += v_B * dt
        u_C += v_C * dt

        # Atualizar tempo
        t += dt

        t_values.append(t)
        uA_values.append(u_A)
        uB_values.append(u_B)
        uC_values.append(u_C)
        
    return t_values, uA_values, uB_values, uC_values

# --- ALÍNEA b) - Simular e Plotar cada Modo Normal ---
print("\n--- b) Movimento para Cada Modo Normal ---")

# Para cada modo normal, as condições iniciais (desvios) serão proporcionais ao vetor próprio
# E as velocidades iniciais serão zero.
for i in range(3):
    mode_num = i + 1
    current_omega = omegas_sorted[i]
    current_eigenvector = eigenvectors_sorted[:, i] # Vetor próprio para este modo
    
    # Normalizar o vetor próprio e escalar para uma amplitude inicial razoável
    # A maior componente do vetor próprio é escalada para amplitude_scaling_factor
    initial_deviations = current_eigenvector / np.max(np.abs(current_eigenvector)) * amplitude_scaling_factor
    
    # Condições iniciais (desvios e velocidades nulas)
    u_A0, u_B0, u_C0 = initial_deviations[0], initial_deviations[1], initial_deviations[2]
    v_A0, v_B0, v_C0 = 0.0, 0.0, 0.0

    # Simular o movimento para este modo
    t_vals, uA_vals, uB_vals, uC_vals = simulate_3_coupled_oscillators(
        u_A0, u_B0, u_C0, v_A0, v_B0, v_C0, dt, t_total
    )

    # Converter desvios para posições absolutas para o gráfico
    xA_vals = np.array(uA_vals) + x_Aeq
    xB_vals = np.array(uB_vals) + x_Beq
    cC_vals = np.array(uC_vals) + x_Ceq

    plt.figure(figsize=(10, 6))
    plt.plot(t_vals, xA_vals, label='Corpo A')
    plt.plot(t_vals, xB_vals, label='Corpo B')
    plt.plot(t_vals, cC_vals, label='Corpo C')
    
    # Linhas para as posições de equilíbrio
    plt.axhline(y=x_Aeq, color='gray', linestyle='--', linewidth=0.8, label='$x_{Aeq}$')
    plt.axhline(y=x_Beq, color='lightgray', linestyle='--', linewidth=0.8, label='$x_{Beq}$')
    plt.axhline(y=x_Ceq, color='darkgray', linestyle='--', linewidth=0.8, label='$x_{Ceq}$')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title(f'Modo Normal {mode_num} ($\omega = {current_omega:.3f}$ rad/s)')
    plt.grid(True)
    plt.legend()
    # Ajustar limites Y para todos os gráficos ficarem consistentes, baseados nas soluções
    plt.ylim(0.9, 1.45) 
    plt.show()

    # Descrever o movimento relativo das massas (baseado nos vetores próprios)
    print(f"\nDescrição do Modo Normal {mode_num}:")
    print(f"  Frequência: {current_omega:.3f} rad/s")
    print(f"  Vetor Próprio (normalizado para CI): [{initial_deviations[0]:.4f}, {initial_deviations[1]:.4f}, {initial_deviations[2]:.4f}]")
    
    if mode_num == 1:
        # Corresponde a [0.7071, 1.0, 0.7071] ou [0.4082, 0.8165, 0.4082] dependendo da normalização.
        # As massas A e C oscilam na mesma direção e fase, e a massa B oscila na mesma direção e fase,
        # mas com maior amplitude (proporcional a sqrt(2) ou 2, dependendo da base do vetor).
        # A solução diz "As três massas oscilam sempre sintonizadas, mas a massa do meio oscila com amplitude 2 vezes maior do que as outras."
        # Isto é consistente com a solução do problema, que usa um vetor próprio diferente, mas descreve o mesmo movimento.
        # No meu eigenvector, o vetor para a menor frequência é [0.4082, 0.8165, 0.4082]
        # Aqui, uB ~ 2 * uA (0.8165 / 0.4082 ~ 2). uA ~ uC.
        print("  Descrição: As massas A e C oscilam em fase, e a massa B também oscila em fase com elas, mas com uma amplitude aproximadamente 2 vezes maior. Todas as massas se movem na mesma direção ao mesmo tempo.")
    elif mode_num == 2:
        # Corresponde a [-0.7071, 0.0, 0.7071] ou [0.5774, 0.0, -0.5774]
        # Minha ordenação: [0.7071, 0.0, -0.7071] para 1.2247 rad/s
        # A massa do meio (B) permanece em repouso. As massas A e C oscilam em oposição de fase (sentidos opostos), com a mesma amplitude.
        print("  Descrição: A massa do meio (Corpo B) permanece essencialmente em repouso (não se move). As massas A e C oscilam com a mesma amplitude, mas em oposição de fase (quando A vai para a direita, C vai para a esquerda).")
    elif mode_num == 3:
        # Corresponde a [0.5774, -0.5774, 0.5774]
        # Minha ordenação: [0.5774, -0.5774, 0.5774] para 1.4142 rad/s
        # As massas A e C oscilam em fase. A massa B oscila em oposição de fase (sentido oposto) a A e C, com a mesma amplitude.
        print("  Descrição: As massas A e C oscilam em fase (na mesma direção). A massa do meio (Corpo B) oscila com a mesma amplitude que A e C, mas em oposição de fase a elas (quando A e C vão para a direita, B vai para a esquerda).")