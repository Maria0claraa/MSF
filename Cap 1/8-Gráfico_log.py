import numpy as np
import matplotlib.pyplot as plt

T = np.array([200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100])  
E = np.array([0.695, 4.363, 15.53, 38.74, 75.08, 125.2, 257.9, 344.1, 557.4, 690.7]) 

plt.figure(figsize=(8, 5))
plt.scatter(T, E, color='blue', label="Medições")
plt.xlabel("Temperatura (K)")
plt.ylabel("Energia (J)")
plt.title("Relação entre Energia Emitida e Temperatura")
plt.legend()
plt.show()


log_T = np.log(T)
log_E = np.log(E)

plt.figure(figsize=(8, 5))
plt.scatter(log_T, log_E, color='green', label="Medições")
p, cov = np.polyfit(log_T, log_E, 1, cov=True)
std_error = np.sqrt(cov[0, 0])
plt.plot(log_T, p[0] * log_T + p[1], color='red', label=f"Ajuste Linear")
plt.xlabel("log(Temperatura)")
plt.ylabel("log(Energia)")
plt.title("Gráfico log-log")
plt.legend()
plt.show()


print(f"Declive (m), que indica a dependência: {p[0]:.2f} ± {std_error:.2f}")
residuos = log_E - (p[0] * log_T + p[1])
SSE = np.sum(residuos**2)
SST = np.sum((log_E - np.mean(log_E))**2)
r2 = 1 - (SSE / SST)
print(f"Coeficiente de determinação (r²): {r2:.4f}")
