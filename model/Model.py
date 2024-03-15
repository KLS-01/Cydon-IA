import itertools
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from Connector import Connector


class Enviroment:

    def __init__(self):

        self.next_state = None
        self.current_state = None
        self.rewards = []
        self.Q = None
        self.moves_pokemon = [0, 1]
        self.state_spaces = []
        self.connector = Connector()

    def elaborate_reward(self, current_state, move):

        (my_pokemon, opponent_pokemon, my_health, opponent_health, my_buff, opponent_buff,
         my_status, opponent_status, switch_advantage) = current_state

        info_first_mon = self.connector.get_pokemon_stats(my_pokemon)
        info_second_mon = self.connector.get_pokemon_stats(opponent_pokemon)

        (hp1, atk1, de1, spatk1, spd1, type1_first_mon, type2_first_mon) = info_first_mon
        (hp2, atk2, de2, spatk2, spd2, type1_second_mon, type2_second_mon) = info_second_mon

        first_mon_type_advantage = self.connector.get_type_advantage(opponent_pokemon, type1_first_mon, type2_first_mon)
        second_mon_type_advantage = self.connector.get_type_advantage(my_pokemon, type1_second_mon, type2_second_mon)

        damage_dealt_by_me = ((((((atk1 + spatk1) / de2) / hp2) * first_mon_type_advantage) * my_buff)
                              * opponent_status)

        damage_dealt_to_me = ((((((atk2 + spatk2) / de1) / hp1) * second_mon_type_advantage) * opponent_buff)
                              * my_status)

        damage_advantage = damage_dealt_by_me >= damage_dealt_to_me

        reward = 0

        if damage_advantage and move == 0:

            opponent_health -= damage_dealt_by_me

            if opponent_health <= 0:
                reward = 100
                self.next_state = self.create_next_state(
                    my_pokemon, opponent_pokemon, 100, 100,
                    my_buff, opponent_buff, my_status, opponent_status, switch_advantage)
                return reward
            else:
                reward = 1
                self.next_state = self.initial_state
                return reward

        elif not damage_advantage and move == 1:
            opponent_health -= 0.1 * damage_dealt_by_me
            reward = 1
            self.next_state = self.create_next_state(
                my_pokemon, opponent_pokemon, my_health, opponent_health,
                my_buff, opponent_buff, my_status, opponent_status, switch_advantage)
            return reward

        else:
            reward = -1
            self.next_state = self.create_next_state(
                my_pokemon, opponent_pokemon, my_health, opponent_health,
                my_buff, opponent_buff, my_status, opponent_status, switch_advantage)
            return reward

    def create_next_state(self, pokemon_name_one, pokemon_name_two, mon_healt, enemy_healt, pokemon_buff,
                          pokemonTwo_buff, pokemon_status, enemy_status, switch_viability):

        return (pokemon_name_one, pokemon_name_two, mon_healt, enemy_healt, pokemon_buff, pokemonTwo_buff,
                pokemon_status, enemy_status, switch_viability)

    def train(self, n_episode, learning_rate, exploration, initial_state):

        self.rewards = []
        episodes = []
        q_value_changes = []

        self.create_new_model(n_episode)
        self.initial_state = initial_state

        self.current_state = initial_state
        self.state_spaces.append(initial_state)

        for episode in range(n_episode):
            move = np.random.choice(self.moves_pokemon)
            reward = self.elaborate_reward(self.current_state, move)
            self.rewards.append(reward)
            self.state_spaces.append(self.next_state)

            if episode == len(self.Q):
                break

            current_state_index = self.state_spaces.index(self.current_state)
            next_state_index = self.state_spaces.index(self.next_state)

            old_q_values = self.Q[current_state_index].copy()

            self.Q[current_state_index][move] = ((1 - learning_rate) * self.Q[current_state_index][move] +
                                                 learning_rate * (
                                                         reward + exploration * np.max(self.Q[next_state_index])))

            episodes.append(episode)

            self.current_state = self.next_state

            q_value_change = np.mean(np.abs(old_q_values - self.Q[current_state_index]))
            q_value_changes.append(q_value_change)

        # IF GRAPHS ARE NEEDED:
        # self.create_training_plot(episodes)
        # plt.plot(episodes, q_value_changes)
        # plt.xlabel("Episode")
        # plt.ylabel("Q Value Change")
        # plt.title("Q Value Convergence")
        # plt.show()

    def best_move(self, state):
        state_n = self.state_spaces.index(state)
        return np.argmax(self.Q[state_n])

    def create_new_model(self, n_episode):
        self.Q = np.zeros((n_episode, len(self.moves_pokemon)))

    def train_model(self, n_episode, learning_rate, exploration, initial_state):

        self.train(n_episode, learning_rate, exploration, initial_state)

        with open("model.pkl", 'wb') as f:
            pickle.dump(self.Q, f)

    def create_training_plot(self, episodes):
        plt.plot(episodes, np.cumsum(self.rewards))
        plt.xlabel("Episode")
        plt.ylabel("Total Reward")
        plt.title("Accumulated Reward")
        plt.show()
