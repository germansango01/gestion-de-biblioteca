import customtkinter as ctk
import pandas as pd
from views.stats.most_borrowed_books import MostBorrowedBooksForm
from views.stats.loans_per_month import LoansPerMonthForm
from views.stats.top_authors import TopAuthorsForm
from views.stats.recent_loans import RecentLoansForm
from views.stats.category_loans import CategoryLoansForm

class StatisticsView(ctk.CTkFrame):
    """
    Vista de estadísticas con botones para abrir gráficas.
    """
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db

        ctk.CTkLabel(self, text="📊 Estadísticas 📊", font=("Arial", 16, "bold")).pack(pady=10)

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill="x", padx=10, pady=10)

        # Configuración de Botones.
        ctk.CTkButton(
            self.buttons_frame, 
            text="Top 10 Libros", 
            command=self.show_top_books,
            fg_color="#4A90E2",
            hover_color="#357ABD",
            text_color="white"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Préstamos por Mes", 
            command=self.show_loans_by_month,
            fg_color="#50E3C2",
            hover_color="#3BBFA1",
            text_color="white"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Autores más prestados", 
            command=self.show_top_authors,
            fg_color="#F5A623",
            hover_color="#D4881D",
            text_color="white"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Últimos 10 préstamos", 
            command=self.show_recent_loans,
            fg_color="#BD10E0",
            hover_color="#8A0DBF",
            text_color="white"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.buttons_frame, 
            text="Préstamos por Categoría", 
            command=self.show_category_loans,
            fg_color="#D0021B",
            hover_color="#A00116",
            text_color="white"
        ).pack(side="left", padx=5)

        self.load_data()


    def load_data(self):
        """
        Cargar datos desde la DB
        """
        loans = self.db.select_all("""
            SELECT books.id, books.title, books.author, books.category, books.available, loans.loan_date
            FROM books
            LEFT JOIN loans ON loans.book_id = books.id
        """)
        if not loans:
            self.df = pd.DataFrame(columns=["book_id","title","author","category","available","loan_date"])
        else:
            self.df = pd.DataFrame(loans, columns=["book_id","title","author","category","available","loan_date"])
            self.df["loan_date"] = pd.to_datetime(self.df["loan_date"])

    # Abrir ventanas modales.
    def show_top_books(self):
        MostBorrowedBooksForm(self, self.df)

    def show_loans_by_month(self):
        LoansPerMonthForm(self, self.df)

    def show_top_authors(self):
        TopAuthorsForm(self, self.df)

    def show_recent_loans(self):
        RecentLoansForm(self, self.df)

    def show_category_loans(self):
        CategoryLoansForm(self, self.df)
