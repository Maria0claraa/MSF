import numpy as np

dt = 0.01 # δt - tamanho do passo
t0 = 0 # Tempo inicial
tf = 4.0 # Tempo final
y0 = 0 # Posição inicial

# Número de passos/iterações
#
# + 0.1 para garantir que não há arrendodamentos
# para baixo
n = int((tf-t0) / dt + 0.1)

t = np.zeros(n + 1) # Tempo
y = np.zeros(n + 1) # Posição
vy = np.zeros(n + 1) # Velocidade

# Valores inicias
t[0] = t0
y[0] = y0

for i in range(n):
  vy[i] = 5 # Em vez de uma constante pode-se também utilizar
            # uma expressão ou função v(t) que calcula a velocidade
            # a partir do tempo

  # x(t + δt) = x(t) + v(t) * δt
  y[i + 1] = y[i] + vy[i] * dt
  t[i + 1] = t[i] + dt