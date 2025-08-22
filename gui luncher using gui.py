# gui.py — Rock-Paper-Scissors GUI with a small learning AI
# Run with:  py gui.py   (or python gui.py)

import tkinter as tk
from tkinter import ttk, messagebox
from gamebase import RockPaperScissors
import random

# --- Small learning AI (predicts your next move from your last move) ---
MOVES = ("rock", "paper", "scissors")

def counter_move(m):
    return {"rock": "paper", "paper": "scissors", "scissors": "rock"}[m]

class Predictor:
    """
    Simple Markov-style predictor:
    - Learns what the user tends to play after their previous move.
    - Uses decay so it adapts to new habits.
    """
    def __init__(self, decay=0.97):
        self.transition = {m: {n: 1.0 for n in MOVES} for m in MOVES}  # Laplace smoothing
        self.last_user = None
        self.decay = decay

    def update(self, user_move: str):
        if self.last_user is not None:
            # decay
            for n in MOVES:
                self.transition[self.last_user][n] *= self.decay
            # observe
            self.transition[self.last_user][user_move] += 1.0
        self.last_user = user_move

    def predict_user(self) -> str:
        if self.last_user is None:
            return random.choice(MOVES)
        counts = self.transition[self.last_user]
        return max(MOVES, key=lambda m: counts[m])

    def choose_ai(self) -> str:
        return counter_move(self.predict_user())


# --- GUI App ---
class RPSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎮 Rock–Paper–Scissors AI (GUI)")
        self.geometry("560x420")
        self.minsize(520, 400)

        # Dark-ish theme colors
        self.bg = "#111318"
        self.card = "#181b22"
        self.txt = "#e7e7e7"
        self.accent = "#5b9cff"
        self.win = "#47d16b"
        self.lose = "#ff6b6b"
        self.draw = "#f1c40f"

        self.configure(bg=self.bg)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TFrame", background=self.bg)
        style.configure("Card.TFrame", background=self.card)
        style.configure("TLabel", background=self.bg, foreground=self.txt, font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.accent)
        style.configure("Hint.TLabel", foreground="#a7a7a7")
        style.configure("Score.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.map("TButton", foreground=[("disabled", "#777")])

        # Game + AI
        self.engine = RockPaperScissors()
        self.ai = Predictor(decay=0.97)

        # Score keeping
        self.user_score = 0
        self.ai_score = 0
        self.draws = 0
        self.rounds = 0

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=16, pady=(16, 8))

        ttk.Label(top, text="🎮 Rock–Paper–Scissors (Learning AI)", style="Title.TLabel").pack(anchor="w")
        ttk.Label(top, text="Click a button or press R / P / S.  Reset with Ctrl+R.", style="Hint.TLabel").pack(anchor="w", pady=(2, 0))

        # Cards container
        cards = ttk.Frame(self)
        cards.pack(fill="both", expand=True, padx=16, pady=8)

        # Buttons card
        btn_card = ttk.Frame(cards, style="Card.TFrame")
        btn_card.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=0)
        ttk.Label(btn_card, text="Your Move", font=("Segoe UI", 13, "bold"), background=self.card).pack(anchor="w", padx=14, pady=(12, 6))

        btns = ttk.Frame(btn_card, style="Card.TFrame")
        btns.pack(padx=14, pady=(6, 12), anchor="w")

        self._mk_btn(btns, "🪨  Rock", lambda: self.play("rock")).grid(row=0, column=0, padx=6, pady=6)
        self._mk_btn(btns, "📄  Paper", lambda: self.play("paper")).grid(row=0, column=1, padx=6, pady=6)
        self._mk_btn(btns, "✂️  Scissors", lambda: self.play("scissors")).grid(row=0, column=2, padx=6, pady=6)

        # Results card
        res_card = ttk.Frame(cards, style="Card.TFrame")
        res_card.pack(side="left", fill="both", expand=True, padx=(8, 0))

        ttk.Label(res_card, text="Result", font=("Segoe UI", 13, "bold"), background=self.card).pack(anchor="w", padx=14, pady=(12, 6))

        self.result_lbl = ttk.Label(res_card, text="Make a move to start!", wraplength=240)
        self.result_lbl.pack(anchor="w", padx=14, pady=(2, 10))

        # Scoreboard
        score_row = ttk.Frame(res_card, style="Card.TFrame")
        score_row.pack(anchor="w", padx=14, pady=(0, 10))

        ttk.Label(score_row, text="You:", style="Score.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.you_val = ttk.Label(score_row, text="0", style="Score.TLabel")
        self.you_val.grid(row=0, column=1, sticky="w", padx=(0, 16))

        ttk.Label(score_row, text="AI:", style="Score.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.ai_val = ttk.Label(score_row, text="0", style="Score.TLabel")
        self.ai_val.grid(row=0, column=3, sticky="w", padx=(0, 16))

        ttk.Label(score_row, text="Draws:", style="Score.TLabel").grid(row=0, column=4, sticky="w", padx=(0, 6))
        self.draw_val = ttk.Label(score_row, text="0", style="Score.TLabel")
        self.draw_val.grid(row=0, column=5, sticky="w")

        # Controls
        ctrl = ttk.Frame(res_card, style="Card.TFrame")
        ctrl.pack(anchor="w", padx=14, pady=(0, 14))

        reset_btn = ttk.Button(ctrl, text="↺  Reset (Ctrl+R)", command=self.reset)
        reset_btn.grid(row=0, column=0, padx=(0, 8))
        quit_btn = ttk.Button(ctrl, text="✖  Quit", command=self.quit_app)
        quit_btn.grid(row=0, column=1)

        # Keyboard shortcuts
        self.bind("<r>", lambda e: self.play("rock"))
        self.bind("<p>", lambda e: self.play("paper"))
        self.bind("<s>", lambda e: self.play("scissors"))
        self.bind("<Control-r>", lambda e: self.reset())

        # Footer
        footer = ttk.Frame(self)
        footer.pack(fill="x", padx=16, pady=(0, 12))
        ttk.Label(footer, text="Tip: Repeat a pattern (e.g., Rock→Paper→Scissors). The AI will try to catch it.",
                  style="Hint.TLabel").pack(anchor="w")

    def _mk_btn(self, parent, text, cmd):
        return ttk.Button(parent, text=text, command=cmd)

    def play(self, user_move: str):
        # AI selects a move based on prediction
        ai_move = self.ai.choose_ai()

        # Decide winner using shared engine logic
        winner = self.engine.decide_winner(user_move, ai_move)

        self.rounds += 1
        if winner == "player":
            self.user_score += 1
            self._set_result(f"🎉 You win!  You: {self._icon(user_move)}   AI: {self._icon(ai_move)}", self.win)
        elif winner == "computer":
            self.ai_score += 1
            self._set_result(f"💻 AI wins!  You: {self._icon(user_move)}   AI: {self._icon(ai_move)}", self.lose)
        else:
            self.draws += 1
            self._set_result(f"🤝 Draw.  You: {self._icon(user_move)}   AI: {self._icon(ai_move)}", self.draw)

        # Update scoreboard
        self.you_val.config(text=str(self.user_score))
        self.ai_val.config(text=str(self.ai_score))
        self.draw_val.config(text=str(self.draws))

        # Teach the AI what the user actually played
        self.ai.update(user_move)

    def _icon(self, move: str) -> str:
        return {"rock": "🪨 Rock", "paper": "📄 Paper", "scissors": "✂️ Scissors"}[move]

    def _set_result(self, text: str, color: str):
        self.result_lbl.config(text=text, foreground=color)

    def reset(self):
        self.user_score = self.ai_score = self.draws = self.rounds = 0
        self.you_val.config(text="0")
        self.ai_val.config(text="0")
        self.draw_val.config(text="0")
        self.result_lbl.config(text="Reset. Make a move!", foreground=self.txt)
        self.ai = Predictor(decay=0.97)  # fresh memory

    def quit_app(self):
        if messagebox.askokcancel("Quit", "Exit the game?"):
            self.destroy()


if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
