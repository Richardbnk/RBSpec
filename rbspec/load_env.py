import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(os.path.join(os.path.expanduser('~'), 'Repositories', 'files', '.env'))
load_dotenv(dotenv_path=dotenv_path)
