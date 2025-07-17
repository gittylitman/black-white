from typing import Optional

import flet as ft


class Column(ft.Column):
    def __init__(
        self,
        controls: list[ft.Control],
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment: ft.CrossAxisAlignment = None,
        expand: bool = True,
        rtl: Optional[bool] = None,
        scroll: ft.ScrollMode = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
        spacing: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.controls = controls
        self.alignment = alignment
        self.expand = expand
        self.horizontal_alignment = horizontal_alignment
        self.rtl = rtl
        self.scroll = scroll
        self.height = height
        self.width = width
        self.spacing = spacing
