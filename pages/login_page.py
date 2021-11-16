from tkinter import Entry, Frame, Label, Misc, messagebox
from tkinter.constants import W
from typing import Callable, Optional

from .abc_page import Page
from db.db import find_one_user
from utils.my_widgets import MyButton, MyHeading, MyMediumFont, MySmallFont
from utils.globals import *


class LoginPage(Page):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[int]], None]) -> None:
        super().__init__(parent, change_page_callback)

        self.__retreived_user = {}
        self.__validations: Dict[str, Callable[[str], bool]] = {
            # access db/file and store user data in self.__retreived_user
            IS_ALNUM: lambda s: s.isalnum(),
            IS_FOUND: lambda username: self.__retreived_user["username"] == username,
            IS_MATCH: lambda password: self.__retreived_user["password"] == password
        }

    def display(self) -> None:
        super().display()

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

        login_btn = MyButton(form_container,
                             font=MyMediumFont(),
                             text="Login",
                             width=15,
                             command=lambda: self.login(username_entry.get(),
                                                        password_entry.get()
                                                        )
                             )

        login_btn.grid(row=3, column=0, pady=20, columnspan=2)

    def login(self, username: str, password: str) -> None:
        if not self.__validations[IS_ALNUM](username):
            messagebox.showerror(
                "Invalid username", "username must contains only letters or digits"
            )
            return

        user = find_one_user(username)
        if user == None:
            messagebox.showerror(
                "Invalid", "the username or password is incorrect"
            )

        self.__retreived_user["username"] = user[1]
        self.__retreived_user["password"] = user[2]

        if not self.__validations[IS_FOUND](username) or not self.__validations[IS_MATCH](password):
            messagebox.showerror(
                "Invalid", "the username or password is incorrect"
            )
            return

        store.user["username"] = user[1]
        messagebox.showinfo("Logged in", "You have logged in")
        self._change_page_cb(MAIN_PAGE)
