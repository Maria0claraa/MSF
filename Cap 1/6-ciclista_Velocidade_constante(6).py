
import numpy as np
import matplotlib.pyplot as plt

tempo = np.arange(0, 10, 1) 
distancia = np.array([0.00, 0.735, 1.363, 1.739, 2.805, 3.814, 4.458, 4.955, 5.666, 6.329])  

coef, intercept = np.polyfit(tempo, distancia, 1)  
reta_ajustada = coef * tempo + intercept

residuos = distancia - reta_ajustada
SSE = np.sum(residuos**2)  
SST = np.sum((distancia - np.mean(distancia))**2)  
r2 = 1 - (SSE / SST)  

velocidade_media = (distancia[-1] - distancia[0]) / (tempo[-1] - tempo[0]) 
velocidade_kmh = velocidade_media * 60  

plt.scatter(tempo, distancia, color='blue', label="Medições")
plt.plot(tempo, reta_ajustada, color='red', label="Ajuste Linear")
plt.xlabel("Tempo (min)")
plt.ylabel("Distância (km)")
plt.title("Relação entre Tempo e Distância Percorrida")
plt.legend()
plt.show()

n = len(tempo)
erro_declive = np.sqrt(SSE / (n - 2)) / np.sqrt(np.sum((tempo - np.mean(tempo))**2))
erro_intercepto = erro_declive * np.sqrt(np.sum(tempo**2) / n)

print(f"Declive (velocidade média em km/min): {coef:.3f} km/min")
print(f"Ordenada na origem: {intercept:.3f} km")
print(f"Erro do declive: {erro_declive:.3f} km/min")
print(f"Erro da ordenada na origem: {erro_intercepto:.3f} km")
print(f"Coeficiente de determinação (R²): {r2:.3f}")
print(f"Velocidade média em km/h: {velocidade_kmh:.2f} km/h")
