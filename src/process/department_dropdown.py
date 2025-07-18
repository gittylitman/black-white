from typing import Any

import flet as ft

from utils.gcloud_calls import get_folders_and_files
from utils.basic_function import show_message, get_department
from classes.column import Column
from classes.container import Container
from classes.dropdown import Dropdown
from classes.text import Text
from config.const import (
    COLORS,
    ERROR_MESSAGES,
    TEXTS,
    VALIDATION_MESSAGES,
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
        show_message(page, error_message, COLORS)
        return Container()

    result_container = Container()
    selected_folder_text = Text("")
    selected_folder = ""

    def get_folders_list(bucket: str) -> object:
        """Get a folder list."""
        try:
            result = get_folders_and_files(bucket)
            return get_folders_from_folders_and_files(result)
        except Exception:
            show_message(
                page,
                ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value,
                COLORS.FAILED_COLOR.value,
            )
            return {}

    def get_folders_from_folders_and_files(folders_and_files: str):
        """Get folder hierarchy."""
        list_folders_and_files = folders_and_files.split("\n")
        list_folders = [
            file[file.index("gs://") + 5 : -2].split("/")
            for file in list_folders_and_files
            if file.endswith(":")
        ]
        list_folders = [folder[1:] for folder in list_folders]
        list_folders = [folder for folder in list_folders if len(folder)]
        folders = {}
        for folder in list_folders:
            folders["/".join(folder)] = []
        for folder in list_folders:
            name_folder = folder.pop()
            if not len(folder):
                if not folders.get(""):
                    folders[""] = []
                folders[""].append(name_folder)
            else:
                path_folder = "/".join(folder)
                folders[path_folder].append(name_folder)
        return folders

    def on_change_dropdown(e: ft.ControlEvent):
        """On change drop-down."""
        nonlocal selected_folder
        selected_folder = ""
        selected_bucket = e.control.value
        on_folder_selected(f"{selected_bucket}/{selected_folder}")
        try:
            folders = get_folders_list(selected_bucket)
            if not folders:
                selected_folder_text.value = VALIDATION_MESSAGES.NO_FOLDERS_ALERT.value
                result_container.content = None
                page.update()
                return
            folder_selector = hierarchical_folder_selector(
                page, selected_bucket, on_folder_selected, folders
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
