import numpy as np
import matplotlib.pyplot as plt

R = np.array([6.37, 7.02, 7.61, 8.02, 8.43, 8.92, 9.31, 9.78, 10.25, 10.74]) * 10**6  
a = np.array([9.8, 8.0, 6.6, 6.3, 5.5, 5.1, 4.6, 4.1, 3.8, 3.6]) 

x = 1 / R**2  
y = a         

p, cov = np.polyfit(x, y, 1, cov=True)
K = p[0]  
erro_K = np.sqrt(cov[0, 0])

plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='blue', label="Medições")
plt.plot(x, K * x + p[1], color='orange', label=f"Ajuste Linear")

plt.xlabel(r"$1/R^2 \, (10^{-14} \, m^{-2})$")
plt.ylabel(r"$a \, (m/s^2)$")
plt.title("Gráfico Linearizado da Aceleração da Gravidade")
plt.legend()
plt.show()

print(f"K = ({K:.0f} ± {erro_K:.0f}) × 10¹² m³/s²")
