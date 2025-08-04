from typing import Any

import flet as ft

from utils.basic_function import show_message, get_department
from classes.column import Column
from classes.container import Container
from classes.dropdown import Dropdown
from classes.text import Text
from config.const import (
    COLORS,
    ERROR_MESSAGES,
    TEXTS,
    Run_Type,
    Env_Type,
)
from process.folder_selector import hierarchical_folder_selector


def get_bucket_by_run_type(env_type: Env_Type, run_type: Run_Type) -> Any:
    """Get bucket that matches the department."""
    department = get_department(env_type, run_type)
    bucket = department.department_bucket
    return bucket


def dropdown(
    page: ft.Page, on_folder_selected: Any, run_type: Run_Type, env_type: Env_Type
) -> Container:
    """Show a drop-down menu with the list of folders in the bucket"""
    try:
        bucket = get_bucket_by_run_type(env_type, run_type)
    except ValueError as e:
        error_message = ERROR_MESSAGES.BASIC_ERROR_MESSAGE.format(str(e))
        show_message(page, error_message, COLORS.FAILED_COLOR.value)
        return Container()

    result_container = Container()
    selected_folder_text = Text("")

    def on_change_dropdown(e: ft.ControlEvent):
        selected_bucket = e.control.value
        on_folder_selected(selected_bucket)

        try:
            folder_selector = hierarchical_folder_selector(
                page, selected_bucket, on_folder_selected
            )
            result_container.content = folder_selector
            page.update()
        except Exception as ex:
            error_message = ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.format(str(ex))
            show_message(page, error_message, COLORS.FAILED_COLOR.value)

    department_dropdown = Dropdown(
        label=TEXTS.CHOOSE_DEPARTMENT.value,
        options=[
            ft.dropdown.Option(text=item.department, key=item.bucket) for item in bucket
        ],
        width=300,
        on_change=on_change_dropdown,
    )

    return Container(
        content=Column(
            controls=[department_dropdown, result_container, selected_folder_text],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        height=320,
    )
