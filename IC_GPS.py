import F_GPS
'''----------------------------------------------------------------------'''
# Belém, , Marabá, Palmas, Brasília, São José dos Campos, Porto Alegre
linha_vertical = ["bele", "maba", "topl", "braz", "sjsp", "poal"]
linha1 = ['bele', 'mabb', 'pitn', 'rnpf', 'peaf', 'perc']
linha2 = ['naus', 'paar', 'topl', 'babr', 'babj', 'bavc']
linha3 = ['amtg', 'pove', 'cuib', 'goja', 'spja', 'sjsp']
estacoes1 = ['aps1', 'impz', 'braz', 'sjsp', 'scca', 'poal']
estacoes2 = ['azul', 'sico', 'sarm', 'unpa', 'autf', 'palm']
estacoes = linha3
fase_principal = [14, 12, 14, 23, 17, 23]
F_GPS.Graf_contorno(estacoes, dia=16, mes=1, ano=2022)
F_GPS.ROT(['ykro'], [30, 31], 5)
F_GPS.ROTi(['ykro'], 30, 31, 5)  # ok
F_GPS.s4(['ykro'], 30, 31, 5)
dias_calmos = [5, 6, 7, 10, 11, 12, 13, 24]
F_GPS.Tec_vs_tec_medio(estacoes, 13, 18, dias_calmos, 1, ano=2022, fase_principal=fase_principal)
F_GPS.indices("dados/dados30_31Maio2023.txt", 30, 31)

