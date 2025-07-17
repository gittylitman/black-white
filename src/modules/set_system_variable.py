from config.config_variables import ACTION_TYPE, GCLOUD_PATH

class _SetupEnv:
    def init_settings(self):
        try:
            self.ACTION_TYPE: str = ACTION_TYPE
            self.GCLOUD_PATH: str = GCLOUD_PATH

        except KeyError as e:
            raise ValueError(f"Missing key in env: {e}")
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
