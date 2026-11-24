import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from finance_classes import Transaction, FinanceManager, TransactionType


COLORS = {
    "window": "#0f1117",
    "surface": "#171a23",
    "surface_alt": "#1f2430",
    "field": "#232936",
    "border": "#2c3345",
    "text": "#e8ebf5",
    "muted": "#98a0b8",
    "accent": "#7c5cff",
    "accent_hover": "#9a82ff",
    "accent_pressed": "#6a4ae0",
    "selection": "#3b3178",
    "green": "#3ddc97",
    "red": "#ff6b81",
    "danger_bg": "#3a2430",
    "danger_hover": "#4a2a38",
}

FONT = ("Segoe UI", 10)
FONT_MEDIUM = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 24, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_SECTION = ("Segoe UI", 12, "bold")
FONT_VALUE = ("Segoe UI", 11, "bold")
FONT_BALANCE = ("Segoe UI", 28, "bold")


def format_money(value):
    """Форматирует сумму с пробелами между разрядами."""
    return f"{value:,.2f}".replace(",", " ") + " ₽"


class FinanceApp:
    def __init__(self, root):
        self.manager = FinanceManager()
        self.root = root
        self.root.title("Личные финансы")
        self.root.geometry("1080x760")
        self.root.minsize(920, 640)
        self.root.configure(bg=COLORS["window"])
        # Тёмное оформление выпадающего списка Combobox.
        self.root.option_add(
            "*TCombobox*Listbox.background", COLORS["surface_alt"]
        )
        self.root.option_add(
            "*TCombobox*Listbox.foreground", COLORS["text"]
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectBackground", COLORS["accent"]
        )
        self.root.option_add(
            "*TCombobox*Listbox.selectForeground", "#ffffff"
        )
        self.root.option_add("*TCombobox*Listbox.font", FONT_MEDIUM)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()
        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Размещает окно по центру экрана."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = max((self.root.winfo_screenwidth() - width) // 2, 0)
        y = max((self.root.winfo_screenheight() - height) // 2, 0)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def configure_styles(self):
        """Настраивает стили ttk-виджетов под тёмную тему."""
        style = self.style

        style.configure("Window.TFrame", background=COLORS["window"])
        style.configure("TFrame", background=COLORS["surface"])
        style.configure(
            "TLabelframe",
            background=COLORS["surface"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
            relief="solid",
            borderwidth=1,
        )
        # Заголовок LabelFrame рисуется отдельным стилем и не наследует
        # foreground от TLabelframe (его родитель — стиль Label).
        style.configure(
            "TLabelframe.Label",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=FONT_SECTION,
        )

        style.configure(
            "TLabel",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            font=FONT,
        )
        style.configure(
            "Title.TLabel",
            background=COLORS["window"],
            foreground=COLORS["text"],
            font=FONT_TITLE,
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["window"],
            foreground=COLORS["muted"],
            font=FONT_SUBTITLE,
        )
        style.configure(
            "Caption.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=FONT,
        )
        style.configure(
            "Field.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=FONT_BOLD,
        )
        style.configure(
            "Muted.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=FONT_MEDIUM,
        )
        style.configure(
            "Balance.TLabel",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            font=FONT_BALANCE,
        )

        style.configure(
            "TEntry",
            background=COLORS["field"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["field"],
            insertcolor=COLORS["text"],
            selectbackground=COLORS["selection"],
            selectforeground="#ffffff",
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
            padding=(6, 4),
            font=FONT_MEDIUM,
        )
        style.map(
            "TEntry",
            bordercolor=[("focus", COLORS["accent"])],
            lightcolor=[("focus", COLORS["accent"])],
            darkcolor=[("focus", COLORS["accent"])],
        )

        style.configure(
            "TCombobox",
            background=COLORS["field"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["field"],
            insertcolor=COLORS["text"],
            arrowcolor=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
            padding=(6, 4),
            font=FONT_MEDIUM,
        )
        # У темы clam для readonly-состояния поле принудительно светлое,
        # поэтому цвета нужно переопределить именно через map().
        style.map(
            "TCombobox",
            fieldbackground=[
                ("readonly", COLORS["field"]),
                ("disabled", COLORS["field"]),
            ],
            foreground=[
                ("readonly", COLORS["text"]),
                ("disabled", COLORS["muted"]),
            ],
            selectbackground=[("readonly", COLORS["field"])],
            selectforeground=[("readonly", COLORS["text"])],
            background=[
                ("readonly", COLORS["field"]),
                ("active", COLORS["field"]),
                ("pressed", COLORS["field"]),
            ],
            arrowcolor=[("disabled", COLORS["muted"])],
            bordercolor=[("focus", COLORS["accent"])],
            lightcolor=[("focus", COLORS["accent"])],
            darkcolor=[("focus", COLORS["accent"])],
        )

        style.configure(
            "TButton",
            background=COLORS["surface_alt"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["surface_alt"],
            darkcolor=COLORS["surface_alt"],
            padding=(14, 8),
            font=FONT_BOLD,
            relief="flat",
        )
        style.map(
            "TButton",
            background=[("pressed", COLORS["field"]), ("active", COLORS["field"])],
            foreground=[("active", COLORS["text"])],
        )
        style.configure(
            "Accent.TButton",
            background=COLORS["accent"],
            foreground="#ffffff",
            bordercolor=COLORS["accent"],
            lightcolor=COLORS["accent"],
            darkcolor=COLORS["accent"],
        )
        style.map(
            "Accent.TButton",
            background=[
                ("pressed", COLORS["accent_pressed"]),
                ("active", COLORS["accent_hover"]),
            ],
            foreground=[("pressed", "#ffffff"), ("active", "#ffffff")],
        )
        style.configure(
            "Danger.TButton",
            background=COLORS["danger_bg"],
            foreground=COLORS["red"],
            bordercolor=COLORS["danger_bg"],
            lightcolor=COLORS["danger_bg"],
            darkcolor=COLORS["danger_bg"],
        )
        style.map(
            "Danger.TButton",
            background=[
                ("pressed", COLORS["danger_hover"]),
                ("active", COLORS["danger_hover"]),
            ],
            foreground=[("pressed", COLORS["red"]), ("active", COLORS["red"])],
        )
        style.configure(
            "Ghost.TButton",
            background=COLORS["surface_alt"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["surface_alt"],
            darkcolor=COLORS["surface_alt"],
        )
        style.map(
            "Ghost.TButton",
            background=[("pressed", COLORS["field"]), ("active", COLORS["field"])],
            foreground=[("active", COLORS["text"])],
        )

        style.configure(
            "Treeview",
            background=COLORS["surface_alt"],
            fieldbackground=COLORS["surface_alt"],
            foreground=COLORS["text"],
            rowheight=34,
            font=FONT_MEDIUM,
            borderwidth=0,
            bordercolor=COLORS["border"],
            lightcolor=COLORS["border"],
            darkcolor=COLORS["border"],
        )
        style.map(
            "Treeview",
            background=[("selected", COLORS["selection"])],
            foreground=[("selected", "#ffffff")],
        )
        style.configure(
            "Treeview.Heading",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=FONT_BOLD,
            relief="flat",
            padding=(10, 8),
            borderwidth=0,
        )
        style.map(
            "Treeview.Heading",
            background=[("active", COLORS["surface_alt"])],
        )

        style.configure(
            "TScrollbar",
            background=COLORS["field"],
            troughcolor=COLORS["surface_alt"],
            bordercolor=COLORS["surface_alt"],
            arrowcolor=COLORS["muted"],
            lightcolor=COLORS["field"],
            darkcolor=COLORS["field"],
        )
        style.configure("TSeparator", background=COLORS["border"])

    def setup_ui(self):
        # Шапка
        header = ttk.Frame(self.root, style="Window.TFrame")
        header.pack(fill=tk.X, padx=24, pady=(20, 16))
        ttk.Label(header, text="Личные финансы", style="Title.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="Доходы, расходы и наглядная аналитика",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(2, 0))
        tk.Frame(
            header, bg=COLORS["accent"], height=2, width=52
        ).pack(anchor=tk.W, pady=(10, 0))

        # Верхняя часть: форма и сводка
        top = ttk.Frame(self.root, style="Window.TFrame")
        top.pack(fill=tk.X, padx=24)
        top.columnconfigure(0, weight=3)
        top.columnconfigure(1, weight=2)

        # Карточка формы
        input_frame = ttk.LabelFrame(top, text="Новая операция", padding=16)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Сумма, ₽", style="Field.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 12), pady=(0, 10)
        )
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, sticky="ew", pady=(0, 10))

        ttk.Label(input_frame, text="Категория", style="Field.TLabel").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 12), pady=(0, 10)
        )
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            input_frame, textvariable=self.category_var, state="readonly"
        )
        categories = [cat.name for cat in self.manager.categories]
        self.category_combo["values"] = categories
        if categories:
            self.category_combo.current(0)
        self.category_combo.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД)", style="Field.TLabel").grid(
            row=2, column=0, sticky=tk.W, padx=(0, 12), pady=(0, 10)
        )
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1, sticky="ew", pady=(0, 10))

        ttk.Label(input_frame, text="Описание", style="Field.TLabel").grid(
            row=3, column=0, sticky=tk.W, padx=(0, 12), pady=(0, 10)
        )
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=3, column=1, sticky="ew", pady=(0, 10))

        # Кнопки формы
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        ttk.Button(
            button_frame,
            text="Аналитика",
            style="Ghost.TButton",
            command=self.show_analytics,
            cursor="hand2",
        ).pack(side=tk.LEFT)

        ttk.Button(
            button_frame,
            text="Добавить",
            style="Accent.TButton",
            command=self.add_transaction,
            cursor="hand2",
        ).pack(side=tk.RIGHT)

        # Карточка сводки
        info_frame = ttk.LabelFrame(top, text="Сводка", padding=16)
        info_frame.grid(row=0, column=1, sticky="nsew")

        ttk.Label(
            info_frame, text="Текущий баланс", style="Caption.TLabel"
        ).pack(anchor=tk.W)

        self.balance_label = ttk.Label(info_frame, text="", style="Balance.TLabel")
        self.balance_label.pack(anchor=tk.W, pady=(2, 12))

        ttk.Separator(info_frame, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=(0, 12)
        )

        self.totals_label = ttk.Label(info_frame, text="", style="Muted.TLabel")
        self.totals_label.pack(anchor=tk.W)

        ttk.Label(
            info_frame,
            text="Баланс = доходы − расходы",
            style="Caption.TLabel",
        ).pack(side=tk.BOTTOM, anchor=tk.W, pady=(12, 0))

        self.update_balance()

        # Карточка истории операций
        table_frame = ttk.LabelFrame(
            self.root, text="История операций", padding=16
        )
        table_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=(14, 24))

        toolbar = ttk.Frame(table_frame)
        toolbar.pack(fill=tk.X, pady=(0, 8))

        self.count_label = ttk.Label(toolbar, text="", style="Caption.TLabel")
        self.count_label.pack(side=tk.LEFT)

        ttk.Button(
            toolbar,
            text="Удалить выбранную",
            style="Danger.TButton",
            command=self.delete_transaction,
            cursor="hand2",
        ).pack(side=tk.RIGHT)

        tree_wrap = ttk.Frame(table_frame)
        tree_wrap.pack(fill=tk.BOTH, expand=True)

        columns = ("date", "category", "type", "amount", "description")
        self.tree = ttk.Treeview(
            tree_wrap, columns=columns, show="headings"
        )
        self.tree.heading("date", text="Дата", anchor=tk.W)
        self.tree.heading("category", text="Категория", anchor=tk.W)
        self.tree.heading("type", text="Тип", anchor=tk.CENTER)
        self.tree.heading("amount", text="Сумма", anchor=tk.E)
        self.tree.heading("description", text="Описание", anchor=tk.W)

        self.tree.column("date", width=110, minwidth=90, anchor=tk.W, stretch=False)
        self.tree.column(
            "category", width=150, minwidth=110, anchor=tk.W, stretch=False
        )
        self.tree.column(
            "type", width=100, minwidth=80, anchor=tk.CENTER, stretch=False
        )
        self.tree.column(
            "amount", width=130, minwidth=100, anchor=tk.E, stretch=False
        )
        self.tree.column(
            "description", width=300, minwidth=180, anchor=tk.W, stretch=True
        )

        # Цветовая индикация типа операции в таблице
        self.tree.tag_configure("income", foreground=COLORS["green"])
        self.tree.tag_configure("expense", foreground=COLORS["red"])

        scrollbar = ttk.Scrollbar(
            tree_wrap, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.update_table()

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            category_name = self.category_var.get()
            date = self.date_entry.get()
            description = self.desc_entry.get()

            if not all([amount, category_name, date]):
                messagebox.showwarning("Ошибка", "Заполните обязательные поля!")
                return

            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД!"
                )
                return

            category = next(
                (cat for cat in self.manager.categories
                 if cat.name == category_name),
                None,
            )
            if not category:
                messagebox.showwarning("Ошибка", "Выберите корректную категорию!")
                return

            transaction = Transaction(amount, category, date, description)
            self.manager.add_transaction(transaction)

            self.update_table()
            self.update_balance()
            self.clear_inputs()

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму!")

    def delete_transaction(self):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            self.manager.delete_transaction(index)
            self.update_table()
            self.update_balance()
        else:
            messagebox.showinfo("Информация", "Выберите операцию для удаления!")

    def show_analytics(self):
        summary = self.manager.get_category_summary()

        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("Аналитика")
        analytics_window.geometry("420x560")
        analytics_window.minsize(380, 420)
        analytics_window.configure(bg=COLORS["window"])
        analytics_window.transient(self.root)

        header = ttk.Frame(analytics_window, style="Window.TFrame")
        header.pack(fill=tk.X, padx=24, pady=(20, 14))
        ttk.Label(header, text="Аналитика", style="Title.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="Доходы и расходы по категориям",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(2, 0))

        if not summary:
            card = ttk.LabelFrame(
                analytics_window, text="Результат", padding=16
            )
            card.pack(fill=tk.BOTH, expand=True, padx=24)
            ttk.Label(
                card,
                text="Пока нет данных для аналитики.\nДобавьте первую операцию.",
                style="Muted.TLabel",
                justify=tk.CENTER,
            ).pack(expand=True)
        else:
            card = ttk.LabelFrame(
                analytics_window, text="По категориям", padding=16
            )
            card.pack(fill=tk.BOTH, expand=True, padx=24)
            card.columnconfigure(0, weight=1)

            for row, (category, amount) in enumerate(summary.items()):
                color = COLORS["green"] if amount >= 0 else COLORS["red"]
                ttk.Label(card, text=category).grid(
                    row=row, column=0, sticky=tk.W, pady=3
                )
                ttk.Label(
                    card,
                    text=format_money(amount),
                    foreground=color,
                    font=FONT_VALUE,
                ).grid(row=row, column=1, sticky=tk.E, pady=3)

            ttk.Separator(card, orient=tk.HORIZONTAL).grid(
                row=len(summary),
                column=0,
                columnspan=2,
                sticky=tk.EW,
                pady=(10, 10),
            )

            income, expenses = self.manager.get_totals()
            total_row = len(summary) + 1
            ttk.Label(card, text="Доходы", style="Muted.TLabel").grid(
                row=total_row, column=0, sticky=tk.W, pady=2
            )
            ttk.Label(
                card,
                text=format_money(income),
                foreground=COLORS["green"],
                font=FONT_VALUE,
            ).grid(row=total_row, column=1, sticky=tk.E)
            ttk.Label(card, text="Расходы", style="Muted.TLabel").grid(
                row=total_row + 1, column=0, sticky=tk.W, pady=2
            )
            ttk.Label(
                card,
                text=format_money(expenses),
                foreground=COLORS["red"],
                font=FONT_VALUE,
            ).grid(row=total_row + 1, column=1, sticky=tk.E)

        ttk.Button(
            analytics_window,
            text="Закрыть",
            style="Ghost.TButton",
            command=analytics_window.destroy,
            cursor="hand2",
        ).pack(pady=(14, 20))

        # Размещаем окно аналитики по центру главного окна.
        analytics_window.update_idletasks()
        x = self.root.winfo_rootx() + (
            self.root.winfo_width() - analytics_window.winfo_width()
        ) // 2
        y = self.root.winfo_rooty() + (
            self.root.winfo_height() - analytics_window.winfo_height()
        ) // 2
        analytics_window.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for transaction in self.manager.transactions:
            tag = (
                "income"
                if transaction.category.type == TransactionType.INCOME
                else "expense"
            )
            self.tree.insert(
                "",
                tk.END,
                values=(
                    transaction.date,
                    transaction.category.name,
                    transaction.category.type.value,
                    format_money(transaction.amount),
                    transaction.description,
                ),
                tags=(tag,),
            )

        count = len(self.manager.transactions)
        self.count_label.config(text=f"Операций: {count}")

    def update_balance(self):
        balance = self.manager.get_balance()
        income, expenses = self.manager.get_totals()
        color = COLORS["green"] if balance >= 0 else COLORS["red"]
        self.balance_label.config(
            text=format_money(balance), foreground=color
        )
        self.totals_label.config(
            text=f"Доходы: {format_money(income)}\n"
                 f"Расходы: {format_money(expenses)}"
        )

    def clear_inputs(self):
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
