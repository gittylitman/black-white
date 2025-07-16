import os
import shutil
import tempfile
import flet as ft
from classes.text import Text
from classes.buttons import IconButton, ElevatedButton
from classes.file_picker import FilePicker
from classes.column import Column
from utils.basic_function import show_message
from utils.gcloud_calls import upload_files_to_gcp
from process.department_dropdown import dropdown
from config.const import (
    TEXTS,
    Run_Type,
    COLORS,
    VALIDATION_MESSAGES,
    ERROR_MESSAGES,
    Env_Type,
)
from process.progress_popup import show_progress_popup


def upload_files(page: ft.Page, run_type: Run_Type, env_type: Env_Type) -> Column:
    selected_files = {"files": []}
    bucket = ""
    folder = ""

    def handle_folder_selection(selected_folder: str):
        nonlocal bucket, folder
        try:
            bucket, folder = selected_folder.split("/", 1)
            page.update()
        except ValueError:
            show_message(page, ERROR_MESSAGES.INVALID_FOLDER.value, ft.colors.RED)

    department_dropdown = dropdown(
        page, handle_folder_selection, run_type=run_type, env_type=env_type
    )

    file_picker = FilePicker(on_result=lambda e: select_files(e))
    folder_picker = FilePicker(on_result=lambda e: select_folder(e))
    page.overlay.extend([file_picker, folder_picker])

    def select_files(e):
        if e.files:
            selected_files["files"] = e.files
            update_file_label(len(selected_files["files"]))
        else:
            reset_file_selection()

    def select_folder(e):
        if e.path:
            try:
                original_folder_name = os.path.basename(e.path)
                temp_dir = tempfile.gettempdir()
                zip_base_name = os.path.join(temp_dir, original_folder_name)
                zip_path = f"{zip_base_name}.zip"

                shutil.make_archive(
                    base_name=zip_base_name, format="zip", root_dir=e.path
                )

                selected_files["files"] = [
                    {"name": f"{original_folder_name}.zip", "path": zip_path}
                ]
                update_file_label(1)

            except Exception:
                show_message(
                    page, TEXTS.ERROR_UPLOAD_FOLDER.value, COLORS.FAILED_COLOR.value
                )
        else:
            reset_file_selection()

    def update_file_label(file_count: int) -> None:
        file_label.value = f"{TEXTS.CHOOSE_FILES.value}{file_count}"
        page.update()

    def reset_file_selection() -> None:
        selected_files["files"] = []
        file_label.value = VALIDATION_MESSAGES.NO_FILES_ALERT.value
        page.update()

    def upload_file(e) -> None:
        try:
            if validate_upload():
                file_paths = [
                    file.path if hasattr(file, "path") else file["path"]
                    for file in selected_files["files"]
                ]
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
            show_message(page, error_message, ft.colors.RED)

    def validate_upload() -> bool:
        return bool(selected_files["files"]) and bucket and folder

    def show_alert_not_found() -> None:
        alert_message = (
            VALIDATION_MESSAGES.NO_FOLDER_OR_BUCKET.value
            if not bucket or not folder
            else VALIDATION_MESSAGES.NO_FILES_ALERT.value
        )
        show_message(page, alert_message, ft.colors.ORANGE)

    upload_icon_button = IconButton(
        icon=ft.icons.UPLOAD_FILE,
        icon_color=COLORS.MAIN_COLOR.value,
        icon_size=70,
        tooltip=TEXTS.CHOOSE_FILES.value,
        on_click=lambda e: file_picker.pick_files(allow_multiple=True),
        border_radius=5,
    )

    folder_icon_button = IconButton(
        icon=ft.icons.FOLDER_OUTLINED,
        icon_color=COLORS.MAIN_COLOR.value,
        icon_size=70,
        tooltip=TEXTS.CHOOSE_FOLDER.value,
        on_click=lambda e: folder_picker.get_directory_path(),
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
            ft.Row(
                [upload_icon_button, folder_icon_button],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            file_label,
            file_picker,
            folder_picker,
            department_dropdown,
            upload_button,
            back_button,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
