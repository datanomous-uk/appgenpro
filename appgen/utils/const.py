from pathlib import Path


def get_root():
    """Search upwards to find the project root directory."""
    current_path = Path.cwd()
    return current_path


ROOT = get_root()
APPGEN_ROOT = ROOT / 'appgen'
AVATARS_ROOT = ROOT / 'public/avatars'
EXAMPLES_ROOT = ROOT / 'examples'
WORKSPACE_ROOT = ROOT / 'workspace'

