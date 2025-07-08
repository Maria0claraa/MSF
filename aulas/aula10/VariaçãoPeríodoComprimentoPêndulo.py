
import numpy as np
import matplotlib.pyplot as plt

# ------------------- Funções de interpolação -------------------

def intlagv(xinp,xm1,xm2,xm3,ym1,ym2,ym3):
    xab=xm1-xm2
    xac=xm1-xm3
    xbc=xm2-xm3
    xi1=xinp-xm1
    xi2=xinp-xm2
    xi3=xinp-xm3
    a=xi2*xi3/(xab*xac) 
    b=-xi1*xi3/(xab*xbc)
    c=xi1*xi2/(xac*xbc)
    yout=a*ym1+b*ym2+c*ym3
    return xinp, yout

def intlaginvv(yinp,xm1,xm2,xm3,ym1,ym2,ym3):
    xab=xm1-xm2
    xac=xm1-xm3
    xbc=xm2-xm3
    a=ym1/(xab*xac)
    b=-ym2/(xab*xbc)
    c=ym3/(xac*xbc)
    am=a+b+c
    bm=a*(xm2+xm3)+b*(xm1+xm3)+c*(xm1+xm2)
    cm=a*xm2*xm3+b*xm1*xm3+c*xm1*xm2-yinp
    xout=(bm+np.sqrt(bm*bm-4*am*cm))/(2*am)
    if xm3 > xm1 and (xout < xm1 or xout > xm3):
        xout=(bm-np.sqrt(bm*bm-4*am*cm))/(2*am)
    if xm1 > xm3 and (xout < xm3 or xout > xm1):
        xout=(bm-np.sqrt(bm*bm-4*am*cm))/(2*am)
    xta=xout-xm1
    xtb=xout-xm2
    xtc=xout-xm3
    yout=a*xtb*xtc+b*xta*xtc+c*xta*xtb
    return xout, yout

def maxminv(xm1,xm2,xm3,ym1,ym2,ym3):
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

# ------------------- Simulação -------------------

g = 9.8                # aceleração gravítica (m/s²)
dt = 0.01              # passo de tempo
T_total = 10           # tempo total de simulação (s)
n_steps = int(T_total / dt)

def euler_cromer(theta0, L):
    theta = np.zeros(n_steps)
    omega = np.zeros(n_steps)
    t = np.linspace(0, T_total, n_steps)
    theta[0] = theta0
    omega[0] = 0.0
    for i in range(n_steps - 1):
        omega[i+1] = omega[i] - dt * (g / L) * np.sin(theta[i])
        theta[i+1] = theta[i] + dt * omega[i+1]
    return t, theta

def solucao_analitica(theta0, L):
    t = np.linspace(0, T_total, n_steps)
    A = theta0
    w = np.sqrt(g / L)
    theta = A * np.cos(w * t)
    return t, theta

# ------------------- Medição do período -------------------

def medir_periodo(t, theta):
    maximos = []
    for i in range(1, len(theta) - 1):
        if theta[i-1] < theta[i] and theta[i+1] < theta[i]:
            xm, _ = maxminv(t[i-1], t[i], t[i+1], theta[i-1], theta[i], theta[i+1])
            maximos.append(xm)
            if len(maximos) == 2:
                break
    if len(maximos) == 2:
        return maximos[1] - maximos[0]
    return None

comprimentos = np.linspace(0.1, 2.0, 20)
periodos = []

for L_val in comprimentos:
    t_sim, theta_sim = euler_cromer(0.1, L_val)
    T = medir_periodo(t_sim, theta_sim)
    periodos.append(T)

logL = np.log(comprimentos)
logT = np.log(periodos)

# Ajuste linear e erro
coef, cov = np.polyfit(logL, logT, deg=1, cov=True)
declive = coef[0]  #declive da reta em concordancia ocm o do    
erro_declive = np.sqrt(cov[0, 0])

# Gráfico
plt.figure(figsize=(8, 6))
plt.plot(logL, logT, 'o', label='Simulação')
plt.plot(logL, np.polyval(coef, logL), 'r-', label=f'Ajuste linear: declive = {declive:.3f} ± {erro_declive:.3f}')
plt.xlabel('log(L)')
plt.ylabel('log(T)')
plt.title('log(T) vs log(L)')
plt.grid(True)
plt.legend()
plt.show()

print(f"Declive = {declive:.4f} ± {erro_declive:.4f} (esperado: 0.5)")