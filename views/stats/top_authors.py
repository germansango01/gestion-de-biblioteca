import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TopAuthorsForm(ctk.CTkToplevel):
    """
    Ventana modal: Autores con más préstamos.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("Autores Más Prestados")
        self.geometry("600x500")
        self.grab_set()

        fig, ax = plt.subplots(figsize=(6,5))
        df['author'].value_counts().nlargest(10).plot(kind='bar', ax=ax, color='lightgreen')
        ax.set_ylabel("Cantidad")
        ax.set_title("Autores con Más Préstamos")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
