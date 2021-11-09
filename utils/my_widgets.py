from tkinter import Frame, Label, Button, Misc
from tkinter.constants import X, LEFT, RIGHT
from tkinter.font import Font
from typing import Callable, Optional, Dict

from utils.const import *


class MyBigFont(Font):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(family="Helvetica", size=30, weight="bold", *args, **kwargs)


class MyMediumFont(Font):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(family="Helvetica", size=20, weight="bold", *args, **kwargs)


class MySmallFont(Font):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(family="Helvetica", size=15, weight="bold", *args, **kwargs)


class MyHeading(Label):
    def __init__(self, parent: Misc, font: Font = MyBigFont,
                 text: str = "", *args, **kwargs) -> None:
        super().__init__(parent,
                         font=font() if type(font) == type else font,
                         text=text, fg="orange", *args, **kwargs
                         )

    def pack(self, *args, **kwargs) -> None:
        super().pack(pady=15, *args, **kwargs)


class MyButton(Button):
    def __init__(self, parent: Misc, font: Font = MySmallFont,
                 text: str = "", *args, **kwargs) -> None:
        super().__init__(parent,
                         font=font() if type(font) == type else font,
                         text=text, *args, **kwargs
                         )

    def pack(self, *args, **kwargs) -> None:
        super().pack(pady=10, *args, **kwargs)


class MyNavbar(Frame):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str, Optional[int]], None],
                 *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.__change_page_cb = change_page_callback

        self.__btns: Dict[str, MyButton] = {
            MY_LIST_BTN: MyButton(
                self, text="My List"
            ),
            SIGNUP_BTN: MyButton(
                self, text="Signup",
                command=lambda: self.focus_and_change_page(
                    SIGNUP_BTN, SIGNUP_PAGE
                )
            ),
            LOGIN_BTN: MyButton(
                self, text="Login",
                command=lambda: self.focus_and_change_page(
                    LOGIN_BTN, LOGIN_PAGE
                )
            ),
            BACK_BTN: MyButton(
                self, text="Back",
                command=lambda: self.focus_and_change_page(
                    "", MAIN_PAGE
                )
            )
        }

        self.__btns[MY_LIST_BTN].pack(side=LEFT, padx=10)
        self.__btns[SIGNUP_BTN].pack(side=RIGHT, padx=10)
        self.__btns[LOGIN_BTN].pack(side=RIGHT, padx=10)

    def pack(self, *args, **kwargs) -> None:
        super().pack(fill=X, *args, **kwargs)

    def focus_and_change_page(self, btn_name: str, page_name: str) -> None:
        self.focus_btn(btn_name)
        self.__change_page_cb(page_name)

    def display_back_btn(self) -> None:
        self.__btns[BACK_BTN].pack(side=RIGHT, padx=10)

    def remove_back_btn(self) -> None:
        self.__btns[BACK_BTN].pack_forget()

    def focus_btn(self, btn_name: str) -> None:
        for k, v in self.__btns.items():
            v.config(fg="orange" if k == btn_name else "black")
