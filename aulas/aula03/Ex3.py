import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Definição da gravidade e velocidade terminal
g = 9.8
vT = 6.8

# Definição das variáveis simbólicas
t = sp.symbols('t')

# Equação da altura y(t)
y_t = (vT**2 / g) * sp.log(sp.cosh(g * t / vT))

# Criar uma faixa de tempo para os gráficos
tempo = np.linspace(0, 4, 100)

# Converter y(t) para uma função numérica
y_func = sp.lambdify(t, y_t, 'numpy')

# Plot da altura
plt.plot(tempo, y_func(tempo), 'g', label='Distância percorrida pelo volante')

# Calcular a velocidade v(t) = dy/dt
v_t = sp.diff(y_t, t)
v_func = sp.lambdify(t, v_t, 'numpy')

# Plot da velocidade
plt.plot(tempo, v_func(tempo), 'b', label='Velocidade Instantânea')

# Calcular a aceleração a(t) = dv/dt
a_t = sp.diff(v_t, t)
a_func = sp.lambdify(t, a_t, 'numpy')

# Plot da aceleração
plt.plot(tempo, a_func(tempo), 'y', label='Aceleração Instantânea')

# Calcular a aceleração usando a equação teórica a(t) = g - (g/vT²) * v(t) * |v(t)|
a_teorica = g - (g / vT**2) * v_func(tempo) * np.abs(v_func(tempo))

# Plot da aceleração teórica
plt.plot(tempo, a_teorica, 'orange', label='Aceleração por fórmula teórica')

# Cálculo do tempo de queda sem resistência do ar: y = (1/2) g t^2
t_sem_resistencia = sp.nsolve((1/2) * g * t**2 - 20, t, 2)

# Cálculo do tempo de queda com resistência do ar
t_com_resistencia = sp.nsolve(y_t - 20, t, 3.4)

# Exibir tempos calculados
print(f"Tempo para atingir o solo com resistência do ar: {float(t_com_resistencia):.2f} segundos")
print(f"Tempo para atingir o solo sem resistência do ar: {float(t_sem_resistencia):.2f} segundos")

# Calcular velocidade e aceleração ao atingir o solo (com resistência do ar)
vel_final = v_func(float(t_com_resistencia))
ace_final = a_func(float(t_com_resistencia))

# Exibir valores finais de velocidade e aceleração
print(f"Velocidade ao atingir o solo: {vel_final:.2f} m/s")
print(f"Aceleração ao atingir o solo: {ace_final:.2f} m/s²")

# Configuração do gráfico
plt.xlabel('Tempo (s)')
plt.title("Queda do volante de badmington")
plt.legend()
plt.grid()
plt.show()
