import subprocess
import os

from config.const import COLORS, ERROR_MESSAGES
from utils.basic_function import show_message


def set_project_id(project_id: str):
    """Set Project Id."""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result = subprocess.run(
        [
            "cmd",
            "/c",
            "gcloud",
            "config"
            "set",
            "project",
            project_id,
        ],
        capture_output=True,
        text=True,
        startupinfo=startupinfo,
    )
    if result.returncode != 0:
        raise Exception("not return code")
    return result.stdout


def get_folders_and_files(page, bucket_name: str):
    """Bringing the files and folders from GCP."""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(
            [
                "cmd",
                "/c",
                "gcloud",
                "storage",
                "ls",
                "--recursive",
                "--format=gsutil",
                f"gs://{bucket_name}/",
            ],
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
        )
        if result.returncode != 0:
            show_message(
                page,
                ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value,
                COLORS.VALID_MESSAGES_COLORS.value,
            )
            return ""
        return result.stdout
    except Exception:
        show_message(
            page, ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value, COLORS.FAILED_COLOR.value
        )
        return {}


def upload_files_to_gcp(bucket_name: str, folder_name: str, file_path: str) -> None:
    """Upload a file or directory to GCP using gsutil."""
    try:
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        gs_path = f"gs://{bucket_name}/{folder_name}/"
        command = ["cmd", "/c", "gsutil", "cp", "-r", f'"{file_path}"', gs_path]
        full_command = " ".join(command)

        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
            timeout=60,
        )

        if result.returncode != 0:
            raise Exception(f"Failed to upload {file_path}: {result.stderr}")

    except Exception as e:
        raise e


def get_files_from_folder(page, bucket_name: str, folder: str):
    """Get files from folder"""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(
            ["cmd", "/c", "gcloud", "storage", "ls", f"gs://{bucket_name}/{folder}/"],
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
        )
        if result.returncode != 0:
            show_message(
                page,
                ERROR_MESSAGES.INVALID_FOLDER.value,
                COLORS.VALID_MESSAGES_COLORS.value,
            )
            return ""
        return result.stdout
    except Exception:
        show_message(
            page, ERROR_MESSAGES.INVALID_FOLDER.value, COLORS.FAILED_COLOR.value
        )
        return ""


def download_files_from_gcp(page, bucket_name: str, folder_path: str, file_name: str):
    """Download files from GCP"""
    try:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(
            [
                "cmd",
                "/c",
                "gsutil",
                "cp",
                f"gs://{bucket_name}/{folder_path}/{file_name}",
                f"{downloads_folder}",
            ],
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
        )
        if result.returncode != 0:
            show_message(
                page,
                ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value,
                COLORS.VALID_MESSAGES_COLORS.value,
            )
            raise Exception(result.stderr)
        return result.stdout
    except Exception as ex:
        show_message(
            page,
            ERROR_MESSAGES.ERROR_FETCHING_FOLDERS.value,
            COLORS.FAILED_COLOR.value,
        )
        raise ex
