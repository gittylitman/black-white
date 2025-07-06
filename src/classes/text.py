from typing import Optional

import flet as ft


class Text(ft.Text):
    def __init__(
        self,
        text: str,
        weight: Optional[ft.FontWeight] = None,
        text_align: Optional[ft.TextAlign] = None,
        size: Optional[int] = None,
        width: Optional[int] = None,
        color: ft.colors = None,
        rtl: bool = False,
        elevation: Optional[int] = None
    ):
        super().__init__()
        self.value = text
        self.weight = weight
        self.text_align = text_align
        self.size = size
        self.width = width
        self.color = color
        self.rtl = rtl
        self.elevation = elevation
