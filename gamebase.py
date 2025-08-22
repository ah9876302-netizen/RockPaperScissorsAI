# gamebase.py
import random

class RockPaperScissors:
    def __init__(self):
        self.choices = ["rock", "paper", "scissors"]

    def get_computer_choice(self):
        return random.choice(self.choices)

    def decide_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return "draw"
        elif (
            (player_choice == "rock" and computer_choice == "scissors") or
            (player_choice == "scissors" and computer_choice == "paper") or
            (player_choice == "paper" and computer_choice == "rock")
        ):
            return "player"
        else:
            return "computer"
