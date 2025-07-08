import numpy as np
import matplotlib.pylab as plt

T = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]  # Temperaturas (K)
E = [0.6950, 4.363, 15.53, 38.74, 75.08, 125.2, 257.9, 344.1, 557.4, 690.7]  # Energias (J)

plt.plot(T, E, color='pink')
plt.scatter(T, E, color='pink')
plt.xlabel('Temperatura (K)')
plt.ylabel('Energia (J)')
plt.title('Energia emitida por um corpo negro em função da temperatura')
plt.show()

plt.semilogy(T, E, color='pink')
plt.xlabel('Temperatura (K)')
plt.ylabel('Log(Energia) (log(J))')
plt.title('Gráfico Log-Linear de Energia em função da Temperatura')
plt.show()

plt.loglog(T, E, color='pink')
plt.xlabel('Log(Temperatura) (log(K))')
plt.ylabel('Log(Energia) (log(J))')
plt.title('Gráfico Log-Log de Energia em função da Temperatura')
plt.show()

#A dependência segue uma lei de potência, gráfico loglog linear


log_T = np.log(T)
log_E = np.log(E)

def minimos_quadrados(x,y):
    if len(x) != len(y):   #regressão linear só faz sentido se tivermos pares ordenados 
        raise ValueError("As listas x e y devem ter o mesmo tamanho.")
    
    N = len(x) #Conta o número de pontos da regressão

    x = np.array(x)  # Converte x para um array numpy
    y = np.array(y)  # Converte y para um array numpy

    sum_x = np.sum(x)  # Soma de todos os valores de X
    sum_y = np.sum(y)  # Soma de todos os valores de Y   
    sum_x2 = np.sum(x ** 2)  # Soma dos quadrados de X
    sum_y2 = np.sum(y ** 2)  # Soma dos quadrados de Y 
    sum_xy = np.sum(x * y)  # Soma das multiplicações 

    m = (N * sum_xy - sum_x * sum_y) / (N * sum_x2 - sum_x ** 2) #Declive 
    b = (sum_x2 * sum_y - sum_x * sum_xy) / (N * sum_x2 - sum_x ** 2) #Ordenada na origem 
    r2 = (N * sum_xy - sum_x * sum_y) ** 2 / ((N * sum_x2 - sum_x ** 2) * (N * sum_y2))

    return m, b, r2


m, b, r2= minimos_quadrados(T, E)
print("m = {}".format(m))
print("b = {}".format(b))
print("r**2 = {}".format(r2))


def funcao_energia(T, a, b):
    return a * T**b


