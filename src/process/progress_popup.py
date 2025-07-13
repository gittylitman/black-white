import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

import flet as ft
from classes.progress_bar import ProgressBar
from classes.alert_dialog import AlertDialog
from classes.text import Text
from classes.row import Row
from classes.column import Column
from config.const import COLORS
from modules.set_system_variable import get_env_instance
from utils.basic_function import show_message


def create_progress_row(file_name: str, action_type: str) -> dict:
    """Create a progress row UI control for a single file."""
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
                ft.icons.INSERT_DRIVE_FILE_OUTLINED,
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

    return {
        "row": progress_row,
        "progress_bar": progress_bar,
        "status_text": status_text,
    }


def process_file(
    pc: dict, bucket: str, folder: str, file_path: str, action_func: Callable
) -> bool:
    """Process a single file and update the progress UI."""
    progress_bar, status_text = pc["progress_bar"], pc["status_text"]

    try:
        status_text.value = "Processing..."
        status_text.color = COLORS.PROCESS_COLOR.value

        action_func(bucket, folder, file_path)

        progress_bar.value = 1.0
        progress_bar.color = COLORS.SUCCESS_COLOR.value
        status_text.value = "Success"
        status_text.color = COLORS.SUCCESS_COLOR.value

        return True
    except Exception:
        progress_bar.value = 1.0
        progress_bar.color = COLORS.FAILED_COLOR.value
        status_text.value = "Failed"
        status_text.color = COLORS.FAILED_COLOR.value

        return False


def show_progress_popup(
    page, file_paths: list, bucket: str, folder: str, action_func: Callable[[str, str, str], None]
) -> None:
    """Show the popup display with the running progress"""
    action_type = get_env_instance().ACTION_TYPE
    progress_controls = []

    for file_path in file_paths:
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        pc = create_progress_row(file_name, action_type)
        pc["file_path"] = file_path
        progress_controls.append(pc)

    summary_text = Text(
        f"{action_type} file 1 of {len(file_paths)}...",
        size=14,
        color=COLORS.GRAY_COLOR.value,
        weight=ft.FontWeight.BOLD,
    )

    progress_dialog = AlertDialog(
        title=f"{action_type} files to GCP...",
        content=Column(
            [pc["row"] for pc in progress_controls] + [summary_text],
            spacing=15,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        actions=[ft.TextButton("Close", on_click=lambda e: progress_dialog.close_dialog(page))],
    )

    progress_dialog.open_dialog(page)

    def worker():
        success_count = 0
        failure_count = 0

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(
                    process_file, pc, bucket, folder, pc["file_path"], action_func
                )
                for pc in progress_controls
            ]

            for future in as_completed(futures):
                if future.result():
                    success_count += 1
                else:
                    failure_count += 1

                summary_text.value = (
                    f"{success_count} succeeded, {failure_count} failed"
                )
                page.update()

        summary_text.value = f"{action_type} completed: {success_count} succeeded, {failure_count} failed"
        page.update()

        if failure_count == 0:
            show_message(
                page, f"✅ All files {action_type} successfully!", COLORS.SUCCESS_COLOR.value
            )
        else:
            show_message(
                page, f"⚠️ Some files failed: {failure_count} failed.", COLORS.ERROR_MESSAGES_COLORS.value
            )

    threading.Thread(target=worker, daemon=True).start()
    