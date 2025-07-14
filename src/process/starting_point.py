from classes.column import Column
from classes.buttons import ElevatedButton
from config.const import Run_Type, COLORS, Env_Type
import flet as ft

from modules.set_system_variable import get_env_instance


def display_upload_page(page: ft.Page, run_type: Run_Type, env_type:Env_Type):
    from process.upload import upload_files

    page.controls.clear()
    background_container = ft.Container(
        bgcolor=COLORS.BACKGROUND_COLOR.value,
        padding=20,
        width=page.width,
        height=page.height,
    )
    background_container.content = upload_files(page, run_type, env_type)
    page.add(background_container)
    page.update()

def display_download_page(page: ft.Page, run_type: Run_Type, env_type:Env_Type):
    from process.download import download_files

    page.controls.clear()
    background_container = ft.Container(
        bgcolor=COLORS.BACKGROUND_COLOR.value,
        padding=20,
        width=page.width,
        height=page.height,
    )
    background_container.content = download_files(page, run_type, env_type) 
    page.add(background_container)
    page.update()


def starting_point(page: ft.Page)-> Column:
    """Display the splash screen according to the type of operation."""
    page.controls.clear()

    background_container = ft.Container(
        bgcolor=COLORS.BACKGROUND_COLOR.value,
        padding=20,
        width=page.width,
        height=page.height,
    )

    dev_button = ElevatedButton(
        text = Env_Type.DEV.value,
        on_click = lambda e: set_env_type(page, Env_Type.DEV.value), 
        width=200,
    )
    prod_button = ElevatedButton(
        text = Env_Type.PROD.value,
        on_click=lambda e: set_env_type(page, Env_Type.PROD.value),
        width=200
    )

    main_column = ft.Column(
            controls=[
                prod_button, dev_button
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    background_container.content = main_column
    page.add(background_container)
    page.update()

def set_env_type(page: ft.Page, env_type: Env_Type):
    ACTION_TYPE = get_env_instance().ACTION_TYPE

    if ACTION_TYPE == Run_Type.UPLOAD.value:
        display_upload_page(page, Run_Type.UPLOAD, env_type)
    else:
        display_download_page(page, Run_Type.DOWNLOAD, env_type)

