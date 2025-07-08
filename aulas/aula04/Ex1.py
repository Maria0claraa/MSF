import numpy as np
import matplotlib.pyplot as plt

t0 = 0.0
tf = 4.0
x0 = 0.0
v0 = 0.0
dt = 0.1  #passo de tempo(s)

g = 9.80

t = np.arange(t0, tf, dt)  # Criar um array com os instantes de tempo
v = np.empty(np.size(t))  # Criar um array vazio para armazenar velocidades
x = np.empty(np.size(t))  # Criar um array vazio para armazenar posições

v[0] = v0 #velocidade inicial
x[0] = x0 #posição inicial 
for i in range(np.size(t) - 1):
    v[i+1] = v[i] + g * dt
    x[i+1] = x[i] + v[i] * dt

i3 = 3.0/dt
i3 = int(i3)
v3 = v[i3]
print("A velocidade no instante 3s é ", v3)
print("A solução numérica é independente do tamanho do passo porque é linear em t")

print("A posição do objeto no instante 3s é", x[i3])
print("A solução numérica depende do passo, e aproxima-se da solução exata à medida que o diminuimos")

passo =np.array([0.1, 0.01, 0.001, 0.0001])
desvio = np.array([1.46, 0.147, 0.0147, 0.00147])
# Representar desvio de Δx num grafico (usando o matplotlib)
plt.loglog(passo, desvio, 'o-')
plt.xlabel("Passo, δt [s]")
plt.ylabel("Desvio da Posição, Δx [m]")
plt.show()