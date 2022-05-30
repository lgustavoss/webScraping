import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

# Coloque aqui a cidade que deseja buscar as informações
local = 'Maceio'

options = Options()
# nao mostrar o navegador
# options.add_argument('--headless')
options.add_argument('window-size=400,800')

navegador = webdriver.Chrome(options=options)
navegador.delete_all_cookies()

navegador.get('https://www.tripadvisor.com.br')

sleep(1)

cookies = navegador.find_element(By.ID, 'onetrust-accept-btn-handler')
cookies.click()

sleep(1)

input_place = navegador.find_element(By.TAG_NAME, 'input')
input_place.send_keys(local)
sleep(1)

buscar = navegador.find_element(By.CSS_SELECTOR, 'a > div > svg')
buscar.click()

sleep(3)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

# Trazendo informações sobre o local
sobre = site.find(
    'div', attrs={'data-test-target': 'geo-description'}).findAll('div')
sobre = [detalhe.text for detalhe in sobre]


# Exportando os dados para um arquivo
dados = pd.DataFrame(sobre)
dados.to_csv('sobreLocal.txt')
