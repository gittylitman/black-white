from typing import Any

import flet as ft

from classes.text import Text


class AlertDialog(ft.AlertDialog):
    def __init__(
        self,
        title: str,
        content: Any,
        actions: list[ft.Control],
        modal: bool = True,
    ) -> None:
        super().__init__(
            title=Text(title, size=20, weight=ft.FontWeight.BOLD),
            content=content,
            actions=actions,
            modal=modal,
        )

    def open_dialog(self, page: ft.Page):
        """Opens the dialog and updates the page."""
        page.dialog = self
        self.open = True
        page.update()

    def close_dialog(self, page: ft.Page):
        """Closes the dialog and updates the page."""
        self.open = False
        page.dialog = None
        page.update()
