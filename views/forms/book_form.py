import customtkinter as ctk

class BookForm(ctk.CTkToplevel):

    def __init__(self, master, book_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Libro")
        self.geometry("300x350")
        self.manager = book_manager
        self.callback = refresh_callback
        self.grab_set()

        self.entries = {}
        self.errors = {}
        
        fields = ["title", "isbn", "author", "category"]
        for f in fields:
            ctk.CTkLabel(self, text=f.capitalize()).pack(pady=2)
            self.entries[f] = ctk.CTkEntry(self)
            self.entries[f].pack(pady=2)
            self.errors[f] = ctk.CTkLabel(self, text="", text_color="red")
            self.errors[f].pack()

        ctk.CTkButton(self, text="Guardar", command=self.save).pack(pady=10)


    def save(self):
        data = {k: v.get() for k, v in self.entries.items()}
        for lbl in self.errors.values(): lbl.configure(text="")

        res = self.manager.create(data['title'], data['isbn'], data['author'], data['category'])
        
        if res is True:
            self.callback()
            self.destroy()
        elif isinstance(res, dict):
            for k, v in res.items():
                if k in self.errors: self.errors[k].configure(text=v)