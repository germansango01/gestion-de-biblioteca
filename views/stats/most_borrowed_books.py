import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class MostBorrowedBooksForm(ctk.CTkToplevel):
    """
    Ventana modal para mostrar los Top 10 libros más prestados.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("📚 Top 10 Libros más Prestados")
        self.geometry("700x500")
        self.grab_set()

        top_books = df['title'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8,5))
        ax.barh(top_books.index[::-1], top_books.values[::-1], color="#4A90E2")
        ax.set_xlabel("Cantidad de préstamos")
        ax.set_ylabel("Libro")
        ax.set_title("Top 10 Libros más Prestados")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
