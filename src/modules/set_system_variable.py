import os
from dotenv import load_dotenv
load_dotenv()

class _SetupEnv:
    def init_settings(self):
        try:
            # self.ENVIRONMENT_TYPE: str = os.environ["ENVIRONMENT_TYPE"]
            self.ACTION_TYPE: str = os.environ["ACTION_TYPE"]
            self.GCLOUD_PATH: str = os.environ["GCLOUD_PATH"]
            
           
        except KeyError as e:
            raise ValueError(f"Missing key in env file: {e}")
        return self
env = None


def get_env_instance() -> _SetupEnv:
    try:
        global env
        if env is None:
            env = _SetupEnv().init_settings()
        return env
    except Exception as error:
        raise Exception(str(error))
    