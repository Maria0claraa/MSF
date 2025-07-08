import numpy as np
import matplotlib.pyplot as plt

# Parâmetros físicos do sistema
m = 1.0         # Massa (kg)
k = 0.2         # Constante elástica (N/m)
alpha = 1.0     # Parâmetro do termo não linear (N/m^3)
b = 0.01        # Coeficiente de amortecimento (kg/s)
F0 = 5.0        # Amplitude da força externa (N)
omega_f = 0.6   # Frequência da força externa (rad/s)

# Função que define o sistema de equações diferenciais
def derivadas(t, y):
    x, v = y  # y[0] = posição, y[1] = velocidade
    dxdt = v
    dvdt = (F0 * np.cos(omega_f * t) - b * v - k * x - 4 * alpha * x**3) / m
    return np.array([dxdt, dvdt])

# Método de Runge-Kutta de 4ª ordem
def rk4(derivadas, y0, t0, tf, dt):
    N = int((tf - t0) / dt)  # Número de passos
    t = np.linspace(t0, tf, N)
    y = np.zeros((N, len(y0)))
    y[0] = y0

    for i in range(1, N):
        ti = t[i-1]
        yi = y[i-1]

        k1 = dt * derivadas(ti, yi)
        k2 = dt * derivadas(ti + dt/2, yi + k1/2)
        k3 = dt * derivadas(ti + dt/2, yi + k2/2)
        k4 = dt * derivadas(ti + dt, yi + k3)

        y[i] = yi + (k1 + 2*k2 + 2*k3 + k4) / 6

    return t, y

# Condição inicial: x = 1.0 m, v = 0.0 m/s
y0 = [1.0, 0.0]
t0 = 0
tf = 50
dt = 0.01  # valor de dt inicial

t, y = rk4(derivadas, y0, t0, tf, dt)
x = y[:, 0]
v = y[:, 1]

# Gráfico da posição em função do tempo
plt.figure(figsize=(10, 4))
plt.plot(t, x, label='x(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Oscilador Não Harmônico - x(t)')
plt.grid()
plt.legend()
plt.show()

#observa-se o comportamento oscilatório do sistema sob ação de uma força externa periódica,
#com presença de não linearidade e amortecimento. A posição x(t) mostra oscilações complexas e não harmônicas

#A precisão da solução numérica depende do valor de dt. Com valores maiores de dt (ex: 0.1),
#pode haver perda de precisão e até instabilidades numéricas. Valores menores de dt (ex: 0.001) resultam
#em maior precisão, mas com custo computacional mais elevado.

# Mudar ligeiramente a condição inicial para verificar sensibilidade
y0_perturbado = [1.0001, 0.0]
t2, y2 = rk4(derivadas, y0_perturbado, t0, 50, dt)
x2 = y2[:, 0]

#Com uma pequena alteração na condição inicial (de x0 = 1.0000 para x0 = 1.0001),
#observa-se que, com o passar do tempo, as soluções se afastam significativamente.
#Isto indica que o sistema é sensível às condições iniciais 

# Comparar com a trajetória original
plt.figure(figsize=(10, 4))
plt.plot(t, x, label='x(t) com x0 = 1.0000')
plt.plot(t2, x2, label='x(t) com x0 = 1.0001', linestyle='--')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Sensibilidade às Condições Iniciais')
plt.legend()
plt.grid()
plt.show()

# O gráfico no espaço de fase (velocidade vs posição) mostra a natureza do movimento do sistema.
# Neste caso, a trajetória não forma uma elipse fechada (como em osciladores harmônicos),
# mas sim um padrão mais complexo, indicando a presença de não linearidade e amortecimento.

# Espaço de fase: v(t) vs x(t)
plt.figure(figsize=(6, 6))
plt.plot(x, v, label='Trajetória no espaço de fase')
plt.xlabel('Posição x(t) (m)')
plt.ylabel('Velocidade v(t) (m/s)')
plt.title('Espaço de Fase: v(t) vs x(t)')
plt.grid()
plt.legend()
plt.show()
