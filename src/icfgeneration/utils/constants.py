from pathlib import Path
import os

project_root_dir = Path(__file__).parent.parent.parent.parent
env_path = os.path.join(project_root_dir, ".env")
