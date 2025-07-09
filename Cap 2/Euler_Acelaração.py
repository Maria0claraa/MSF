import numpy as np

# Parâmetros
dt = 0.01 # δt - tamanho do passo
t0 = 0 # Tempo inicial
tf = 4.0 # Tempo final
y0 = 0 # Posição inicial
vy0 = 0 # Velocidade inicial
g = 9.8 # Aceleração gravítica

# Número de passos/iterações
#
# + 0.1 para garantir que não há arrendodamentos
# para baixo
n = int((tf-t0) / dt + 0.1)

t = np.zeros(n + 1) # Tempo
y = np.zeros(n + 1) # Posição
vy = np.zeros(n + 1) # Velocidade
ay = np.zeros(n + 1) # Aceleração

# Valores inicias
vy[0] = vy0
t[0] = t0
y[0] = y0

for i in range(n):
  ay[i] = g # Pode também ser substituído por uma
            # expressão ou uma função a(t).

  # Primeira ordem (velocidade)
  # v(t + δt) = v(t) + a(t) * δt
  vy[i + 1] = vy[i] + ay[i] * dt
  # Segunda ordem (posição)
  # x(t + δt) = x(t) + v(t) * δt
  y[i + 1] = y[i] + vy[i] * dt 
  t[i + 1] = t[i] + dt



#Encontrar instante 
# Instante onde está o valor, neste caso 3 segundos
target = 3
# Calcular o indíce nos arrays mais perto do instante que queremos obter,
# depende do instante e do passo
targetIdx = int(np.ceil(target / dt))

# Agora basta aceder ao array que tem o valor (neste caso `vy`, que contêm a
# velocidade) com `targetIdx` para obter o valor no instante.
v = vy[targetIdx]
# Obtemos também o instante em que foi calculado o valor para verificar que
# o índice escolhido está correto.
I = t[targetIdx]




# Calcular o índice onde ocorre o máximo no array (neste caso `y`, que
# contêm a posição)
idx = y.argmax()
# Obter o valor
yMax = y[idx]
# Obter o instante em que ocorreu
tMax = t[idx]



#Primeiro zero e instante em que ocorreu 
for i in range(n):
  if y[i] == 0 or y[i] * y[i + 1] < 0:
    idx = i
    break

yZero = y[idx]
tZero = t[idx]