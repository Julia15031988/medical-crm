import customtkinter as ctk

from frontend.styles.colors import (
    BACKGROUND,
    WHITE,
    TEXT,
    MUTED_TEXT,
    PRIMARY_HOVER,
    ACCENT,
)
from frontend.styles.fonts import TITLE, SUBTITLE, TEXT as TEXT_FONT, BUTTON


class ProfilePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)

        self.create_header()
        self.create_profile_card()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color=BACKGROUND)
        header.pack(fill="x", padx=30, pady=(30, 20))

        title = ctk.CTkLabel(
            header,
            text="Profile",
            font=TITLE,
            text_color=TEXT,
        )
        title.pack(side="left")

        edit_button = ctk.CTkButton(
            header,
            text="Edit profile",
            font=BUTTON,
            fg_color=ACCENT,
            hover_color=PRIMARY_HOVER,
            width=140,
        )
        edit_button.pack(side="right")

    def create_profile_card(self):
        card = ctk.CTkFrame(
            self,
            fg_color=WHITE,
            corner_radius=14,
        )
        card.pack(fill="x", padx=30, pady=(0, 30))

        avatar = ctk.CTkFrame(
            card,
            width=90,
            height=90,
            fg_color=ACCENT,
            corner_radius=45,
        )
        avatar.pack(pady=(30, 10))
        avatar.pack_propagate(False)

        initials = ctk.CTkLabel(
            avatar,
            text="A",
            font=("Arial", 34, "bold"),
            text_color=WHITE,
        )
        initials.pack(expand=True)

        name = ctk.CTkLabel(
            card,
            text="Admin User",
            font=SUBTITLE,
            text_color=TEXT,
        )
        name.pack(pady=(5, 5))

        role = ctk.CTkLabel(
            card,
            text="Clinic administrator",
            font=TEXT_FONT,
            text_color=MUTED_TEXT,
        )
        role.pack(pady=(0, 25))

        self.add_info_row(card, "Email", "admin@example.com")
        self.add_info_row(card, "Role", "ADMIN")
        self.add_info_row(card, "Phone", "+380000000000")
        self.add_info_row(card, "Status", "Active")

    def add_info_row(self, parent, label_text, value_text):
        row = ctk.CTkFrame(parent, fg_color=WHITE)
        row.pack(fill="x", padx=60, pady=12)

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
