from abc import ABC, abstractmethod
from tkinter import Frame, BOTH


class Page(ABC):
    def __init__(self, on_display: bool, page: Frame) -> None:
        self.__on_display = on_display
        self.__page = page

    @abstractmethod
    def set_on_display(self, on_display: bool) -> None:
        self.__on_display = on_display
        if self.__on_display:
            self.__page.pack(fill=BOTH)
        else:
            self.__page.pack_forget()

    @abstractmethod
    def is_on_display(self) -> bool:
        return self.__on_display
