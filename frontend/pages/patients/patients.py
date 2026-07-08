import customtkinter as ctk
from tkinter import messagebox

from frontend.api.client import api_client
from frontend.pages.patients.patient_detail import PatientDetailPage
from frontend.pages.patients.add_patient_modal import AddPatientModal

from frontend.styles.colors import (
    BACKGROUND,
    WHITE,
    TEXT,
    MUTED_TEXT,
    PRIMARY_HOVER,
    ACCENT,
)
from frontend.styles.fonts import TITLE, TEXT as TEXT_FONT, BUTTON


class PatientsPage(ctk.CTkFrame):
    COLUMN_WIDTHS = [40, 170, 145, 95, 120, 190]

    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)

        self.create_header()
        self.create_table()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=BACKGROUND)
        header.pack(fill="x", padx=30, pady=(30, 20))

        title = ctk.CTkLabel(
            header,
            text="Patients",
            font=TITLE,
            text_color=TEXT,
        )
        title.pack(side="left")

        add_button = ctk.CTkButton(
            header,
            text="+ Add patient",
            font=BUTTON,
            fg_color=ACCENT,
            hover_color=PRIMARY_HOVER,
            text_color=WHITE,
            width=140,
            command=self.open_add_patient_modal,
        )
        add_button.pack(side="right")

    def create_table(self):
        table = ctk.CTkFrame(
            self,
            fg_color=WHITE,
            corner_radius=14,
        )
        table.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        columns = ["ID", "Full name", "Phone", "Gender", "Birth date", "Address"]

        header = ctk.CTkFrame(table, fg_color=WHITE)
        header.pack(fill="x", padx=20, pady=(20, 10))

        for column, width in zip(columns, self.COLUMN_WIDTHS):
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
            patients = api_client.get_patients()
        except Exception as error:
            messagebox.showerror("Error", str(error))
            patients = []

        if not patients:
            empty_label = ctk.CTkLabel(
                table,
                text="Пацієнтів не знайдено",
                font=TEXT_FONT,
                text_color=MUTED_TEXT,
            )
            empty_label.pack(pady=50)
            return

        for patient in patients:
            self.create_patient_row(table, patient)

    def create_patient_row(self, parent, patient):
        row = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND,
            corner_radius=10,
            cursor="hand2",
        )
        row.pack(fill="x", padx=20, pady=6)

        values = [
            str(patient.get("id", "—")),
            patient.get("full_name", "—"),
            patient.get("phone", "—"),
            patient.get("gender", "—"),
            patient.get("date_of_birth", "—"),
            patient.get("address", "—"),
        ]

        for value, width in zip(values, self.COLUMN_WIDTHS):
            label = ctk.CTkLabel(
                row,
                text=value,
                font=TEXT_FONT,
                text_color=TEXT,
                width=width,
                anchor="w",
            )
            label.pack(side="left", padx=5, pady=12)

        row.bind("<Button-1>", lambda event: self.open_patient_detail(patient))

        for child in row.winfo_children():
            child.bind("<Button-1>", lambda event: self.open_patient_detail(patient))

    def open_add_patient_modal(self):
        AddPatientModal(
            self,
            on_success=self.reload_page,
        )

    def open_patient_detail(self, patient):
        for widget in self.winfo_children():
            widget.destroy()

        detail_page = PatientDetailPage(
            self,
            patient=patient,
            on_back=self.reload_page,
        )
        detail_page.pack(fill="both", expand=True)

    def reload_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_header()
        self.create_table()
