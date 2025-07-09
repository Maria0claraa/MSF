import matplotlib.pyplot as plt
import numpy as np

r = 0.11
m = 0.45
g = 9.8
rho = 0.11  #densidade do ar 
vt = 100 * 1000 / 3600
A = np.pi * r**2
dt = 0.001

# Vetores iniciais
v = np.array([25, 5, -50], dtype=float)  # m/s
x = np.array([0, 0, 23.8], dtype=float)  # m
omega = np.array([0, 400, 0], dtype=float)  # rad/s

t = 0
max_t = 5

# Guardar trajetória e tempo
traj = []
tempos = []

# Loop principal - Método de Euler
while t < max_t and x[1] >= 0:
    v_mod = np.linalg.norm(v)
    
    # Forças
    F_ar = -m * g * v / vt**2 * v_mod
    F_magnus = 0.5 * A * x * r * np.cross(omega, v)
    Fg = np.array([0, -m * g, 0])
    
    F_total = Fg + F_ar + F_magnus
    
    # Movimento
    a = F_total / m
    v += a * dt
    x += v * dt

    traj.append(x.copy())
    tempos.append(t)
    t += dt

# Transformar em arrays
traj = np.array(traj)
tempos = np.array(tempos)

# Verificar se foi golo em algum ponto da trajetória
golo = False
for pos in traj:
    x, y, z = pos
    if x < 0 and 0 < z < 7.3 and 0 < y < 2.4:
        golo = True
        break

# Mostrar resultado
if golo:
    print("🎯 Golo!")
else:
    print("❌ Não foi golo.")

# Gráfico x(t), y(t), z(t)
plt.plot(tempos, traj[:, 0], label="x(t)")
plt.plot(tempos, traj[:, 1], label="y(t)")
plt.plot(tempos, traj[:, 2], label="z(t)")
plt.title("Bola com rotação   (x,y,z) em função do tempo")
plt.xlabel("t (s)")
plt.legend()
plt.grid(True)
plt.show()