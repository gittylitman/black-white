from typing import Callable

import flet as ft


class Checkbox(ft.Checkbox):
    def __init__(self, value: bool, on_change: Callable) -> None:
        super().__init__()
        self.value = value
        self.on_change = on_change
