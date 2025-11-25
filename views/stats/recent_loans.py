import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class RecentLoansForm(ctk.CTkToplevel):
    """
    Ventana modal para mostrar los últimos 10 préstamos.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("🆕 Últimos 10 Préstamos")
        self.geometry("700x500")
        self.grab_set()

        recent_loans = df.sort_values('loan_date', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8,5))
        ax.barh(recent_loans['title'][::-1], recent_loans.index[::-1]+1, color="#BD10E0")
        ax.set_xlabel("Orden de préstamo")
        ax.set_ylabel("Libro")
        ax.set_title("Últimos 10 Préstamos")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
