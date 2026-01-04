import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

users = {}  # In-memory store for username-password pairs

player1_name = ""
player2_name = ""
scores = {}

def login_screen(player_num, on_success):
    login = tk.Tk()
    login.title(f"Login Player {player_num}")
    login.geometry("300x180")
    login.resizable(False, False)
    larger_font = tkFont.Font(family="Arial", size=14)
    login.configure(bg="#f0f0f0")  # colour of background

    tk.Label(login, text="Username", font=larger_font, bg="#f0f0f0").pack(pady=(10, 0))
    username_entry = tk.Entry(login, font=larger_font)
    username_entry.pack() 

    tk.Label(login, text="Password", font=larger_font, bg="#f0f0f0").pack(pady=(10, 0))
    password_entry = tk.Entry(login, show='*', font=larger_font)
    password_entry.pack()

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        if username in users:
              if users[username] == password:
                messagebox.showinfo("Welcome", f"Welcome back, {username}")

                login.destroy()
                on_success(username)
              else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            users[username] = password
            messagebox.showinfo("Registered", f"User '{username}' registered.")
            login.destroy()
            on_success(username)

    tk.Button(login, text="Login / Register", command=handle_login).pack(pady=10)
    login.mainloop()


class TicTacToe:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.current_player = self.p1
        self.symbols = {self.p1: "X", self.p2: "O"}
        self.board = ["" for _ in range(9)]
        self.buttons = []
        self.history = []
        scores.setdefault(self.p1, 0)
        scores.setdefault(self.p2, 0)

        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x550")
        self.root.configure(bg="#e6f2ff")  # light blue background

        self.status = tk.Label(self.root, text=f"{self.p1}'s Turn (X)", font=("Arial", 20), bg="#e6f2ff")
        self.status.pack(pady=10)

        self.frame = tk.Frame(self.root, bg="#e6f2ff")
        self.frame.pack()

        for i in range(9):
            btn = tk.Button(self.frame, text="", font=("Arial", 20), width=5, height=2,
                            command=lambda i=i: self.make_move(i),
                            bg="white", activebackground="#99ccff")
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 18), bg="#e6f2ff")
        self.score_label.pack(pady=5)

        self.history_label = tk.Label(self.root, text="Game History:\n", font=("Arial", 16), bg="#e6f2ff", justify="left")
        self.history_label.pack(pady=5)

        tk.Button(self.root, text="Restart Game", command=self.reset_board, bg="#3399ff", fg="white",
                  activebackground="#66b3ff", font=("Arial", 12)).pack(pady=5)

        
        tk.Button(self.root, text="Logout", command=self.logout, bg="red", fg="white",
                  activebackground="#ff6666", font=("Arial", 12)).pack(pady=5)

        self.root.mainloop()

    def get_score_text(self):
        return f"{self.p1}: {scores[self.p1]} | {self.p2}: {scores[self.p2]}"

    def make_move(self, index):
        if self.board[index] == "" and not self.check_winner():
            self.board[index] = self.symbols[self.current_player]
            self.buttons[index].config(text=self.board[index], state="disabled")
            winner = self.check_winner()
            if winner:
                self.end_game(winner)
            else:
                self.switch_player()

    def switch_player(self):
        self.current_player = self.p1 if self.current_player == self.p2 else self.p2
        symbol = self.symbols[self.current_player]
        self.status.config(text=f"{self.current_player}'s Turn ({symbol})")

    def check_winner(self):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            a, b, c = line
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.current_player
        if "" not in self.board:
            return "Draw"
        return None

    def end_game(self, result):
        if result == "Draw":
            self.status.config(text="It's a Draw🤝!")
            self.history.append("Draw")
        else:
            self.status.config(text=f"{result} wins🏆!")
            scores[result] += 1
            self.score_label.config(text=self.get_score_text())
            self.history.append(f"{result} won")
        for btn in self.buttons:
            btn.config(state="disabled")
        self.update_history()

    def reset_board(self):
        self.board = ["" for _ in range(9)]
        for btn in self.buttons:
            btn.config(text="", state="normal")
        self.current_player = self.p1
        self.status.config(text=f"{self.p1}'s Turn (X)")

    def update_history(self):
        self.history_label.config(text="Game History:\n" + "\n".join(self.history))

    def logout(self):
        self.root.destroy()
        start()


def start():
    def after_p1(name):
        global player1_name
        player1_name = name
        login_screen(2, after_p2)

    def after_p2(name):
        global player2_name
        player2_name = name
        TicTacToe(player1_name, player2_name)

    login_screen(1, after_p1)


start()
