import numpy as np
import matplotlib.pyplot as plt

t0 = 0.0 
tf = 4.0 
x0 = 0.0 
v0 = 10.0 
vT = 100 * 1000 / 3600 # velocidade terminal [m/s]
dt = 0.0001

g = 9.8 
D = g / vT ** 2 # parâmetro de resitência ao ar [m^-1]


t = np.arange(t0, tf, dt) 
x = np.empty(np.size(t)) 
v = np.empty(np.size(t))  
a = np.empty(np.size(t)) 


x[0] = x0
v[0] = v0

for i in range(np.size(t) - 1):
    a[i] = - g - D * v[i] * np.abs(v[i])
    v[i+1] = v[i] + a[i] * dt
    x[i+1] = x[i] + v[i] * dt


plt.plot(t, x, 'b-')
plt.plot(t, x0 + v0 * t - 0.5 * g * t**2, 'r-')
plt.grid(axis = "y", color = 'black', linewidth = 0.5)
plt.xlabel("Tempo, t [s]")
plt.ylabel("Posição, y [m]")
plt.show()


imax = np.argmax(x)  #valor máximo de x
tmax = t[imax]  #tempo correspondente
print("Tempo correspondente à altura máxima, tmax = ", tmax, "s")
print("Altura máxima, ymax = ", x[imax], "m")


izero = np.size(x) - np.size(x[x<0]) #primeiro valor negativo de x
tzero = t[izero]
print("Tempo de rotorno à orígem, tzero = ", tzero, "s")