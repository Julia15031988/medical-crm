import customtkinter as ctk

from frontend.styles.colors import SIDEBAR, PRIMARY


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_page_change):
        super().__init__(master, width=220, fg_color=SIDEBAR)

        self.on_page_change = on_page_change

        title = ctk.CTkLabel(
            self,
            text="Medical CRM",
            font=("Arial", 22, "bold"),
            text_color="white",
        )
        title.pack(pady=(30, 40))

        self.add_button("Dashboard", "dashboard")
        self.add_button("Patients", "patients")
        self.add_button("Doctors", "doctors")
        self.add_button("Appointments", "appointments")
        self.add_button("Profile", "profile")

        logout_button = ctk.CTkButton(
            self,
            text="Logout",
            fg_color=PRIMARY,
            command=master.master.show_login_page,
        )
        logout_button.pack(side="bottom", pady=30, padx=20, fill="x")

    def add_button(self, text, page_name):
        button = ctk.CTkButton(
            self,
            text=text,
            fg_color="transparent",
            anchor="w",
            command=lambda: self.on_page_change(page_name),
        )
        button.pack(pady=6, padx=20, fill="x")
