import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class CategoryLoansForm(ctk.CTkToplevel):
    """
    Ventana modal para mostrar préstamos por categoría.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("📂 Préstamos por Categoría")
        self.geometry("700x500")
        self.grab_set()

        category_count = df['category'].value_counts()
        fig, ax = plt.subplots(figsize=(8,5))
        ax.barh(category_count.index[::-1], category_count.values[::-1], color="#D0021B")
        ax.set_xlabel("Cantidad de préstamos")
        ax.set_ylabel("Categoría")
        ax.set_title("Préstamos por Categoría")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
