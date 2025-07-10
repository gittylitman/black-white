from typing import Any

import flet as ft


class FilePicker(ft.FilePicker):
    def __init__(self, on_result: Any) -> None:
        super().__init__(on_result=on_result)

