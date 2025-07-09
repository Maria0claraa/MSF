import matplotlib.pyplot as plt
import numpy as np

v0 = 200
v0 = v0 * 1000 / 3600
theta_deg = 10 #ângulo que faz com a horizontal
theta = np.radians(theta_deg) #converte para radianos
g = 9.8 
vt = 6.8
dt = 0.001

x = 0
y = 3
t = 0
#cálculo das componentes horizontais e verticais da velocidade inicial
vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)

#listas para guardar os pontos da trajetória
X = [x]
Y = [y]
T = [t]

while y >= 0:
    v = np.sqrt(vx**2 + vy**2)  #módulo da velocidade
    #aceleração
    ax = -g * vx * v / vt**2
    ay = -g + (-g * vy * v / vt**2)
    #velocidade
    vx += ax * dt
    vy += ay * dt
    #posição
    x += vx * dt
    y += vy * dt

    t += dt  #incrementa o tempo

    #guarda as novas posições na lista
    X.append(x)
    Y.append(y)
    T.append(t)


plt.plot(X, Y)
plt.title("Trajetória do volante")
plt.xlabel("Distância horizontal (m)")
plt.ylabel("Altura (m)")
plt.grid(True)
plt.show()


#Ponto em que cai no chão e quanto tempo demorou
alcance = X[-1]
tempo = T[-1]
print(f"Alcance horizontal: {alcance:.2f} m")
print(f"Tempo total de voo: {tempo:.2f} s")