import numpy as np
import matplotlib.pyplot as plt

# --- a) Cálculo da constante C ---
g = 9.8  # m/s^2 [cite: 946]
v_terminal_medida = 6.80  # m/s [cite: 1172]

# Expressão da velocidade terminal: 0 = g - C * v_terminal => C = g / v_terminal
C = g / v_terminal_medida
print(f"a) A constante C é: {C:.4f} s^-1\n")

# --- Configuração para o Método de Euler (b e c) ---
dt = 0.001  # Passo de tempo (escolha pequena para boa precisão)
t_final = 2.0  # Tempo final da simulação, ajustado para cobrir os dados experimentais

# Condições iniciais
t0 = 0.0
y0 = 0.0
vy0 = 0.0

# Número de passos
n_passos = int((t_final - t0) / dt + 0.1) # +0.1 para evitar problemas de arredondamento [cite: 1341]

# Criar arrays para armazenar os resultados
t_euler = np.zeros(n_passos + 1)
y_euler = np.zeros(n_passos + 1)
vy_euler = np.zeros(n_passos + 1)

# Inicializar os valores nos arrays
t_euler[0] = t0
y_euler[0] = y0
vy_euler[0] = vy0

# --- Implementação do Método de Euler (Loop) --- [cite: 1354]
for i in range(n_passos):
    # Calcular a aceleração no instante atual t_euler[i] e vy_euler[i]
    # a_y(t) = g - C * v_y
    a_y = g - C * vy_euler[i]

    # Atualizar velocidade usando a_y no instante atual [cite: 1490]
    vy_euler[i+1] = vy_euler[i] + a_y * dt

    # Atualizar posição usando vy_euler no instante atual [cite: 1490]
    y_euler[i+1] = y_euler[i] + vy_euler[i] * dt
    
    # Atualizar o tempo [cite: 1490]
    t_euler[i+1] = t_euler[i] + dt

# --- b) Gráfico da Velocidade em função do tempo ---
plt.figure(figsize=(10, 6))
plt.plot(t_euler, vy_euler, label='Velocidade (Método de Euler)', color='blue')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade do Volante de Badminton vs. Tempo (Método de Euler)')
plt.grid(True)
plt.legend()
plt.show()

# --- c) Gráfico da Posição em função do tempo ---
plt.figure(figsize=(10, 6))
plt.plot(t_euler, y_euler, label='Posição (Método de Euler)', color='green')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição do Volante de Badminton vs. Tempo (Método de Euler)')
plt.grid(True)
plt.legend()
plt.show()

# --- d) Comparar com os valores medidos ---
# Assumimos que o ficheiro 'data_cap2_queda_volante.txt' está no mesmo diretório
# Se não estiver, precisaria do caminho completo para o ficheiro.
try:
    # Os dados no slide 17  parecem ter um formato de duas colunas y(m) e t(s). 
    # Vou reverter a ordem para (t, y) para carregar mais facilmente.
    # Se o ficheiro real tiver (t, y) na ordem correta, o np.loadtxt funcionaria diretamente.
    # Com base no slide[cite: 1136], a primeira coluna é y(m) e a segunda é t(s).
    dados_medidos = np.loadtxt('data_cap2_queda_volante.txt', skiprows=1) # Assumindo que a primeira linha é cabeçalho
    t_medido = dados_medidos[:, 1] # Coluna de tempo
    y_medido = dados_medidos[:, 0] # Coluna de posição
    
    # Ajustar a posição medida para que o início seja 0, se necessário (o problema diz "largado de uma altura considerável")
    # Se os dados medidos começarem de uma altura maior, subtraímos y_medido[0] para comparar a queda.
    y_medido_ajustado = y_medido - y_medido[0] 

    plt.figure(figsize=(10, 6))
    plt.plot(t_euler, y_euler, label='Posição (Método de Euler)', color='green')
    plt.scatter(t_medido, y_medido_ajustado, label='Posição Medida (data_cap2_queda_volante.txt)', color='red', marker='o', s=20)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Comparação da Posição: Método de Euler vs. Dados Medidos')
    plt.grid(True)
    plt.legend()
    plt.show()

    print("\nd) Comparação da posição:")
    print("Os dados medidos e a solução do Método de Euler foram plotados no mesmo gráfico para comparação.")
    print("Observa-se se o modelo com resistência do ar linear na velocidade descreve bem os dados experimentais, especialmente no início da queda.")


except FileNotFoundError:
    print("\nErro: O ficheiro 'data_cap2_queda_volante.txt' não foi encontrado.")
    print("Certifique-se de que o ficheiro está no mesmo diretório do script ou forneça o caminho completo.")
except Exception as e:
    print(f"\nOcorreu um erro ao carregar ou processar o ficheiro de dados: {e}")