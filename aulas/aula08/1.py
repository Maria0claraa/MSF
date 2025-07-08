import numpy as np
import matplotlib.pyplot as plt

# Dados iniciais
r0 = np.array([0, 2, 3])
v0 = np.array([160, 20, -20]) * 1000 / 3600

t0 = 0
tf = 0.4
dt = 0.001

g = 9.80
vt = 120 * 1000 / 3600
Dr = g / (vt**2)  

n = int((tf - t0) / dt + 0.1)
t = np.zeros(n + 1)

vx = np.zeros(n + 1)
vy = np.zeros(n + 1)
vz = np.zeros(n + 1)

rx = np.zeros(n + 1)
ry = np.zeros(n + 1)
rz = np.zeros(n + 1)

rx[0] = r0[0]
ry[0] = r0[1]
rz[0] = r0[2]

vx[0] = v0[0]
vy[0] = v0[1]
vz[0] = v0[2]

for i in range(n):
    v = np.sqrt(vx[i]**2 + vy[i]**2 + vz[i]**2)

    ax = -Dr * v * vx[i]
    ay = -Dr * v * vy[i]
    az = -g - Dr * v * vz[i]

    vx[i+1] = vx[i] + ax * dt
    vy[i+1] = vy[i] + ay * dt
    vz[i+1] = vz[i] + az * dt

    rx[i+1] = rx[i] + vx[i] * dt
    ry[i+1] = ry[i] + vy[i] * dt
    rz[i+1] = rz[i] + vz[i] * dt

    t[i+1] = t[i] + dt

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

campo_x = [0, 25, 25, 0, 0]
campo_y = [0, 0, 10, 10, 0]
campo_z = [0, 0, 0, 0, 0]
ax.plot3D(campo_x, campo_y, campo_z, color='green', alpha=0.5, label='Campo')
ax.add_collection3d(plt.fill_between(campo_x[:4], campo_y[:4], color='green', alpha=0.3))

ax.plot3D(rx[rz >= 0], ry[rz >= 0], rz[rz >= 0], color='blue', linewidth=2, label='Trajetória da bola')

redex = [11.9, 11.9, 11.9, 11.9, 11.9]
redey = [0, 0, 8.2, 8.2, 0]
redez = [0, 1, 1, 0, 0]
ax.plot3D(redex, redey, redez, color='black', linewidth=2, label='Rede')

campox = [11.9, 18.3, 18.3, 11.9, 11.9]
campoy = [4.1, 4.1, 8.2, 8.2, 4.1]
campoz = [0, 0, 0, 0, 0]
ax.plot3D(campox, campoy, campoz, color='red', label='Zona alvo')

campox = [11.9, 18.3, 18.3, 11.9, 11.9]
campoy = [4.1, 4.1, 8.2, 8.2, 4.1]
campoz = [0, 0, 0, 0, 0]
ax.plot3D(campox, campoy, campoz, color='red', label='Zona alvo')

ax.set_xlim3d(0, 25)
ax.set_ylim3d(0, 10)
ax.set_zlim3d(0, 5)
ax.set_box_aspect((14, 8, 3)) 
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
ax.set_title('Trajetória 3D da bola de tênis')
ax.legend()

plt.show()

m = 0.057
Em = np.zeros(n+1)
Ep = np.zeros(n+1)
Ec = np.zeros(n+1)

for i in range(n+1):
    h = rz[i]
    Ep[i] = m * g * h
    v = np.sqrt(vx[i]**2 + vy[i]**2 + vz[i]**2)
    Ec[i] = 0.5 * m * v**2
    Em[i] = Ec[i] + Ep[i]

variacao = Em[-1] - Em[0]
print(f"A variação de energia mecânica é {variacao:.2f} Joules")

plt.plot(t, Ep, label="Energia Potencial")
plt.plot(t, Ec, label="Energia Cinética")
plt.plot(t, Em, label="Energia Mecânica")
plt.legend(loc="center right")
plt.title("Energias da bola")
plt.xlabel("Tempo (s)")
plt.ylabel("Energia (J)")
plt.show()

def integral(f, intervalo, a, b):
    dt = (intervalo[1] - intervalo[0]) / len(f)
    i_a = int((a - intervalo[0]) / dt)
    i_b = int((b - intervalo[0]) / dt)
    soma = 0.0

    for i in range(i_a, i_b):
        soma += (f[i] + f[i+1]) / 2.0 * dt

    return soma

t1 = 0.2
t2 = 0.4
intervalo = np.array([t0, tf])
F_res = np.zeros((n+1, 3))

for i in range(n+1):
    v = np.sqrt(vx[i]**2 + vy[i]**2 + vz[i]**2)
    F_res[i, 0] = -Dr * v * vx[i]
    F_res[i, 1] = -Dr * v * vy[i]
    F_res[i, 2] = -g - Dr * v * vz[i]

F_dot_v = np.sum(F_res * np.vstack((vx, vy, vz)).T, axis=1)

W0 = integral(F_dot_v, intervalo, t0, t0)
W1 = integral(F_dot_v, intervalo, t0, t1)
W2 = integral(F_dot_v, intervalo, t0, t2)

print(f"O trabalho realizado pela força resultante de t0 a t0 é {W0:.2f} Joules")
print(f"O trabalho realizado pela força resultante de t0 a t1 é {W1:.2f} Joules")
print(f"O trabalho realizado pela força resultante de t0 a t2 é {W2:.2f} Joules")

solo_index = np.argmax(rz <= 0)
print(f"A bola atinge o solo em x = {rx[solo_index]:.2f} m, y = {ry[solo_index]:.2f} m")

#A vantagem de sacar a bola de um ponto mais alto é que isso permite que a bola 
# tenha uma trajetória mais inclinada, o que aumenta a probabilidade de passar por
#  cima da rede e atingir a zona desejada (verde clara) dentro do campo adversário.