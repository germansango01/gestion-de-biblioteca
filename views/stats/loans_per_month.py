import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class LoansPerMonthForm(ctk.CTkToplevel):
    """
    Ventana modal: Préstamos por mes.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("Préstamos por Mes")
        self.geometry("600x500")
        self.grab_set()

        fig, ax = plt.subplots(figsize=(6,5))
        df.groupby(pd.Grouper(key='loan_date', freq='M'))['book_id'].count().plot(
            kind='line', ax=ax, marker='o', color='orange'
        )
        ax.set_ylabel("Cantidad de préstamos")
        ax.set_xlabel("Mes")
        ax.set_title("Préstamos por Mes")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
