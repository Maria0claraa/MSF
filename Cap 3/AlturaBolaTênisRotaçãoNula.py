import numpy as np
import matplotlib.pyplot as plt

m = 0.057     
g = 9.81      
v_terminal = 100 * 1000 / 3600  
k = m * g / v_terminal**2  #resistencia do ar

v0 = 130 * 1000 / 3600    
angle_deg = 10                
angle_rad = np.radians(angle_deg)

vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)

pos = np.array([-10.0, 1.0], dtype=float)  # posição inicial
vel = np.array([vx0, vy0], dtype=float)    # velocidade inicial

dt = 0.001
trajectory = [pos.copy()]
alturas = [pos[1]]

for _ in range(100000):
    v = np.linalg.norm(vel)
    F_drag = -k * v * vel
    acc = F_drag / m
    acc[1] -= g  # gravidade no eixo Y

    vel += acc * dt
    pos += vel * dt

    trajectory.append(pos.copy())
    alturas.append(pos[1])

    if pos[1] <= 0:  #verifica se a bola toca o chão
        break

trajectory = np.array(trajectory)


altura_max = np.max(alturas)
alcance = trajectory[-1, 0]  # compensar x inicial (-10)

print(f"dt = {dt}")
print(f"altura máxima = {altura_max:.8f} m")
print(f"alcance = {alcance:.5f} m")

plt.plot(trajectory[:, 0], trajectory[:, 1])
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Trajetória da Bola de Ténis (sem rotação)")
plt.grid(True)
plt.show()
