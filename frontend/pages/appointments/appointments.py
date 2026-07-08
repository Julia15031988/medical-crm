import customtkinter as ctk
from tkinter import messagebox

from frontend.api.client import api_client
from frontend.pages.appointments.appointment_detail import AppointmentDetailPage
from frontend.pages.appointments.add_appointment_modal import AddAppointmentModal
from frontend.styles.colors import (
    BACKGROUND,
    WHITE,
    TEXT,
    MUTED_TEXT,
    PRIMARY_HOVER,
    ACCENT,
)
from frontend.styles.fonts import TITLE, TEXT as TEXT_FONT, BUTTON


class AppointmentsPage(ctk.CTkFrame):
    COLUMN_WIDTHS = [40, 90, 90, 120, 100, 120, 220]

    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)

        self.create_header()
        self.create_table()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=BACKGROUND)
        header.pack(fill="x", padx=30, pady=(30, 20))

        title = ctk.CTkLabel(
            header,
            text="Appointments",
            font=TITLE,
            text_color=TEXT,
        )
        title.pack(side="left")

        add_button = ctk.CTkButton(
            header,
            text="+ Add appointment",
            font=BUTTON,
            fg_color=ACCENT,
            hover_color=PRIMARY_HOVER,
            width=170,
            command=self.open_add_appointment_modal,
        )
        add_button.pack(side="right")

    def create_table(self):
        table = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=14)
        table.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        columns = [
            "ID",
            "Patient ID",
            "Doctor ID",
            "Date",
            "Time",
            "Status",
            "Reason",
        ]

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
            appointments = api_client.get_appointments()
        except Exception as error:
            messagebox.showerror("Error", str(error))
            appointments = []

        if not appointments:
            empty_label = ctk.CTkLabel(
                table,
                text="Записів на прийом не знайдено",
                font=TEXT_FONT,
                text_color=MUTED_TEXT,
            )
            empty_label.pack(pady=50)
            return

        for appointment in appointments:
            self.create_appointment_row(table, appointment)

    def create_appointment_row(self, parent, appointment):
        row = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND,
            corner_radius=10,
            cursor="hand2",
        )
        row.pack(fill="x", padx=20, pady=6)

        values = [
            str(appointment.get("id", "—")),
            str(appointment.get("patient_id", "—")),
            str(appointment.get("doctor_id", "—")),
            appointment.get("appointment_date", "—"),
            appointment.get("appointment_time", "—"),
            appointment.get("status", "—"),
            appointment.get("reason", "—"),
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

        row.bind("<Button-1>", lambda event: self.open_appointment_detail(appointment))

        for child in row.winfo_children():
            child.bind("<Button-1>", lambda event: self.open_appointment_detail(appointment))

    def open_add_appointment_modal(self):
        AddAppointmentModal(
            self,
            on_success=self.reload_page,
        )

    def open_appointment_detail(self, appointment):
        for widget in self.winfo_children():
            widget.destroy()

        detail_page = AppointmentDetailPage(
            self,
            appointment=appointment,
            on_back=self.reload_page,
        )
        detail_page.pack(fill="both", expand=True)

    def reload_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_header()
        self.create_table()
