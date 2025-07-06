import flet as ft  
from classes.text import Text
 
    
def show_message(page: ft.Page, message: str, color: str) -> None:
        """Displays an error message in a snackbar."""
        page.snack_bar = ft.SnackBar(Text(message), bgcolor=color)
        page.snack_bar.open = True
        page.update()