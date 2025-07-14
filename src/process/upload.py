import flet as ft

from classes.buttons import ElevatedButton, IconButton
from classes.column import Column
from classes.file_picker import FilePicker
from classes.text import Text
from config.const import COLORS, ERROR_MESSAGES, TEXTS, VALIDATION_MESSAGES, Run_Type
from process.department_dropdown import dropdown
from process.progress_popup import show_progress_popup
from utils.basic_function import show_message
from utils.gcloud_calls import upload_files_to_gcp


def upload_files(page: ft.Page, run_type: Run_Type) -> Column:
    """Upload files to GCP."""
    selected_files = {"files": []}
    bucket = ""
    folder = ""

    def handle_folder_selection(selected_folder: str):
        """Select a folder where the files will be uploaded."""
        nonlocal bucket, folder
        try:
            bucket, folder = selected_folder.split("/", 1)
            page.update()
        except ValueError:
            show_message(
                page, ERROR_MESSAGES.INVALID_FOLDER.value, COLORS.FAILED_COLOR.value
            )

    department_dropdown = dropdown(page, handle_folder_selection, run_type=run_type)

    file_picker = FilePicker(on_result=lambda e: select_file(e))

    def select_file(e):
        """Selecting files to upload."""
        if e.files:
            selected_files["files"] = e.files
            update_file_label(len(selected_files["files"]))
        else:
            reset_file_selection()

    def update_file_label(file_count: int) -> None:
        """Update the tag showing the number of files selected for upload."""
        file_label.value = f"Selected {file_count} files."
        page.update()

    def reset_file_selection() -> None:
        selected_files["files"] = []
        file_label.value = VALIDATION_MESSAGES.NO_FILES_ALERT.value
        page.update()

    def upload_file(e) -> None:
        """Upload files"""
        try:
            if validate_upload():
                file_paths = [file.path for file in selected_files["files"]]
                show_progress_popup(
                    page,
                    file_paths,
                    bucket,
                    folder,
                    action_func=lambda bucket, folder, file_path: upload_files_to_gcp(
                        bucket, folder, file_path
                    ),
                )
            else:
                show_alert_not_found()
        except Exception as ex:
            error_message = ERROR_MESSAGES.ERROR_DURING_UPLOAD.format(ex)
            show_message(page, error_message, COLORS.FAILED_COLOR.value)

    def validate_upload() -> bool:
        """Checking the integrity of uploaded files."""
        return bool(selected_files["files"]) and bucket and folder

    def show_alert_not_found() -> None:
        """Show alert not found."""
        alert_message = (
            VALIDATION_MESSAGES.NO_FOLDER_OR_BUCKET.value
            if not bucket or not folder
            else VALIDATION_MESSAGES.NO_FILES_ALERT.value
        )
        show_message(page, alert_message, COLORS.ERROR_MESSAGES_COLORS.value)

    upload_icon_button = IconButton(
        icon=ft.icons.CLOUD_UPLOAD_OUTLINED,
        icon_color=COLORS.MAIN_COLOR.value,
        icon_size=70,
        tooltip=TEXTS.CHOOSE_FILES.value,
        on_click=lambda e: file_picker.pick_files(allow_multiple=True),
        border_radius=5,
    )

    file_label = Text(TEXTS.CHOOSE_FOLDER.value, size=30, color=COLORS.MAIN_COLOR.value)

    upload_button = ElevatedButton(
        text=TEXTS.UPLOAD_BUTTON.value, on_click=upload_file, width=200
    )

    from process.starting_point import starting_point

    back_button = ElevatedButton(
        text=TEXTS.BACK_TO_MAIN.value,
        on_click=lambda e: starting_point(page),
        width=200,
    )

    return Column(
        controls=[
            upload_icon_button,
            file_label,
            file_picker,
            department_dropdown,
            upload_button,
            back_button,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
