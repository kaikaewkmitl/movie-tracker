import tkinter as tk
from tkinter.font import Font


def get_big_font() -> Font:
    return Font(
        family="Helvetica",
        size=30,
        weight="bold"
    )


def get_medium_font() -> Font:
    return Font(
        family="Helvetica",
        size=20,
        weight="bold"
    )


def get_small_font() -> Font:
    return Font(
        family="Helvetica",
        size=15,
        weight="bold"
    )


class MyHeading(tk.Label):
    def __init__(self, master, font: Font = ("Helvetica", 30, "bold"), text=""):
        super().__init__(master=master, font=font, text=text, fg="orange")
