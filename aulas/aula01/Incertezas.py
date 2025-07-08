import numpy as np
import matplotlib.pyplot as plt

N=10   
X = np.random.normal(4.5,0.5,size=N) #Gerar 10 valores de X com média esperada de 4.5 e desvio padrão de 0.5
Xmedia = np.mean(X) #Média dos valores
Xerro = np.std(X)/np.sqrt(N) #Erro da média (incerteza)
print("X:", X, "Xmedia:", Xmedia, "Xerro:", Xerro)
    
#Conjunto de valores Y (media 10.0 e desvio padrão 1.0)
Y = np.random.normal(10.0,1.0,size=N)
Ymedia = np.mean(Y)
Yerro = np.std(Y)/np.sqrt(N)
print("Y:", Y, "Ymedia:", Ymedia, "Yerro:", Yerro)

Z = X+Y 
Zmedia = np.mean(Z) #media dos valores de Z
# Estimando a incerteza de Z de duas maneiras:
# i) Diretamente do desvio padrão de Z:
Zerro_i = np.std(Z) / np.sqrt(N) 
# ii) Usando a propagação de incertezas: (SOMA)
Zerro_ii = Xerro + Yerro
print("Z:", Z, "Zmedia:", Zmedia, "Zerro_i:", Zerro_i, "Zerro_ii:", Zerro_ii)

W = X*Y 
Wmedia = np.mean(W) 
# Estimando a incerteza de W de duas maneiras: (PRODUTO)
# i) Diretamente do desvio padrão dos valores de W
Werro_i = np.std(W) / np.sqrt(N)
# ii) Usando a propagação de incertezas:
Werro_ii = Wmedia * ((Xerro / Xmedia) + (Yerro / Ymedia))
print("W:", W, "Wmedia:", Wmedia, "Werro_i:", Werro_i, "Werro_ii:", Werro_ii)
