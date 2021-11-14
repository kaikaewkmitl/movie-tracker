from tkinter import Entry, Frame, Label, Misc
from tkinter.constants import W
from tkinter import messagebox
from typing import Any, Callable, Dict, Optional
from utils.globals import *

from utils.my_widgets import MyButton, MyHeading, MyMediumFont, MySmallFont
from .abc_page import Page


class SignupPage(Page):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[int]], None]) -> None:
        super().__init__(parent, change_page_callback)
        self.__min_len = 5
        self.__max_len = 25
        self.__validations: Dict[str, Callable[[str], bool]] = {
            WITHIN_MIN_LEN: lambda s: len(s) >= self.__min_len,
            WITHIN_MAX_LEN: lambda s: len(s) <= self.__max_len,
            IS_ALNUM: lambda s: s.isalnum()
        }
        self.display()

    def display(self) -> None:
        super().display()

        form_container = Frame(self._page)
        form_container.pack(padx=250, pady=100, anchor=W)
        form_heading = MyHeading(form_container, text="Signup")
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

        signup_btn = MyButton(form_container,
                              font=MyMediumFont(),
                              text="Signup",
                              width=15,
                              command=lambda: self.signup(username_entry.get(),
                                                          password_entry.get()
                                                          )
                              )
        signup_btn.grid(row=3, column=0, pady=20, columnspan=2)

    def signup(self, username: str, password: str) -> None:
        if not self.__validations[WITHIN_MIN_LEN](username) or not self.__validations[WITHIN_MAX_LEN](username):
            print(
                f"Invalid username: must be between {self.__min_len} - {self.__max_len} characters long"
            )
            return

        if not self.__validations[IS_ALNUM](username):
            print("Invalid username: must contains only letters or digits")
            return

        if not self.__validations[WITHIN_MIN_LEN](password) or not self.__validations[WITHIN_MAX_LEN](password):
            print(
                f"Invalid password: must be between {self.__min_len} - {self.__max_len} characters long"
            )
            return

        # save to db/file
        tmp["username"] = username
        tmp["password"] = password

        messagebox.showinfo(
            "Signed up", "You have successfully signed up, proceed to login"
        )
        self._change_page_cb(LOGIN_PAGE)
