import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

# Coloque aqui a cidade que deseja buscar as informações
local = 'Maragogi'

options = Options()
# definindo o tamanho da janela
options.add_argument('window-size=400,800')

navegador = webdriver.Chrome(options=options)
navegador.delete_all_cookies()

navegador.get('https://www.tripadvisor.com.br')

sleep(2)

cookies = navegador.find_element(By.ID, 'onetrust-accept-btn-handler')
cookies.click()

sleep(2)

input_place = navegador.find_element(By.TAG_NAME, 'input')
input_place.send_keys(local)
sleep(2)

buscar = navegador.find_element(By.CSS_SELECTOR, 'a > div > svg')
buscar.click()

sleep(3)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

# Trazendo informações sobre o local
sobre = site.find(
    'div', attrs={'data-test-target': 'geo-description'}).findAll('div')
sobre = [detalhe.text for detalhe in sobre]
sobre = "Sobre " + local + ": " + sobre[1]

# print(sobre)

sleep(3)

atracoes = navegador.find_element(
    By.XPATH, '//*[@id="lithium-root"]/main/div[6]/div[1]/div[2]/div[1]/div/div[1]/a')
atracoes.click()

sleep(3)


page_atracoes = navegador.page_source

site2 = BeautifulSoup(page_atracoes, 'html.parser')

dados_local = []
dados_local.append(sobre)

sleep(3)

dados_local.append("As 10 melhores atrações: ")
detalheAtracoes = site2.findAll(
    'span', attrs={'name': 'title'})


for detalheAtracao in range(10):
    detalheAtracao = [listaAtracoes.text for listaAtracoes in detalheAtracoes]


for i in range(10):
    dados_local.append(detalheAtracao[i])


# Exportando os dados para um arquivo
dados = pd.DataFrame(dados_local)
dados.to_json('sobreLocal.json', index=False)
