from typing import Any, Optional
import flet as ft
from flet_core.alignment import Alignment
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import OffsetValue, PaddingValue


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