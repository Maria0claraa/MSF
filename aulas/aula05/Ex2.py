import numpy as np
import matplotlib.pyplot as plt

# Definição dos parâmetros
t0 = 0.0
tf = 0.5
dt = 0.001  # Passo de tempo

r0 = np.array([0.0, 0.0, 23.8])  # Posição inicial [x, y, z]
v0 = np.array([25.0, 5.0, -50.0])  # Velocidade inicial [vx, vy, vz]
w = 390.0  # Velocidade angular constante (efeito Magnus)

g = 9.80  # Gravidade
R = 0.11  # Raio da bola
A = np.pi * R**2  # Área da bola
m = 0.45  # Massa da bola
rho = 1.225  # Densidade do ar
v_T = 100 * 1000 / 3600  # Velocidade terminal (conversão de km/h para m/s)
D = g / v_T**2  # Coeficiente de arrasto

# Criação do vetor de tempo
t = np.arange(t0, tf, dt)

# Inicialização das variáveis
N = np.size(t)
a = np.zeros([3, N])
v = np.zeros([3, N])
r = np.zeros([3, N])

# Condições iniciais
v[:, 0] = v0
r[:, 0] = r0

# Loop de integração numérica
for i in range(N - 1):
    v_norm = np.linalg.norm(v[:, i])  # Norma da velocidade

    # Cálculo da aceleração
    a[0, i] = -D * v[0, i] * v_norm + (A * rho * R * w * v[2, i]) / (2 * m)  # Efeito Magnus
    a[1, i] = -g - D * v[1, i] * v_norm  # Gravidade e arrasto
    a[2, i] = -D * v[2, i] * v_norm - (A * rho * R * w * v[0, i]) / (2 * m)  # Efeito Magnus

    # Atualização da velocidade e posição
    v[:, i + 1] = v[:, i] + a[:, i] * dt
    r[:, i + 1] = r[:, i] + v[:, i] * dt

# Plot da trajetória
plt.plot(r[0, :], r[2, :])  # r[0] = x, r[2] = z (altura)
plt.xlabel("Posição Horizontal [m]")
plt.ylabel("Posição Vertical [m]")
plt.title("Trajetória da bola considerando o efeito Magnus")
plt.show()

ixzero = np.size(r[0, r[0,:]>=0])  
txzero = t[ixzero]
print("Tempo correspondente ao cruzamento da linha de fundo, txzero =", txzero, "s")
print("Coordenadas da bola quando cruza a linha de fundo:")
print("   x = ", r[0,ixzero], "m")
print("   y = ", r[1,ixzero], "m")
print("   z = ", r[2,ixzero], "m")
