import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CategoryLoansForm(ctk.CTkToplevel):
    """
    Ventana modal: Préstamos por categoría.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("Préstamos por Categoría")
        self.geometry("600x500")
        self.grab_set()

        fig, ax = plt.subplots(figsize=(6,5))
        df['category'].value_counts().plot(kind='bar', ax=ax, color='coral')
        ax.set_ylabel("Cantidad")
        ax.set_title("Préstamos por Categoría")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
