from dotenv import load_dotenv
from icfgeneration.utils.constants import project_root_dir

load_dotenv()

log_dir = project_root_dir / "logs"
data_dir = project_root_dir / "data"
rough_dir = project_root_dir / "rough"
