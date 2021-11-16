from tkinter import Frame, Label, Button, Misc
from tkinter.constants import X, LEFT, RIGHT
from tkinter.font import Font
from typing import Callable, Optional, Dict

from utils.globals import *


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
                         text=text, fg="orange", wraplength=700, *args, **kwargs
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

        self.__page_to_btn_dict: Dict[str, str] = {
            USER_LIST_PAGE: USER_LIST_BTN,
            SIGNUP_PAGE: SIGNUP_BTN,
            LOGIN_PAGE: LOGIN_BTN,
            MAIN_PAGE: BACK_BTN
        }

        self.__btns: Dict[str, MyButton] = {
            USER_LIST_BTN: MyButton(
                self, text="My List",
                command=lambda: self.__change_page_cb(USER_LIST_PAGE)
            ),
            SIGNUP_BTN: MyButton(
                self, text="Signup",
                command=lambda: self.__change_page_cb(SIGNUP_PAGE)
            ),
            LOGIN_BTN: MyButton(
                self, text="Login",
                command=lambda: self.__change_page_cb(LOGIN_PAGE)
            ),
            BACK_BTN: MyButton(
                self, text="Back",
                command=lambda: self.focus_and_change_page(
                    BACK_BTN, MAIN_PAGE
                )
            ),
            WELCOME_USER: Label(
                self, font=MySmallFont(),
                text=""
            )
        }

        self.display()

    def display(self):
        self.update()
        self.focus_btn()

        self.display_btn(USER_LIST_BTN, LEFT)

        if len(store.user) == 0:
            self.display_btn(SIGNUP_BTN)
            self.display_btn(LOGIN_BTN)
            self.remove_btn(WELCOME_USER)
        else:
            self.remove_btn(SIGNUP_BTN)
            self.remove_btn(LOGIN_BTN)

            username = store.user["username"]
            self.display_btn(WELCOME_USER)
            self.__btns[WELCOME_USER].config(
                text=f"Welcome, {username}",
                fg="orange"
            )

        if store.curpage == MAIN_PAGE and len(store.search_history) == 1:
            self.remove_btn(BACK_BTN)
        else:
            self.display_btn(BACK_BTN)

    def pack(self, *args, **kwargs) -> None:
        super().pack(fill=X, *args, **kwargs)

    def focus_and_change_page(self, btn_name: str, page_name: str) -> None:
        if btn_name == BACK_BTN:
            if len(store.search_history) > 1 and store.curpage == MAIN_PAGE:
                store.search_history.pop()

        self.__change_page_cb(page_name)

    def display_btn(self, btn_name: str, side: str = RIGHT) -> None:
        self.__btns[btn_name].pack(side=side, padx=10)

    def remove_btn(self, btn_name: str) -> None:
        self.__btns[btn_name].pack_forget()

    def focus_btn(self) -> None:
        for k, v in self.__btns.items():
            if store.curpage in self.__page_to_btn_dict and k == self.__page_to_btn_dict[store.curpage] and k != BACK_BTN:
                v.config(fg="orange")
            else:
                v.config(fg="black")
