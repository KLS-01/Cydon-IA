from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

# Inizializza il driver del browser (Chrome) una sola volta
driver = webdriver.Chrome()

def accept_cookie():
    try:
        # Aspetta fino a quando l'elemento HTML per i cookie diventa cliccabile
        consent_cookie_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button"))
        )
        consent_cookie_button.click()
    except Exception as e:
        print("Errore durante l'attesa o clic del pulsante dei cookie alla pagina:", page)

def download_file(href):
    linkLog = "https://replay.pokemonshowdown.com/" + href + ".log"
    log_response = requests.get(linkLog)
    # Controlla se la stringa inizia con "smogtours-" ed elimina la sottostringa iniziale "smogtours-" dal futuro nome del file di log
    if href.startswith("smogtours-"):
        # Rimuovi la sottostringa "smogtours-"
        href = href[len("smogtours-"):]
    # Salva il log in un file nella directory specificata con l'encoding 'utf-8'
    username = "YOUR_USERNAME"
    with open(os.path.join("C:\\Users\\" + username + "\\Documents\\DataPokemon\\gen9ouRating", href + ".log"), 'w', encoding='utf-8') as f:
        f.write(log_response.text)

# page di inizio della raccolta dati (fa riferimento al parametro page dell'URL: https://replay.pokemonshowdown.com/?format=gen8ou&page=X)
page = 1

while True:
    # struttura base dell'URL da cui scaricare i log
    url = "https://replay.pokemonshowdown.com/?format=gen9ou&page=" + str(page)
    # Nel caso in cui si volessero prendere i report delle battaglie col rating più alto,
    # usare: url = "https://replay.pokemonshowdown.com/?format=gen8ou&page=" + str(page) + "&sort=rating"
    driver.get(url)
    
    # Chiama la funzione per accettare i cookie
    accept_cookie()

    # Analizza la risposta con BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    li_elements = soup.find('ul', class_='linklist').find_all('li', recursive=False)

    # Specifica il numero massimo di thread per il download
    with ThreadPoolExecutor(max_workers=10) as executor:  
        futures = []
        for li in li_elements:
            href = li.find('a')['href']
            futures.append(executor.submit(download_file, href))

        # Attendi il completamento di tutti i download
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("Errore durante il download:", str(e))

    page += 1
    print("Page da esplorare: " + str(page))

# Chiudi il driver del browser alla fine dell'iterazione
driver.quit()
