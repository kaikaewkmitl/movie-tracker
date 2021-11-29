from abc import ABC, abstractmethod
from tkinter import Frame, Misc
from tkinter.constants import BOTH
from typing import Any, Callable, Dict, Optional

from utils.globals import *


class Page(ABC):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[Dict[str, Any]]], None]) -> None:
        self._on_display = False
        self._change_page_cb = change_page_callback
        self._page = Frame(parent, bg=store.theme[BG])

    @abstractmethod
    def display(self) -> None:
        self._page.update()

    def set_on_display(self, on_display: bool) -> None:
        self._on_display = on_display
        if self._on_display:
            for widget in self._page.winfo_children():
                widget.destroy()

            self.display()
            self._page.pack(fill=BOTH)
            self._page.configure(background=store.theme[BG])
        else:
            self._page.pack_forget()

    def get_page(self) -> Frame:
        return self._page
