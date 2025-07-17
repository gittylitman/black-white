from typing import Optional

import flet as ft


class Row(ft.Row):
    def __init__(
        self,
        controls: list[ft.Control],
        spacing: Optional[int] = None,
        visible: Optional[bool] = None,
        alignment: ft.MainAxisAlignment = None,
        expand: Optional[bool | int] = None,
        tight: Optional[bool] = None,
        width: Optional[int] = None,
        scroll: ft.ScrollMode = None,
        vertical_alignment: Optional[ft.CrossAxisAlignment] = None,
        horizontal_alignment: Optional[ft.MainAxisAlignment] = None,
    ):
        super().__init__()
        self.controls = controls
        self.spacing = spacing
        self.visible = visible
        self.alignment = alignment
        self.expand = expand
        self.tight = tight
        self.width = width
        self.scroll = scroll
        self.vertical_alignment = vertical_alignment
        self.horizontal_alignment = horizontal_alignment
