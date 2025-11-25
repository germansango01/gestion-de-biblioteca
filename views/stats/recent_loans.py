import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RecentLoansForm(ctk.CTkToplevel):
    """
    Ventana modal: Últimos 10 libros prestados.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("Últimos 10 Libros Prestados")
        self.geometry("600x500")
        self.grab_set()

        fig, ax = plt.subplots(figsize=(6,5))
        df_sorted = df.sort_values("loan_date", ascending=False).head(10)
        ax.barh(df_sorted['title'], df_sorted['loan_date'].dt.strftime('%Y-%m-%d'), color='purple')
        ax.set_xlabel("Fecha Préstamo")
        ax.set_title("Últimos 10 Libros Prestados")
        ax.invert_yaxis()
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
