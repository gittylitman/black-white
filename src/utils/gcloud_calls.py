import subprocess
import os

from config.const import COLORS
from utils.basic_function import show_message
from typing import List


def set_project_id(project_id: str):
    """Set Project Id"""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.run(
            [
                "cmd",
                "/c",
                "gcloud",
                "config",
                "set",
                "project",
                project_id,
            ],
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout
    
    except Exception as e:
        raise e

def get_folders_and_files(bucket_name: str, path: str = "") -> List[str]:
    """Bringing the files and folders from GCP."""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        full_path = f"gs://{bucket_name}/{path}".rstrip("/") + "/"

        command = ["cmd", "/c", "gcloud", "storage", "ls", full_path]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        list_folders_and_files = result.stdout.strip().split("\n")
        list_folders = [
            line.strip().split("/")[-2]
            for line in list_folders_and_files
            if line.strip().endswith("/")
        ]

        return sorted(set(list_folders))

    except Exception as e:
        raise e


def upload_files_to_gcp(bucket_name: str, folder_name: str, file_path: str) -> None:
    """Upload a file or directory to GCP using gsutil."""
    try:
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        if any(c in bucket_name + folder_name for c in [';', '&', '|', '`']):
            raise ValueError("Invalid characters in bucket or folder name")

        gs_path = f"gs://{bucket_name}/{folder_name}/"
        command = ["cmd", "/c", "gsutil", "cp", "-r", file_path, gs_path]
        full_command = " ".join(command)

        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
            timeout=360,
        )

        if result.returncode != 0:
            raise Exception(f"Failed to upload {file_path}: {result.stderr}")

    except Exception as e:
        raise e
    

def get_files_from_folder(bucket_name: str, folder: str):
    """Get files from folder"""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        if any(c in folder + bucket_name for c in [';', '&', '|', '`']):
            raise ValueError("Invalid characters in input")
        
        gs_uri = f"gs://{bucket_name}/{folder}/"

        result = subprocess.run(
            ["cmd", "/c", "gcloud", "storage", "ls", gs_uri],
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout
    
    except Exception as e:
        raise e


def download_files_from_gcp(page, bucket_name: str, folder_path: str, file_name: str):
    """Download files from GCP"""
    try:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        for val in [bucket_name, folder_path, file_name]:
            if any(c in val for c in [';', '&', '|', '`']):
                raise ValueError(f"Invalid characters in input: {val}")
            
        gs_uri = f"gs://{bucket_name}/{folder_path}/{file_name}"
        result = subprocess.run(
            [
                "cmd",
                "/c",
                "gsutil",
                "cp",
                gs_uri,
                downloads_folder,
            ],
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)
        return result.stdout
    
    except Exception as e:
        raise e
