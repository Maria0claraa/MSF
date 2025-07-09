import numpy as np
import matplotlib.pyplot as plt


m = 0.057  # kg
g = 9.81  # m/s²
v_terminal = 100 * 1000 / 3600  # 100 km/h em m/s → 27.78 m/s
k = m * g / v_terminal**2       # coeficiente resistência do ar

# Propriedades da bola
r = 0.0335 
A = np.pi * r**2  # área de secção reta
rho = 1.225  # densidade do ar (kg/m³)

# Vetor de rotação (rad/s)
omega = np.array([0, 0, 100])  #ROTAÇÃO INSIRIDA AQUI

# === CONDIÇÕES INICIAIS ===
v0 = 130 * 1000 / 3600  # 130 km/h em m/s
angle_deg = 10
angle_rad = np.radians(angle_deg)

vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)

pos = np.array([-10.0, 1.0, 0.0], dtype=float)
vel = np.array([vx0, vy0, 0.0], dtype=float)

dt = 0.001
trajectory = [pos.copy()]
alturas = [pos[1]]

for _ in range(100000):
    v = np.linalg.norm(vel)
    
    # Força de arrasto
    F_drag = -k * v * vel

    # Força de Magnus
    F_magnus = 0.5 * A * rho * r * np.cross(omega, vel)

    # Força total
    F_total = F_drag + F_magnus
    acc = F_total / m
    acc[1] -= g  # gravidade

    # Atualiza velocidade e posição
    vel += acc * dt
    pos += vel * dt

    trajectory.append(pos.copy())
    alturas.append(pos[1])

    if pos[1] <= 0:
        break

trajectory = np.array(trajectory)


altura_max = np.max(alturas)
alcance = trajectory[-1, 0]  # compensar x inicial

print(f"dt = {dt}")
print(f"altura máxima = {altura_max:.8f} m")
print(f"alcance = {alcance:.5f} m")

plt.plot(trajectory[:, 0], trajectory[:, 1])
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("Trajetória da Bola de Ténis com rotação (Magnus)")
plt.grid(True)
plt.show()
