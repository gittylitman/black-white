import flet as ft

from classes.text import Text

from config.const import (
    ERROR_MESSAGES,
    Departments,
    Run_Type,
    Env_Type,
)


def show_message(page: ft.Page, message: str, color: str) -> None:
    """Displays an error message in a snackbar."""
    page.snack_bar = ft.SnackBar(Text(message), bgcolor=color)
    page.snack_bar.open = True
    page.update()


def get_department(env: Env_Type, run_type: Run_Type) -> Departments:
    """Get department."""
    for dept in Departments:
        if dept.env == env and dept.run_type == run_type:
            return dept
    raise ValueError(ERROR_MESSAGES.DEPARTMENT_NOT_FOUND.value)
