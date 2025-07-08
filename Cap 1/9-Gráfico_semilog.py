import numpy as np
import matplotlib.pyplot as plt

comprimento = np.arange(1.2, 4.2, 11, 20, 22, 37, 45)   
massa = np.array([00.3, 0.54, 9.1, 38, 577, 230, 480])  

plt.scatter(comprimento, massa, color='blue', label="Medições")
plt.xlabel("Tempo (dias)")
plt.ylabel("Atividade (mCi)")
plt.title("Decaimento da Atividade ao Longo do Tempo")
plt.legend()
plt.show()

log_atividade = np.log(massa)

plt.figure(figsize=(8, 5))
plt.scatter(comprimento, log_atividade, color='green', label="Medições")

p, cov = np.polyfit(comprimento, log_atividade, 1, cov=True)
declive = p[0]
incerteza_declive = np.sqrt(cov[0, 0])  

plt.plot(comprimento, declive * comprimento + p[1], color='red', label=f"Ajuste Linear (m={declive:.4f} ± {incerteza_declive:.4f})")
plt.xlabel("Tempo (dias)")
plt.ylabel("log(Atividade)")
plt.title("Gráfico Semilog")
plt.legend()
plt.show()

print(f"Declive (m): {declive:.4f} ± {incerteza_declive:.4f} dias⁻¹")
