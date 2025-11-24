import customtkinter as ctk
from tkinter import ttk, messagebox
from clases.book import Book
from views.forms.book_form import BookForm

class BookView(ctk.CTkFrame):

    def __init__(self, master, db):
        super().__init__(master)
        self.manager = Book(db)

        frame_btn = ctk.CTkFrame(self)
        frame_btn.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(frame_btn, text="Nuevo Libro", command=self.open_form).pack(side="left")
        ctk.CTkButton(frame_btn, text="Borrar Libro", command=self.delete, fg_color="red").pack(side="right")

        self.tree = ttk.Treeview(self, columns=("ID", "Titulo", "ISBN", "Autor", "Categoría", "Disp"), show="headings")
        cols = ["ID", "Titulo", "ISBN", "Autor", "Categoría", "Disp"]
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh()


    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.manager.list():
            vals = list(row)
            vals[5] = "Si" if vals[5] else "No"
            self.tree.insert("", "end", values=vals)


    def open_form(self):
        BookForm(self, self.manager, self.refresh)


    def delete(self):
        sel = self.tree.selection()
        if sel:
            bid = self.tree.item(sel[0])['values'][0]
            if messagebox.askyesno("Confirmar", "¿Borrar libro?"):
                self.manager.soft_delete(int(bid))
                self.refresh()