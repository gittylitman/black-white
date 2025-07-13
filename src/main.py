from process.login import setup_ui
from config.const import TEXTS
from modules.set_system_variable import get_env_instance
import flet as ft
import os

gcloud_path = get_env_instance().GCLOUD_PATH

gcloud_path = gcloud_path
os.environ["PATH"] = gcloud_path + os.pathsep + os.environ["PATH"]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = TEXTS.PAGE_TITLE.value
    page.scroll = ft.ScrollMode.AUTO
    setup_ui(page)


ft.app(target=main)
