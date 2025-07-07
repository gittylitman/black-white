from enum import Enum
import flet as ft

        

class Run_Type(Enum):
    UPLOAD = "Upload"
    DOWNLOAD = "Download"
    
    
class DepartmentsBucketsUploadDev(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-dev-t-lgupld-1")
    DRONES = ("רחפנים", "dig-drn-dev-t-lgupld")
    MAPPING = ("מיפוי", "dig-geo-dev-t-lgupld")
    SATELLITES = ("לווינות", "dig-sat-dev-t-lgupld")
        
    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket
        
        
class DepartmentsBucketsUploadProd(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-prd-t-lgupld-1")
    DRONES = ("רחפנים", "dig-drn-prd-t-lgupld")
    MAPPING = ("מיפוי", "dig-geo-prd-t-lgupld")
    SATELLITES = ("לווינות", "dig-sat-prd-t-lgupld")
        
    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket
    
    
class DepartmentsBucketsDownloadDev(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-dev-t-lgdnld-1")
    DRONES = ("רחפנים", "dig-drn-dev-t-lgdnld")
    MAPPING = ("מיפוי", "dig-geo-dev-t-lgdnld")
    SATELLITES = ("לווינות", "dig-sat-dev-t-lgdnld")
        
    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket
    
    
class DepartmentsBucketsDownloadProd(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-prd-t-lgdnld-1")
    DRONES = ("רחפנים", "dig-drn-prd-t-lgdnld")
    MAPPING = ("מיפוי", "dig-geo-prd-t-lgdnld")
    SATELLITES = ("לווינות", "dig-sat-prd-t-lgdnld")
    
    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket
        
        
class Departments(Enum):
    BLACK_PROD = (DepartmentsBucketsDownloadProd, "PROD", Run_Type.DOWNLOAD)
    BLACK_DEV = (DepartmentsBucketsDownloadDev, "DEV", Run_Type.DOWNLOAD)
    WHITE_DEV = (DepartmentsBucketsUploadDev, "DEV", Run_Type.UPLOAD)
    WHITE_PROD = (DepartmentsBucketsUploadProd, "PROD", Run_Type.UPLOAD)
    
    def __init__(self, department_bucket, env, run_type) -> None:
        self.department_bucket = department_bucket
        self.env = env
        self.run_type = run_type
       
       
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
    UPLOAD_BUTTON = "Upload"
    DOWNLOAD_BUTTON = "Download"
    BACK_TO_MAIN = "Back"
    INSTRUCTIONS = "1. Sign in with Google\n2. Copy the verification code that appears in the browser\n3. Paste it here and click 'Next'"
    PAGE_TITLE = "שער האריות"
    BASIC_TITLE = "ברוך הבא לשער האריות"
    VERIFICATION_CODE = "Paste the verification code here"
    CONFIRM_VERIFICATION = "Confirm verification code"
    LOGGED_IN = "🎉 You have successfully logged in! Loading user information..."

class COLORS(Enum):
    MAIN_COLOR = ft.colors.BLUE_ACCENT_700
    BACKGROUND_COLOR = ft.colors.GREY_300
