from abc import ABC, abstractmethod
from tkinter import Frame, Misc
from tkinter.constants import BOTH
from typing import Any, Callable, Dict, Optional

from utils.globals import *


class Page(ABC):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[Dict[str, Any]]], None]) -> None:
        self.on_display = False
        self.change_page_cb = change_page_callback
        self.page = Frame(parent, bg=store.theme[BG])

    @abstractmethod
    def display(self) -> None:
        self.page.update()

    def set_on_display(self, on_display: bool) -> None:
        self.on_display = on_display
        if self.on_display:
            for widget in self.page.winfo_children():
                widget.destroy()

            self.display()
            self.page.pack(fill=BOTH)
            self.page.config(background=store.theme[BG])
        else:
            self.page.pack_forget()

    def get_page(self) -> Frame:
        return self.page
