import numpy as np

# Parâmetros
m = 0.058  # Massa (kg)
g = 9.81  # Gravidade (m/s^2)
h = 5.0  # Altura inicial (m)
vT_tenis = 100 / 3.6  # Velocidade terminal da bola de ténis (m/s)
vT_badminton = 6.80  # Velocidade terminal do volante (m/s)

# Coeficientes de resistência
k_tenis = m * g / vT_tenis
k_badminton = m * g / vT_badminton

# Método de Euler
def queda_tempo(k, dt=0.001):  # Reduzindo dt para maior precisão
    t = 0
    y = h
    v = 0
    while y > 0:
        a = g - (k/m) * v  # Aceleração
        v += a * dt  # Atualiza velocidade
        y -= v * dt  # Atualiza posição
        t += dt
    return t

# Cálculo do tempo de queda
t_tenis = queda_tempo(k_tenis)
t_badminton = queda_tempo(k_badminton)

# Resultados
print(f"Tempo de queda da bola de ténis: {t_tenis:.2f} s")  # Deve ser ~1.02 s
print(f"Tempo de queda do volante de badminton: {t_badminton:.2f} s")  # Deve ser ~1.19 s

if t_tenis < t_badminton:
    print("A bola de ténis chega primeiro ao solo.")
elif t_badminton < t_tenis:
    print("O volante de badminton chega primeiro ao solo.")
else:
    print("Ambos chegam ao mesmo tempo.")
