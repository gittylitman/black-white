from modules.set_system_variable import get_env_instance
from classes.text import Text
from classes.column import Column
from classes.column import Column
from classes.buttons import ElevatedButton
from config.const import TEXTS, Run_Type, COLORS
import flet as ft


def display_upload_page(page: ft.Page, run_type: Run_Type):
    from process.upload import upload_files
    page.controls.clear()
    background_container = ft.Container(
        bgcolor=COLORS.BACKGROUND_COLOR.value,
        padding=20,
        width=page.width,
        height=page.height,
    )
    background_container.content = upload_files(page, run_type)
    page.add(background_container)
    page.update()
def display_download_page(page: ft.Page, run_type: Run_Type):
    from process.download import download_files
    page.controls.clear()
    background_container = ft.Container(
        bgcolor=COLORS.BACKGROUND_COLOR.value,
        padding=20,
        width=page.width,
        height=page.height,
    )
    background_container.content = download_files(page, run_type) 
    page.add(background_container)
    page.update()






def starting_point(page: ft.Page)-> Column:
    ACTION_TYPE = get_env_instance().ACTION_TYPE
    page.controls.clear()

    background_container = ft.Container(
        bgcolor=COLORS.BACKGROUND_COLOR.value,
        padding=20,
        width=page.width,
        height=page.height,
    )
    title = Text(
        TEXTS.BASIC_TITLE.value, 
        size=50,
        elevation=5,
        weight=ft.FontWeight.BOLD, 
        color=COLORS.MAIN_COLOR.value,
        text_align=ft.TextAlign.CENTER,
        )

    upload_button = ElevatedButton(
        text=TEXTS.UPLOAD_BUTTON.value,
        icon = ft.icons.CLOUD_UPLOAD_OUTLINED,
        on_click = lambda e: display_upload_page(page, Run_Type.UPLOAD), 
        width=200,
    )
    download_button = ElevatedButton(
        text=TEXTS.DOWNLOAD_BUTTON.value,
        icon = ft.icons.CLOUD_DOWNLOAD_OUTLINED,
        on_click=lambda e: display_download_page(page, Run_Type.DOWNLOAD),
        width=200
    )

    main_column = ft.Column(
            controls=[
                title,
                upload_button if ACTION_TYPE == 'Upload' else download_button
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    background_container.content = main_column
    page.add(background_container)
    page.update()
