# game.py
from gamebase import RockPaperScissors

def main():
    game = RockPaperScissors()
    print("🎮 Welcome to Rock-Paper-Scissors AI 🎮")
    print("Type 'rock', 'paper', or 'scissors' to play. Type 'quit' to exit.\n")

    while True:
        player_choice = input("👉 Your choice: ").lower()

        if player_choice == "quit":
            print("Thanks for playing! 👋")
            break

        if player_choice not in game.choices:
            print("❌ Invalid choice! Please type rock, paper, or scissors.\n")
            continue

        computer_choice = game.get_computer_choice()
        print(f"🤖 Computer chose: {computer_choice}")

        winner = game.decide_winner(player_choice, computer_choice)

        if winner == "draw":
            print("😐 It's a draw!\n")
        elif winner == "player":
            print("🎉 You win!\n")
        else:
            print("💻 Computer wins!\n")

if __name__ == "__main__":
    main()
