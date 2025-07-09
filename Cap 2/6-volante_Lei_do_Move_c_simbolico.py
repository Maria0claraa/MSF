import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Definição de constantes
vt = 6.80  # Velocidade terminal (m/s)
g = 9.81   # Gravidade (m/s^2)

t = sp.Symbol('t')
y_expr = (vt**2 / g) * sp.log(sp.cosh(g * t / vt))

# a) Gráfico da posição
T_vals = np.linspace(0, 4, 100)
Y_vals = [(vt**2 / g) * np.log(np.cosh(g * T / vt)) for T in T_vals]

plt.figure()
plt.plot(T_vals, Y_vals, label='y(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Altura (m)')
plt.title('Gráfico da posição y(t)')
plt.legend()
plt.grid()
plt.show()

# b) Velocidade v(t) e gráfico
v_expr = sp.diff(y_expr, t)
V_vals = [vt * np.tanh(g * T / vt) for T in T_vals]

plt.figure()
plt.plot(T_vals, V_vals, label='v(t)', color='r')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Gráfico da velocidade v(t)')
plt.legend()
plt.grid()
plt.show()

# c) Aceleração a(t) e gráfico
a_expr = sp.diff(v_expr, t)
A_vals = [g * (1 / np.cosh(g * T / vt))**2 for T in T_vals]

plt.figure()
plt.plot(T_vals, A_vals, label='a(t)', color='g')
plt.xlabel('Tempo (s)')
plt.ylabel('Aceleração (m/s²)')
plt.title('Gráfico da aceleração a(t)')
plt.legend()
plt.grid()
plt.show()

# d) Verificação da equivalência da aceleração
a_alt_expr = g - (v_expr**2 / vt**2) * g
simplified_expr = sp.simplify(a_expr - a_alt_expr)
print("Diferença entre expressões de a(t):", simplified_expr)

# e) Tempo para atingir o solo
y0 = 20  # Altura inicial
t_solve = sp.solveset(y_expr - y0, t, domain=sp.S.Reals)
print("Tempo para atingir o solo (com resistência do ar):", t_solve)

# Tempo sem resistência
t_free_fall = sp.solve(y0 - (1/2) * g * t**2, t)
print("Tempo para atingir o solo (sem resistência):", t_free_fall)

# f) Velocidade e aceleração ao atingir o solo
t_impact = float(max([sol.evalf() for sol in t_solve]))  # Converter para float
v_impact = vt * np.tanh(g * t_impact / vt)  # Agora funciona corretamente
a_impact = g * (1 / np.cosh(g * t_impact / vt))**2
print(f"Velocidade ao atingir o solo: {v_impact:.2f} m/s")
print(f"Aceleração ao atingir o solo: {a_impact:.3f} m/s²")