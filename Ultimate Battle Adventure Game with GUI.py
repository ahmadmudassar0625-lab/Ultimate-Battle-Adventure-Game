import tkinter as tk
from tkinter import ttk
import random
import json
import os

class BattleGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Battle Adventure")
        self.root.geometry("800x650")
        self.root.configure(bg="#1e1e2f")

        self.maxLevel = 4
        self.maxPower = 100
        self.level = 1
        self.score = 0

        self.enemies = {
            1: {"name": "Goblin", "power": 60, "min": 5, "max": 10},
            2: {"name": "Dragon", "power": 80, "min": 10, "max": 15},
            3: {"name": "T-Rex", "power": 100, "min": 15, "max": 20},
            4: {"name": "Demon", "power": 140, "min": 30, "max": 40}
        }

        self.player = {"power": self.maxPower, "hearts": 3}
        self.enemy = None
        self.enemyPower = 0

        self.createStartScreen()

    # ---------------- START SCREEN ---------------- #

    def createStartScreen(self):
        self.clearScreen()

        tk.Label(self.root, text="⚔️ ULTIMATE BATTLE ⚔️",
                 font=("Arial", 28, "bold"),
                 bg="#1e1e2f", fg="white").pack(pady=60)

        tk.Button(self.root, text="Start Game",
                  font=("Arial", 16),
                  bg="#27ae60", fg="black",
                  width=15,
                  command=self.createGameScreen).pack(pady=10)

        tk.Button(self.root, text="Load Save",
                  font=("Arial", 16),
                  bg="#2980b9", fg="black",
                  width=15,
                  command=self.loadGame).pack(pady=10)

    # ---------------- GAME SCREEN ---------------- #

    def createGameScreen(self):
        self.clearScreen()

        self.hearts_label = tk.Label(self.root, font=("Arial", 18),
                                     bg="#1e1e2f", fg="red")
        self.hearts_label.pack()

        self.score_label = tk.Label(self.root, font=("Arial", 14),
                                    bg="#1e1e2f", fg="white")
        self.score_label.pack()

        # Canvas Arena
        self.canvas = tk.Canvas(self.root, width=700, height=250,
                                bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Background layers
        self.canvas.create_rectangle(0, 0, 700, 120, fill="#34495e", outline="")
        self.canvas.create_rectangle(0, 120, 700, 250, fill="#2c3e50", outline="")

        # Draw Player
        self.player_body = self.canvas.create_rectangle(120, 110, 180, 200, fill="#3498db", outline="white", width=2)
        self.player_head = self.canvas.create_oval(135, 70, 165, 110, fill="#f1c40f")
        self.player_sword = self.canvas.create_line(180, 120, 220, 80, fill="silver", width=4)

        # Draw Enemy
        self.enemy_body = self.canvas.create_rectangle(500, 110, 580, 200, fill="#e74c3c", outline="black", width=2)
        self.enemy_eye1 = self.canvas.create_oval(520, 130, 535, 145, fill="white")
        self.enemy_eye2 = self.canvas.create_oval(545, 130, 560, 145, fill="white")
        self.enemy_mouth = self.canvas.create_arc(520, 150, 560, 190, start=180, extent=180, fill="black")

        # Health Bars
        self.player_bar = ttk.Progressbar(self.root, length=500, maximum=self.maxPower)
        self.player_bar.pack(pady=5)

        self.enemy_bar = ttk.Progressbar(self.root, length=500, maximum=250)
        self.enemy_bar.pack(pady=5)

        # Message Box
        self.message = tk.Label(self.root, text="",
                                bg="#2e2e40", fg="white",
                                height=4, wraplength=700)
        self.message.pack(pady=15)

        # ---------------- BUTTONS ---------------- #

        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=30)

        button_style = {
            "font": ("Arial", 18, "bold"),
            "width": 15,
            "height": 2,
            "bd": 4,
            "relief": "raised",
            "activebackground": "black",
            "cursor": "hand2"
        }

        tk.Button(btn_frame, text="⚔ STRIKE",
                  command=self.playerStrike,
                  bg="#e74c3c", fg="black",
                  **button_style).grid(row=0, column=0, padx=15)

        tk.Button(btn_frame, text="🛡 DEFEND",
                  command=self.playerDefend,
                  bg="#3498db", fg="black",
                  **button_style).grid(row=0, column=1, padx=15)

        tk.Button(btn_frame, text="💚 HEAL",
                  command=self.playerHeal,
                  bg="#2ecc71", fg="black",
                  **button_style).grid(row=0, column=2, padx=15)

        tk.Button(self.root, text="Save Game",
                  command=self.saveGame,
                  font=("Arial", 14, "bold"),
                  bg="gray", fg="black",
                  width=18, height=2).pack(pady=15)

        self.startLevel()

    # ---------------- GAME LOGIC ---------------- #

    def startLevel(self):
        if self.level > self.maxLevel:
            self.winScreen()
            return

        self.enemy = self.enemies[self.level]
        scale = 1 + (self.level * 0.25)
        self.enemyPower = int(self.enemy["power"] * scale)

        self.updateDisplay()
        self.message.config(text=f"Level {self.level}: {self.enemy['name']} appears!")

    def updateDisplay(self):
        self.player_bar["value"] = self.player["power"]
        self.enemy_bar["value"] = self.enemyPower
        self.hearts_label.config(text="❤️" * self.player["hearts"])
        self.score_label.config(text=f"Score: {self.score}")

    def playerStrike(self):
        damage = random.randint(15, 30)
        self.enemyPower -= damage
        self.player["power"] -= 10
        self.animateDamage([self.enemy_body])
        self.afterTurn()

    def playerDefend(self):
        self.player["power"] -= 5
        self.afterTurn()

    def playerHeal(self):
        self.player["power"] = min(self.maxPower, self.player["power"] + 15)
        self.afterTurn()

    def enemyAttack(self):
        damage = random.randint(self.enemy["min"], self.enemy["max"])
        self.player["power"] -= damage
        self.animateDamage([self.player_body])

    def afterTurn(self):
        if self.enemyPower > 0:
            self.enemyAttack()

        if self.player["power"] <= 0:
            self.player["hearts"] -= 1
            self.player["power"] = self.maxPower

            if self.player["hearts"] <= 0:
                self.gameOver()
                return

        if self.enemyPower <= 0:
            self.score += 100 * self.level
            self.level += 1
            self.player["power"] = self.maxPower
            self.startLevel()

        self.updateDisplay()

    # ---------------- ANIMATION ---------------- #

    def animateDamage(self, parts):
        for part in parts:
            self.canvas.itemconfig(part, fill="white")
        self.root.after(150, self.resetColors)

    def resetColors(self):
        self.canvas.itemconfig(self.player_body, fill="#3498db")
        self.canvas.itemconfig(self.enemy_body, fill="#e74c3c")

    # ---------------- SAVE / LOAD ---------------- #

    def saveGame(self):
        data = {
            "level": self.level,
            "score": self.score,
            "hearts": self.player["hearts"]
        }
        with open("savegame.json", "w") as file:
            json.dump(data, file)
        self.message.config(text="Game Saved!")

    def loadGame(self):
        if os.path.exists("savegame.json"):
            with open("savegame.json", "r") as file:
                data = json.load(file)
            self.level = data["level"]
            self.score = data["score"]
            self.player["hearts"] = data["hearts"]
            self.createGameScreen()

    # ---------------- END SCREENS ---------------- #

    def winScreen(self):
        self.clearScreen()
        tk.Label(self.root, text="🏆 YOU WON! 🏆",
                 font=("Arial", 30),
                 bg="#1e1e2f", fg="gold").pack(pady=100)

    def gameOver(self):
        self.clearScreen()
        tk.Label(self.root, text="💀 GAME OVER 💀",
                 font=("Arial", 30),
                 bg="#1e1e2f", fg="red").pack(pady=100)

    # ---------------- UTILITY ---------------- #

    def clearScreen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------- RUN ---------------- #

root = tk.Tk()
game = BattleGame(root)
root.mainloop()
