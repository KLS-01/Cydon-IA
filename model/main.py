import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from Model import Enviroment
import re
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://play.pokemonshowdown.com"}})


@app.route('/api/ia/cydonia', methods=['POST'])
def model_caller():

    enviroment = Enviroment()

    data = request.get_json()

    pokemon_1 = data["pokemon1"]
    pokemon_2 = data["pokemon2"]

    name_1 = re.match(r'(.+?)\sL\d+', pokemon_1["name"]).group(1)
    name_2 = re.match(r'(.+?)\sL\d+', pokemon_2["name"]).group(1)

    hp_1 = (int(pokemon_1["hp"]) / 100) * 1.5
    hp_2 = (int(pokemon_2["hp"]) / 100) * 1.5

    boost_1 = pokemon_1["has_boost"]
    boost_2 = pokemon_2["has_boost"]

    state_1 = pokemon_1["has_status"]
    state_2 = pokemon_2["has_status"]

    can_switch = pokemon_1["can_switch"]

    current_state = (
        name_1, name_2, hp_1, hp_2, boost_1, boost_2, state_1, state_2, can_switch)

    print(current_state)

    enviroment.train_model(10000, 0.8, 0.8, current_state)

    response_data = {
        "best_move": int(enviroment.best_move(current_state))
    }

    response = jsonify(response_data)
    response.status_code = 200

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
