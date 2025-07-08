import numpy as np
import matplotlib.pyplot as plt

# Dados fornecidos
massa = 2000  # massa do carro em kg
g = 9.81  # aceleração gravitacional em m/s^2
potencia_subida = 40e3  # potência do motor na subida em W
potencia_descida = -30e3  # potência do motor na descida em W
angulo = np.radians(5)  # ângulo de inclinação em radianos
mu = 0.04  # coeficiente de resistência de rolamento
C_res = 0.25  # coeficiente de resistência do ar
A = 2  # área frontal do carro em m^2
rho_ar = 1.225  # densidade do ar em kg/m^3
distancia = 2000  # distância a percorrer em m

# Função para calcular a aceleração
def aceleracao(v, potencia, massa, angulo, mu, C_res, A, rho_ar):
    P_x = -massa * g * np.sin(angulo)  # força gravitacional
    F_rol = -mu * massa * g * np.cos(angulo)  # força de rolamento
    F_res = -0.5 * C_res * A * rho_ar * v**2  # força de resistência do ar
    F_motor = potencia / v if v > 0 else 0  # força gerada pelo motor
    return (F_motor + P_x + F_rol + F_res) / massa

# Subida
dt = 0.1  # passo de tempo em segundos
v = [1]  # velocidade inicial em m/s
x = [0]  # posição inicial em m
t = [0]  # tempo inicial em s

while x[-1] < distancia:
    a = aceleracao(v[-1], potencia_subida, massa, angulo, mu, C_res, A, rho_ar)
    v.append(v[-1] + a * dt)
    x.append(x[-1] + v[-1] * dt)
    t.append(t[-1] + dt)

tempo_subida = t[-1]
trabalho_motor_subida = potencia_subida * tempo_subida

print(f"Tempo para percorrer 2 km na subida: {tempo_subida:.2f} s")
print(f"Trabalho feito pelo motor na subida: {trabalho_motor_subida / 1e6:.2f} MJ")

# Descida
v_descida = [20]  # velocidade inicial na descida em m/s
x_descida = [0]  # posição inicial na descida em m
t_descida = [0]  # tempo inicial na descida em s

while x_descida[-1] < distancia:
    a = aceleracao(v_descida[-1], potencia_descida, massa, -angulo, mu, C_res, A, rho_ar)
    v_descida.append(v_descida[-1] + a * dt)
    x_descida.append(x_descida[-1] + v_descida[-1] * dt)
    t_descida.append(t_descida[-1] + dt)

tempo_descida = t_descida[-1]
trabalho_motor_descida = potencia_descida * tempo_descida

print(f"Tempo para percorrer 2 km na descida: {tempo_descida:.2f} s")
print(f"Trabalho feito pelo motor na descida: {trabalho_motor_descida / 1e6:.2f} MJ")

# Recuperação de energia
energia_recuperada = -0.5 * trabalho_motor_descida  # 50% da energia recuperada
diferenca_energia = trabalho_motor_subida + trabalho_motor_descida + energia_recuperada

print(f"Diferença de energia na bateria após subida e descida: {diferenca_energia / 1e6:.2f} MJ")