from typing import Callable

import flet as ft

from config.const import COLORS


class Checkbox(ft.Checkbox):
    def __init__(self, label: str, value: bool, on_change: Callable) -> None:
        super().__init__(
            label_style=ft.TextStyle(color=COLORS.BLACK_COLOR.value),
            check_color=COLORS.BLACK_COLOR.value,
            fill_color=COLORS.BACKGROUND_COLOR.value,
        )
        self.label = label
        self.value = value
        self.on_change = on_change
        self.active_color = COLORS.MAIN_COLOR.value
