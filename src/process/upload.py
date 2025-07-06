from classes.text import Text
from classes.buttons import IconButton
from classes.file_picker import FilePicker
from classes.column import Column
from utils.basic_function import show_message
from process.department_dropdown import dropdown
from config.const import TEXTS, Run_Type
import flet as ft



def upload_files(page: ft.Page, run_type: Run_Type)-> Column:
    selected_files = {"files": []}
    bucket = ""
    folder = ""

    def handle_folder_selection(selected_folder: str):
        nonlocal bucket, folder
        try:
            bucket, folder = selected_folder.split("/", 1)
            #TODO: handle selected bucket and folder
            page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(Text(TEXTS.INVALID_FOLDER.value))
            page.snack_bar.open = True
            page.update()

    department_dropdown = dropdown(page, handle_folder_selection, run_type=run_type)

    file_picker = FilePicker(
        on_result=lambda e: select_file(e)
    )

    def select_file(e):
        if e.files:
            selected_files["files"] = e.files
            update_file_label(len(selected_files["files"]))
        else:
            reset_file_selection()
        
    def update_file_label(file_count: int) -> None:
        file_label.value = f"Selected {file_count} files."
        page.update()    
        
    def reset_file_selection() -> None:
        selected_files["files"] = []
        file_label.value = TEXTS.NO_FILES_ALERT.value
        page.update()

    def upload_file(e) -> None:
        try:
            if validate_upload():
                # TODO: please add here code to upload files.
                # TODO: Implement the file upload logic here
                # upload_page(page, selected_files["files"])
                page.update()
            else:
                show_alert()
        except Exception as ex:
            error_message = f"Error during upload: {str(ex)}"
            show_message(page, error_message, ft.colors.RED)
        

        
    def validate_upload() -> bool:
        return bool(selected_files["files"]) and bucket and folder

    def show_alert() -> None:
        alert_message = TEXTS.NO_FOLDER_OR_BUCKET.value if not bucket or not folder else TEXTS.NO_FILES_ALERT.value
        show_message(page, alert_message, ft.colors.ORANGE)
            
    upload_icon_button=IconButton(
        icon=ft.icons.ARROW_UPWARD,
        icon_color = ft.colors.LIGHT_BLUE_ACCENT_200,
        icon_size=70,
        tooltip=TEXTS.CHOOSE_FILES.value,
        on_click=lambda e: file_picker.pick_files(allow_multiple = True),
        border_radius=5
    )

    file_label = Text(TEXTS.CHOOSE_FILES.value, size=30)

    upload_button = ft.ElevatedButton(
        text=TEXTS.UPLOAD_BUTTON.value ,
        on_click=upload_file,
        width=200
    )

    return Column(
        controls=[
            upload_icon_button,
            file_label,
            file_picker,
            department_dropdown,
            upload_button
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
