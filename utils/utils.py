from tkinter import Label, Button, Misc
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


class MyHeading(Label):
    def __init__(self, parent: Misc, font: Font = ("Helvetica", 30, "bold"),
                 text: str = "", *args, **kwargs) -> None:
        super().__init__(parent, font=font, text=text, fg="orange", *args, **kwargs)

    def pack(self, *args, **kwargs) -> None:
        super().pack(pady=15, *args, **kwargs)


class MyButton(Button):
    def __init__(self, parent: Misc, font: Font = ("Helvetica", 15, "bold"),
                 text: str = "", *args, **kwargs) -> None:
        super().__init__(parent, font=font, text=text, *args, **kwargs)

    def pack(self, *args, **kwargs) -> None:
        super().pack(pady=10, *args, **kwargs)
