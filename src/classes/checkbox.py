from typing import Callable
from config.const import COLORS

import flet as ft


class Checkbox(ft.Checkbox):
    
    def __init__(self, label:str, value: bool, on_change: Callable) -> None:
        super().__init__(
            label_style = ft.TextStyle(color=COLORS.MAIN_COLOR.value),
            check_color=COLORS.MAIN_COLOR.value, 
            fill_color = COLORS.BACKGROUND_COLOR.value 
            )
        self.label = label
        self.value = value
        self.on_change = on_change
        self.active_color = COLORS.MAIN_COLOR.value
