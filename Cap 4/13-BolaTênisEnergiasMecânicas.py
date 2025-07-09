import matplotlib.pyplot as plt
import numpy as np

vf = 100 * 1000/3600
g = 9.81
theta_deg = 10
theta_rad = np.radians(theta_deg)
m = 0.057

#calcular energia mecânica sem resistência do ar
#no instante inicial: 
E_sem_ar = (1/2) * m * vf**2 
print("Energia Mecânica sem resistêcia do ar: ", E_sem_ar)



#energia mecânica com resistência do ar
vx = vf * np.cos(theta_rad)
vy = vf * np.sin(theta_rad)
x, y = 0.0, 0.0

# Integração
dt = 0.001
t_total = 0.81  #limite superior tempo de isimulação
n = int(t_total / dt)  #uqantidade de interações que serão realizadas

# Armazenar tempo, energia, velocidades
tempos = []
energias = []

for i in range(n):
    t = i * dt
    v = np.sqrt(vx**2 + vy**2)  #modulo da velocidade
    
    # Forças: gravidade e resistência do ar
    fax = -m * g / vf**2 * v * vx
    fay = -m * g / vf**2 * v * vy - m * g
    
    ax = fax / m
    ay = fay / m
    
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    
    #Cálculo da nova energia mecânica
    Ec = 0.5 * m * (vx**2 + vy**2)
    Ep = m * g * y
    Em = Ec + Ep
    
    #armazenar os dados
    tempos.append(t)
    energias.append(Em)

# Energia nos tempos pedidos:
def energia_em_tempo(t_alvo):
    idx = int(t_alvo / dt)
    return energias[idx]

print("Energia mecânica com resistência do ar:")
for t in [0, 0.4, 0.8]:
    print(f"t = {t:.1f} s → E_m = {energia_em_tempo(t):.4f} J")


#Trabalho realizado pela resistência do ar
#Aproximação trapezoidal
def trabalho_resistencia_em_tempo(t_alvo):
    Em = energia_em_tempo(t_alvo)
    W_ar = Em - E_sem_ar
    return W_ar  # será negativo (trabalho dissipativo)

print("\nTrabalho realizado pela força de resistência do ar:")
for t in [0, 0.4, 0.8]:
    W = trabalho_resistencia_em_tempo(t)
    print(f"t = {t:.1f} s → Trabalho = {W:.4f} J")