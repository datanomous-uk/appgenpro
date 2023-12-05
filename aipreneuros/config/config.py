import os
import yaml

from aipreneuros.utils import logger
from aipreneuros.utils.const import WORKSPACE_ROOT, ROOT
from aipreneuros.utils.singleton import Singleton


class NotConfiguredException(Exception):
    """Exception raised for errors in the configuration.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="The required configuration is not set"):
        self.message = message
        super().__init__(self.message)


class Config(metaclass=Singleton):
    _instance = None
    default_yaml_file = f"{ROOT}/config.yaml"


    def __init__(self, yaml_file=default_yaml_file):
        self._configs = {}
        self._init_with_config_files_and_env(self._configs, yaml_file)

        self.mermaid_engine = self._get("MERMAID_ENGINE", "nodejs")
        self.puppeteer_config = self._get("PUPPETEER_CONFIG", "")
        self.mmdc = self._get("MMDC", "mmdc")
        
        self.total_cost = 0.0
        
        self.github_token = self._get("GITHUB_TOKEN", "")
        self.config_list = self._get("OAI_CONFIG_LIST", {})
        self.llm_config = {
            "cache_seed": 42,
            "temperature": 0,
            "config_list": self.config_list,
            "timeout": 250,
            "stream": False,
        }
        logger.info(f"Config is loaded: {self.config_list}")

        self.artifacts = dict(docs={}, code={})
        self.root_dir = WORKSPACE_ROOT
        self.package_dir = WORKSPACE_ROOT
        self.use_chainlit = False
        

    def _init_with_config_files_and_env(self, configs: dict, yaml_file):
        """Load from config/key.yaml, config/config.yaml, and env in decreasing order of priority"""
        configs.update(os.environ)

        if not yaml_file:
            raise FileNotFoundError(f"YAML file not found: {yaml_file}")

        # Load local YAML file
        with open(yaml_file, "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)
            if not yaml_data:
                return
            os.environ.update({k: v for k, v in yaml_data.items() if isinstance(v, str) or isinstance(v, dict)})
            configs.update(yaml_data)

    def _get(self, *args, **kwargs):
        return self._configs.get(*args, **kwargs)

    def get(self, key, *args, **kwargs):
        """Search for a value in config/key.yaml, config/config.yaml, and env; raise an error if not found"""
        value = self._get(key, *args, **kwargs)
        if value is None:
            raise ValueError(f"Key '{key}' not found in environment variables or in the YAML file")
        return value


CONFIG = Config()



 