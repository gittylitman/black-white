from typing import Any, Callable, Optional
from config.const import COLORS
import flet as ft


class ElevatedButton(ft.ElevatedButton):
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
        icon: str = "",
    ) -> None:
        super().__init__(bgcolor=COLORS.MAIN_COLOR.value, color=ft.colors.WHITE)
        self.text = text
        self.on_click = on_click
        self.width = width
        self.height = height
        self.disabled = disabled
        self.visible = visible
        self.icon = icon
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=5,
        )


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
        border_radius: ft.BorderRadius = None,
    ) -> None:
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.width = width
        self.height = height
        self.disabled = disabled
        self.visible = visible
        self.icon = icon
        self.border_radius = border_radius


class IconButton(ft.IconButton):
    def __init__(
        self,
        icon: ft.icons,
        on_click: Callable,
        style: Any = None,
        icon_color: ft.colors = None,
        tooltip: ft.Tooltip = None,
        visible: Optional[bool] = True,
        data: Any = None,
        icon_size: Optional[int] = None,
        border_radius: ft.BorderRadius = None,
    ) -> None:
        super().__init__()
        self.icon = icon
        self.style = style
        self.tooltip = tooltip
        self.on_click = on_click
        self.icon_color = icon_color
        self.visible = visible
        self.data = data
        self.icon_size = icon_size
        self.border_radius = border_radius
