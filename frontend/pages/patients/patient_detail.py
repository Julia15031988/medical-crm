import customtkinter as ctk

from frontend.styles.colors import BACKGROUND, WHITE, TEXT, MUTED_TEXT, ACCENT
from frontend.styles.fonts import TITLE, TEXT as TEXT_FONT, BUTTON


class PatientDetailPage(ctk.CTkFrame):
    def __init__(self, master, patient, on_back):
        super().__init__(master, fg_color=BACKGROUND)

        self.patient = patient
        self.on_back = on_back

        self.create_header()
        self.create_card()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=BACKGROUND)
        header.pack(fill="x", padx=30, pady=(30, 20))

        back_button = ctk.CTkButton(
            header,
            text="← Back",
            font=BUTTON,
            fg_color=ACCENT,
            width=100,
            command=self.on_back,
        )
        back_button.pack(side="left")

        title = ctk.CTkLabel(
            header,
            text="Patient medical card",
            font=TITLE,
            text_color=TEXT,
        )
        title.pack(side="left", padx=20)

    def create_card(self):
        card = ctk.CTkFrame(
            self,
            fg_color=WHITE,
            corner_radius=14,
        )
        card.pack(fill="x", padx=30, pady=10)

        self.add_info_row(card, "Patient ID", str(self.patient.get("patient_id", "—")))
        self.add_info_row(card, "Gender", self.patient.get("gender", "—"))
        self.add_info_row(card, "Birth date", self.patient.get("date_of_birth", "—"))
        self.add_info_row(card, "Address", self.patient.get("address", "—"))

    def add_info_row(self, parent, label_text, value_text):
        row = ctk.CTkFrame(parent, fg_color=WHITE)
        row.pack(fill="x", padx=30, pady=14)

        label = ctk.CTkLabel(
            row,
            text=label_text,
            font=TEXT_FONT,
            text_color=MUTED_TEXT,
            width=160,
            anchor="w",
        )
        label.pack(side="left")

        value = ctk.CTkLabel(
            row,
            text=value_text,
            font=TEXT_FONT,
            text_color=TEXT,
            anchor="w",
        )
        value.pack(side="left")
