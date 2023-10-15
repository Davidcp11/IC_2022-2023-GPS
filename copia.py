import datetime as dt
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
import F_GPS
'''----------------------------------------------------------------------'''

arq = open("dados/pcnpcs.txt")
a = arq.readline()
PCN = []
PCS = []
for line in arq:
    line = line.split()
    PCN.append(float(line[2]))
    PCS.append(float(line[3]))

dig, axes = plt.subplots(2, 1)
axes[0].plot(np.linspace(0, 96, len(PCN)), PCN)
axes[0].set_title("PCN")
axes[1].plot(np.linspace(0, 96, len(PCS)), PCS)
axes[1].set_title("PCS")
# Definir os valores e rótulos desejados para o eixo x
x_ticks = list(range(0, 104, 8)) # Cria uma lista com o dobro do tamanho de x
x_labels = [str(i%24) for i in x_ticks]  # Rótulos repetidos usando módulo
# Configurar os marcadores no eixo x
axes[0].set_xticks(x_ticks, x_labels)
axes[1].set_xticks(x_ticks, x_labels)
axes[0].grid(True)
axes[1].grid(True)
plt.tight_layout()

plt.show()

