import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class TopAuthorsForm(ctk.CTkToplevel):
    """
    Ventana modal para mostrar los autores con más préstamos.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("✍️ Autores con más Préstamos")
        self.geometry("700x500")
        self.grab_set()

        top_authors = df['author'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(8,5))
        ax.barh(top_authors.index[::-1], top_authors.values[::-1], color="#F5A623")
        ax.set_xlabel("Cantidad de préstamos")
        ax.set_ylabel("Autor")
        ax.set_title("Autores con más Préstamos")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
