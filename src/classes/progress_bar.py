import flet as ft


class ProgressBar(ft.ProgressBar):
    def __init__(self, width: str, color: str, bgcolor: str) -> None:
        super().__init__()
        self.width = width
        self.color = color
        self.bgcolor = bgcolor
