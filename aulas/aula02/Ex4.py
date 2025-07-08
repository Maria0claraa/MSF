import numpy as np
import matplotlib.pylab as plt

T = np.array([0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0])
A = np.array([9.676, 6.355, 4.261, 2.729, 1.862, 1.184, 0.7680, 0.4883, 0.3461, 0.2119])

# a) Gráfico de dispersão
plt.scatter(T, A)
plt.xlabel("Tempo (dias)")
plt.ylabel("Atividade (mCi)")
plt.title("Atividade de 131I com o Tempo")
plt.show()

# b) Gráfico log-linear
log_atividade = np.log(A)

plt.plot(T, log_atividade, label="Log(Atividade) vs Tempo")
plt.xlabel("Tempo (dias)")
plt.ylabel("log(Atividade)")
plt.title("Gráfico Semilog (log Atividade vs Tempo)")
plt.legend()
plt.show()

# c) Logaritmo da atividade
Y_i = np.log(A)

# Função para realizar a regressão linear
def minimos_quadrados(x, y):
    if len(x) != len(y):   # Regressão linear só faz sentido se tivermos pares ordenados
        raise ValueError("As listas x e y devem ter o mesmo tamanho.")
    
    N = len(x)  # Número de pontos da regressão

    x = np.array(x)  # Converte x para um array numpy
    y = np.array(y)  # Converte y para um array numpy

    sum_x = np.sum(x)  # Soma de todos os valores de X
    sum_y = np.sum(y)  # Soma de todos os valores de Y   
    sum_x2 = np.sum(x ** 2)  # Soma dos quadrados de X
    sum_y2 = np.sum(y ** 2)  # Soma dos quadrados de Y 
    sum_xy = np.sum(x * y)  # Soma das multiplicações

    # Cálculo da inclinação (m) e interceptação (b) da reta
    m = (N * sum_xy - sum_x * sum_y) / (N * sum_x2 - sum_x ** 2)  # Declive
    b = (sum_x2 * sum_y - sum_x * sum_xy) / (N * sum_x2 - sum_x ** 2)  # Ordenada na origem

    # Cálculo do coeficiente de determinação (r²)
    r2 = (N * sum_xy - sum_x * sum_y) ** 2 / ((N * sum_x2 - sum_x ** 2) * (N * sum_y2))

    # Cálculo do erro nos parâmetros
    dm = np.sqrt((1 / r2 - 1) / (N - 2))  # Erro no declive (m)
    db = dm * np.sqrt(sum_x2 / N)  # Erro na interceptação (b)

    return m, b, r2, dm, db

# Aplicar regressão linear aos dados
m, b, r2, dm, db = minimos_quadrados(T, Y_i)

# Exibir os resultados
print(f"Declive (m) = {m:.4f}")
print(f"Interceptação (b) = {b:.4f}")
print(f"Coeficiente de determinação r² = {r2:.4f}")
print(f"Erro no declive (dm) = {dm:.4f}")
print(f"Erro na interceptação (db) = {db:.4f}")

# Gerar o gráfico da reta ajustada
X = np.linspace(0.0, 45.0, 100)  # Gera 100 pontos de tempo para o gráfico
Y = m * X + b  # Calcula os valores de Y (log(atividade)) para a reta ajustada

# Plotando os pontos e a reta de melhor ajuste
plt.scatter(T, Y_i, color='blue', label='Dados log(Atividade)')
plt.plot(X, Y, color='red', label='Ajuste linear')  # A reta ajustada
plt.xlabel("Tempo (dias)")
plt.ylabel("Log(Atividade) (log(mCi))")
plt.title("Ajuste Linear da Atividade com o Tempo")
plt.legend()
plt.show()



lambda_ = -m
t_half = np.log(2) / lambda_
print(f"A semivida (t1/2) do isótopo 131I é de {t_half} dias.")

