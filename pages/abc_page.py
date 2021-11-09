from abc import ABC, abstractmethod
from tkinter import Frame, BOTH, Misc
from typing import Callable


class Page(ABC):
    def __init__(self, on_display: bool, parent: Misc,
                 change_page_callback: Callable[[str], None]) -> None:
        self.__on_display = on_display
        self.__change_page_cb = change_page_callback
        self.__page = Frame(parent)

    @abstractmethod
    def display(self) -> None:
        pass

    def set_on_display(self, on_display: bool) -> None:
        self.__on_display = on_display
        if self.__on_display:
            self.__page.pack(fill=BOTH)
            self.display()
        else:
            self.__page.pack_forget()

    def get_on_display(self) -> bool:
        return self.__on_display

    def get_page(self) -> Frame:
        return self.__page

    def get_change_page_cb(self) -> Callable[[str], None]:
        return self.__change_page_cb
