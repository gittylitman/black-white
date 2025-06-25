from typing import Any, Callable, Optional

import flet as ft


class Dropdown(ft.Dropdown):
    def __init__(
        self,
        on_change: Optional[Callable] = None,
        on_click: Optional[Callable] = None,
        value: str = "",
        options: list = [],
        label: str = "",
        width: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.value = value
        self.options = options
        self.label = label
        self.width = width
        self.on_change = on_change
        self.on_click = on_click

    def add_option(self, value: str) -> None:
        option_exists = any(option.key == value for option in self.options)
        if not option_exists:
            self.options.append(ft.dropdown.Option(value))
            self.value = value

    def remove_option(self, list_options: list[Any]) -> None:
        self.options = [option for option in self.options if option.key in list_options]
