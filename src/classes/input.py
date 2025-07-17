import flet as ft

from config.const import COLORS


class Input(ft.TextField):
    DEFAULT_WIDTH = 300
    DEFAULT_HEIGHT = 47

    def __init__(
        self,
        label: str,
        value: str = "",
        width: float = DEFAULT_WIDTH,
        height: float = DEFAULT_HEIGHT,
        color: str = COLORS.MAIN_COLOR.value,
        border_color: str = COLORS.MAIN_COLOR.value,
    ):
        super().__init__(
            label=label, label_style=ft.TextStyle(color=COLORS.MAIN_COLOR.value)
        )
        self.label = label
        self.value = value
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
