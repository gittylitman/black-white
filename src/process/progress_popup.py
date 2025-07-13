import flet as ft
import threading
from classes.progress_bar import ProgressBar
from classes.text import Text
from classes.row import Row
from config.const import COLORS
from classes.column import Column
from modules.set_system_variable import get_env_instance
from utils.basic_function import show_message

def show_progress_popup(page, file_paths: list, bucket: str, folder:str,action_func):
    action_type = get_env_instance().ACTION_TYPE
    progress_controls = []

    for file_path in file_paths:
        file_name = file_path.split("/")[-1]
        progress_bar = ProgressBar(width=150)
        status_text = Text(f"{action_type}...", color=COLORS.PROCESS_COLOR, size=14, weight=ft.FontWeight.BOLD)

        progress_row = Row([
            ft.Icon(ft.icons.INSERT_DRIVE_FILE_OUTLINED, color=COLORS.GRAY_COLOR, size=24),
            Text(file_name, size=16, weight=ft.FontWeight.BOLD, expand=True),
            progress_bar,
            status_text
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10)

        progress_controls.append({
            "row": progress_row,
            "progress_bar": progress_bar,
            "status_text": status_text
        })

    summary_text = Text(
        f"{action_type} file 1 of {len(file_paths)}...",
        size=14, color=COLORS.GRAY_COLOR, weight=ft.FontWeight.BOLD
    )

    progress_dialog = ft.AlertDialog(
        title=Text(f"{action_type} files to GCP..."),
        content=Column(
            [pc["row"] for pc in progress_controls] + [summary_text],
            spacing=15,
            scroll=ft.ScrollMode.ALWAYS
        ),
        actions=[
            ft.TextButton("Close", on_click=lambda e: close_dialog())
        ],
        modal=True
    )

    def close_dialog():
        progress_dialog.open = False
        page.dialog = None
        page.update()

    page.dialog = progress_dialog
    progress_dialog.open = True
    page.update()

    def worker():
        success_count = 0
        failure_count = 0

        for index, (pc, file_path) in enumerate(zip(progress_controls, file_paths), start=1):
            progress_bar = pc["progress_bar"]
            status_text = pc["status_text"]

            summary_text.value = f"{action_type} file {index} of {len(file_paths)}..."
            page.update()

            try:
                status_text.value = f"{action_type}..."
                status_text.color = COLORS.PROCESS_COLOR
                page.update()
                action_func(bucket, folder, file_path)
                progress_bar.value = 1.0
                progress_bar.color = COLORS.SUCCESS_COLOR.value
                status_text.value = "Success"
                status_text.color = COLORS.SUCCESS_COLOR.value
                page.update()
                success_count += 1
            except Exception as e:
                progress_bar.value = 1.0
                progress_bar.color = COLORS.FAILED_COLOR.value
                status_text.value = "Failed"
                status_text.color = COLORS.FAILED_COLOR.value
                page.update()
                failure_count += 1

            summary_text.value = f"{success_count} succeeded, {failure_count} failed"
            page.update()

        summary_text.value = f"{action_type} completed: {success_count} succeeded, {failure_count} failed"
        page.update()

        if failure_count == 0:
            show_message(page, f"✅ All files {action_type} successfully!", COLORS.SUCCESS_COLOR)
        else:
            show_message(page, f"⚠️ Some files failed: {failure_count} failed.", ft.colors.ORANGE)

    threading.Thread(target=worker, daemon=True).start()
