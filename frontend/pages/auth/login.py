import customtkinter as ctk
from tkinter import messagebox

from frontend.api.client import api_client


class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="Medical CRM",
            font=("Arial", 32, "bold"),
        )
        title.pack(pady=(120, 20))

        self.email_entry = ctk.CTkEntry(
            self,
            placeholder_text="Email",
            width=320,
        )
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Password",
            show="*",
            width=320,
        )
        self.password_entry.pack(pady=10)

        login_button = ctk.CTkButton(
            self,
            text="Login",
            width=320,
            command=self.login,
        )
        login_button.pack(pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        try:
            api_client.login(email, password)

            self.master.show_dashboard()

        except Exception as e:
            messagebox.showerror(
                "Login failed",
                str(e),
            )
