from tkinter import Frame, Label, Button, Misc
from tkinter.constants import X, LEFT, RIGHT
from tkinter.font import Font
from typing import Callable, Optional

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

        self.__my_list_btn = MyButton(self, text="My List")
        self.__my_list_btn.pack(side=LEFT, padx=10)

        self.__signup_btn = MyButton(self, text="Signup")
        self.__signup_btn.pack(side=RIGHT, padx=10)

        self.__login_btn = MyButton(self, text="Login")
        self.__login_btn.pack(side=RIGHT)

        self.__back_btn = MyButton(
            self, text="Back", command=lambda: change_page_callback(MAIN_PAGE)
        )

    def pack(self, *args, **kwargs) -> None:
        super().pack(fill=X, *args, **kwargs)

    def display_back_btn(self) -> None:
        self.__back_btn.pack(side=RIGHT, padx=10)

    def remove_back_btn(self) -> None:
        self.__back_btn.pack_forget()
