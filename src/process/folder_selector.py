from typing import Callable, Dict, List

import flet as ft

from classes.buttons import IconButton, ElevatedButton
from classes.column import Column
from classes.container import Container
from classes.row import Row
from classes.text import Text
from config.const import COLORS, TEXTS


def get_folders_in_path(folders: Dict[str, List[str]], path: str = "") -> List[str]:
    """Get the list of folders in a given path."""

    normalized_path = path.strip("/")
    return folders.get(normalized_path, [])


def hierarchical_folder_selector(
    page: ft.Page,
    bucket: str,
    on_folder_selected: Callable[[str], None],
    folders,
) -> Container:
    """Hierarchical folder selector."""
    current_path = ""
    path_stack = []
    folder_column = Column(spacing=10, scroll=ft.ScrollMode.AUTO, controls=[])
    folder_scroll_container = Container(
        content=folder_column, height=130, width=300, alignment=ft.alignment.center
    )
    current_path_text = Text(text="", size=20, width=500)
    chosen_folder = Text(
        text=TEXTS.CHOSEN_FOLDER.value + TEXTS.NONE.value,
        size=12,
    )

    def update_folder_list():
        """ "Update folder list."""
        nonlocal folders
        folders_chosen = get_folders_in_path(folders, current_path)
        folder_column.controls.clear()

        if folders_chosen:
            for folder in folders_chosen:
                row = ft.Row(
                    [
                        ft.TextButton(
                            icon=ft.icons.CREATE_NEW_FOLDER_ROUNDED,
                            text=folder,
                            on_click=lambda e, f=folder: enter_folder(f),
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.DEFAULT: COLORS.BLACK_COLOR.value
                                },
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=5,
                )
                folder_column.controls.append(row)
        else:
            folder_column.controls.append(Text(TEXTS.NO_SUBFOLDER.value))

        current_path_display = (
            TEXTS.CURRENT_PATH.value + current_path
            if current_path
            else TEXTS.CHOOSE_FOLDER.value
        )
        current_path_text.value = current_path_display
        page.update()

    def enter_folder(folder: str):
        """Enter folder"""
        nonlocal current_path
        path_stack.append(current_path)
        current_path = f"{current_path}/{folder}".strip("/")
        update_folder_list()

    def go_back(e):
        """Go back."""
        nonlocal current_path
        if path_stack:
            current_path = path_stack.pop()
            update_folder_list()
        chosen_folder.value = TEXTS.CHOSEN_FOLDER.value + TEXTS.NONE.value
        on_folder_selected(f"{bucket}/")

    def choose_this_folder(e):
        """Choose folder"""
        full_path = f"{bucket}/{current_path}".strip("/")
        chosen_folder.value = TEXTS.CHOSEN_FOLDER.value + current_path
        on_folder_selected(full_path)
        page.update()

    back_button = IconButton(
        icon=ft.icons.ARROW_BACK_OUTLINED,
        icon_color=COLORS.MAIN_COLOR.value,
        on_click=go_back,
        icon_size=20,
        tooltip=TEXTS.BACK_TO_MAIN.value,
    )
    choose_button = ElevatedButton(
        text=TEXTS.APPLY.value, on_click=choose_this_folder, width=150
    )

    buttons_row = Row(
        [back_button, choose_button], spacing=10, alignment=ft.MainAxisAlignment.CENTER
    )

    chosen_folder_column = Column(
        scroll=ft.ScrollMode.AUTO, controls=[chosen_folder], height=17
    )
    current_path_text_column = Column(
        scroll=ft.ScrollMode.AUTO, controls=[current_path_text], height=25
    )
    main_column = Column(
        [
            current_path_text_column,
            chosen_folder_column,
            folder_scroll_container,
            buttons_row,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )

    container = Container(
        content=main_column, alignment=ft.alignment.top_center, width=300
    )

    update_folder_list()
    return container
