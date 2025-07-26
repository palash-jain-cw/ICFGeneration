import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

project_root_dir = Path(os.getenv("project_root_dir"))
log_dir = project_root_dir / "logs"
data_dir = project_root_dir / "data"
rough_dir = project_root_dir / "rough"
