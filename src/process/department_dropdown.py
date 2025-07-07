from typing import Any

from utils.gcloud_calls import set_gcloud_project
from utils.basic_function import show_message
from modules.set_system_variable import get_env_instance
from classes.column import Column
from classes.text import Text
from classes.container import Container
from classes.dropdown import Dropdown
from config.const import TEXTS, VALIDATION_MESSAGES, ERROR_MESSAGES

import flet as ft
from config.const import Run_Type, Departments, TEXTS

def get_department(env: str, run_type: Run_Type) -> Departments:
    for dept in Departments:
        if dept.env == env and dept.run_type == run_type:
            return dept
    raise ValueError(ERROR_MESSAGES.DEPARTMENT_NOT_FOUND.value)


def get_bucket_by_run_type(run_type):
    ENVIRONMENT_TYPE = get_env_instance().ENVIRONMENT_TYPE
    department = get_department(ENVIRONMENT_TYPE, run_type)
    bucket = department.department_bucket
    return bucket


def dropdown(
    page: ft.Page,
    on_folder_selected: Any,
    run_type: Run_Type
) -> Container:
    
    try:
        bucket = get_bucket_by_run_type(run_type)
    except ValueError as e:
        error_message = ERROR_MESSAGES.BASIC_ERROR_MESSAGE.format(str(e))
        show_message(page, error_message, ft.colors.RED)
        return Container()
    
    result_container = Container()
    selected_folder_text = Text("")
    selected_folder = ""

    def get_folders_list(bucket: str):
        # result = set_gcloud_project(bucket, page)
        # if result != []:
        #     return result
        # TODO: implement actual fetching
        return  ['folder a', 'folder b', 'folder c', 'folder d']

    def on_change_folder(e: ft.ControlEvent, selected_bucket: str):
        nonlocal selected_folder
        selected_folder = e.control.value
        if selected_folder:
            on_folder_selected(f"{selected_bucket}/{selected_folder}")
            page.update()

    def on_change_dropdown(e: ft.ControlEvent):
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
            folder_dropdown = Dropdown(
                label=TEXTS.CHOOSE_FOLDER.value,
                options=[ft.dropdown.Option(folder) for folder in folders],
                width=300,
                on_change=lambda e: on_change_folder(e, selected_bucket)
            )
            result_container.content = folder_dropdown
            page.update()
        except Exception as ex:
            error_message =  ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value.format(str(ex))
            show_message(page, error_message, ft.colors.RED)

    department_dropdown = Dropdown(
        label=TEXTS.CHOOSE_DEPARTMENT.value,
        options=[
            ft.dropdown.Option(text=item.department, key=item.bucket)
            for item in bucket
        ],
        width=300,
        on_change=on_change_dropdown
    )

    return Container(
        content=Column(
            controls=[
                department_dropdown,
                result_container,
                selected_folder_text
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        height=130,
    )
