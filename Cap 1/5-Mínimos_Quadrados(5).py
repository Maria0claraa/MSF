#soma, declive, coeficiente de determinação r^2, ordenada na origem, pontos experimentais, X quando L = 165.0 cm
import numpy as np
import matplotlib.pyplot as plt

L = np.array([222.0, 207.5, 194.0, 171.5, 153.0, 133.0, 113.0, 92.0])
X = np.array([2.3, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0])

# a) - Representar os dados num gráfico
plt.scatter(L, X, color='purple')
plt.xlabel('L (cm)')
plt.ylabel('X (cm)')
plt.title('Dados Experimentais')
plt.show()

# b) - Soma das expressões 
N = len(L)
sum_xy = np.sum(L*X)
sum_x = np.sum(L)
sum_y = np.sum(X)
sum_x2 = np.sum(L**2)
sum_y2 = np.sum(X**2)

# c) - Coeficientes da reta
d = (N*sum_xy - sum_x*sum_y) / (N*sum_x2 - (sum_x)**2)
b = (sum_x2*sum_y - sum_x*sum_xy) / (N*sum_x2 - (sum_x)**2)
r2 = ((N*sum_xy - sum_x*sum_y)**2) / ((N*sum_x2 - (sum_x)**2)*(N*sum_y2 - (sum_y)**2))

# d) - Representar a reta de ajuste
plt.scatter(L, X, color='purple')
plt.plot(L, d * L + b, color='pink') # pontos da reta de regressão todos unidos 
plt.xlabel('L (cm)')
plt.ylabel('X (cm)')
plt.title('Dados Experimentais e Reta de Regressão')
plt.show()

# e)
# e) Encontrar o valor de X quando L = 165.0 cm
L_new = 165.0
X_new = d * L_new + b
print(f"O valor de X quando L = 165.0 cm é {X_new:.2f} cm")

# f) - Comparar coeficientes de determinação com valores de y afastados
