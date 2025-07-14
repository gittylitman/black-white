import flet as ft
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable
from classes.progress_bar import ProgressBar
from classes.alert_dialog import AlertDialog
from classes.text import Text
from classes.row import Row
from classes.column import Column
from classes.buttons import ElevatedButton, IconButton
from classes.file_picker import FilePicker
from config.const import COLORS, ERROR_MESSAGES, TEXTS, VALIDATION_MESSAGES, Run_Type, Env_Type
from modules.set_system_variable import get_env_instance
from utils.basic_function import show_message
from process.department_dropdown import dropdown
import subprocess


def show_progress_popup(
    page, file_paths: list, bucket: str, folder: str, action_func: Callable[[str, str, str], None]
) -> None:
    action_type = get_env_instance().ACTION_TYPE
    progress_controls = []

    for file_path in file_paths:
        file_name = os.path.basename(file_path.rstrip("/\\"))
        progress_bar = ProgressBar(width=150)
        status_text = Text(
            f"{action_type}...",
            color=COLORS.PROCESS_COLOR.value,
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        progress_row = Row(
            [
                ft.Icon(
                    ft.icons.FOLDER if os.path.isdir(file_path) else ft.icons.INSERT_DRIVE_FILE_OUTLINED,
                    color=COLORS.GRAY_COLOR.value,
                    size=24,
                ),
                Text(file_name, size=16, weight=ft.FontWeight.BOLD, expand=True),
                progress_bar,
                status_text,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        )

        progress_controls.append({
            "row": progress_row,
            "progress_bar": progress_bar,
            "status_text": status_text,
            "file_path": file_path
        })

    summary_text = Text(
        f"{action_type} file 1 of {len(file_paths)}...",
        size=14,
        color=COLORS.GRAY_COLOR.value,
        weight=ft.FontWeight.BOLD,
    )

    progress_dialog = AlertDialog(
        title=Text(f"{action_type} files/folders to GCP..."),
        content=Column(
            [pc["row"] for pc in progress_controls] + [summary_text],
            spacing=15,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        actions=[ft.TextButton("Close", on_click=lambda e: progress_dialog.close_dialog(page))],
        modal=True,
    )

    progress_dialog.open_dialog(page)

    def process_file(pc):
        """Upload a single file or directory."""
        file_path = pc["file_path"]
        progress_bar = pc["progress_bar"]
        status_text = pc["status_text"]

        try:
            status_text.value = f"{action_type}..."
            status_text.color = COLORS.PROCESS_COLOR.value
            page.update()

            if os.path.isdir(file_path):
                upload_directory_to_gcp(bucket, folder, file_path)
            else:
                upload_file_to_gcp(bucket, folder, file_path)

            progress_bar.value = 1.0
            progress_bar.color = COLORS.SUCCESS_COLOR.value
            status_text.value = "Success"
            status_text.color = COLORS.SUCCESS_COLOR.value

            return True
        except Exception as e:
            progress_bar.value = 1.0
            progress_bar.color = COLORS.FAILED_COLOR.value
            status_text.value = "Failed"
            status_text.color = COLORS.FAILED_COLOR.value
            return False
        finally:
            page.update()

    def worker():
        success_count = 0
        failure_count = 0

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_file, pc) for pc in progress_controls]

            for index, future in enumerate(as_completed(futures), start=1):
                result = future.result()
                if result:
                    success_count += 1
                else:
                    failure_count += 1

                summary_text.value = f"{success_count} succeeded, {failure_count} failed"
                page.update()

        summary_text.value = f"{action_type} completed: {success_count} succeeded, {failure_count} failed"
        page.update()

        if failure_count == 0:
            show_message(page, f"✅ All uploads completed successfully!", COLORS.SUCCESS_COLOR.value)
        else:
            show_message(page, f"⚠️ Some uploads failed: {failure_count} failed.", COLORS.ERROR_MESSAGES_COLORS.value)

    threading.Thread(target=worker, daemon=True).start()


def upload_file_to_gcp(bucket, folder, file_path):
    """Upload a single file to GCP."""
    command = [
        "gsutil", "cp", file_path, f"gs://{bucket}/{folder}/"
    ]
    run_command(command, file_path)


def upload_directory_to_gcp(bucket, folder, dir_path):
    """Upload an entire directory to GCP."""
    command = [
        "gsutil", "-m", "cp", "-r", dir_path, f"gs://{bucket}/{folder}/"
    ]
    run_command(command, dir_path)


def run_command(command, path):
    """Run subprocess command."""
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise Exception(f"Upload failed for {path}: {result.stderr}")


def upload_files(page: ft.Page, run_type: Run_Type, env_type: Env_Type) -> Column:
    """Upload files or folders to GCP."""
    selected_files = {"files": []}
    bucket = ""
    folder = ""

    def handle_folder_selection(selected_folder: str):
        """Handle bucket/folder selection."""
        nonlocal bucket, folder
        try:
            bucket, folder = selected_folder.split("/", 1)
            page.update()
        except ValueError:
            show_message(page, ERROR_MESSAGES.INVALID_FOLDER.value, COLORS.FAILED_COLOR.value)

    department_dropdown = dropdown(page, handle_folder_selection, run_type=run_type, env_type=env_type)

    file_picker = FilePicker(on_result=lambda e: select_file(e))

    def select_file(e):
        """Handle file/folder selection."""
        if e.files:
            selected_files["files"] = e.files
            update_file_label(len(selected_files["files"]))
        else:
            reset_file_selection()

    def update_file_label(file_count: int):
        file_label.value = f"Selected {file_count} items."
        page.update()

    def reset_file_selection():
        selected_files["files"] = []
        file_label.value = VALIDATION_MESSAGES.NO_FILES_ALERT.value
        page.update()

    def upload_file(e):
        try:
            if validate_upload():
                file_paths = [file.path for file in selected_files["files"]]
                show_progress_popup(page, file_paths, bucket, folder, action_func=None)
            else:
                show_alert_not_found()
        except Exception as ex:
            error_message = ERROR_MESSAGES.ERROR_DURING_UPLOAD.format(ex)
            show_message(page, error_message, COLORS.FAILED_COLOR.value)

    def validate_upload() -> bool:
        return bool(selected_files["files"]) and bucket and folder

    def show_alert_not_found():
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
        tooltip="Choose files or folders",
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=True,
            allow_directory_selection=True,
        ),
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
        controls=[upload_icon_button, file_label, file_picker, department_dropdown, upload_button, back_button],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
