import re
import subprocess
import threading

import flet as ft

from classes.buttons import ElevatedButton
from classes.column import Column
from classes.container import Container
from classes.input import Input
from classes.text import Text
from config.const import COLORS, ERROR_MESSAGES, TEXTS, VALIDATION_MESSAGES
from process.starting_point import starting_point
from utils.basic_function import show_message

gcloud_process = None


def setup_ui(page: ft.Page) -> None:
    """Initial screen setup."""
    background_container = _create_background_container(page)
    column = _create_main_column()
    title = _create_title()
    instructions = Text(TEXTS.INSTRUCTIONS.value, color=COLORS.MAIN_COLOR.value)
    login_button = ElevatedButton(
        TEXTS.SIGN_IN.value,
        on_click=lambda e: start_login_process(page, column, login_button),
    )

    column.controls = [title, instructions, login_button]
    background_container.content = column
    page.add(background_container)


def start_login_process(
    page: ft.Page, column: Column, login_button: ElevatedButton
) -> None:
    """Disables button and starts login thread."""
    login_button.disabled = True
    page.update()
    threading.Thread(
        target=perform_gcloud_login, args=(page, column, login_button), daemon=True
    ).start()


def perform_gcloud_login(
    page: ft.Page, column: Column, login_button: ElevatedButton
) -> None:
    """Launches gcloud login process and updates UI to input code."""
    global gcloud_process

    auth_code_field = Input(label=TEXTS.VERIFICATION_CODE.value)
    confirm_button = ElevatedButton(
        TEXTS.CONFIRM_VERIFICATION.value,
        on_click=lambda e: handle_auth_code_submission(
            page, auth_code_field.value, column, login_button
        ),
    )
    back_button = ElevatedButton(
        TEXTS.BACK_TO_MAIN.value,
        on_click=lambda e: reset_ui(page, column, login_button),
    )

    column.controls = [auth_code_field, confirm_button, back_button]
    page.update()
    
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        gcloud_process = subprocess.Popen(
            ["cmd", "/c", "gcloud", "auth", "login", "--no-launch-browser"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            startupinfo=startupinfo
        )
        google_account = "https://accounts.google.com/o/oauth2/auth?"
        rgx = r"(https://accounts\.google\.com/o/oauth2/auth\?[^ \n]+)"
        for line in iter(gcloud_process.stdout.readline, ""):
            if google_account in line:
                match = re.search(rgx, line)
                if match:
                    page.launch_url(match.group(1))
                    break

    except Exception as e:
        _handle_error(
            page, column, login_button, ERROR_MESSAGES.ERROR_RUNNING_GCLOUD.format(e)
        )


def handle_auth_code_submission(
    page: ft.Page, code: str, column: Column, login_button: ElevatedButton
) -> None:
    """Handles auth code submission and validation."""
    global gcloud_process

    code = code.strip()
    if not code:
        show_message(
            page,
            VALIDATION_MESSAGES.MISSING_VERIFICATION_CODE.value,
            COLORS.VALID_MESSAGES_COLORS.value,
        )
        return

    if not gcloud_process:
        show_message(
            page,
            ERROR_MESSAGES.GCLOUD_PROCESS_NOT_AVAILABLE.value,
            COLORS.VALID_MESSAGES_COLORS.value,
        )
        return

    try:
        gcloud_process.stdin.write(code + "\n")
        gcloud_process.stdin.flush()
        output, _ = gcloud_process.communicate(timeout=30)

        if gcloud_process.returncode == 0:
            show_message(page, TEXTS.LOGGED_IN.value, COLORS.SUCCESS_COLOR.value)
            starting_point(page)
        else:
            _handle_error(
                page,
                column,
                login_button,
                ERROR_MESSAGES.BASIC_ERROR_MESSAGE.format(output),
            )

    except Exception as e:
        _handle_error(
            page, column, login_button, ERROR_MESSAGES.ERROR_SENDING_CODE.format(e)
        )


def reset_ui(page: ft.Page, column: Column, login_button: ElevatedButton) -> None:
    """Resets UI to initial state."""
    login_button.disabled = False
    title = _create_title()
    instructions = Text(TEXTS.INSTRUCTIONS.value, color=COLORS.MAIN_COLOR.value)
    column.controls = [title, instructions, login_button]
    page.update()


def _create_title() -> Text:
    return Text(
        TEXTS.BASIC_TITLE.value,
        size=50,
        elevation=5,
        weight=ft.FontWeight.BOLD,
        color=COLORS.MAIN_COLOR.value,
        text_align=ft.TextAlign.CENTER,
    )


def _create_background_container(page) -> Container:
    return ft.Container(
        bgcolor=COLORS.BACKGROUND_COLOR.value,
        padding=20,
        width=page.width,
        height=page.height,
    )


def _create_main_column() -> Column:
    return Column(
        controls=[],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


def _handle_error(
    page: ft.Page, column: Column, login_button: ElevatedButton, message: str
) -> None:
    show_message(page, message, COLORS.FAILED_COLOR.value)
    reset_ui(page, column, login_button)
