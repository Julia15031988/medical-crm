import customtkinter as ctk

from frontend.widgets.sidebar import Sidebar
from frontend.widgets.topbar import Topbar
from frontend.styles.colors import BACKGROUND, TEXT
from frontend.styles.fonts import TITLE

from frontend.pages.patients.patients import PatientsPage
from frontend.pages.doctors.doctors import DoctorsPage
from frontend.pages.appointments.appointments import AppointmentsPage
from frontend.pages.profile.profile import ProfilePage



class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)

        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = ctk.CTkFrame(self, fg_color=BACKGROUND)
        self.main_area.pack(side="right", fill="both", expand=True)

        self.topbar = Topbar(self.main_area)
        self.topbar.pack(fill="x")

        self.content = ctk.CTkFrame(self.main_area, fg_color=BACKGROUND)
        self.content.pack(fill="both", expand=True)

        self.show_page("dashboard")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, page_name):
        self.clear_content()

        if page_name == "dashboard":
            page = ctk.CTkFrame(self.content, fg_color=BACKGROUND)

            label = ctk.CTkLabel(
                page,
                text="Dashboard",
                font=TITLE,
                text_color=TEXT,
            )
            label.pack(pady=60)

        elif page_name == "patients":
            page = PatientsPage(self.content)

        elif page_name == "doctors":
            page = DoctorsPage(self.content)

        elif page_name == "appointments":
            page = AppointmentsPage(self.content)

        elif page_name == "profile":
            page = ProfilePage(self.content)

        else:
            page = ctk.CTkFrame(self.content, fg_color=BACKGROUND)

        page.pack(fill="both", expand=True)
