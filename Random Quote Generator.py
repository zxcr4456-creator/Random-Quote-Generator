# quote_generator.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator - Расширенная версия")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Загрузка данных
        self.data_file = "quotes_data.json"
        self.quotes = []  # Список цитат: [{"text": "", "author": "", "topic": ""}, ...]
        self.history = []  # История: [{"quote": {...}, "timestamp": ""}, ...]
        
        # Предопределённые цитаты (текст, автор, тема)
        self.default_quotes = [
            {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы", "author": "Джон Леннон", "topic": "жизнь"},
            {"text": "Будь тем изменением, которое хочешь видеть в мире", "author": "Махатма Ганди", "topic": "мотивация"},
            {"text": "Тьма не может изгнать тьму: только свет может это сделать", "author": "Мартин Лютер Кинг", "topic": "мудрость"},
            {"text": "Единственный способ делать великую работу - любить то, что делаешь", "author": "Стив Джобс", "topic": "работа"},
            {"text": "Не судите по успеху, судите по тому, как вы справляетесь с неудачами", "author": "Нельсон Мандела", "topic": "успех"},
            {"text": "Жизнь - это то, что мы делаем с ней", "author": "Мать Тереза", "topic": "жизнь"},
            {"text": "Сложнее всего начать действовать, остальное зависит от упорства", "author": "Пауло Коэльо", "topic": "мотивация"},
            {"text": "Образование - самое мощное оружие, которое можно использовать, чтобы изменить мир", "author": "Нельсон Мандела", "topic": "образование"},
            {"text": "Успех - это способность идти от неудачи к неудаче, не теряя энтузиазма", "author": "Уинстон Черчилль", "topic": "успех"},
            {"text": "Время, которое тебе нравится тратить, не потрачено зря", "author": "Джон Леннон", "topic": "время"},
            {"text": "Знание - сила", "author": "Фрэнсис Бэкон", "topic": "знание"},
            {"text": "Воображение важнее знания", "author": "Альберт Эйнштейн", "topic": "творчество"},
            {"text": "Кто ходит медленно и осторожно, тот безопасно идёт", "author": "Лао-цзы", "topic": "мудрость"},
            {"text": "Делай, что можешь, с тем, что имеешь, там, где ты есть", "author": "Теодор Рузвельт", "topic": "действие"},
        ]
        
        # Загрузка данных из JSON
        self.load_data()
        
        # Создание GUI
        self.setup_ui()
        
        # Статистика
        self.update_stats()
        
        # Привязка клавиш
        self.root.bind('<F5>', lambda e: self.generate_quote())
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quotes = data.get('quotes', [])
                    self.history = data.get('history', [])
                    
                # Проверка корректности данных
                if not self.quotes:
                    self.quotes = self.default_quotes.copy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
                self.quotes = self.default_quotes.copy()
                self.history = []
        else:
            self.quotes = self.default_quotes.copy()
            self.history = []
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            data = {
                'quotes': self.quotes,
                'history': self.history,
                'metadata': {
                    'total_quotes': len(self.quotes),
                    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
            return False
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
        # ===== ЛЕВАЯ ПАНЕЛЬ =====
        left_frame = ttk.LabelFrame(main_frame, text="Генератор цитат", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Отображение текущей цитаты
        self.quote_frame = ttk.Frame(left_frame)
        self.quote_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Текст цитаты
        self.quote_text = tk.Text(self.quote_frame, height=8, wrap=tk.WORD, font=("Georgia", 12), relief=tk.GROOVE, borderwidth=2)
        self.quote_text.pack(fill=tk.BOTH, expand=True)
        
        # Информация об авторе и теме
        info_frame = ttk.Frame(left_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text="Автор:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        self.author_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.author_var, font=("Arial", 10)).grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        ttk.Label(info_frame, text="Тема:", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=tk.W)
        self.topic_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.topic_var, font=("Arial", 10)).grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # Кнопки управления
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.generate_btn = ttk.Button(button_frame, text="Сгенерировать цитату (F5)", command=self.generate_quote)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.add_quote_btn = ttk.Button(button_frame, text="Добавить цитату", command=self.add_quote_dialog)
        self.add_quote_btn.pack(side=tk.LEFT, padx=5)
        
        # Статистика
        stats_frame = ttk.LabelFrame(left_frame, text="Статистика", padding="5")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_label = ttk.Label(stats_frame, text="Всего цитат: 0\nИстория: 0")
        self.stats_label.pack()
        
        # ===== ПРАВАЯ ПАНЕЛЬ (ИСТОРИЯ И ФИЛЬТРАЦИЯ) =====
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Фильтрация
        filter_frame = ttk.LabelFrame(right_frame, text="Фильтрация", padding="5")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Фильтр по автору
        ttk.Label(filter_frame, text="По автору:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.author_filter = ttk.Combobox(filter_frame, values=self.get_authors(), width=20)
        self.author_filter.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=5)
        self.author_filter.set("Все")
        self.author_filter.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Фильтр по теме
        ttk.Label(filter_frame, text="По теме:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.topic_filter = ttk.Combobox(filter_frame, values=self.get_topics(), width=20)
        self.topic_filter.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=5)
        self.topic_filter.set("Все")
        self.topic_filter.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Кнопка сброса фильтров
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=2, column=0, columnspan=2, pady=10)
        
        # История
        history_frame = ttk.LabelFrame(right_frame, text="История цитат", padding="5")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Список истории
        self.history_listbox = tk.Listbox(history_frame, height=15, font=("Arial", 9))
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.history_listbox, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
        # Кнопки управления историей
        history_buttons_frame = ttk.Frame(history_frame)
        history_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(history_buttons_frame, text="Очистить историю", command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(history_buttons_frame, text="Сохранить историю", command=self.save_data).pack(side=tk.LEFT, padx=5)
        
        # Привязка двойного клика для показа цитаты из истории
        self.history_listbox.bind('<Double-Button-1>', self.show_quote_from_history)
    
    def get_authors(self) -> List[str]:
        """Получение списка всех авторов"""
        authors = sorted(set(quote['author'] for quote in self.quotes))
        return ["Все"] + authors
    
    def get_topics(self) -> List[str]:
        """Получение списка всех тем"""
        topics = sorted(set(quote['topic'] for quote in self.quotes))
        return ["Все"] + topics
    
    def update_filters(self):
        """Обновление списков фильтров"""
        self.author_filter['values'] = self.get_authors()
        self.topic_filter['values'] = self.get_topics()
    
    def apply_filters(self):
        """Применение фильтров к истории"""
        selected_author = self.author_filter.get()
        selected_topic = self.topic_filter.get()
        
        filtered_history = []
        for item in self.history:
            quote = item['quote']
            if (selected_author == "Все" or quote['author'] == selected_author) and \
               (selected_topic == "Все" or quote['topic'] == selected_topic):
                filtered_history.append(item)
        
        self.update_history_display(filtered_history)
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.author_filter.set("Все")
        self.topic_filter.set("Все")
        self.apply_filters()
    
    def update_history_display(self, history_list=None):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        display_list = history_list if history_list is not None else self.history
        
        for idx, item in enumerate(display_list[::-1], 1):  # Показываем последние сверху
            quote = item['quote']
            timestamp = item.get('timestamp', '')
            display_text = f"{idx}. {quote['text'][:50]}... - {quote['author']}"
            if timestamp:
                display_text += f" [{timestamp}]"
            self.history_listbox.insert(tk.END, display_text)
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        if not self.quotes:
            messagebox.showwarning("Внимание", "Нет доступных цитат!")
            return
        
        # Выбор случайной цитаты
        quote = random.choice(self.quotes)
        
        # Отображение цитаты
        self.quote_text.delete(1.0, tk.END)
        self.quote_text.insert(1.0, f'"{quote["text"]}"')
        self.author_var.set(quote["author"])
        self.topic_var.set(quote["topic"])
        
        # Добавление в историю
        history_item = {
            'quote': quote,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_item)
        
        # Обновление отображения
        self.update_history_display()
        self.update_stats()
        self.save_data()
        
        # Визуальный эффект
        self.generate_btn.config(state='disabled')
        self.root.after(100, lambda: self.generate_btn.config(state='normal'))
    
    def show_quote_from_history(self, event):
        """Показ цитаты из истории при двойном клике"""
        selection = self.history_listbox.curselection()
        if selection:
            idx = len(self.history) - 1 - selection[0]  # Индекс в оригинальном списке
            if 0 <= idx < len(self.history):
                quote = self.history[idx]['quote']
                self.quote_text.delete(1.0, tk.END)
                self.quote_text.insert(1.0, f'"{quote["text"]}"')
                self.author_var.set(quote["author"])
                self.topic_var.set(quote["topic"])
    
    def add_quote_dialog(self):
        """Диалог добавления новой цитаты с проверкой ввода"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление новой цитаты")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        
        # Центрирование окна
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Поля ввода
        ttk.Label(dialog, text="Текст цитаты:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        text_entry = tk.Text(dialog, height=8, width=60, wrap=tk.WORD)
        text_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Автор:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        author_entry = ttk.Entry(dialog, width=40)
        author_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Тема:", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        topic_entry = ttk.Entry(dialog, width=40)
        topic_entry.pack(pady=5)
        
        def validate_and_add():
            """Проверка корректности ввода и добавление цитаты"""
            text = text_entry.get(1.0, tk.END).strip()
            author = author_entry.get().strip()
            topic = topic_entry.get().strip()
            
            # Проверка на пустые строки
            if not text:
                messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
                return
            if not author:
                messagebox.showerror("Ошибка", "Автор не может быть пустым!")
                return
            if not topic:
                messagebox.showerror("Ошибка", "Тема не может быть пустой!")
                return
            
            # Добавление цитаты
            new_quote = {
                'text': text,
                'author': author,
                'topic': topic
            }
            
            self.quotes.append(new_quote)
            self.update_filters()
            self.update_stats()
            self.save_data()
            
            messagebox.showinfo("Успех", "Цитата успешно добавлена!")
            dialog.destroy()
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Добавить", command=validate_and_add).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def clear_history(self):
        """Очистка истории с подтверждением"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.update_history_display()
            self.update_stats()
            self.save_data()
            messagebox.showinfo("Успех", "История очищена!")
    
    def update_stats(self):
        """Обновление статистики"""
        stats_text = f"Всего цитат: {len(self.quotes)}\n"
        stats_text += f"История: {len(self.history)} цитат\n"
        stats_text += f"Уникальных авторов: {len(set(q['author'] for q in self.quotes))}\n"
        stats_text += f"Уникальных тем: {len(set(q['topic'] for q in self.quotes))}"
        self.stats_label.config(text=stats_text)
    
    def on_closing(self):
        """Обработка закрытия окна"""
        if self.save_data():
            self.root.destroy()


def main():
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()