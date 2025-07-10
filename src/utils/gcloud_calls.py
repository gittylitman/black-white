import subprocess

import flet as ft
from config.const import ERROR_MESSAGES
from utils.basic_function import show_message
    
def get_folders_and_files(page, bucket_name: str):
    try:
        result = subprocess.run(
            ["gcloud", "storage", "ls", "--recursive", "--format=gsutil", f"gs://{bucket_name}/"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            show_message(page, ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value, ft.colors.ORANGE)
            return {}
        return result.stdout
    except Exception as e:
        show_message(page, ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value, ft.colors.RED)
        return {}

def get_files_from_folder(page, bucket_name: str, folder: str):
    try:
        result = subprocess.run(
            ["gcloud", "storage", "ls", f"gs://{bucket_name}/{folder}/"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            show_message(page, ERROR_MESSAGES.INVALID_FOLDER.value, ft.colors.ORANGE)
            return {}
        return result.stdout
    except Exception:
        show_message(page, ERROR_MESSAGES.INVALID_FOLDER.value, ft.colors.RED)
        return {}
