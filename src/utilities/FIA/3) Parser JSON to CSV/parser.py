import pandas as pd
import json
import os

# Definisci il percorso della cartella contenente i file JSON
username = 'YOUR_USERNAME'
folder_path = 'C:/Users/' + username + '/Desktop/DataPokemon/output'

# Inizializza una lista vuota per contenere i DataFrame di ogni file JSON
dfs = []

# Itera attraverso tutti i file nella cartella
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)

        # Estrai informazioni sui team
        team1 = data.get('team1', [])
        team2 = data.get('team2', [])

        # Rimuovi la specifica di 'record_path' e usa 'turns' direttamente
        df_turns = pd.json_normalize(data.get('turns', []), sep='_')

        # Aggiungi colonne aggiuntive dal livello superiore del JSON
        df_turns['Player1'] = data.get('Player1')
        df_turns['Player2'] = data.get('Player2')
        df_turns['PrimoMonP1'] = data.get('PrimoMonP1')
        df_turns['PrimoMonP2'] = data.get('PrimoMonP2')
        df_turns['Winner'] = data.get('winner')

        # Aggiungi informazioni sui team ai DataFrame dei turni
        df_turns['Team1'] = ', '.join(team1)
        df_turns['Team2'] = ', '.join(team2)

        # Aggiungi il DataFrame alla lista
        dfs.append(df_turns)

# Concatena tutti i DataFrame nella lista in un unico DataFrame
final_df = pd.concat(dfs, ignore_index=True)

# Salva il DataFrame in un file CSV
final_df.to_csv('output_merged.csv', index=False)

# Conferma che il salvataggio sia avvenuto con successo
print("Il file CSV è stato creato con successo.")
