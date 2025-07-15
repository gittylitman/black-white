from classes.text import Text
from process.department_dropdown import dropdown
from classes.container import Container
from classes.checkbox import Checkbox
from classes.row import Row
from classes.column import Column
from classes.buttons import ElevatedButton
from config.const import (
    TEXTS,
    Run_Type,
    COLORS,
    ERROR_MESSAGES,
    VALIDATION_MESSAGES,
    Env_Type,
)
from utils.basic_function import show_message
from utils.gcloud_calls import get_files_from_folder, download_files_from_gcp
from process.progress_popup import show_progress_popup

import flet as ft


def download_files(page: ft.Page, run_type: Run_Type, env_type: Env_Type) -> Column:
    """Creates a UI for downloading files from a specified bucket and folder."""
    selected_files = []
    bucket = ""
    folder = ""
    files = []
    checkboxes = {}
    checkbox_container = Container(width=300, height=100)

    def handle_folder_selection(selected_folder: str) -> None:
        """Handles the selection of a folder and updates the file list."""
        nonlocal bucket, folder, files, checkboxes
        try:
            bucket, folder = selected_folder.split("/", 1)
            checkboxes.clear()
            checkbox_container.content = Row(controls=[])

            if bucket and folder:
                files = get_files(bucket, folder)
                update_checkboxes()
                page.update()
            page.update()
        except ValueError:
            show_message(
                page,
                ERROR_MESSAGES.INVALID_FOLDER.value,
                COLORS.VALID_MESSAGES_COLORS.value,
            )

    def update_checkboxes() -> None:
        """Updates the checkbox container with the list of files."""
        for file in files:
            checkboxes[file] = Checkbox(label=file, on_change=select_file, value=False)
        checkbox_container.content = Row(
            [
                Column(
                    controls=list(checkboxes.values()),
                    alignment=ft.MainAxisAlignment.START,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.START,
            width=300,
            scroll=ft.ScrollMode.AUTO,
        )

    def get_files(bucket: str, folder: str) -> list[str]:
        """Fetches files from the specified bucket and folder."""
        files_result = get_files_from_folder(page, bucket, folder)
        list_folders_and_files = files_result.split("\n")
        list_files = [
            file.split("/").pop()
            for file in list_folders_and_files
            if not file.endswith("/") and not file.endswith(":") and file
        ]
        return list_files

    department_dropdown = dropdown(
        page, handle_folder_selection, run_type=run_type, env_type=env_type
    )

    def select_file(e) -> None:
        """Updates the list of selected files based on checkbox states."""
        nonlocal selected_files
        selected_files = [file for file in files if checkboxes[file].value]
        update_file_label(len(selected_files))

    def update_file_label(file_count: int) -> None:
        """Updates the label showing the number of selected files."""
        file_label.value = f"Selected {file_count} files."
        page.update()

    def download_file(e) -> None:
        """Handles the file download action."""
        try:
            if validate_download():
                show_progress_popup(
                    page,
                    selected_files,
                    bucket,
                    folder,
                    action_func=lambda bucket,
                    folder,
                    file_path: download_files_from_gcp(page, bucket, folder, file_path),
                )
                show_message(
                    page,
                    f"✅ Downloaded {len(selected_files)} files successfully!",
                    COLORS.SUCCESS_COLOR.value,
                )
                page.update()
            else:
                show_alert_not_found()
        except Exception as ex:
            error_message = ERROR_MESSAGES.ERROR_DURING_DOWNLOAD.format(str(ex))
            show_message(page, error_message, COLORS.VALID_MESSAGES_COLORS.value)

    def validate_download() -> bool:
        """Validates the download action."""
        return len(selected_files) > 0 and bucket and folder

    def show_alert_not_found() -> None:
        """Shows an alert if the download validation fails."""
        alert_message = (
            VALIDATION_MESSAGES.NO_FOLDER_OR_BUCKET.value
            if not bucket or not folder
            else VALIDATION_MESSAGES.NO_FILES_ALERT.value
        )
        show_message(page, alert_message, COLORS.VALID_MESSAGES_COLORS.value)

    download_icon = ft.Icon(
        color=COLORS.MAIN_COLOR.value,
        name=ft.icons.CLOUD_DOWNLOAD_OUTLINED,
        size=70,
    )

    file_label = Text(TEXTS.CHOOSE_FILES.value, size=30, color=COLORS.MAIN_COLOR.value)

    download_button = ElevatedButton(
        text=TEXTS.DOWNLOAD_BUTTON.value, on_click=download_file, width=200
    )

    from process.starting_point import starting_point

    back_button = ElevatedButton(
        text=TEXTS.BACK_TO_MAIN.value,
        on_click=lambda e: starting_point(page),
        width=200,
    )

    column = Column(
        controls=[
            download_icon,
            file_label,
            department_dropdown,
            checkbox_container,
            download_button,
            back_button,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return column
