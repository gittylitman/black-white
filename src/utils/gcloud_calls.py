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

def upload_files_to_gcp(bucket_name: str, files: list):
    try:
        command = ["gsutil", "cp"] + files + [f"gs://{bucket_name}/"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return False
        return True

    except Exception as e:
        return False
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
