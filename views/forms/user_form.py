import customtkinter as ctk

class UserForm(ctk.CTkToplevel):

    def __init__(self, master, user_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Usuario")
        self.geometry("300x250")
        self.manager = user_manager
        self.callback = refresh_callback
        self.grab_set()

        ctk.CTkLabel(self, text="Username").pack(pady=5)
        self.entry_user = ctk.CTkEntry(self)
        self.entry_user.pack(pady=5)
        self.lbl_err_user = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_err_user.pack()

        ctk.CTkLabel(self, text="Password").pack(pady=5)
        self.entry_pass = ctk.CTkEntry(self, show="*")
        self.entry_pass.pack(pady=5)
        self.lbl_err_pass = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_err_pass.pack()

        ctk.CTkButton(self, text="Guardar", command=self.save).pack(pady=10)


    def save(self):
        self.lbl_err_user.configure(text="")
        self.lbl_err_pass.configure(text="")
        
        res = self.manager.create(self.entry_user.get(), self.entry_pass.get())
        
        if res is True:
            self.callback()
            self.destroy()
        elif isinstance(res, dict):
            if 'username' in res: self.lbl_err_user.configure(text=res['username'])
            if 'password' in res: self.lbl_err_pass.configure(text=res['password'])
            if 'general' in res: self.lbl_err_pass.configure(text=res['general'])