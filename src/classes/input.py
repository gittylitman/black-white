import flet as ft

class Input(ft.TextField):
    
    DEFAULT_WIDTH = 300
    DEFAULT_HEIGHT = 47
    
    def __init__(
        self,
        label: str,
        value: str = "",
        width: float = DEFAULT_WIDTH,
        height: float = DEFAULT_HEIGHT
    ):
        super().__init__()
        self.label = label
        self.value = value
        self.width = width
        self.height = height
