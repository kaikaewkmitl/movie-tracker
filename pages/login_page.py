from tkinter import Entry, Frame, Label, Misc
from tkinter.constants import W
from typing import Callable, Optional

from utils.my_widgets import MyButton, MyHeading, MyMediumFont, MySmallFont
from .abc_page import Page


class LoginPage(Page):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[int]], None]) -> None:
        super().__init__(parent, change_page_callback)
        self.display()

    def display(self) -> None:
        form_container = Frame(self._page)
        form_container.pack(padx=250, pady=100, anchor=W)
        form_heading = MyHeading(form_container, text="Login")
        form_heading.grid(row=0, column=0, pady=20)
        username_label = Label(form_container,
                               font=MySmallFont(),
                               text="Username"
                               )
        username_label.grid(row=1, column=0)

        password_label = Label(form_container,
                               font=MySmallFont(),
                               text="Password"
                               )
        password_label.grid(row=2, column=0, pady=10)

        username_entry = Entry(form_container,
                               bg="white",
                               fg="black",
                               insertbackground="black"
                               )
        username_entry.grid(row=1, column=1)

        password_entry = Entry(form_container,
                               bg="white",
                               fg="black",
                               insertbackground="black"
                               )
        password_entry.grid(row=2, column=1, pady=10)

        login_btn = MyButton(
            form_container, font=MyMediumFont(), text="Login",
            width=15
        )
        login_btn.grid(row=3, column=0, pady=20, columnspan=2)
