import selenium
import lxml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()
options.headless = False  # Observar a operação.

navegador = webdriver.Chrome(options=options)

link = "https://urs.earthdata.nasa.gov/home"

navegador.get(url=link)
sleep(3)

inputUsuario = navegador.find_element(by=By.ID, value="username")
inputUsuario.send_keys("daviddcp")
inputSenha = navegador.find_element(by=By.ID, value="password")
inputSenha.send_keys("Houston8#8")

buttonLogin = navegador.find_element(by=By.NAME, value="commit")
buttonLogin.click()
sleep(3)

link_baixar = "https://cddis.nasa.gov/archive/gnss/data/daily/"
navegador.get(url=link_baixar)
sleep(5)
run = True
stations = ["sch2"] #, "hnpt", "rdsd", "falk"]
types = ["22d", "22n", "22g", "22m", "22l"]
# Essa parte depende de cada caso. Se precisar, mude.
for i in range(1, 5):
    numb = ('%03d' % i)
    for sta in stations:
        for type in types:
            # Endereço dos dados a serem baixados. Especifique o tipo do dado.
            BASE_URL = f'https://cddis.nasa.gov/archive/gnss/data/daily/2022/{numb}/{type}/{sta}{numb}0.{type}.gz'
            navegador.get(url=BASE_URL)
            sleep(2)

