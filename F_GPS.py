import datetime as dt
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cffi.backend_ctypes import xrange
from matplotlib.pyplot import figure
import seaborn as sns
from pylab import *
import calendar
from termcolor import colored
import random
from scipy.interpolate import interpn
import matplotlib as mpl

cores = [['#8EC4A2'],
         ['#06B285'],
         ['#FE9B53'],
         ['#183E51'],
         ['#DF4960'],
         ['#08490F'],
         ['#C87CA9'],
         ['#69CFD3'],
         ['#788832'],
         ['#46FF19'],
         ['#B03F7D'],
         ['#4530B1'],
         ['#4B0700'],
         ['#9945D5'],
         ['#0D5F6D'],
         ['#751774'],
         ['#634756'],
         ['#45E9B2'],
         ['#C9E9A6'],
         ['#5DF0B6'],
         ['#075651'],
         ['#5E3995'],
         ['#963DD4'],
         ['#BAD525'],
         ['#80136B'],
         ['#496547'],
         ['#BBDBDC'],
         ['#39E8DD'],
         ['#33E9D6'],
         ['#5A7F58'],
         ['#5592E7'],
         ['#56C86E'],
         ['#C57C10']]
meses = ['Jan',
         'Feb',
         'Mar',
         'Apr',
         'May',
         'Jun',
         'Jul',
         'Aug',
         'Sep',
         'Oct',
         'Nov',
         'Dec']


def correcao_tec_med(tec):
    '''
    :param tec:
    :return:
    '''
    for i in range(len(tec)):
        if i == 0 and tec[0] < tec[1]*0.99:
            tec[0] = tec[1]
        elif i == len(tec)-1 and tec[i] < tec[i-1]*0.99:
            tec[i] = tec[i-1]
        elif 0 < i and i < len(tec)-2:
            med = np.mean([tec[i-1], tec[i+1]])
            if tec[i] < med*0.99 :
                tec[i] = med
    return tec


def Deriv_Ord1(xi, yi, zi=0):
    '''
    :param xi: Valores de x
    :param yi: Valores de f(x)
    :param zi: Um fator para deslocar os valores no grafico (ROT)
    :return: array com a derivada em cada um dos pontos (x)
    '''
    n = len(xi)
    deriv = np.zeros(n)
    '''Para o primeiro ponto'''
    deriv[0] = (yi[1] - yi[0]) / (xi[1] - xi[0])
    '''Para os demais pontos'''
    for k in range(1, n - 1):
        deriv[k] = (yi[k + 1] - yi[k - 1]) / (xi[k + 1] - xi[k - 1])
    '''Para o último ponto'''
    deriv[n - 1] = (yi[n - 1] - yi[n - 2]) / (xi[n - 1] - xi[n - 2])
    deriv = deriv + 50 * zi
    return deriv


def Tec_medio(estacao, dias_calmos: list, mes: int, ano=2023):
    '''
    :param estacao:
    :param dias_calmos:
    :param mes:
    :return:
    '''
    tec = np.zeros(1440)
    time = np.zeros(1440)
    tec_err = np.zeros(1440)
    mes = ('%02d' % mes)
    k = False
    dados = []
    for x in dias_calmos:
        d1 = ('%03d' % x)
        d2 = ('%02d' % x)
        arq = open(f'Output_GPS/{estacao}{d1}-{ano}-{mes}-{d2}.Std', 'r')
        n = 0
        dado = []
        for linha in arq:
            if linha:
                linha = linha.split()
                if linha[1] != '-':
                    dado.append(float(linha[1]))
                else:
                    dado.append(float(0))
                if not k:
                    time[n] = float(linha[0])
                if len(dias_calmos) == 1 and linha[2] != '-':
                    tec_err[n] = float(linha[2])
            n = n+1
        dados.append(dado)
        k = True
    if len(dias_calmos) == 1:
        tec_uni = np.array(dados[0])
        dif = np.abs(tec_uni.shape[0] - time.shape[0])
        # Método numpy.pad() para adicionar zeros à segunda array
        tec_uni = np.pad(tec_uni, (0, dif), mode='constant')
        return tec_uni, time, tec_err
    min = len(dados[0])
    for d in dados:
        if min > len(d):
            min = len(d)
    for i in range(min):
        valores = []
        for l in dados:
            if float(l[i]) != 0:
                valores.append(float(l[i]))
        tec[i] = np.mean(valores)
        desvio = np.std(valores, ddof=1)
        tec_err[i] = desvio
        # tec = correcao_tec_med(tec)
    dif = tec.shape[0] - time.shape[0]
    # Método numpy.pad() para adicionar zeros à segunda array
    tec = np.pad(tec, (0, dif), mode='constant')
    return tec, time, tec_err


def Lat_max_e_min(dados: list):
    '''
    :param dados: Dados de todas as estações.
    :return: Latitude máxima e mínima, respectivamnte.
    '''
    max_l = []
    min_l = []
    for i in range(1, 33):
        if dados[i][2]:
            max_l.append(max(dados[i][2]))
            min_l.append(min(dados[i][2]))
    return max(max_l), min(min_l)


def Arquivos_cmn(estacoes: list, dia_i, dia_f, mes, ano=2023):
    '''
    :param estacoes: Lista com os nomes de todas as estações.
    :param dia_i: Dia inicial.
    :param dia_f: Dia final.
    :param mes: Mes (1-12).
    :param ano: Ano (padrão 2023).
    :return: Nome do arquivo no padrão desejado.
    '''
    x = []
    mes = ('%02d' % mes)
    for y in estacoes:
        y = y.lower()
        for d in range(dia_i, dia_f+1):
            d1 = ('%03d' % d)
            d2 = ('%02d' % d)
            x.append(f'{y}{d1}-{ano}-{mes}-{d2}.Cmn')
    return x


def Tec_vs_tec_medio(estacoes: list, dia_i: int, dia_f: int, dias_calmos: list, mes, ano=2023, fase_principal = None, path="imagens") -> nan:
    '''
    :param estacoes: Lista com os nomes de todas as estações.
    :param dia_i: Dia inicial.
    :param dia_f: Dia final.
    :param dias_calmos: Lista com os dias calmos (coloque dados do tipo int).
    :param mes: Mes (1-12).
    :param ano: Ano.
    :param fase_principal: Lista com as datas de inicio da fase principal e de fim, bem como o fim da
           fase de recuperção. Da forma [dia de inicio, hora, dia final, hora, dia de termino da fase de recupera, hora]
           Ex: [14, 12, 14, 23, 17, 23], começa dia 14, às 12hrs e termina dia 14 às 23hrs, a fase de
           recuperação vai até dia 17 às 23hrs.
    :param path: Caminho para pasta onde se deseja salvar.
    :return: Imagem.
    '''
    plt.figure(dpi=500) # Qualidade da figura.
    plt.suptitle(colored('Avarege Value', 'red'))
    subplots_adjust(hspace=0.000, wspace=0.000) # Espaçamento vertical e horizontal, respectivamente.
    number_of_subplots = len(estacoes)
    colunas = dia_f - dia_i + 1
    xg = (colunas) * (len(estacoes))
    yg = (colunas) * (len(estacoes)-1)
    v = 0

    for estacao in estacoes:
        med, time, med_err = Tec_medio(estacao, dias_calmos, mes, ano)
        for i in range(dia_i, dia_f+1):
            v = v + 1
            n = [i]
            y1, x1, y1_err = Tec_medio(estacao, n, mes, ano=ano)
            ax1 = subplot(number_of_subplots, colunas, v)
            ax1.scatter(x1, y1, s=0.01, c='red', label='TEC')
            ax1.scatter(x1, med, s=0.01, c='green',  marker='.', label='Avarege Value')
            ax1.fill_between(time, med - med_err, med + med_err, alpha=0.2, color='black')

            if fase_principal != None:
                limits = np.array(fase_principal, dtype=float).reshape(3, 2)
                # Colorir fase principal
                if limits[0][0] <= int(i) and int(i) <= limits[1][0]:
                    if limits[0][0] == limits[1][0]:
                        ax1.axvspan(limits[0][1], limits[1][1], alpha=0.2, color='red')
                    elif int(i) == limits[0][0]:
                        ax1.axvspan(limits[0][1], 24, alpha=0.2, color='red')
                    elif int(i) == limits[1][0]:
                        ax1.axvspan(0, limits[1][1], alpha=0.2, color='red')
                # Colorir fase de recuperação
                if limits[1][0] <= int(i) and int(i) <= limits[2][0]:
                    if int(i) == limits[1][0]:
                        ax1.axvspan(limits[1][1], 24, alpha=0.2, color='yellow')
                    elif int(i) == limits[2][0]:
                        ax1.axvspan(0, limits[2][1], alpha=0.2, color='yellow')
                    else:
                        ax1.axvspan(0, 24, alpha=0.2, color='yellow')

            '''Ajustar conforme a necessidade de cada gráfico (*)'''
            ax1.set_xlim(0, 24)
            ax1.set_ylim(0, 55)
            ax1.set_xticks(range(0, 25, 8))
            ax1.set_yticks(range(0, 56, 20))
            if v <= colunas:
                i = '%02d' % i
                ax1.set_title(f'{i} {meses[mes - 1]}')
            if v % colunas == 1:
                ax1.set_ylabel(estacao.upper())
                if v == xg - colunas + 1:
                    ax1.set_yticks(range(0, 46, 15)) # (*)
                else:
                    ax1.set_yticks(range(15, 46, 15)) # (*)
            if v % colunas != 1:
                plt.gca().axes.get_yaxis().set_visible(False)
            if v <= yg or xg < v:
                ax1.set_xticks([])
            elif v == xg - colunas + 1:
                ax1.set_xticks(range(0, 25, 8)) # (*)
            else:
                ax1.set_xticks(range(8, 25, 8)) # (*)

    plt.text(0.03, 0.4, 'VTEC (TECU)', rotation=90, transform=plt.gcf().transFigure)
    plt.text(0.5, 0.03, 'UT (hrs)', transform=plt.gcf().transFigure)
    plt.savefig(f'{path}/Tec_tecmed.png', dpi=300) # Regular a resolução com o dpi.
    #plt.show()

def Vtec_vs_t(estacao: list, dia, mes, ano=2023):
    '''
    :param estacao: Lista com uma estação.
    :param dia: Dia.
    :param mes: Mes.
    :param ano: Ano.
    :return: Gráfico do Vtec vs tempo.
    '''
    arquivo = Arquivos_cmn(estacao, dia, dia, mes)
    ler = open(f'Output_GPS/{arquivo[0]}', 'r')
    for i in range(2):
        ler.readline()
    c = ler.readline()
    c = c.split()
    for i in range(2):
        ler.readline()
    coordenadas = [c[0], c[1], c[2]]
    dados = [[[] for _ in range(3)] for _ in
    range(33)]  # numero do satelite(32 satelites), tempo e Vtec para cada satelite
    elev = int(20)  # int(input('Elevacao minima:'))
    for linha in ler:
        if linha:
            linha = linha.split()
            '''Tempo negativo = ausência de dados. Elevação mínima do satélite'''
            if float(linha[1]) >= 0 and float(linha[4]) >= elev and linha[1] and linha[8] and linha[5]:
                dados[int(linha[2])][0].append(float(linha[1]))
                dados[int(linha[2])][1].append(float(linha[8]))
                dados[int(linha[2])][2].append(float(linha[5]))
    '''Latitudes máxima e mínima'''
    x1, x2 = Lat_max_e_min(dados)
    print(x1,x2)
    '''--------------------------------------'''
    n = [dia]
    tec_med, time, tec_err = Tec_medio(estacao[0], n, 1, ano=ano)
    '''Plotar 'Vtec vs tempo' para todos os satélites'''
    #plt.figure(dpi=500)
    for i in range(1, 33):
        if dados[i][2]:
            plt.scatter(dados[i][0], dados[i][1], s=0.5, marker='.', c=dados[i][2], vmin=x2, vmax=x1, cmap='gist_ncar')
    plt.colorbar(label='Latitude', boundaries=np.linspace(x2, x1, 1000))
    plt.scatter(time, tec_med, s=0.5, marker='.', c='black')
    plt.xlim(0, 24)
    plt.xticks(range(0, 25, 4))
    plt.yticks(range(0, 56, 5))
    plt.fill_between(time, tec_med - tec_err, tec_med + tec_err, alpha=0.1, color='black')
    plt.xlabel('UT (hrs)')
    plt.ylabel('TEC units')
    date = str(dt.datetime.today())
    plt.text(0, 50, f'Date:{arquivo[0][8:18]} (Elev Mask {elev} deg)')
    plt.text(0, 52, f'Lat(deg):{coordenadas[0]} Lon(deg):{coordenadas[1]} Alt(m):{coordenadas[2]}')
    plt.text(0, 54, f'Station: {arquivo[0][0:4].upper()}')
    plt.tight_layout()
    plt.savefig(f'imagens/Vtec_vs_t.png', dpi=300)
    # plt.show()


def ROT(estacoes: list, dias: list, mes: int, ano=2023, path="imagens") -> nan:
    '''
    :param estacoes: Lista com todas as estações
    :param dias: Lista com todos os dias
    :param mes: Mes (1-12)
    :param path: Caminho para pasta onde se deseja salvar.
    :return: ROT para cada estação.
    '''
    subplots_adjust(hspace=0.000, wspace=0.000) # Espaçamento vertical e horizontal, respectivamente.
    number_of_subplots = len(estacoes)
    x1 = (len(dias))*(len(estacoes))
    x2 = (len(dias))*(len(estacoes)-1)
    colunas = len(dias)
    v = 0
    for estacao in estacoes:
        for dia in dias:
            dados = Dados(estacao, dia, mes, ano=ano)
            v = v + 1
            ax1 = subplot(number_of_subplots, colunas, v)
            for i in range(1, 33):
                x = np.array(dados[i][0])
                y = np.array(dados[i][1])
                '''Modificar conforme a necessidade (*)'''
                if len(x) == len(y) and len(x) > 0:
                    rot = Deriv_Ord1(x, y, i)
                    ax1.set_yticks([])
                    ax1.set_xlim(0, 24) #(*)
                    ax1.set_ylim(0, 1800) #(*)
                    if v <= colunas:
                        dia = '%02d' % int(dia)
                        ax1.set_title(f'{dia} {meses[mes - 1]}')
                    if v % colunas == 1:
                        ax1.set_ylabel(estacao.upper())
                    if v <= x2 or x1 < v:
                        ax1.set_xticks([])
                    elif v == x1 - colunas + 1:
                        ax1.set_xticks(range(0, 25, 6)) #(*)
                    else:
                        ax1.set_xticks(range(6, 25, 6)) #(*)
                    ax1.scatter(x, rot, s=0.01, c='black')
    plt.text(0.04, 0.4, 'ROT (TECU)', rotation=90, transform=plt.gcf().transFigure)
    plt.text(0.5, 0.03, 'UT (hrs)', transform=plt.gcf().transFigure)
    plt.savefig(f'{path}/ROT_13_18.png', dpi=1000)
    # plt.show()


def ROTi(estacoes: list, dia_i: int, dia_f: int, mes: int, ano=2022, fase_principal = None, path="imagens") -> nan:
    '''
    :param estacoes:
    :param dia_i:
    :param dia_f:
    :param mes:
    :param fase_principal: Lista com as datas de inicio da fase principal e de fim, bem como o fim da
           fase de recuperção. Da forma [dia de inicio, hora, dia final, hora, dia de termino da fase de recupera, hora]
           Ex: [14, 12, 14, 23, 17, 23], começa dia 14, às 12hrs e termina dia 14 às 23hrs, a fase de
           recuperação vai até dia 17 às 23hrs.
    :param path: Caminho para pasta onde se deseja salvar.
    :return:
    '''
    #plt.suptitle('ROTi')
    #plt.figure(figsize=(10.8, 10.8))
    subplots_adjust(hspace=0.000, wspace=0.000)
    number_of_subplots = len(estacoes)
    colunas = dia_f - dia_i + 1
    v = 0
    x1 = number_of_subplots * colunas
    x2 = (number_of_subplots - 1) * colunas
    if fase_principal != None:
        limits = np.array(fase_principal, dtype= float).reshape(3, 2)

    for estacao in estacoes:
        for dia in range(dia_i, dia_f + 1):
            v = v + 1
            dados = Dados(estacao, dia, mes, ano=ano)
            ax1 = subplot(number_of_subplots, colunas, v)
            if v <= colunas:
                dia = '%02d' % int(dia)
                ax1.set_title(f"{dia} {meses[mes-1]}")
            for i, cor in zip(range(0, 32), cores):
                #ax1 = subplot(number_of_subplots, colunas, v)
                x = np.array(dados[i][0])
                y = np.array(dados[i][1])
                if len(x) == len(y) and len(x) > 0:
                    data = Deriv_Ord1(x, y, 0)
                    num_groups = len(data) // 20
                    data = data[:num_groups * 20] / 60
                    x = x[:num_groups * 20]
                    # Dividindo em grupos de 20 pontos (5 min)
                    groups = [data[i:i + 20] for i in range(0, len(data), 20)]
                    t = [x[i:i + 20] for i in range(0, len(x), 20)]
                    # Calculando o desvio padrão de cada grupo de 20 pontos
                    std_devs = []
                    for group in groups:
                        std_dev = np.std(group)
                        std_devs.append(std_dev)
                    time_roti = []
                    for k in t:
                        time_roti.append(np.mean(k))
                    #ax1.scatter(range(1, len(std_devs)+1), std_devs, s=0.1, marker='.', facecolors='red')
                    #ax1.set_yticks([])
                    #.scatter(time_roti, std_devs, s=1, alpha=0.5, marker='.', c=cor)
                    ax1.scatter(time_roti, std_devs, s=1, alpha=0.9, c=cor)
            ax1.set_xticks([])
            ax1.set_yticks([])
            ax1.set_xlim(0, 24.1)
            ax1.set_ylim(0, 1)
            '''Modificar conforme a necessidade (*)'''
            # Colorir fase principal
            if fase_principal != None:
                if limits[0][0] <= int(dia) and int(dia) <= limits[1][0]:
                    if limits[0][0] == limits[1][0]:
                        ax1.axvspan(limits[0][1], limits[1][1], alpha=0.2, color='red') #(*)
                    elif int(dia) == limits[0][0]:
                        ax1.axvspan(limits[0][1], 24, alpha=0.2, color='red') #(*)
                    elif int(dia) == limits[1][0]:
                        ax1.axvspan(0, limits[1][1], alpha=0.2, color='red') #(*)
                # Colorir fase de recuperação
                if limits[1][0] <= int(dia) and int(dia) <= limits[2][0]:
                    if int(dia) == limits[1][0]:
                        ax1.axvspan(limits[1][1], 24, alpha=0.2, color='yellow') #(*)
                    elif int(dia) == limits[2][0]:
                        ax1.axvspan(0, limits[2][1], alpha=0.2, color='yellow') #(*)
                    else:
                        ax1.axvspan(0, 24, alpha=0.2, color='yellow') #(*)

            if v % colunas == 1:
                ax1.set_ylabel(estacao.upper())
                if v == 1:
                    ax1.set_yticks(np.linspace(0, 1, 5)) #(*)
                else:
                    ax1.set_yticks(np.linspace(0, 0.75, 4)) #(*)
            if x2 < v and v <= x1:
                if v == x2 + 1:
                    ax1.set_xticks(range(0, 25, 6)) #(*)
                else:
                    ax1.set_xticks(range(6, 25, 6)) #(*)
    plt.text(0.01, 0.4, 'ROTI (TECU/mim)', rotation=90, transform=plt.gcf().transFigure)
    plt.text(0.5, 0.03, 'UT (hrs)', transform=plt.gcf().transFigure)
    plt.savefig(f'imagens/ROTi_{dia_i}_{dia_f}.png', dpi=1000)
    #plt.show()


def s4(estacoes: list, dia_i: int, dia_f: int, mes: int) -> nan:
    '''
    :param estacoes: Lista com todas as estações
    :param dia_i: Dia inicial
    :param dia_f: Dia final
    :param mes: Mes
    :return: S4 para cada estação no intervalo de dias especificado.
    '''
    subplots_adjust(hspace=0.000, wspace=0.000) # Espaço horizontal e vertical, respectivamente.
    number_of_subplots = len(estacoes)
    colunas = dia_f - dia_i + 1
    v = 0
    x1 = number_of_subplots * colunas
    x2 = (number_of_subplots - 1) * colunas
    for estacao in estacoes:
        '''Modificar conforme a necessidade (*)'''
        for dia in range(dia_i, dia_f+1):
            v = v + 1
            _, S4 = Dados(estacao, dia, mes, s4=True)
            ax1 = subplot(number_of_subplots, colunas, v)
            if v <= colunas:
                dia = '%02d' % int(dia)
                ax1.set_title(f"{dia} {meses[mes - 1]}")
            for i, cor in zip(range(0, 32), cores):
                #ax1 = subplot(number_of_subplots, colunas, v)
                x = np.array(S4[i][0])
                y = np.array(S4[i][1])
                ax1.scatter(x, y, s=1, alpha=0.9, c=cor)
            ax1.set_xticks([]) #(*)
            ax1.set_yticks([]) #(*)
            ax1.set_xlim(0, 24.1) #(*)
            ax1.set_ylim(0, 2) #(*)
            if v % colunas == 1:
                ax1.set_ylabel(estacao.upper())
                if v == 1:
                    ax1.set_yticks(np.linspace(0, 2, 5)) #(*)
                else:
                    ax1.set_yticks(np.linspace(0, 1.75, 5)) #(*)
            if x2 < v and v <= x1:
                if v == x2 + 1:
                    ax1.set_xticks(range(0, 25, 3)) #(*)
                else:
                    ax1.set_xticks(range(3, 25, 3)) #(*)
    plt.text(0.01, 0.5, 'S4', rotation=90, transform=plt.gcf().transFigure)
    plt.text(0.5, 0.03, 'UT (hrs)', transform=plt.gcf().transFigure)
    plt.savefig(f'imagens/S4_{dia_i}_{dia_f}.png', dpi=1000)

def Dados(estacao: str, dia: int, mes: int, ano=2022, s4=False) -> list:
    '''
    :param estacao: Sigla da estação, em minusculo.
    :param dia: Dia dos dados em questão
    :param mes: Mes
    :param s4: Se desejar o S4, coloque s4=True (se o S4 estiver disponível).
    :return: Matriz com todos os dados para cada satélite. Vtec e S4 OU somente o Vtec
    '''
    l = [estacao]
    arquivo = Arquivos_cmn(l, dia, dia, mes, ano=ano)
    ler = open(f'Output_GPS/{arquivo[0]}', 'r') # Modifique essa linha, coloque o caminho para sua pasta de dados.
    for i in range(2):
        ler.readline()
    c = ler.readline()
    c = c.split()
    for i in range(2):
        ler.readline()
    coordenadas = [c[0], c[1], c[2]]
    dados = [[[] for _ in range(3)] for _ in range(33)]  # numero do satelite(32 satelites), tempo e Vtec
    elev = int(15)  # Elevação mínima. Modifique, caso necessário.
    if s4 == False:
        for linha in ler:
            if linha:
                linha = linha.split()
                '''Tempo negativo == ausência de dados. Elevação mínima do satélite'''
                if float(linha[1]) >= 0 and float(linha[4]) >= elev and linha[1] and linha[8] and linha[5]:
                    dados[int(linha[2])][0].append(float(linha[1]))
                    dados[int(linha[2])][1].append(float(linha[8]))
                    dados[int(linha[2])][2].append(float(linha[5]))
        return dados
    else:
        s4 = [[[] for _ in range(2)] for _ in range(33)] # tempo e s4
        for linha in ler:
            if linha:
                linha = linha.split()
                '''Tempo negativo = ausência de dados. Elevação mínima do satélite'''
                if float(linha[1]) >= 0 and float(linha[4]) >= elev and linha[1] and linha[8] and linha[5]:
                    dados[int(linha[2])][0].append(float(linha[1]))
                    dados[int(linha[2])][1].append(float(linha[8]))
                    dados[int(linha[2])][2].append(float(linha[5]))
                    if float(linha[9]) > 0:
                        s4[int_(linha[2])][0].append(float(linha[1]))
                        s4[int_(linha[2])][1].append(float(linha[9]))
        return dados, s4



def Graf_contorno(estacoes: list, dia: int, mes: int, ano=2023, path1="Output_GPS", path2="imagens") -> nan:
    '''
    :param estacoes: Lista com todas as estações.
    :param dia: Dia.
    :param mes: Mes (1-12).
    :param path1: Caminho para a pasta dos dados.
    :param path2: Caminho para onde se dejesa salvar
    :return: Gráfico de contorno (interpolação).
    '''
    a = []
    first = True
    for estacao in estacoes:
        l = [estacao]
        arquivo = Arquivos_cmn(l, dia, dia, mes, ano=ano)
        ler = open(f'{path1}/{arquivo[0]}', 'r')
        for i in range(2):
            ler.readline()
        c = ler.readline()
        c = c.split()
        for i in range(2):
            ler.readline()
        coordenadas = [c[0], c[1], c[2]]
        a.append(float(coordenadas[0]))
        tec_med, time, _ = Tec_medio(estacao, [dia], mes, ano=ano)
        tec_med = tec_med[::20]
        if first:
            M = np.reshape(tec_med, (-1, 1))
            x = time[::20]
            first = False
        else:
            M = np.hstack((M, tec_med.reshape(-1, 1)))

    lats = np.array(a)
    points = (x, lats)
    #plt.scatter(*np.meshgrid(*points, indexing='ij'), c=M)
    n = 60 # Resolução, cuidado pois o processo pode ficar muito demorado.
    xi = np.linspace(1, 23.5,  n)
    yi = np.linspace(min(lats), max(lats), n)
    for i in range(n):
        for k in range(n):
            point = np.array([xi[i], yi[k]])
            plt.scatter(xi[i], yi[k], c=interpn(points, M, point), vmax=40, vmin=0, cmap="plasma")
    plt.xlabel("Time (UT)")
    plt.ylabel("Latitude")
    char = plt.colorbar()
    char.set_label('VTEC (TECU)')
    plt.grid(True)
    plt.savefig(f"{path2}/graf_contorno")




def indices(path1, dia_i, dia_f,  path2="imagens") -> nan:
    '''
    :param path1: Caminho para o arquivo com todos os dados
    :param dia_i: Dia inicial
    :param dia_f: Dia final
    :param path2: Caminho para a pasta onde se deseja salvar.
    :return:
    '''
    arq = open(path1)
    # Dias, dados, hora
    '''
            FORMAT OF THE SUBSETTED FILE
            
            ITEMS                      FORMAT   
             
         1 YEAR                          I4        
         2 DOY                           I4        
         3 Hour                          I3        
         4 Scalar B, nT                  F6.1      
         5 BZ, nT (GSM)                  F6.1      
         6 SW Proton Density, N/cm^3     F6.1      
         7 SW Plasma Speed, km/s         F6.0            
         8 Kp index                      I3        
         9 Dst-index, nT                 I6   
    '''
    shape = (dia_f-dia_i+1, 7, 24) # Quantidade de dias, quantidade de dados, hora.
    dados = np.ndarray(shape)
    for line in arq:
        d = line.split()
        day = int(d[1]) - 150
        hour = int(d[2])
        '''Adicione ou retire dados caso necessário.'''
        dados[day][0][hour] = float(d[3])
        dados[day][1][hour] = float(d[4])
        dados[day][2][hour] = float(d[5])
        dados[day][3][hour] = float(d[6])
        dados[day][4][hour] = float(d[7])
        dados[day][5][hour] = float(d[8])
        #dados[day][6][hour] = float(d[9])

    '''Dados'''
    B = []
    Bz = []
    Np = []
    Vp = []
    #E = []
    Kp = []
    Dst = []
    t = []
    '''Se atente a ordem dos dados. Modifique caso necessário.'''
    for j in range(0, dia_f-dia_i+ 1):
        B.extend(dados[j][0])
        Bz.extend(dados[j][1])
        Np.extend(dados[j][2])
        Vp.extend(dados[j][3])
        #E.extend(dados[j][4])
        Kp.extend(dados[j][4])
        Dst.extend(dados[j][5])
        t.extend(range(0, 24, 4))

    indices = [B, Bz, Np, Vp, Kp, Dst]
    fig, ax = plt.subplots(6, 1)
    fig.set_size_inches(10.80, 10.80) # Dimensões da imagem. Modifique caso necessário.
    fig.subplots_adjust(hspace=0.000, wspace=0.000)
    for v, i in zip(indices, range(6)):
        if i == 5:
            ax[i].bar(range(0, 24 * (dia_f - dia_i + 1)), v)
        else:
            ax[i].plot(range(0, 24 * (dia_f - dia_i + 1)), v)
        ymax = max(v)
        ymin = min(v)

        '''Modifique os limites de cada gráfico.'''
        '''if i == 0:
            y_indx = np.around(np.linspace(0, 20, 5), 1)
        elif i == 1:
            y_indx = np.around(np.linspace(-20, 5, 6), 1)
        elif i == 2:
            y_indx = np.around(np.linspace(-2.5, 7.5, 5), 1)
        elif i == 3:
            y_indx = np.around(np.linspace(0, 30, 4), 1)
        elif i == 4:
            y_indx = np.around(np.linspace(400, 600, 5), 1)
        elif i == 5:
            y_indx = np.around(np.linspace(0, 80, 5), 1)
        elif i == 6:
            y_indx = np.around(np.linspace(-180, 30, 8), 1)
        else:
            y_indx = np.around(np.linspace(ymin, ymax, 4), 1)
        '''
        #ax[i].set_yticks(y_indx)
        ax[i].set_xticks(range(0, 24 * (dia_f - dia_i + 1), 4), t)
        ax[i].set_xlim(0, 24 * (dia_f - dia_i + 1))
        ax[i].grid(True)
    ax[0].set_ylabel("B, nT")
    ax[1].set_ylabel("Bz, nT")
    #ax[2].set_ylabel("E, mV/m")
    ax[2].set_ylabel("Np, cm^-3")
    ax[3].set_ylabel("Vp, km/s")
    ax[4].set_ylabel("Kp")
    ax[5].set_ylabel("Dst, nT")
    plt.suptitle(f'Days 05/30/2023-05/31/2023') # Legenda
    plt.text(0.5, 0.04, 'UT (hrs)', transform=plt.gcf().transFigure)
    plt.tight_layout()
    fig.align_labels()
    plt.savefig(f"{path2}/indices")




