import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

t = np.linspace(0, 2 * np.pi, 100)
x = np.cos(t) 
y = np.sin(t)

fig, ax = plt.subplots()
terra, = ax.plot([], [], 'bo', markersize=8) 
ax.set_xlim(-1.5, 1.5) 
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Movimento da Terra ao redor do Sol")
ax.grid()

def init():
    terra.set_data([], [])
    return terra,

def update(frame):
    terra.set_data([x[frame]], [y[frame]]) 
    return terra,

ani = FuncAnimation(fig, update, frames=len(t), init_func=init, interval=50, blit=True)

plt.show()
