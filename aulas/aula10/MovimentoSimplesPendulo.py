
import numpy as np
import matplotlib.pyplot as plt

g = 9.8      
L = 1.0 
w0 = 0.0      
dt = 0.01     
T_total = 10  
n_steps = int(T_total / dt)

def euler_cromer(theta0):
    
    theta = np.zeros(n_steps)
    omega = np.zeros(n_steps)
    t = np.linspace(0, T_total, n_steps)


    theta[0] = theta0
    omega[0] = w0

    for i in range(n_steps - 1):
        omega[i+1] = omega[i] - dt * (g / L) * np.sin(theta[i])
        theta[i+1] = theta[i] + dt * omega[i+1]

    return t, theta

def solucao_analitica(theta0):
    
    t = np.linspace(0, T_total, n_steps)
    omega0 = 0.0
    A = theta0
    phi = 0  
    w = np.sqrt(g / L)
    theta = A * np.cos(w * t + phi)
    return t, theta


angulos_iniciais = [0.1, 0.3, 0.5]




for theta0 in angulos_iniciais:
    t_num, theta_num = euler_cromer(theta0)
    t_ana, theta_ana = solucao_analitica(theta0)

    plt.plot(t_num, theta_num, label=f'Numérico θ₀={theta0:.1f} rad')
    plt.plot(t_ana, theta_ana, '--', label=f'Analítico θ₀={theta0:.1f} rad')
    plt.title('Movimento de um pêndulo simples (θ vs. t)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Ângulo (rad)')
    plt.legend()
    plt.grid(True)
    plt.show()