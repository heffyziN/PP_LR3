import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-Нолики")
        self.window.geometry("400x450")

        # Базовые переменные
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.move_count = 0

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """Создает меню приложения"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новая игра", command=self.reset_game)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.window.quit)

        # Меню "Игра"
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Игра", menu=game_menu)
        game_menu.add_command(label="Сброс", command=self.reset_game)

        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Правила", command=self.show_rules)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_widgets(self):
        """Создание базовых виджетов"""
        # Метка статуса
        self.status_label = tk.Label(
            self.window,
            text=f"Ход игрока: {self.current_player}",
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=10)

        # Фрейм для кнопок
        game_frame = tk.Frame(self.window, padx=10, pady=10)
        game_frame.pack()

        # Кнопки поля
        self.buttons = []
        for i in range(9):
            button = tk.Button(
                game_frame,
                text="",
                width=5,
                height=2,
                font=("Arial", 24, "bold"),
                command=lambda idx=i: self.make_move(idx),
                bg="#f0f0f0"
            )
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(button)

        # Кнопка сброса
        reset_frame = tk.Frame(self.window)
        reset_frame.pack(pady=10)

        reset_btn = tk.Button(
            reset_frame,
            text="Новая игра",
            command=self.reset_game,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        reset_btn.pack()

    def make_move(self, position):
        """Обрабатывает ход игрока"""
        if self.game_over or self.board[position] != "":
            return

        self.board[position] = self.current_player
        self.buttons[position].config(
            text=self.current_player,
            fg="red" if self.current_player == "X" else "blue"
        )
        self.move_count += 1

        # Проверка победы
        if self.check_win():
            self.game_over = True
            messagebox.showinfo("Победа!", f"Игрок {self.current_player} победил!")
            return

        # Проверка ничьей
        if self.move_count == 9:
            self.game_over = True
            messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
            return

        # Смена игрока
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Ход игрока: {self.current_player}")

    def check_win(self):
        """Проверяет выигрышные комбинации"""
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for pattern in win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] ==
                    self.board[pattern[2]] != ""):
                return True
        return False

    def reset_game(self):
        """Сбрасывает игру"""
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.move_count = 0

        for button in self.buttons:
            button.config(text="", fg="black")

        self.status_label.config(text=f"Ход игрока: {self.current_player}")

    def show_rules(self):
        """Показывает правила игры"""
        messagebox.showinfo("Правила", "Простая игра в крестики-нолики для двух игроков.")

    def show_about(self):
        """Показывает информацию о программе"""
        messagebox.showinfo("О программе", "Крестики-Нолики v1.0\nСоздано для лабораторной работы №3")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TicTacToe()
    app.run()