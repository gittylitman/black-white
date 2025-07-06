from process.starting_point import starting_point
from config.const import TEXTS

import flet as ft


def main(page: ft.Page):
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = TEXTS.PAGE_TITLE.value
    starting_point(page)

ft.app(target=main)
