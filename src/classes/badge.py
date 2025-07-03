import flet as ft
from flet_core.control import OptionalNumber


class Badge(ft.Badge):
    def __init__(
        self,
        text: str,
        bgcolor: str | None = None,
        label_visible: bool | None = None,
        large_size: OptionalNumber = None,
        small_size: OptionalNumber = None,
        visible: bool = True):
        super().__init__()
        self.text = text
        self.bgcolor = bgcolor
        self.label_visible = label_visible  
        self.large_size = large_size
        self.small_size = small_size
        self.visible = visible