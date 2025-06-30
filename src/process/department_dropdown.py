import string
from typing import Any
from classes.dropdown import Dropdown
import flet as ft
from config.const import Run_Type, Departments, TEXTS


def get_department(env: str, run_type: Run_Type) -> Departments:
    for dept in Departments:
        if dept.env == env and dept.run_type == run_type:
            return dept
    raise ValueError("Department not found")


def drop_down(page: ft.Page, on_folder_selected: Any, env: string = "dev", run_type: Run_Type = Run_Type.BLACK) -> Dropdown:
    department = get_department(env, run_type)
    bucket = department.department_bucket
    
    result_container = ft.Container()
    selected_folder_text = ft.Text("") 
    
    def on_change_dropdown(e: ft.ControlEvent):
        selected_bucket = e.control.value
        folders = get_folders_list(selected_bucket)
        
        if not folders:
            selected_folder_text.value = "No folders available."
            page.update()
            return
        
        folder_dropdown = Dropdown(
            label=TEXTS.CHOOSE_FOLDER.value,
            options=[
                ft.dropdown.Option(folder)
                for folder in folders
            ],
            width=300,
            on_change=lambda e: on_change_folder(e, on_folder_selected, selected_bucket)
        )
        result_container.content = folder_dropdown
        page.update()

    def on_change_folder(e: ft.ControlEvent, on_folder_selected, selected_bucket):
        selected_folder = e.control.value
        if selected_folder:
            on_folder_selected(f"{selected_bucket}/{selected_folder}")
            selected_folder_text.value = f"Selected folder: {selected_folder}"
            page.update()

        
    def get_folders_list(bucket : string):
        #TODO fetch folders
        return ['folder a', 'folder b', 'folder c', 'folder d']
    
    dropdown = Dropdown(
        label=TEXTS.CHOOSE_DEPARTMENT.value,
        options=[
            ft.dropdown.Option(text=item.department, key=item.bucket)
            for item in bucket
        ],
        width=300,
        on_change=on_change_dropdown
    )

    page.add(dropdown, result_container, selected_folder_text)
