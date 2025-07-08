import numpy as np

# Dados fornecidos no exercício 1
massa = 0.057  # massa da bola em kg
g = 9.81  # aceleração gravitacional (m/s^2)

# Resultados do exercício 1 (importados ou calculados previamente)
t = np.array([0, 0.2, 0.4])  # instantes de tempo
v_x = np.array([160, 140, 120]) * 1000 / 3600  # velocidades em x (m/s)
v_y = np.array([20, 15, 10]) * 1000 / 3600  # velocidades em y (m/s)
v_z = np.array([-20, -15, -10]) * 1000 / 3600  # velocidades em z (m/s)
F_res_x = np.array([-0.5, -0.4, -0.3])  # força de resistência em x (N)
F_res_y = np.array([-0.7, -0.6, -0.5])  # força de resistência em y (N)
F_res_z = np.array([0, 0, 0])  # força de resistência em z (N)

# 1. Cálculo da energia mecânica
def energia_mecanica(massa, v_x, v_y, v_z, g):
    v = np.sqrt(v_x**2 + v_y**2 + v_z**2)  # módulo da velocidade
    E_c = 0.5 * massa * v**2  # energia cinética
    E_p = massa * g * np.array([0, 0, 0])  # energia potencial (altura = 0)
    return E_c + E_p

energia_mec = energia_mecanica(massa, v_x, v_y, v_z, g)
print("Energia mecânica nos instantes:", energia_mec)

# 2. Cálculo do trabalho realizado pela força de resistência (aproximação trapezoidal)
def trabalho_resistencia(F_res, v, t):
    integrando = F_res * v
    trabalho = np.trapz(integrando, t)  # integração trapezoidal
    return trabalho

# Trabalho em cada direção
trabalho_x = trabalho_resistencia(F_res_x, v_x, t)
trabalho_y = trabalho_resistencia(F_res_y, v_y, t)
trabalho_z = trabalho_resistencia(F_res_z, v_z, t)

# Trabalho total
trabalho_total = trabalho_x + trabalho_y + trabalho_z
print("Trabalho realizado pela força de resistência do ar:", trabalho_total)

# 3. Cálculo do trabalho usando a conservação de energia
trabalho_conservacao = energia_mec[-1] - energia_mec[0]
print("Trabalho pela conservação de energia:", trabalho_conservacao)

#Os possíveis erros na integração são devido à aproximação trapezoidal e à discretização dos dados. O maior erro provavelmente vem da aproximação trapezoidal