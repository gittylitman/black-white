from classes.text import Text
from classes.column import Column
from classes.column import Column
from classes.buttons import ElevatedButton
from config.const import TEXTS, Run_Type
import flet as ft

def display_upload_page(page: ft.Page, run_type: Run_Type):
    from process.upload import upload_files
    page.controls.clear()
    upload_column = upload_files(page, run_type)  
    page.add(upload_column)
    page.update()
    
def display_download_page(page: ft.Page, run_type: Run_Type):
    from process.download import download_files
    page.controls.clear()
    download_column = download_files(page, run_type)  
    page.add(download_column)
    page.update()
        

def starting_point(page: ft.Page)-> Column:
    page.controls.clear()
    title = Text(TEXTS.BASIC_TITLE.value, size=50, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_ACCENT_200)

    upload_button = ElevatedButton(
        text=TEXTS.UPLOAD_BUTTON.value,
        on_click = lambda e: display_upload_page(page, Run_Type.UPLOAD), 
        width=200
    )
    download_button = ElevatedButton(
        text=TEXTS.DOWNLOAD_BUTTON.value,
        on_click=lambda e: display_download_page(page, Run_Type.DOWNLOAD),
        width=200
    )
    
    main_column = ft.Column(
            controls=[
                title,
                upload_button,
                download_button
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    page.add(main_column)
    page.update()
