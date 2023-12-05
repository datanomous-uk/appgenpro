from pathlib import Path


def get_project_root():
    """Search upwards to find the project root directory."""
    current_path = Path.cwd()
    return current_path


PROJECT_ROOT = get_project_root()
APPGEN_ROOT = PROJECT_ROOT / 'appgen'
AVATARS_ROOT = PROJECT_ROOT / 'public/avatars'
EXAMPLES_ROOT = PROJECT_ROOT / 'examples'
DATA_PATH = PROJECT_ROOT / 'data'
WORKSPACE_ROOT = PROJECT_ROOT / 'workspace'

