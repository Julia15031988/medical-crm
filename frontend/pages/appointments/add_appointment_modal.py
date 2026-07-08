import customtkinter as ctk
from tkinter import messagebox

from frontend.api.client import api_client
from frontend.styles.colors import BACKGROUND, WHITE, TEXT, ACCENT, PRIMARY_HOVER
from frontend.styles.fonts import SUBTITLE, TEXT as TEXT_FONT, BUTTON


class AddAppointmentModal(ctk.CTkToplevel):
    def __init__(self, master, on_success):
        super().__init__(master)

        self.on_success = on_success

        self.title("Add appointment")
        self.geometry("420x560")
        self.resizable(False, False)
        self.configure(fg_color=BACKGROUND)

        self.create_widgets()
        self.grab_set()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Add appointment",
            font=SUBTITLE,
            text_color=TEXT,
        )
        title.pack(pady=(25, 20))

        form = ctk.CTkFrame(
            self,
            fg_color=WHITE,
            corner_radius=14,
        )
        form.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        self.patient_id_entry = self.create_entry(form, "Patient ID")
        self.doctor_id_entry = self.create_entry(form, "Doctor ID")
        self.date_entry = self.create_entry(form, "Date: YYYY-MM-DD")
        self.time_entry = self.create_entry(form, "Time: HH:MM:SS")
        self.status_entry = self.create_entry(form, "Status: SCHEDULED")
        self.reason_entry = self.create_entry(form, "Reason")

        save_button = ctk.CTkButton(
            form,
            text="Save",
            font=BUTTON,
            fg_color=ACCENT,
            hover_color=PRIMARY_HOVER,
            command=self.save_appointment,
        )
        save_button.pack(fill="x", padx=25, pady=(20, 10))

        cancel_button = ctk.CTkButton(
            form,
            text="Cancel",
            font=BUTTON,
            fg_color="gray",
            command=self.destroy,
        )
        cancel_button.pack(fill="x", padx=25, pady=(0, 20))

    def create_entry(self, parent, placeholder):
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=TEXT_FONT,
            height=38,
        )
        entry.pack(fill="x", padx=25, pady=(12, 0))
        return entry

    def save_appointment(self):
        try:
            patient_id = int(self.patient_id_entry.get())
            doctor_id = int(self.doctor_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Patient ID and Doctor ID must be numbers.")
            return

        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": self.date_entry.get(),
            "appointment_time": self.time_entry.get(),
            "status": self.status_entry.get().upper() or "SCHEDULED",
            "reason": self.reason_entry.get(),
        }

        if not all(appointment_data.values()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            api_client.create_appointment(appointment_data)
        except Exception as error:
            messagebox.showerror("Error", str(error))
            return

        messagebox.showinfo("Success", "Appointment created successfully.")
        self.destroy()
        self.on_success()
