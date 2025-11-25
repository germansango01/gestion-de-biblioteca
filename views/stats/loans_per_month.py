import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class LoansPerMonthForm(ctk.CTkToplevel):
    """
    Ventana modal para mostrar préstamos por mes.
    """
    def __init__(self, master, df):
        super().__init__(master)
        self.title("📈 Préstamos por Mes")
        self.geometry("600x500")
        self.grab_set()

        today = pd.to_datetime("today")
        six_months_ago = today - pd.DateOffset(months=5)
        df_recent = df[df['loan_date'] >= six_months_ago]
        df_recent['month'] = df_recent['loan_date'].dt.to_period('M')
        loans_per_month = df_recent.groupby('month').size().reindex(pd.period_range(six_months_ago.to_period('M'), today.to_period('M')), fill_value=0)

        fig, ax = plt.subplots(figsize=(8,5))
        ax.bar(loans_per_month.index.astype(str), loans_per_month.values, color="#50E3C2")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Cantidad de préstamos")
        ax.set_title("Préstamos por Mes (Últimos 6 meses)")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
