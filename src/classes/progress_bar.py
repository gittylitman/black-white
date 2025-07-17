import flet as ft


class ProgressBar(ft.ProgressBar):
    def __init__(self, width: str, color: str = None, value: str = None) -> None:
        super().__init__()
        self.width = width
        self.color = color
        self.value = value
