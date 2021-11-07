from abc import ABC, abstractmethod
import tkinter as tk


class Page(ABC):
    def __init__(self, on_display: bool = False, page: tk.Frame = None) -> None:
        self.__on_display = on_display
        self.__page = page

    @abstractmethod
    def set_on_display(self, on_display: bool):
        self.__on_display = on_display
        if self.__on_display:
            self.__page.pack(fill=tk.BOTH)
        else:
            self.__page.pack_forget()

    @abstractmethod
    def is_on_display(self):
        return self.__on_display
