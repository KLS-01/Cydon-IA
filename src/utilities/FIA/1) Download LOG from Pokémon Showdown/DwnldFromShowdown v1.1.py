import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# page di inizio della raccolta dati (fa riferimento al parametro page dell'URL: https://replay.pokemonshowdown.com/?format=gen8ou&page=X)
page = 1

# Inizializza il driver del browser (Chrome)
driver = webdriver.Chrome()

while True:

    # struttura base dell'URL da cui scaricare i log
    url = "https://replay.pokemonshowdown.com/?format=gen7ou&page=" + str(page)
    # Nel caso in cui si volessero prendere i report delle battaglie col rating più alto,
    # usare: url = "https://replay.pokemonshowdown.com/?format=gen8ou&page=" + str(page) + "&sort=rating"

    # Effettua una richiesta GET all'URL
    driver.get(url)

    print("Download pagina: " + str(page))

    try:
        # Aspetta fino a quando l'elemento HTML per i cookie diventa cliccabile
        consent_cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button"))
        )
        consent_cookie_button.click()
    except Exception as e:
        print("Errore durante l'attesa o clic del pulsante dei cookie alla pagina:", page, "-", str(e))

    # Analizza la risposta con BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Trova tutti gli elementi <li> all'interno dell'elemento <ul> con class="linklist"
    li_elements = soup.find('ul', class_='linklist').find_all('li', recursive=False)

    for li in li_elements:
        href = li.find('a')['href']

        # Trova l'elemento <a> all'interno dell'elemento <li> e ottieni l'attributo 'href'
        href = li.find('a')['href']

        # Crea il link del log concatenando le stringhe
        linkLog = "https://replay.pokemonshowdown.com/" + href + ".log"

        # Scarica il log
        log_response = requests.get(linkLog)
        
        # Controlla se la stringa inizia con "smogtours-" ed elimina la sottostringa iniziale "smogtours-" dal futuro nome del file di log
        if href.startswith("smogtours-"):
            # Rimuovi la sottostringa "smogtours-"
            href = href[len("smogtours-"):]

        # Salva il log in un file nella directory specificata con l'encoding 'utf-8'
        username = "YOUR_USERNAME"
        with open(os.path.join("C:\\Users\\" + username + "\\Documents\\DataPokemon\\gen7OUData", href + ".log"), 'w', encoding='utf-8') as f:
            f.write(log_response.text)

    page += 1

# Chiudi il driver del browser alla fine dell'iterazione
driver.quit()