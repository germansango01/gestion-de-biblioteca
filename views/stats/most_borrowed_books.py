import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MostBorrowedBooksForm(ctk.CTkToplevel):
    """
    Ventana modal: Top 10 libros más prestados.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("Top 10 Libros Más Prestados")
        self.geometry("600x500")
        self.grab_set()

        fig, ax = plt.subplots(figsize=(6,5))
        df['title'].value_counts().nlargest(10).plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel("Cantidad")
        ax.set_title("Top 10 Libros Más Prestados")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
