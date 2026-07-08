import customtkinter as ctk
from tkinter import messagebox

from frontend.api.client import api_client
from frontend.styles.colors import BACKGROUND, WHITE, TEXT, ACCENT, PRIMARY_HOVER
from frontend.styles.fonts import SUBTITLE, TEXT as TEXT_FONT, BUTTON


class AddPatientModal(ctk.CTkToplevel):
    def __init__(self, master, on_success):
        super().__init__(master)

        self.on_success = on_success

        self.title("Add patient")
        self.geometry("420x520")
        self.resizable(False, False)
        self.configure(fg_color=BACKGROUND)

        self.full_name_entry = None
        self.phone_entry = None
        self.gender_entry = None
        self.birth_date_entry = None
        self.address_entry = None

        self.create_widgets()

        self.grab_set()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Add patient",
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

        self.full_name_entry = self.create_entry(form, "Full name")
        self.phone_entry = self.create_entry(form, "Phone")
        self.gender_entry = self.create_entry(form, "Gender: MAN or WOMAN")
        self.birth_date_entry = self.create_entry(form, "Birth date: YYYY-MM-DD")
        self.address_entry = self.create_entry(form, "Address")

        save_button = ctk.CTkButton(
            form,
            text="Save",
            font=BUTTON,
            fg_color=ACCENT,
            hover_color=PRIMARY_HOVER,
            command=self.save_patient,
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
        entry.pack(fill="x", padx=25, pady=(15, 0))
        return entry

    def save_patient(self):
        patient_data = {
            "full_name": self.full_name_entry.get(),
            "phone": self.phone_entry.get(),
            "gender": self.gender_entry.get().upper(),
            "date_of_birth": self.birth_date_entry.get(),
            "address": self.address_entry.get(),
        }

        if not all(patient_data.values()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            api_client.create_patient(patient_data)
        except Exception as error:
            messagebox.showerror("Error", str(error))
            return

        messagebox.showinfo("Success", "Patient created successfully.")
        self.destroy()
        self.on_success()
