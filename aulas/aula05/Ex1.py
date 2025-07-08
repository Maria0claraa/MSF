import numpy as np
import matplotlib.pyplot as plt

instrucoes = [(45, 3), (90, 2), (45, 3), (45, 2), (90, 3)]

plt.axis([-5, 3, -4.5, 1.0])  #Define os limites dos eixos

x = 0.0; y = 0.0; theta = 0.0
pos = np.array([[x, y, theta]])  # Array que armazena as posições do robô
plt.arrow(x, y, np.cos(-theta * np.pi / 180), np.sin(-theta * np.pi / 180), color='pink', width=0.01, head_width=0.1)  #Representa a direção do robo
#np.cos determina a componente x da direção, e a np.sen a componente y
#arrow desenha a seta que indica a direção do robo

for ang, dist in instrucoes:
    theta += ang  # Atualiza o ângulo 
    x += dist * np.cos(-theta * np.pi / 180)#Calcula a nova posição x
    y += dist * np.sin(-theta * np.pi / 180)#Calcula a nova posição y
    pos = np.append(pos, [[x, y, theta]], 0)#Armazena a nova posição

    plt.arrow(x, y, np.cos(-theta * np.pi / 180), np.sin(-theta * np.pi / 180), color='pink', width=0.01, head_width=0.1)


plt.plot(pos[:,0], pos[:,1], color = 'purple')
plt.xlabel("Posição do robô, x[m]")
plt.ylabel("Posição do robô, y[m]")
plt.show()

x_f = x
y_f = y
theta_f = theta
print("As coordenadas finais do robô são r = ({0:.2f},".format(x_f), "{0:.2f})".format(y_f), "e arg = {0:.2f}".format(theta_f))


d = np.sqrt(x_f**2 + y_f**2)
plt.figure(figsize=(6.5,4.5))
plt.axis([-4, 2.5, -4, 0.5])
                
ang = np.remainder(np.arcsin(-y_f / d) - theta_f, 360)   # 1. Rotação ângulo arbitrári
dist = d                                                 # 2. Avanço
theta += ang
x += dist * np.cos(-theta * np.pi / 180)
y += dist * np.sin(-theta * np.pi / 180)
pos = np.append(pos, [[x, y, theta]], 0)

print("Instrução de retorno: dist = ({0:.2f}, ".format(dist), "ang = {0:.2f}".format(ang))

plt.arrow(x, y, np.cos(-theta * np.pi / 180), np.sin(-theta * np.pi / 180), color='r', width=0.01, head_width=0.1)
plt.plot(pos[:,0], pos[:,1])
plt.xlabel("Posição do robô, x[m]")
plt.ylabel("Posição do robô, y[m]")
plt.show()


