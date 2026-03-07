import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = 3
worker_class = "sync"

# Prevent control socket issue
worker_tmp_dir = "/dev/shm"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# ⭐ disable control socket completely
pidfile = None