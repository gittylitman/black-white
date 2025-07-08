import subprocess

import flet as ft
from config.const import TEXTS
from utils.basic_function import show_message


def set_gcloud_project(project_id: str, page) -> list:
        try:
            result = subprocess.run(
                ["gcloud", "config", "set", "project", project_id],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return get_top_level_folders(project_id, page)
            else:
                show_message(page, TEXTS.INVALID_BUCKET.value, ft.colors.ORANGE)
                return []
        except Exception as e:
            print(f"שגיאה בהגדרת פרויקט: {e}")
            return []
        
# def list_bucket_folders(bucket_name: str, page) -> list[str]:
#         """Extracts top-level folders (prefixes) from object names"""
#         try:
#             result = subprocess.run(
#                 # ["gcloud", "storage", "objects", "list", f"gs://{bucket_name}", "--format=json"],
#                 ["gcloud", "storage", "ls", "--recursive", f"gs://{bucket_name}", "--json"],
#                 # ["gcloud", "storage", "objects", "list", f"--bucket={bucket_name}", "--format=json"],
#                 capture_output=True,
#                 text=True
#             )
#             if result.returncode == 0:
#                 show_message(page, "stderr_output", ft.colors.GREEN)
#                 objects = json.loads(result.stdout)
#                 folders = set()
                
#                 show_message(page, result.stdout, ft.colors.GREEN)
#                 for obj in objects:
#                     name = obj["name"]
#                     if "/" in name:
#                         folder = name.split("/")[0]
#                         folders.add(folder)
#                 return sorted(list(folders))
#             else:
#                 show_message(page, result.stderr, ft.colors.ORANGE)
#                 raise Exception(result.stderr)
#         except Exception as e:
#             print(f"שגיאה בשליפת תיקיות: {e}")
#             show_message(page, f"שגיאה בשליפת תיקיות: {e}", ft.colors.RED)
#             return []

# def list_folders(bucket_name: str, page) -> list[str]:
#     try:
#         result = subprocess.run(
#             ["gcloud", "storage", "ls", "--recursive", "--format=gsutil", f"gs://{bucket_name}/"],
#             capture_output=True,
#             text=True
#         )
#         if result.returncode == 0:
#             show_message(page, result.stdout, ft.colors.GREEN)
#             lines = result.stdout.strip().splitlines()
#             folders = [line for line in lines if line.endswith("/")]
#             return folders
#         else:
#             show_message(page, result.stderr, ft.colors.ORANGE)
#             return []
#     except Exception as e:
#         show_message(page, f"שגיאה בשליפת תיקיות: {e}", ft.colors.RED)
#         return []

def get_top_level_folders(bucket_name: str, page) -> list[str]:
    try:
        result = subprocess.run(
            ["gcloud", "storage", "ls", "--recursive", "--format=gsutil", f"gs://{bucket_name}/"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            show_message(page, result.stderr, ft.colors.RED)
            return []

        lines = result.stdout.strip().splitlines()
        show_message(page, result.stdout, ft.colors.GREEN)
        folders = set()
        for line in lines:
            if "/" in line:
                top_level = line.split("/")[0]
                folders.add(top_level)

        return sorted(list(folders))

    except Exception as e:
        show_message(page, f"שגיאה בשליפת תיקיות: {e}", ft.colors.RED)
        return []