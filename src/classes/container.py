from typing import Optional

import flet as ft


class Container(ft.Container):
    def __init__(
        self,
        content: ft.Control = None,
        height: Optional[int | float] = None,
        width: Optional[int | float] = None,
        padding: ft.padding = None,
        alignment: ft.alignment = ft.alignment.center,
        bgcolor: ft.colors = None,
        visible: Optional[bool] = None,
        tooltip: Optional[str] = None,
        border_radius: Optional[int] = None,
        border: ft.border = None,
        expand: Optional[bool] = None,
    ) -> None:
        super().__init__()
        self.content = content
        self.height = height
        self.width = width
        self.padding = padding
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.visible = visible
        self.tooltip = tooltip
        self.border_radius = border_radius
        self.border = border
        self.expand = expand
