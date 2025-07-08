import numpy as np
import matplotlib.pylab as plt

#a)
L_i = np.array([225.0, 222.0, 207.5, 194.0, 171.5, 153.0, 133.0, 113.0, 92.0])
X_i = np.array([6.0, 2.3, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0])

#b)
def minimos_quadrados(x,y):
    if len(x) != len(y):   #regressão linear só faz sentido se tivermos pares ordenados 
        raise ValueError("As listas x e y devem ter o mesmo tamanho.")
    N = len(x) 
    sum_x = np.sum(x) 
    sum_y = np.sum(y)   
    sum_x2 = np.sum(x ** 2) 
    sum_y2 = np.sum(y ** 2) 
    sum_xy = np.sum(x * y)
    m = (N * sum_xy - sum_x * sum_y) / (N * sum_x2 - sum_x ** 2) #Declive 
    b = (sum_x2 * sum_y - sum_x * sum_xy) / (N * sum_x2 - sum_x ** 2) #Ordenada na origem 
    r2 = (N * sum_xy - sum_x * sum_y) ** 2 / ((N * sum_x2 - sum_x ** 2) * (N * sum_y2))
    #Cálculo dos erros
    dm = np.absolute(m) * np.sqrt((1 / r2 - 1) / (N - 2))
    db = dm * np.sqrt((sum_x2) / N)
    return m, b, r2, dm, db

m, b, r2, dm, db = minimos_quadrados(L_i, X_i)
print("m = {}".format(m))
print("b = {}".format(b))
print("r**2 = {}".format(r2))
print("dm = {}".format(dm))
print("db = {}".format(db))

#c)
x = np.array([80.0, 230.0])
y = m * x + b

#d)
print("X[L = 165.0 cm] = {} cm".format(m * 165.0 + b))

#e)


plt.scatter(L_i, X_i)
plt.plot(x,y, color='purple')
plt.xlabel("Distância da fonte de luz ao alvo L")
plt.ylabel("Distância entre máximos ")
plt.show()




