import tkinter as tk
from tkinter import messagebox
import sys


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-Нолики")
        self.window.geometry("400x450")
        self.window.minsize(350, 400)

        # Базовые переменные
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.move_count = 0
        self.winning_pattern = []

        self.create_menu()
        self.create_widgets()
        self.center_window()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        # Центрирует окно на экране
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_menu(self):
        # Создает меню приложения
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новая игра", command=self.reset_game, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_closing, accelerator="Alt+F4")

        # Меню "Игра"
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Игра", menu=game_menu)
        game_menu.add_command(label="Сброс", command=self.reset_game)
        game_menu.add_command(label="Статистика", command=self.show_stats)

        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Правила", command=self.show_rules)
        help_menu.add_command(label="О программе", command=self.show_about)

        # Горячие клавиши
        self.window.bind('<Control-n>', lambda e: self.reset_game())
        self.window.bind('<Control-N>', lambda e: self.reset_game())

    def create_widgets(self):
        # Создание базовых виджетов
        # Метка статуса
        self.status_label = tk.Label(
            self.window,
            text=f"Ход игрока: {self.current_player}",
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=10)

        # Фрейм для кнопок
        game_frame = tk.Frame(self.window, padx=10, pady=10)
        game_frame.pack(expand=True)

        # Кнопки поля
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3

            button = tk.Button(
                game_frame,
                text="",
                width=5,
                height=2,
                font=("Arial", 24, "bold"),
                command=lambda idx=i: self.make_move(idx),
                bg="#f0f0f0"
            )
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.buttons.append(button)

            # Настройка адаптивности сетки
            game_frame.grid_rowconfigure(row, weight=1)
            game_frame.grid_columnconfigure(col, weight=1)

        # Фрейм для кнопок управления
        control_frame = tk.Frame(self.window, pady=10)
        control_frame.pack()

        # Кнопка новой игры
        new_game_btn = tk.Button(
            control_frame,
            text="Новая игра",
            command=self.reset_game,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка сброса
        reset_btn = tk.Button(
            control_frame,
            text="Сброс",
            command=self.reset_game,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=5
        )
        reset_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка выхода
        exit_btn = tk.Button(
            control_frame,
            text="Выход",
            command=self.on_closing,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=5
        )
        exit_btn.pack(side=tk.RIGHT, padx=5)

    def make_move(self, position):
        # Обрабатывает ход игрока
        try:
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
                self.highlight_winning_line()
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

        except Exception as e:
            self.handle_error(f"Ошибка при выполнении хода: {str(e)}")

    def check_win(self):
        # Проверяет выигрышные комбинации
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for pattern in win_patterns:
            if (self.board[pattern[0]] == self.board[pattern[1]] ==
                    self.board[pattern[2]] != ""):
                self.winning_pattern = pattern
                return True
        return False

    def highlight_winning_line(self):
        """Подсвечивает выигрышную линию"""
        for pos in self.winning_pattern:
            self.buttons[pos].config(bg="#A5D6A7")

    def reset_game(self):
        # Сбрасывает игру
        try:
            self.current_player = "X"
            self.board = [""] * 9
            self.game_over = False
            self.move_count = 0
            self.winning_pattern = []

            for button in self.buttons:
                button.config(text="", bg="#f0f0f0", fg="black")

            self.status_label.config(text=f"Ход игрока: {self.current_player}")

        except Exception as e:
            self.handle_error(f"Ошибка при сбросе игры: {str(e)}")

    def show_stats(self):
       # Показывает статистику
        try:
            stats_text = (
                "Статистика игры:\n\n"
                f"Текущий игрок: {self.current_player}\n"
                f"Сделано ходов: {self.move_count}\n"
                f"Статус игры: {'Завершена' if self.game_over else 'Активна'}\n\n"
                "Для более подробной статистики\nнужно реализовать сохранение результатов."
            )
            messagebox.showinfo("Статистика", stats_text)
        except Exception as e:
            self.handle_error(f"Ошибка при показе статистики: {str(e)}")

    def on_closing(self):
        # Обработчик закрытия окна
        if not self.game_over and self.move_count > 0:
            if not messagebox.askyesno(
                    "Выход",
                    "Игра не завершена. Вы уверены, что хотите выйти?"
            ):
                return

        self.window.quit()
        self.window.destroy()

    def show_rules(self):
        # Показывает правила игры
        try:
            rules_text = (
                "Правила игры 'Крестики-Нолики':\n\n"
                "1. Играют два игрока: 'X' и 'O'\n"
                "2. Игроки ходят по очереди\n"
                "3. Цель - выстроить 3 своих символа\n   в ряд по горизонтали, вертикали или диагонали\n"
                "4. Если все клетки заполнены,\n   а победителя нет - объявляется ничья\n\n"
                "Управление:\n"
                "- Нажимайте на клетки для хода\n"
                "- Используйте меню для управления игрой"
            )
            messagebox.showinfo("Правила игры", rules_text)
        except Exception as e:
            self.handle_error(f"Ошибка при показе правил: {str(e)}")

    def show_about(self):
        # Показывает информацию о программе
        try:
            about_text = (
                "Крестики-Нолики\n\n"
                "Автор: Завальный Михаил\n"
                "Курс: Прикладное программирование\n"
                "Лабораторная работа: Приложения с графическим интерфейсом\n\n"
                "Используемые технологии:\n"
                "- Python\n"
                "- Tkinter\n"
                "- Git"
            )
            messagebox.showinfo("О программе", about_text)
        except Exception as e:
            self.handle_error(f"Ошибка при показе информации: {str(e)}")

    def handle_error(self, error_message):
        # Обрабатывает исключения
        try:
            messagebox.showerror(
                "Ошибка",
                f"{error_message}\n\nПрограмма продолжит работу."
            )
            print(f"Ошибка: {error_message}", file=sys.stderr)
        except:
            print("Критическая ошибка в обработчике ошибок")

    def run(self):
        # Запускает главный цикл приложения
        try:
            self.window.mainloop()
        except Exception as e:
            self.handle_error(f"Критическая ошибка приложения: {str(e)}")


def main():
    # Точка входа в программу
    try:
        app = TicTacToe()
        app.run()
    except Exception as e:
        messagebox.showerror(
            "Критическая ошибка",
            f"Не удалось запустить приложение:\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()