import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


t = sp.symbols('t')  # Variável tempo
a_x = 3  


v = sp.integrate(a_x, t) + 0  #integral para obter a velocidade v(0) = 0
x = sp.integrate(v, t) + 0  #x(0) = 0
print("Velocidade em função do tempo (v(t)):", v)
print("Posição em função do tempo (x(t)):", x)

#Gráfico da lei do movimento (x(t))
t_values = np.linspace(0, 25, 500)  # Valores de tempo de 0 a 25 segundos
x_values = [(1.5 * t**2) for t in t_values]  # Avaliar x(t) = 1.5 * t^2

plt.plot(t_values, x_values, label="x(t) = 1.5t²")
plt.xlabel("Tempo (s)")
plt.ylabel("Posição (m)")
plt.title("Lei do Movimento do Avião")
plt.grid()
plt.legend()
plt.show()


v_descolagem = 250 * (1000 / 3600)  # Converter 250 km/h para m/s
print("\nVelocidade de descolagem:", v_descolagem, "m/s")

t_descolagem = sp.nsolve(v - v_descolagem, t, 20)  # Resolver v(t) = 69.44 m/s
print("Tempo de descolagem (t):", t_descolagem, "s")

x_descolagem = x.subs(t, t_descolagem)  # Avaliar x(t) no tempo de descolagem
print("Distância percorrida até a descolagem (x):", x_descolagem, "m")

print("\nVerificação com sympy.integrate():")
print("Velocidade obtida por integração:", v)
print("Posição obtida por integração:", x)