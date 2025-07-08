import sympy as sy  #biblioteca para calculo simbólico
import numpy as np
import matplotlib.pyplot as plt

# Definir variáveis simbólicas
x, y, m, b = sy.symbols('x y m b')
# Definir a expressão
y = m*x**2 + b
# Impôr valores específicos para m e b na expressão y (y2 passa a ser uma função de apenas uma variável x)
y2 = y.subs([(m, 0.01), (b, 0.0)])
y_em_1 = y2.evalf(subs={x: 1}) #substitui x por 1 na y2
print(f'Valor de y2 em x=1: {y_em_1}')

y_lam = sy.lambdify(x, y2, "numpy")  #converte a expressão simbólica y2 em numérica
# Criar valores de x para o gráfico
x_vals = np.linspace(0, 2, 100)
y_vals = y_lam(x_vals)


plt.plot(x_vals, y_vals, label='$y = 0.01x^2$')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gráfico da função y = 0.01x²')
plt.legend()
plt.grid()
plt.show()


# Derivada de y em relação a x
derivada = sy.diff(y, x)
print(f'Derivada de y em relação a x: {derivada}')

# Integral de y em relação a x
integral = sy.integrate(y, x)
print(f'Integral de y em relação a x: {integral}')

# Resolver numericamente y=0 para um x inicial
solucao_x = sy.nsolve(y2, x, 1)  # Chute inicial x0=1
print(f'Solução numérica de y=0: x = {solucao_x}')
