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
        
        
class TEXTS(Enum):
    CHOOSE_DEPARTMENT = "Choose Department:"
    CHOOSE_FOLDER = "Choose Folder:"
    CHOOSE_FILES = "Choose files:"
    NO_FOLDERS_ALERT = "No folders available."
    NO_FILES_ALERT = "No file selected."
    NO_FOLDER_OR_BUCKET = "No bucket or folder selected."
    UPLOAD_BUTTON = "Upload"
    DOWNLOAD_BUTTON = "Download"
    BACK_TO_MAIN = "Back to Main"
    INVALID_FOLDER = "Invalid folder or bucket"
    PAGE_TITLE = "שער האריות"
    BASIC_TITLE = "ברוך הבא לשער האריות"

class COLORS(Enum):
    MAIN_COLOR = ft.colors.BLUE_ACCENT_700
    BACKGROUND_COLOR = ft.colors.GREY_300
