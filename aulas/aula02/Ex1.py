#Reressão linear pelo método dos mínimos quadráticos 
import numpy as np

def minimos_quadrados(x,y):
    if len(x) != len(y):   #regressão linear só faz sentido se tivermos pares ordenados 
        raise ValueError("As listas x e y devem ter o mesmo tamanho.")
    
    N = len(x) #Conta o número de pontos da regressão

    sum_x = np.sum(x) #Soma de todos os valores de X
    sum_y = np.sum(y) ##Soma de todos os valores de Y   
    sum_x2 = np.sum(x ** 2) #Soma dos quadrados de X
    sum_y2 = np.sum(y ** 2) #Soma dos quadrados de Y 
    sum_xy = np.sum(x * y) #Soma da multiplicação

    m = (N * sum_xy - sum_x * sum_y) / (N * sum_x2 - sum_x ** 2) #Declive 
    b = (sum_x2 * sum_y - sum_x * sum_xy) / (N * sum_x2 - sum_x ** 2) #Ordenada na origem 
    r2 = (N * sum_xy - sum_x * sum_y) ** 2 / ((N * sum_x2 - sum_x ** 2) * (N * sum_y2))
    #Cálculo dos erros
    dm = np.absolute(m) * np.sqrt((1 / r2 - 1) / (N - 2))
    db = dm * np.sqrt((sum_x2) / N)
    return m, b, r2, dm, db

