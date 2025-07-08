import numpy as np
import matplotlib.pyplot as plt

media_esperada = 4.5 
desvio_esperado = 0.5

N_values = np.logspace(1, 4, num=50)

medias = []
incertezas = []
for N in N_values:
    medições = np.random.normal(media_esperada, desvio_esperado, int(N))  #gerar uma amostra de n medições
    media = np.mean(medições)  #media das medições
    medias.append(media) 
    incerteza = np.std(medições) / np.sqrt(N)  #incerteza pelo desvio padrão
    incertezas.append(incerteza)

# Criar o gráfico
plt.figure(figsize=(8, 6))
# Plotar as médias das medições
plt.plot(N_values, medias, label='Média das medições', color='blue', marker='o')
# Adicionar linha da média esperada
plt.axhline(media_esperada, color='green', linestyle='--', label=f'Média esperada ({media_esperada})')
# Adicionar as linhas de variação esperada (média ± σ/√N)
plt.plot(N_values, media_esperada + np.array(incertezas), 'r--', label=f'Média + erro')
plt.plot(N_values, media_esperada - np.array(incertezas), 'r--', label=f'Média - erro')
# Configurações do gráfico
plt.xscale('log')  # Escala logarítmica no eixo x
plt.xlabel('Número de medições (N)')
plt.ylabel('Média das medições')
plt.title('Média das medições em função de N')
plt.legend()
plt.grid(True)
# Exibir o gráfico
plt.show()





