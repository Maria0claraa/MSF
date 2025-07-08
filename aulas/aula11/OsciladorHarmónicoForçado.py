import numpy as np
import matplotlib.pyplot as plt

# Parâmetros físicos do sistema
m = 1.0         # Massa (kg)
k = 1.0        # Constante elástica (N/m)
alpha = 1.0     # Parâmetro do termo não linear (N/m^3)
b = 0.05        # Coeficiente de amortecimento (kg/s)
F0 = 7.5        # Amplitude da força externa (N)
omega_f = 0.5   # Frequência da força externa (rad/s)

# Sistema de equações diferenciais
# Sistema de equações diferenciais corrigido (sem termo não linear)
def derivadas(t, y):
    x, v = y
    dxdt = v
    dvdt = (F0 * np.cos(omega_f * t) - b * v - k * x) / m  #PELA SEGUNDA LEI DE NEWTON
    return np.array([dxdt, dvdt])

# Método de Runge-Kutta de 4ª ordem
def rk4(derivadas, y0, t0, tf, dt):
    N = int((tf - t0) / dt)
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

# Função simples para detectar picos no array y (máximos locais)
def detectar_picos(y):
    picos = []
    for i in range(1, len(y)-1):
        if y[i-1] < y[i] > y[i+1]:
            picos.append(i)
    return picos

y0 = [1.0, 0.0]
t0 = 0
tf = 100
dt = 0.01

t, y = rk4(derivadas, y0, t0, tf, dt)
x = y[:, 0]  #extrai vetor posição
v = y[:, 1]  #extrai vetor velocidade 
# Gráfico da posição
plt.figure(figsize=(10, 4))
plt.plot(t, x)
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Oscilador Não Harmônico - x(t)')
plt.grid()
plt.show()

# b) Cálculo da amplitude e período no regime estacionário
#analisa apenas ops últimos 30% 
t_regime = t[int(len(t)*0.7):]
x_regime = x[int(len(t)*0.7):]

amplitude = (np.max(x_regime) - np.min(x_regime)) / 2
picos = detectar_picos(x_regime)  #encontra os picos 

#se houver pelo menos 2 picos seguidos 
if len(picos) >= 2:
    tempos_picos = [t_regime[i] for i in picos]
    periodos = [tempos_picos[i+1] - tempos_picos[i] for i in range(len(tempos_picos)-1)]
    periodo_medio = sum(periodos) / len(periodos)
else:
    periodo_medio = None

print(f"Amplitude no regime estacionário: {amplitude:.4f} m")
print(f"Período médio estimado: {periodo_medio:.4f} s")

# Variação de ω_f de 0.2 a 2 rad/s e cálculo da amplitude
omega_valores = np.linspace(0.2, 2.0, 50)  #arrayu para explorar difrentes frequências forçadas
amplitudes = []

#para cada frequência resolve o rk4 para regime estacionário 
for omega in omega_valores:
    omega_f = omega  # alterar frequência global
    t_temp, y_temp = rk4(derivadas, y0, t0, tf, dt)
    x_temp = y_temp[:, 0]
    x_reg = x_temp[int(len(x_temp)*0.7):]
    amp = (np.max(x_reg) - np.min(x_reg)) / 2
    amplitudes.append(amp)

# Encontrar a frequência que gera maior amplitude
indice_max = np.argmax(amplitudes)
omega_max = omega_valores[indice_max]
amplitude_max = amplitudes[indice_max]

print(f"Maior amplitude: {amplitude_max:.4f} m ocorre em ω_f = {omega_max:.4f} rad/s")

