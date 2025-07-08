import matplotlib.pyplot as plt
import numpy as np
  

def maxminv(xm1,xm2,xm3,ym1,ym2,ym3):  
    # Máximo ou mínimo usando o polinómio de Lagrange
    # Dados (input): (x0,y0), (x1,y1) e (x2,y2) 
    # Resultados (output): xm, ymax 
    xab=xm1-xm2
    xac=xm1-xm3
    xbc=xm2-xm3
    a=ym1/(xab*xac)
    b=-ym2/(xab*xbc)
    c=ym3/(xac*xbc)
    xmla=(b+c)*xm1+(a+c)*xm2+(a+b)*xm3
    xm=0.5*xmla/(a+b+c)
    xta=xm-xm1
    xtb=xm-xm2
    xtc=xm-xm3
    ymax=a*xtb*xtc+b*xta*xtc+c*xta*xtb
    return xm, ymax

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

def medir_periodo(t, theta):
    """Mede o período encontrando dois máximos consecutivos com interpolação."""
    maximos = []

    # Começa no índice 1 e termina no penúltimo
    for i in range(1, len(theta) - 1):
        if theta[i-1] < theta[i] and theta[i+1] < theta[i]:
            # Usar 3 pontos para interpolar o máximo

            xm, _ = maxminv(t[i-1], t[i], t[i+1], theta[i-1], theta[i], theta[i+1])
            maximos.append(xm)

            # Apenas precisamos de dois máximos consecutivos
            if len(maximos) == 2:
                break

    if len(maximos) == 2:
        periodo = maximos[1] - maximos[0]
        return periodo
    else:
        return None


angulos_iniciais = [0.1, 0.3, 0.5]




for theta0 in angulos_iniciais:
    t_num, theta_num = euler_cromer(theta0)
    t_ana, theta_ana = solucao_analitica(theta0)
    periodo = medir_periodo(t_num, theta_num)
    T_teorico = 2 * np.pi * np.sqrt(L / g)

    if periodo:
        print(f"θ₀ = {theta0:.1f} rad: Período medido = {periodo:.4f} s | Período teórico = {T_teorico:.4f} s")
    else:
        print(f"θ₀ = {theta0:.1f} rad: Não foi possível medir o período.")


    plt.plot(t_num, theta_num, label=f'Numérico θ₀={theta0:.1f} rad')
    plt.plot(t_ana, theta_ana, '--', label=f'Analítico θ₀={theta0:.1f} rad')
    plt.title('Movimento de um pêndulo simples (θ vs. t)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Ângulo (rad)')
    plt.legend()
    plt.grid(True)
    plt.show()
