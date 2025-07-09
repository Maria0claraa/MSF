import numpy as np
import matplotlib.pyplot as plt

# Função a integrar
def f(x):
    return x**2

# Valor exato do integral
I_exato = 1/3

# Guardar erros para análise
dx_vals = []
erros = []

# Testar para vários passos dx
for n in [10, 20, 40, 80, 160, 320, 640]:
    a, b = 0, 1
    dx = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)

    # Regra trapezoidal
    I_aprox = dx * (0.5*y[0] + np.sum(y[1:-1]) + 0.5*y[-1])

    erro = abs(I_aprox - I_exato)

    dx_vals.append(dx)
    erros.append(erro)

    print(f"n = {n:<4} dx = {dx:.5f}  I_aprox = {I_aprox:.8f}  Erro = {erro:.2e}")

# Gráfico log-log do erro vs dx
plt.figure()
plt.loglog(dx_vals, erros, 'o-', label='Erro numérico')
plt.loglog(dx_vals, [dx**2 for dx in dx_vals], 'k--', label='$\propto \Delta x^2$')
plt.xlabel('Passo $\Delta x$')
plt.ylabel('Erro absoluto')
plt.title('Erro da Regra Trapezoidal vs $\Delta x$')
plt.legend()
plt.grid(True, which='both')
plt.show()
