import customtkinter as ctk
from tkinter import messagebox

from frontend.api.client import api_client
from frontend.pages.doctors.doctor_detail import DoctorDetailPage
from frontend.pages.doctors.add_doctor_modal import AddDoctorModal
from frontend.styles.colors import (
    BACKGROUND,
    WHITE,
    TEXT,
    MUTED_TEXT,
    PRIMARY_HOVER,
    ACCENT,
)
from frontend.styles.fonts import TITLE, TEXT as TEXT_FONT, BUTTON


class DoctorsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)

        self.create_header()
        self.create_table()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=BACKGROUND)
        header.pack(fill="x", padx=30, pady=(30, 20))

        title = ctk.CTkLabel(
            header,
            text="Doctors",
            font=TITLE,
            text_color=TEXT,
        )
        title.pack(side="left")

        add_button = ctk.CTkButton(
            header,
            text="+ Add doctor",
            font=BUTTON,
            fg_color=ACCENT,
            hover_color=PRIMARY_HOVER,
            width=140,
            command=self.open_add_doctor_modal,
        )
        add_button.pack(side="right")

    def create_table(self):
        table = ctk.CTkFrame(
            self,
            fg_color=WHITE,
            corner_radius=14,
        )
        table.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        columns = [
            "ID",
            "Full name",
            "Phone",
            "Email",
            "Specialization",
            "Exp.",
        ]

        column_widths = [40, 150, 130, 190, 140, 60]

        header = ctk.CTkFrame(table, fg_color=WHITE)
        header.pack(fill="x", padx=20, pady=(20, 10))

        for column, width in zip(columns, column_widths):
            label = ctk.CTkLabel(
                header,
                text=column,
                font=TEXT_FONT,
                text_color=MUTED_TEXT,
                width=width,
                anchor="w",
            )
            label.pack(side="left", padx=5)

        try:
            doctors = api_client.get_doctors()
        except Exception as error:
            messagebox.showerror("Error", str(error))
            doctors = []

        if not doctors:
            empty_label = ctk.CTkLabel(
                table,
                text="Лікарів не знайдено",
                font=TEXT_FONT,
                text_color=MUTED_TEXT,
            )
            empty_label.pack(pady=50)
            return

        for doctor in doctors:
            self.create_doctor_row(table, doctor)

    def create_doctor_row(self, parent, doctor):
        row = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND,
            corner_radius=10,
            cursor="hand2",
        )
        row.pack(fill="x", padx=20, pady=6)

        values = [
            str(doctor.get("id", "—")),
            doctor.get("full_name", "—"),
            doctor.get("phone", "—"),
            doctor.get("email", "—"),
            doctor.get("specialization", "—"),
            str(doctor.get("experience_years", "—")),
        ]

        column_widths = [40, 150, 130, 190, 140, 60]

        for value, width in zip(values, column_widths):
            label = ctk.CTkLabel(
                row,
                text=value,
                font=TEXT_FONT,
                text_color=TEXT,
                width=width,
                anchor="w",
            )
            label.pack(side="left", padx=5, pady=12)

        row.bind("<Button-1>", lambda event: self.open_doctor_detail(doctor))

        for child in row.winfo_children():
            child.bind("<Button-1>", lambda event: self.open_doctor_detail(doctor))

    def open_add_doctor_modal(self):
        AddDoctorModal(
            self,
            on_success=self.reload_page,
        )

    def open_doctor_detail(self, doctor):
        for widget in self.winfo_children():
            widget.destroy()

        detail_page = DoctorDetailPage(
            self,
            doctor=doctor,
            on_back=self.reload_page,
        )
        detail_page.pack(fill="both", expand=True)

    def reload_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_header()
        self.create_table()
