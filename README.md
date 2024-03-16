<p align="center"><img src="https://github.com/KLS-01/Cydon-IA/blob/main/extension/icons/chromeball.png?raw=true" height="400"></p>

# Cydon-IA - Intelligenza Artificiale per Pokémon

Cydon-IA è un progetto che implementa un sistema di Intelligenza Artificiale utilizzando l'algoritmo di Q-Learning con addestramento online. Questo sistema è progettato per fornire suggerimenti sulle mosse da fare durante le battaglie Pokémon, mirando ad aiutare i giocatori inesperti a migliorare le proprie abilità nel gioco.

## Panoramica delle Tecnologie

Il progetto Cydon-IA fa uso di diverse tecnologie per la sua implementazione:

- **Q-Learning con Addestramento Online**: L'algoritmo di Q-Learning è utilizzato per addestrare l'IA a prendere decisioni ottimali durante le battaglie Pokémon. L'addestramento online consente all'IA di continuare a migliorare le proprie capacità mentre interagisce con i giocatori.

- **<img src="https://miro.medium.com/v2/resize:fit:640/format:webp/1*0G5zu7CnXdMT9pGbYUTQLQ.png" alt="Flask" height="20"/> Flask**: Flask è utilizzato per sviluppare il backend del sistema IA. Gestisce le richieste dei client, elabora i dati e fornisce risposte ai suggerimenti delle mosse Pokémon.

- **<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" height="20"/> Python**: Python è il linguaggio di programmazione principale utilizzato per lo sviluppo del backend, inclusa l'implementazione dell'algoritmo di Q-Learning e l'integrazione con Flask.

- **<img src="https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png" alt="JavaScript" height="20"/> JavaScript**: JavaScript è utilizzato per l'estensione integrata nel gioco Pokémon per interagire con l'interfaccia e fornire suggerimenti in tempo reale ai giocatori durante le battaglie.

## Membri del Team

I membri del team che hanno contribuito al progetto Cydon-IA sono:

- **Leonardo Schiavo** - https://github.com/KLS-01
- **Emmanuel De Luca** - https://github.com/avatarkorraa

## Installazione e Utilizzo

Per installare e utilizzare Cydon-IA, seguire questi passaggi:

1. Clonare il repository da GitHub: `git clone https://github.com/KLS-01/Cydon-IA.git`
2. Navigare nella directory del progetto: `cd cydon-ia`
3. Installare le dipendenze Python utilizzando pip: `pip install -r requirements.txt`
4. Avviare il server Flask: `python Main.py`
5. Assicurarsi che l'estensione JavaScript sia abilitata nel gioco Pokémon per ricevere i suggerimenti delle mosse.

## Contributi e Segnalazione di Bug

Siamo aperti ai contributi da parte della community e apprezziamo qualsiasi segnalazione di bug o suggerimento per migliorare Cydon-IA. Per contribuire, seguire queste linee guida:

1. Forkare il repository
2. Creare un branch per il proprio lavoro: `git checkout -b feature/nuova-funzionalità`
3. Committare le modifiche: `git commit -m 'Aggiunta nuova funzionalità'`
4. Pushare il branch al repository remoto: `git push origin feature/nuova-funzionalità`
5. Aprire una Pull Request

Per segnalare bug o proporre miglioramenti, aprire una nuova issue nel repository.
