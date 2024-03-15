import numpy as np
import pandas as pd


class Connector:

    def __init__(self):

        self.source = pd.read_csv('model\pokemon.csv')

    def get_pokemon_stats(self, nome):

        pokemon_stats = self.source[self.source['name'] == nome]

        if not pokemon_stats.empty:

            stats = pokemon_stats[['hp', 'attack', 'defense', 'special', 'speed', 'type1', 'type2']].iloc[0]

            return stats.values

        else:

            return None

    def get_type_advantage(self, nome_mon, type1_mon, type2_mon):

        if type1_mon == "fighting":
            type1_mon = "fight"

        if type2_mon == "fighting":
            type2_mon = "fight"

        nome_colonna = type1_mon + '_dmg'
        flag_missing_second_type = False

        if isinstance(type2_mon, float) and np.isnan(type2_mon):

            type2_mon_enemy = type1_mon
            nome_colonna_due = type2_mon_enemy + '_dmg'
            flag_missing_second_type = True

        else:
            nome_colonna_due = type2_mon + '_dmg'

        pokemon_type_dmg = self.source[self.source['name'] == nome_mon]

        if not pokemon_type_dmg.empty:

            type_dmg = pokemon_type_dmg[nome_colonna].values[0]

            if not flag_missing_second_type:

                type_dmg *= pokemon_type_dmg[nome_colonna_due].values[0]

            return type_dmg

        else:

            return None
