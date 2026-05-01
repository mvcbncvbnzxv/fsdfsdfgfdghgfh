import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("650x550")
        self.movies = []
        self.load_data()
        self.create_widgets()

    def load_data(self):
        """Загрузка данных из JSON-файла"""
        try:
            if os.path.exists("movies.json"):
                with open("movies.json", "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            else:
                self.movies = []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            self.movies = []

    def save_data(self):
        """Сохранение данных в JSON-файл"""
        try:
            with open("movies.json", "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def validate_input(self, title, genre, year, rating):
        """Валидация входных данных"""
        if not title.strip():
            messagebox.showerror("Ошибка", "Заполните название фильма")
            return False
        if not genre.strip():
            messagebox.showerror("Ошибка", "Заполните жанр")
            return False

        try:
            year_int = int(year.strip())
            if year_int < 1888 or year_int > 2030:
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2030")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return False

        try:
            rating_float = float(rating.strip())
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return False

        return True

    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        if self.validate_input(title, genre, year, rating):
            movie = {
                "title": title.strip(),
                "genre": genre.strip(),
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_data()
            self.update_table()
            self.update_genre_filter()
            # Очистка полей ввода
            self.title_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.rating_entry.delete(0, tk.END)
            messagebox.showinfo("Успех", "Фильм успешно добавлен!")

    def update_table(self, filtered_movies=None):
        """Обновление таблицы с фильмами"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Определяем, какие фильмы показывать
        movies_to_show = filtered_movies if filtered_movies is not None else self.movies

        # Заполняем таблицу
        for movie in movies_to_show:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

    def update_genre_filter(self):
        """Обновление списка жанров в фильтре"""
        # Получаем уникальные жанры и сортируем их
        genres = sorted(set(movie["genre"] for movie in self.movies))
        self.genre_filter["values"] = ["Все"] + genres
        self.genre_filter.set("Все")

    def filter_by_genre(self):
        """Фильтрация по жанру"""
        selected_genre = self.genre_filter.get()

        if selected_genre == "Все" or not selected_genre:
            self.update_table()
            return

        filtered_movies = [movie for movie in self.movies if movie["genre"] == selected_genre]
        self.update_table(filtered_movies)

    def filter_by_year(self):
        """Фильтрация по году выпуска"""
        year_filter = self.year_filter.get().strip()

        if not year_filter:
            messagebox.showwarning("Предупреждение", "Введите год для фильтрации")
            return

        try:
            year = int(year_filter)
            filtered_movies = [movie for movie in self.movies if movie["year"] == year]

            if not filtered_movies:
                messagebox.showinfo("Информация", f"Фильмы за {year} год не найдены")

            self.update_table(filtered_movies)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")

    def reset_filters(self):
        """Сброс всех фильтров"""
        self.year_filter.delete(0, tk.END)
        self.genre_filter.set("Все")
        self.update_table()

    def create_widgets(self):
        # Основной фрейм для формы
        form_frame = tk.LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        # Поля ввода
        tk.Label(form_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Жанр:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.genre_entry = tk.Entry(form_frame, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Год выпуска:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.year_entry = tk.Entry(form_frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Рейтинг (0–10):").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.rating_entry = tk.Entry(form_frame, width=30)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=2)

        # Кнопка добавления
        add_button = tk.Button(form_frame, text="Добавить фильм", command=self.add_movie, bg="lightgreen")
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Фрейм для фильтров
        filter_frame = tk.LabelFrame(self.root, text="Фильтры", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Фильтр по жанру
        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.genre_filter = ttk.Combobox(filter_frame, state="readonly")
        self.genre_filter.grid(row=0, column=1, padx=5, pady=2)
        filter_genre_button = tk.Button(filter_frame, text="Фильтровать", command=self.filter_by_genre)
        filter_genre_button.grid(row=0, column=2, padx=5, pady=2)

        # Фильтр по году
        tk.Label(filter_frame, text="Фильтр по году:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.year_filter = tk.Entry(filter_frame, width=15)
        self.year_filter.grid(row=1, column=1, padx=5, pady=2)
        filter_year_button = tk.Button(filter_frame, text="Фильтровать", command=self.filter_by_year)
        filter_year_button.grid(row=1, column=2, padx=5, pady=2)

        reset_button = tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters, bg="orange")
        reset_button.grid(row=2, column=0, columnspan=3, pady=5)

        # Таблица
        table_frame = tk.LabelFrame(self.root, text="Коллекция фильмов", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Настройка колонок
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")

        self.tree.column("Название", width=200)
        self.tree.column("Жанр", width=120)
        self.tree.column("Год", width=80, anchor="center")
        self.tree.column("Рейтинг", width=80, anchor="center")

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.update_table()
        self.update_genre_filter()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
