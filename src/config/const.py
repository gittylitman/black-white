from enum import Enum

import flet as ft


class Run_Type(Enum):
    UPLOAD = "Upload"
    DOWNLOAD = "Download"


class Project_id(Enum):
    UPLOAD_PROD = "dig-drn-dev-t-lgupld-1"
    UPLOAD_DEV = "dig-drn-dev-t-lgupld-1"
    DOWNLOAD_DEV = "dig-drn-dev-t-lgupld-1"
    DOWNLOAD_PROD = "dig-drn-dev-t-lgupld-1"


class Env_Type(Enum):
    DEV = "DEV"
    PROD = "PROD"


class DepartmentsBucketsUploadDev(Enum):
    DRONES = ("רחפנים", "example-download-upload")
    MAPPING = ("מיפוי", "empty-bucket-example")
    SATELLITES = ("לווינות", "empty-bucket-example")

    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket


class DepartmentsBucketsUploadProd(Enum):
    DRONES = ("רחפנים", "dig-drn-prd-t-lgupld")
    MAPPING = ("מיפוי", "dig-geo-prd-t-lgupld")
    SATELLITES = ("לווינות", "dig-sat-prd-t-lgupld")

    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket


class DepartmentsBucketsDownloadDev(Enum):
    DRONES = ("רחפנים", "example-download-upload")
    MAPPING = ("מיפוי", "empty-bucket-example")
    SATELLITES = ("לווינות", "empty-bucket-example")

    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket


class DepartmentsBucketsDownloadProd(Enum):
    DRONES = ("רחפנים", "dig-drn-prd-t-lgdnld")
    MAPPING = ("מיפוי", "dig-geo-prd-t-lgdnld")
    SATELLITES = ("לווינות", "dig-sat-prd-t-lgdnld")

    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket


class Departments(Enum):
    BLACK_PROD = (
        DepartmentsBucketsDownloadProd,
        Env_Type.PROD.value,
        Run_Type.DOWNLOAD,
        Project_id.DOWNLOAD_PROD.value,
    )
    BLACK_DEV = (
        DepartmentsBucketsDownloadDev,
        Env_Type.DEV.value,
        Run_Type.DOWNLOAD,
        Project_id.DOWNLOAD_DEV.value,
    )
    WHITE_DEV = (
        DepartmentsBucketsUploadDev,
        Env_Type.DEV.value,
        Run_Type.UPLOAD,
        Project_id.UPLOAD_DEV.value,
    )
    WHITE_PROD = (
        DepartmentsBucketsUploadProd,
        Env_Type.PROD.value,
        Run_Type.UPLOAD,
        Project_id.UPLOAD_PROD.value,
    )

    def __init__(self, department_bucket, env, run_type, project_id) -> None:
        self.department_bucket = department_bucket
        self.env = env
        self.run_type = run_type
        self.project_id = project_id


class ERROR_MESSAGES(Enum):
    BASIC_ERROR_MESSAGE = "Error: {}"
    DEPARTMENT_NOT_FOUND = "Department not found"
    ERROR_FETCHING_FOLDERS = "Error fetching folders: {}"
    ERROR_DURING_DOWNLOAD = "Error during download: {}"
    ERROR_DURING_UPLOAD = "Error during upload: {}"
    ERROR_RUNNING_GCLOUD = "Error while running gcloud: {}"
    ERROR_SENDING_CODE = "Error sending code: {}"
    GCLOUD_PROCESS_NOT_AVAILABLE = "The gcloud process is no longer available.😢"
    INVALID_BUCKET = "No such bucket in gcloud"
    INVALID_FOLDER = "Invalid folder or bucket"
    FILES_FILED = "⚠️ Some files failed: "

    def format(self, *args, **kwargs):
        return self.value.format(*args, **kwargs)


class VALIDATION_MESSAGES(Enum):
    NO_FOLDERS_ALERT = "No folders available."
    NO_FILES_ALERT = "No file selected."
    NO_FOLDER_OR_BUCKET = "No bucket or folder selected."
    MISSING_VERIFICATION_CODE = "Verification code must be entered."

    def format(self, *args, **kwargs):
        return self.value.format(*args, **kwargs)


class TEXTS(Enum):
    SIGN_IN = "Sign in with Google"
    CHOOSE_DEPARTMENT = "Choose Department:"
    CHOOSE_FOLDER = "Choose Folder:"
    CHOOSE_FILES = "Choose files:"
    CHOSEN_FOLDER = "Chosen folder: "
    NONE = "None"
    UPLOAD_BUTTON = "Upload"
    DOWNLOAD_BUTTON = "Download"
    APPLY = "Apply"
    BACK_TO_MAIN = "Back to Main"
    INSTRUCTIONS = "1. Sign in with Google\n2. Copy the verification code that appears in the browser\n3. Paste it here and click 'Next'"
    VERIFICATION_CODE = "Paste the verification code here"
    CONFIRM_VERIFICATION = "Confirm verification code"
    CURRENT_PATH = "Current path: /"
    LOGGED_IN = "🎉 You have successfully logged in! Loading user information..."
    NO_SUBFOLDER = "No subfolders found"
    PAGE_TITLE = "שער האריות"
    BASIC_TITLE = "Welcome"
    INVALID_FOLDER = "Invalid folder or bucket"
    SUCCESSFUL = "completed successfully."
    ERROR_UPLOAD_FOLDER = "Error while upload folder"
    ITEM_SELECTED = "Selected item:"


class COLORS(Enum):
    MAIN_COLOR = ft.colors.GREEN_700
    BACKGROUND_COLOR = ft.colors.WHITE
    GRAY_COLOR = ft.colors.GREY
    FAILED_COLOR = ft.colors.RED
    SUCCESS_COLOR = ft.colors.GREEN
    PROCESS_COLOR = ft.colors.BLUE
    VALID_MESSAGES_COLORS = ft.colors.ORANGE
    BLACK_COLOR = ft.colors.BLACK
