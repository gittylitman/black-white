import subprocess
import os

import flet as ft
from config.const import ERROR_MESSAGES
from utils.basic_function import show_message
from config.const import COLORS


def get_folders_and_files(page, bucket_name: str):
    try:
        result = subprocess.run(
            ["cmd", "/c", "gcloud", "storage", "ls", "--recursive", "--format=gsutil", f"gs://{bucket_name}/"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            show_message(
                page, ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value, COLORS.ERROR_MESSAGES_COLORS.value
            )
            return ""
        return result.stdout
    except Exception as e:
        show_message(page, ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value, COLORS.FAILED_COLOR.value)
        return {}


def upload_files_to_gcp(bucket_name: str, folder_name: str, file_path: str) -> None:
    try:
        command = ["cmd", "/c", "gsutil", "cp", file_path, f"gs://{bucket_name}/{folder_name}"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise Exception(f"Failed to upload {file_path}: {result.stderr}")
    except Exception as e:
        raise str(e)


def get_files_from_folder(page, bucket_name: str, folder: str):
    try:
        result = subprocess.run(
            ["cmd", "/c", "gcloud", "storage", "ls", f"gs://{bucket_name}/{folder}/"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            show_message(page, ERROR_MESSAGES.INVALID_FOLDER.value, COLORS.ERROR_MESSAGES_COLORS.value)
            return ""
        return result.stdout
    except Exception:
        show_message(page, ERROR_MESSAGES.INVALID_FOLDER.value, COLORS.FAILED_COLOR.value)
        return ""


def download_files_from_gcp(page, bucket_name: str, folder_path: str, file_name: str):
    try:
        result = subprocess.run(
            ["cmd", "/c", "gsutil", "cp", f"gs://{bucket_name}/{folder_path}/{file_name}", "."],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            show_message(
                page, ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value, COLORS.ERROR_MESSAGES_COLORS.value
            )
            raise result.stderr
        return result.stdout
    except Exception as e:
        show_message(page, ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value,COLORS.FAILED_COLOR.value)
        raise result.stderr
