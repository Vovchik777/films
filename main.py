import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Подключение к БД (замените на вашу реальную базу)
conn = sqlite3.connect("films.db")
cursor = conn.cursor()

def get_films_by_genre(genre: str, minutes: list, years: list, isAdult: int, rating:str):
  global result
  if years == []: years = [-1,-1]
  if minutes == []: minutes = [-1,-1]
  genre_str = '(1=1'
  if genre != '':
      for g in genre.split(','):
          genre_str += " AND UPPER(genres) LIKE UPPER('%"+g+"%')"
  else: genre_str += ' AND UPPER(genres) LIKE UPPER("%COMEDY%")'
  genre_str += ')'
  query = '''
  SELECT COALESCE(ru_films.name, films.name) as name, year,genres, minutes, COALESCE(films_rating.rating, "--") as rating
  FROM films
  LEFT JOIN ru_films ON ru_films.id = films.id 
  LEFT JOIN films_rating ON films_rating.id = films.id
  WHERE ''' + genre_str + ''' 
    AND minutes >= ? 
    AND minutes <= ? 
    AND year >= ? 
    AND year <= ?
    AND isAdult = ?
    AND rating >= ?
  ORDER BY year
  '''
  print(query)
  result = cursor.execute(query, (f'{minutes[0]}' if minutes[0] != -1 else 0,
                                f'{minutes[1]}' if minutes[1] != -1 else 999,
                                f'{years[0]}' if years[0]  != -1 else 0,
                                f'{years[1]}' if years[1] != -1 else 9999, 
                                f'{isAdult}',
                                f'{rating}')
                        ).fetchall()

class FilmSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск фильмов")
        self.root.geometry("900x700")
        
        # Переменные для хранения данных
        self.selected_genres = []
        self.genre_vars = [tk.StringVar() for _ in range(3)]
        self.min_from_var = tk.StringVar()
        self.min_to_var = tk.StringVar()
        self.year_from_var = tk.StringVar()
        self.year_to_var = tk.StringVar()
        self.adult_var = tk.IntVar(value=0)
        self.rating_var = tk.DoubleVar(value=0.0)
        
        # Создание виджетов
        self.create_widgets()
        
    def create_widgets(self):
        # Основные фреймы
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Панель поиска
        search_frame = ttk.LabelFrame(main_frame, text="Параметры поиска", padding=10)
        search_frame.pack(fill=tk.X, pady=5)
        
        # Жанры
        ttk.Label(search_frame, text="Жанры (макс. 3):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Combobox для выбора жанров
        self.genre_combos = []
        all_genres = self.get_all_genres()  # Получаем жанры из БД
        
        for i in range(3):
            combo = ttk.Combobox(
                search_frame, 
                textvariable=self.genre_vars[i],
                values=all_genres,
                state="readonly",
                width=15
            )
            combo.grid(row=0, column=i+1, padx=5, pady=2)
            combo.bind("<<ComboboxSelected>>", lambda e, idx=i: self.genre_selected(idx))
            self.genre_combos.append(combo)
        #Рейтинг
        ttk.Label(search_frame, text="★ Рейтинг:").grid(row=2, column=9, sticky=tk.E, padx=5)
        ttk.Combobox(search_frame, textvariable=self.rating_var, values=[str(i/10) for i in range(101)], state="readonly", width=10).grid(row=2, column=10, padx=5, pady=2)
        
        # Кнопка сброса жанров
        ttk.Button(
            search_frame, 
            text="Сбросить", 
            command=self.reset_genres,
            width=10
        ).grid(row=0, column=4, padx=5, pady=2)
        
        # Длительность
        ttk.Label(search_frame, text="Длительность (мин):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(search_frame, textvariable=self.min_from_var, width=8).grid(row=1, column=1, padx=5)
        ttk.Label(search_frame, text="до").grid(row=1, column=2)
        ttk.Entry(search_frame, textvariable=self.min_to_var, width=8).grid(row=1, column=3, padx=5)
        
        # Годы
        ttk.Label(search_frame, text="Год выпуска:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(search_frame, textvariable=self.year_from_var, width=8).grid(row=2, column=1, padx=5)
        ttk.Label(search_frame, text="до").grid(row=2, column=2)
        ttk.Entry(search_frame, textvariable=self.year_to_var, width=8).grid(row=2, column=3, padx=5)
        
        # Возрастное ограничение
        ttk.Checkbutton(
            search_frame, 
            text="Только для взрослых (18+)",
            variable=self.adult_var
        ).grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
        
        # Кнопка поиска
        ttk.Button(
            search_frame, 
            text="Начать поиск", 
            command=self.search_films,
            width=20
        ).grid(row=4, column=0, columnspan=5, pady=10)
        
        # Результаты поиска
        result_frame = ttk.LabelFrame(main_frame, text="Результаты поиска", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Таблица результатов
        self.result_tree = ttk.Treeview(
            result_frame, 
            columns=("name", "year", "genres", "minutes", "rating"), 
            show="headings"
        )
        
        # Настройка столбцов
        self.result_tree.heading("name", text="Название")
        self.result_tree.heading("year", text="Год")
        self.result_tree.heading("genres", text="Жанры")
        self.result_tree.heading("minutes", text="Длительность")
        self.result_tree.heading("rating", text="Рейтинг")
        
        
        self.result_tree.column("name", width=250)
        self.result_tree.column("year", width=60, anchor=tk.CENTER)
        self.result_tree.column("genres", width=200)
        self.result_tree.column("minutes", width=50, anchor=tk.CENTER)
        self.result_tree.column("rating", width=50, anchor=tk.CENTER)
        
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tree.pack(fill=tk.BOTH, expand=True)
    
    def get_all_genres(self):
        """Получение уникальных жанров из базы данных"""
        cursor.execute("SELECT DISTINCT genres FROM films")
        all_genres = set()
        for row in cursor.fetchall():
            genres = row[0].split(',')
            for genre in genres:
                all_genres.add(genre.strip())
        return sorted(all_genres)
    
    def genre_selected(self, index):
        """Обработка выбора жанра"""
        selected = self.genre_vars[index].get()
        if selected and selected not in self.selected_genres:
            if len(self.selected_genres) >= 3:
                messagebox.showwarning("Ошибка", "Можно выбрать не более 3 жанров!")
                self.genre_vars[index].set('')
                return
            self.selected_genres.append(selected)
    
    def reset_genres(self):
        """Сброс выбранных жанров"""
        for var in self.genre_vars:
            var.set('')
        self.selected_genres = []
    
    def search_films(self):
        """Выполнение поиска фильмов"""
        # Подготовка параметров
        genre_str = ','.join(self.selected_genres)
        
        minutes = [
            int(self.min_from_var.get()) if self.min_from_var.get() else -1,
            int(self.min_to_var.get()) if self.min_to_var.get() else -1
        ]
        
        years = [
            int(self.year_from_var.get()) if self.year_from_var.get() else -1,
            int(self.year_to_var.get()) if self.year_to_var.get() else -1
        ]
        
        is_adult = 1 if self.adult_var.get() else 0
        rating = float(self.rating_var.get()) if self.rating_var.get() else 0.0
        # Вызов функции поиска
        get_films_by_genre(genre_str, minutes, years, is_adult, rating)
        
        # Очистка предыдущих результатов
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # Отображение новых результатов
        for row in result:  # result - глобальная переменная из вашей функции
            self.result_tree.insert('', tk.END, values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = FilmSearchApp(root)
    root.mainloop()
    conn.close()  # Закрытие соединения при выходе