import numpy as np
import matplotlib.pyplot as plt

massa = np.array([0.15, 0.20, 0.16, 0.11, 0.25, 0.32, 0.40, 0.45, 0.50, 0.55])
periodo = np.array([1.21, 1.40, 1.26, 1.05, 1.60, 1.78, 2.00, 2.11, 2.22, 2.33])  

plt.scatter(massa, periodo, color='blue', label="Medições")
plt.xlabel("Massa (kg)")
plt.ylabel("Período (s)")
plt.title("Relação entre Período e Massa")
plt.legend()
plt.show()

log_massa = np.log(massa)
log_periodo = np.log(periodo)

plt.scatter(log_massa, log_periodo, color='blue', label="Medições")
coef, intercept = np.polyfit(log_massa, log_periodo, 1)  
plt.plot(log_massa, coef * log_massa + intercept, color='red', label="Ajuste Linear")
plt.xlabel("log(Massa)")
plt.ylabel("log(Período)")
plt.title("Gráfico log-log")
plt.legend()
plt.show()

tempo_quadrado = periodo ** 2
plt.scatter(massa, tempo_quadrado, color='blue', label="Medições")
coef_t2, intercept_t2 = np.polyfit(massa, tempo_quadrado, 1) 
plt.plot(massa, coef_t2 * massa + intercept_t2, color='red', label="Ajuste Linear")
plt.xlabel("Massa (kg)")
plt.ylabel("T^2 (s^2)")
plt.title("Relação Linear entre T^2 e M")
plt.legend()
plt.show()

residuos = tempo_quadrado - (coef_t2 * massa + intercept_t2)
SSE = np.sum(residuos**2)  
SST = np.sum((tempo_quadrado - np.mean(tempo_quadrado))**2)  
r2 = 1 - (SSE / SST)

n = len(massa)
erro_declive = np.sqrt(SSE / (n - 2)) / np.sqrt(np.sum((massa - np.mean(massa))**2))
erro_intercepto = erro_declive * np.sqrt(np.sum(massa**2) / n)

K = 4 * np.pi**2 / coef_t2
erro_K = (4 * np.pi**2 * erro_declive) / coef_t2**2

print(f"Declive (m): {coef_t2:.2f} ± {erro_declive:.2f} s²/kg")
print(f"Ordenada na origem (b): {intercept_t2:.2f} ± {erro_intercepto:.2f} s²")
print(f"Coeficiente de determinação (R²): {r2:.4f}")
print(f"Constante elástica (K): {K:.2f} ± {erro_K:.2f} kg/s²")
