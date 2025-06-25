from typing import Callable, Optional

import flet as ft


class Button(ft.CupertinoFilledButton):
    DEFAULT_WIDTH = 300
    DEFAULT_HEIGHT = 35

    def __init__(
        self,
        text: Optional[str],
        on_click: Callable,
        width: float = DEFAULT_WIDTH,
        height: float = DEFAULT_HEIGHT,
        disabled: bool = False,
        visible: bool = True,
        icon: ft.icons = None,
    ) -> None:
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.width = width
        self.height = height
        self.disabled = disabled
        self.visible = visible
        self.icon = icon
