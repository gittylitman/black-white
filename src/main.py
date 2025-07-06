import flet as ft
import subprocess
import re
import threading


def setup_ui(page, context):
    context["login_button"] = ft.ElevatedButton("Sign in with Google")
    context["status_text"] = ft.Text()
    context["auth_code_field"] = ft.TextField(label="Paste the verification code here", visible=False)
    context["confirm_button"] = ft.ElevatedButton("Confirm verification code", visible=False)
    context["hello_text"] = ft.Text(visible=False)

    context["login_button"].on_click = lambda e: threading.Thread(target=start_gcloud_login, args=(page, context)).start()
    context["confirm_button"].on_click = lambda e: handle_auth_code_submission(page, context)

    page.add(
        context["login_button"],
        context["status_text"],
        context["auth_code_field"],
        context["confirm_button"],
        context["hello_text"]
    )


def start_gcloud_login(page, context):
    context["login_button"].disabled = True
    page.update()

    try:
        process = subprocess.Popen(
            ["gcloud", "auth", "login", "--no-launch-browser"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True
        )

        while True:
            line = process.stdout.readline()
            if not line:
                break

            if "https://accounts.google.com/o/oauth2/auth?" in line:
                match = re.search(r"(https://accounts\.google\.com/o/oauth2/auth\?[^ \n]+)", line)
                if match:
                    url = match.group(1)

                    page.launch_url(url)

                    context["status_text"].value = (
                        "1. Sign in with Google\n"
                        "2. Copy the verification code that appears in the browser\n"
                        "3. Paste it here and click 'Next'"
                    )
                    context["auth_code_field"].visible = True
                    context["confirm_button"].visible = True
                    context["process"] = process
                    break

    except Exception as e:
        context["status_text"].value = f"Error while running gcloud: {e}"

    context["login_button"].disabled = False
    page.update()


def handle_auth_code_submission(page, context):
    code = context["auth_code_field"].value.strip()
    if not code:
        context["status_text"].value = "Verification code must be entered."
        page.update()
        return

    process = context.get("process")
    if not process:
        context["status_text"].value = "The gcloud process is no longer available.😢"
        page.update()
        return


    try:
        process.stdin.write(code + "\n")
        process.stdin.flush()

        output, _ = process.communicate(timeout=30)

        if process.returncode == 0:
            context["status_text"].value = "🎉 You have successfully logged in! Loading user information..."
            page.update()

            account_result = subprocess.run(
                ["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"],
                capture_output=True,
                text=True
            )

            if account_result.returncode == 0:
                user_email = account_result.stdout.strip()
                context["status_text"].visible = False
                context["auth_code_field"].visible = False
                context["confirm_button"].visible = False
                context["login_button"].visible = False

                context["hello_text"].value = f"👋 Hello, {user_email}"
                context["hello_text"].visible = True
            else:
                context["status_text"].value = "You logged in, but the username could not be retrieved."

        else:
            context["status_text"].value = f"שגיאה:\n{output}"

    except Exception as e:
        context["status_text"].value = f"Error sending code: {e}"

    page.update()


def main(page: ft.Page):
    context = {}  
    setup_ui(page, context)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
from classes.buttons import ElevatedButton
from classes.text import Text
from config.const import TEXTS
from process.download import download_files
from config.const import Run_Type
from process.upload import upload_files

import flet as ft


def main(page: ft.Page):
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = TEXTS.PAGE_TITLE.value

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

    page.add(
        ft.Column(
            controls=[
                title,
                upload_button,
                download_button
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def display_upload_page(page: ft.Page, run_type: Run_Type):
    page.controls.clear()
    upload_column = upload_files(page, run_type)  
    page.add(upload_column)
    page.update()

def display_download_page(page: ft.Page, run_type: Run_Type):
    page.controls.clear()
    download_column = download_files(page, run_type)  
    page.add(download_column)
    page.update()
    
ft.app(target=main)
