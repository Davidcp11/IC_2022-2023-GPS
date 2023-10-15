import requests
import os


def baixar_arquivos(url, endereco):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('A solicitação GET falhou: ', e)
        resposta = None
    if resposta:
        # Se a solicitação for bem-sucedida, execute o código aqui
        if resposta.status_code == requests.codes.OK:
            with open(endereco, 'wb') as novo_arquivo:
                novo_arquivo.write(resposta.content)
            print(f"Donwload finalizado. Salvo em : {endereco}")
    else:
        # Se a solicitação falhar, execute o código aqui
        print('Não foi possível obter uma resposta do servidor.')


# Local de armazenamento dos dados baixados
OUTPUT_DIR = 'Input_GPS'
stations = [
    'alar',
    'alma',
    'amco',
    'amcr',
    'amha',
    'ampt',
    'amte',
    'amtg',
    'amua',
    'aplj',
    'apma',
    'aps1',
    'babj',
    'babr',
    'bail',
    'bait',
    'bapa',
    'batf',
    'bavc',
    'bele',
    'bepa',
    'braz',
    'brft',
    'ceeu',
    'cefe',
    'ceft',
    'cesb',
    'chpi',
    'coru',
    'crat',
    'cruz',
    'cuib',
    'each',
    'eesc',
    'esnv',
    'gogy',
    'goja',
    'gour',
    'gva1',
    'ifsc',
    'ilha',
    'imbt',
    'itai',
    'maba',
    'mabb',
    'mabs',
    'mgbh',
    'mgin',
    'mgjf',
    'mgjp',
    'mgla',
    'mgmc',
    'mgmt',
    'mgrp',
    'mgto',
    'mgub',
    'mgv1',
    'msaq',
    'msbl',
    'msdr',
    'msgr',
    'msjr',
    'msmj',
    'msmn',
    'msnv',
    'mspm',
    'mspp',
    'mtca',
    'mtcn',
    'mtga',
    'mtji',
    'mtla',
    'mtnx',
    'mtsc',
    'naus',
    'neia',
    'onrj',
    'paar',
    'pait',
    'pasm',
    'pbcg',
    'pbjp',
    'pbpt',
    'peaf',
    'pepe',
    'perc',
    'picr',
    'pifl',
    'pisr',
    'pitn',
    'poal',
    'poli',
    'pove',
    'ppte',
    'prgu',
    'prma',
    'prur',
    'riob',
    'rjcg',
    'rjni',
    'rjva',
    'rnmo',
    'rnna',
    'rnpf',
    'roji',
    'rosa',
    'rsal',
    'rscl',
    'rspe',
    'rspf',
    'rssl',
    'saga',
    'salu',
    'savo',
    'scaq',
    'scca',
    'scch',
    'scfl',
    'scla',
    'seaj',
    'sjrp',
    'sjsp',
    'smar',
    'spar',
    'spbo',
    'spbp',
    'spc1',
    'spdr',
    'spfe',
    'spfr',
    'spja',
    'spli',
    'spor',
    'sps1',
    'sptu',
    'ssa1',
    'togu',
    'topl',
    'uba1',
    'ube1',
    'ufpr',
    'vico'
]
# Essa parte depende de cada caso. Se precisar, mude.
for i in range(1, 32):
    numb = ('%03d' % i)
    for sta in stations:
        # Endereço dos dados a serem baixados. Especifique o tipo de dado.
        BASE_URL = f'http://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/2022/{numb}/{sta}{numb}1.zip'
        nome_arquivo = os.path.join(OUTPUT_DIR, f'station_{sta}{numb}1.zip')
        baixar_arquivos(BASE_URL.format(sta), nome_arquivo)
