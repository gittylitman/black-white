import os

import flet as ft

from config.const import TEXTS
from modules.set_system_variable import get_env_instance
from process.login import setup_ui

gcloud_path = get_env_instance().GCLOUD_PATH

os.environ["PATH"] = gcloud_path + os.pathsep + os.environ["PATH"]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = TEXTS.PAGE_TITLE.value
    page.scroll = ft.ScrollMode.AUTO
    setup_ui(page)


ft.app(target=main)
