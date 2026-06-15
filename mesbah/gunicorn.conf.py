import multiprocessing
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

bind = "0.0.0.0:8000"
wsgi_app = "mesbah.wsgi:application"

workers = multiprocessing.cpu_count() * 2 + 1
threads = 1
timeout = 120

accesslog = str(LOG_DIR / "access.log")
errorlog = str(LOG_DIR / "error.log")
loglevel = "info"
