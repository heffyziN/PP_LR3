import tkinter as tk


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-Нолики")
        self.window.geometry("400x450")

        # Базовые переменные
        self.current_player = "X"
        self.board = [""] * 9

        self.create_widgets()

    def create_widgets(self):
        # Создание базовых виджетов
        # Метка статуса
        self.status_label = tk.Label(
            self.window,
            text=f"Ход игрока: {self.current_player}",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=10)

        # Фрейм для кнопок
        game_frame = tk.Frame(self.window)
        game_frame.pack()

        # Кнопки поля
        self.buttons = []
        for i in range(9):
            button = tk.Button(
                game_frame,
                text="",
                width=5,
                height=2,
                font=("Arial", 16)
            )
            button.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(button)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TicTacToe()
    app.run()