import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Defina o caminho para o executável do ChromeDriver
chrome_driver_path = '/caminho/para/seu/chromedriver'

# Defina o diretório do ChromeDriver no PATH
os.environ["PATH"] += os.pathsep + chrome_driver_path

# Inicialize o driver do Chrome sem especificar o caminho do ChromeDriver
driver = webdriver.Chrome()

# Definindo a URL do Airbnb em Campos do Jordão
url = "https://www.booking.com/searchresults.pt-br.html?ss=Campos+do+Jord%C3%A3o%2C+Estado+de+S%C3%A3o+Paulo%2C+Brasil&label=yho748jc-1DCAEoggI46AdILVgDaCCIAQGYAS24ARnIAQzYAQPoAQH4AQKIAgGoAgO4Au7FkrAGwAIB0gIkOTI1ZDc2MGQtYWRjZC00YzYwLWE4NjUtMGE0MmRkYTRhOGEy2AIE4AIB&aid=397646&lang=pt-br&sb=1&src_elem=sb&src=index&dest_id=-634196&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=xb&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=a9d5a0b753ea0298&ac_meta=GhBhOWQ1YTBiNzUzZWEwMjk4IAAoATICeGI6CWNhbXBvcyBkb0AASgBQAA%3D%3D&checkin=2024-03-27&checkout=2024-03-28&group_adults=2&no_rooms=1&group_children=0"

# Acessando a página do Airbnb
driver.get(url)

# Esperando um tempo para a página carregar completamente
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.XPATH, '//title')))

# Encontrando todos os elementos de preços de imóveis na página usando XPath
prices_elements = driver.find_elements(By.XPATH, '//span[@class="f6431b446c fbfd7c1165 e84eb96b1f"]')
name_elements = driver.find_elements(By.XPATH, '//span[@class="f6431b446c a15b38c233"]')
room_elements = driver.find_elements(By.XPATH, '//h3[@class="f343f1e8f0 b6288ebfe2"]')
rating_elements = driver.find_elements(By.XPATH, '//div[@class="a48d4ed374 c7d21728fd"]')

# Inicializando listas vazias para armazenar as informações
prices = []
names = []
rooms = []
ratings = []

# Iterando sobre cada elemento e extraindo as informações
for i in range(len(prices_elements)):
    price = prices_elements[i].text.replace('R$&nbsp;', '')
    name = name_elements[i].text
    room = room_elements[i].text
    rating = rating_elements[i].text.replace('Nota ', '') if rating_elements else ''

    # Adicionar as informações às listas correspondentes
    prices.append(price)
    names.append(name)
    rooms.append(room)
    ratings.append(rating)

# Fechando o navegador
driver.quit()

# Verificando se há dados antes de salvar no CSV
if prices:
    # Criar um DataFrame pandas com as informações
    data = {'Nome do Hotel': names, 'Nome do Quarto': rooms, 'Preço': prices, 'Nota': ratings}
    df = pd.DataFrame(data)

    # Salvar o DataFrame em um arquivo CSV
    df.to_csv('informacoes_airbnb.csv', index=False, encoding='utf-8')

    print("Informações salvas em informacoes_airbnb.csv")
else:
    print("Nenhuma informação encontrada para salvar.")
