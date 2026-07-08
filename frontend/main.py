import customtkinter as ctk

from frontend.pages.auth.login import LoginPage


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class MedicalCRMApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Medical CRM")
        self.geometry("1100x700")
        self.resizable(False, False)

        self.show_login_page()

    def show_login_page(self):
        self.clear_window()
        LoginPage(self).pack(fill="both", expand=True)

    def show_dashboard(self):
        self.clear_window()
        from frontend.pages.dashboard.dashboard import DashboardPage

        DashboardPage(self).pack(fill="both", expand=True)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MedicalCRMApp()
    app.mainloop()
