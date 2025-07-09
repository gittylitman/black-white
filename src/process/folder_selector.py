import flet as ft
from typing import Callable

from classes.text import Text
from classes.buttons import ElevatedButton, IconButton
from classes.column import Column
from classes.row import Row
from classes.container import Container
from config.const import COLORS, TEXTS,ERROR_MESSAGES

def get_folders_in_path(bucket: str, folders, path: str = ""):
    return folders.get(path.strip("/"), [])

def hierarchical_folder_selector(
    page: ft.Page,
    bucket: str,
    on_folder_selected: Callable[[str], None],
    folders,
) -> Container:

    current_path = ""
    path_stack = []
    folder_column = Column(spacing=10, scroll=ft.ScrollMode.AUTO, controls=[])
    folder_scroll_container = Container(
        content=folder_column,
        height=130,
        width=300,
        alignment=ft.alignment.center
    )
    current_path_text = Text(text="", size=20, color=COLORS.MAIN_COLOR.value, width= 500)
    chosen_folder = Text(text=TEXTS.CHOSEN_FOLDER.value + TEXTS.NONE.value, size=12, color=COLORS.MAIN_COLOR.value)

    def update_folder_list():
        nonlocal folders
        folders_chosen = get_folders_in_path(bucket, folders, current_path)
        folder_column.controls.clear()

        if folders_chosen:
            for folder in folders_chosen:
                row = ft.Row([
                    ft.TextButton(
                        icon = ft.icons.CREATE_NEW_FOLDER_ROUNDED,
                        text=folder,
                        on_click=lambda e, f=folder: enter_folder(f),
                        style=ft.ButtonStyle(
                            color={ft.ControlState.DEFAULT: COLORS.MAIN_COLOR.value},
                        )
                    )
                ], alignment=ft.MainAxisAlignment.START, spacing=5)
                folder_column.controls.append(row)
        else:
            folder_column.controls.append(Text(TEXTS.NO_SUBFOLDER.value, color=COLORS.MAIN_COLOR.value))

        current_path_display = TEXTS.CURRENT_PATH.value + current_path if current_path else TEXTS.CHOOSE_FOLDER.value
        current_path_text.value = current_path_display
        page.update()

    def enter_folder(folder: str):
        nonlocal current_path
        path_stack.append(current_path)
        current_path = f"{current_path}/{folder}".strip("/")
        update_folder_list()

    def go_back(e):
        nonlocal current_path
        if path_stack:
            current_path = path_stack.pop()
            update_folder_list()
        chosen_folder.value = TEXTS.CHOSEN_FOLDER.value + TEXTS.NONE.value
        on_folder_selected(f"{bucket}/")

    def choose_this_folder(e):
        full_path = f"{bucket}/{current_path}".strip("/")
        chosen_folder.value = TEXTS.CHOSEN_FOLDER.value + current_path
        on_folder_selected(full_path)
        page.update()

    back_button = IconButton(
        icon = ft.icons.ARROW_BACK_OUTLINED,
        icon_color = COLORS.MAIN_COLOR.value,
        on_click=go_back, 
        icon_size=20,
        tooltip=TEXTS.BACK_TO_MAIN.value
        )
    choose_button = IconButton(
        icon = ft.icons.CHECK_BOX_OUTLINED, 
        icon_color = COLORS.MAIN_COLOR.value, 
        on_click=choose_this_folder, 
        icon_size=20,
        tooltip=TEXTS.CHOOSE_FOLDER.value
    )

    buttons_row = Row([
        back_button,
        choose_button
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)


    chosen_folder_column = Column(scroll=ft.ScrollMode.AUTO, controls=[chosen_folder], height=17)
    current_path_text_column = Column( scroll=ft.ScrollMode.AUTO, controls=[current_path_text], height=25)
    main_column = Column([
        current_path_text_column,
        chosen_folder_column,
        folder_scroll_container,
        buttons_row
    ], spacing=10, alignment=ft.MainAxisAlignment.START)

    container = Container(
        content=main_column,
        alignment=ft.alignment.top_center,
        width=300
    )

    update_folder_list()
    return container
