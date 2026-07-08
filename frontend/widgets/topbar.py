import customtkinter as ctk

from frontend.styles.colors import SECONDARY, TEXT


class Topbar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=70, fg_color=SECONDARY)

        title = ctk.CTkLabel(
            self,
            text="Admin Panel",
            font=("Arial", 20, "bold"),
            text_color=TEXT,
        )
        title.pack(side="left", padx=30)

        user = ctk.CTkLabel(
            self,
            text="Admin",
            font=("Arial", 15),
            text_color=TEXT,
        )
        user.pack(side="right", padx=30)
