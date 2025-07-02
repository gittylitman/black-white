from enum import Enum

        

class Run_Type(Enum):
    BLACK = "black"
    WHITE = "white"
    
    
class DepartmentsBucketsWhiteDev(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-dev-t-lgupld-1")
    DRONES = ("רחפנים", "dig-drn-dev-t-lgupld")
    MAPPING = ("מיפוי", "dig-geo-dev-t-lgupld")
    SATELLITES = ("לווינות", "dig-sat-dev-t-lgupld")
        
    def __init__(self, departement, bucket) -> None:
        self.departement = departement
        self.bucket = bucket
        
        
class DepartmentsBucketsWhiteProd(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-prd-t-lgupld-1")
    DRONES = ("רחפנים", "dig-drn-prd-t-lgupld")
    MAPPING = ("מיפוי", "dig-geo-prd-t-lgupld")
    SATELLITES = ("לווינות", "dig-sat-prd-t-lgupld")
        
    def __init__(self, departement, bucket) -> None:
        self.departement = departement
        self.bucket = bucket
    
    
class DepartmentsBucketsBlackDev(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-dev-t-lgdnld-1")
    DRONES = ("רחפנים", "dig-drn-dev-t-lgdnld")
    MAPPING = ("מיפוי", "dig-geo-dev-t-lgdnld")
    SATELLITES = ("לווינות", "dig-sat-dev-t-lgdnld")
        
    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket
    
    
class DepartmentsBucketsBlackProd(Enum):
    WHITENING = ("הלבנה 9900", "sky-geo-dig-prd-t-lgdnld-1")
    DRONES = ("רחפנים", "dig-drn-prd-t-lgdnld")
    MAPPING = ("מיפוי", "dig-geo-prd-t-lgdnld")
    SATELLITES = ("לווינות", "dig-sat-prd-t-lgdnld")
    
    def __init__(self, department, bucket) -> None:
        self.department = department
        self.bucket = bucket
        
        
class Departments(Enum):
    BLACK_PROD = (DepartmentsBucketsBlackProd, "PROD", Run_Type.BLACK)
    BLACK_DEV = (DepartmentsBucketsBlackDev, "DEV", Run_Type.BLACK)
    WHITE_DEV = (DepartmentsBucketsWhiteDev, "DEV", Run_Type.WHITE)
    WHITE_PROD = (DepartmentsBucketsWhiteProd, "PROD", Run_Type.WHITE)
    
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
