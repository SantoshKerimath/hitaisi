# ---------- Base Image ----------
    FROM python:3.12-slim

    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    
    WORKDIR /app
    
    # ---------- System Dependencies ----------
    RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        gcc \
        netcat-openbsd \
        && rm -rf /var/lib/apt/lists/*
    
    # ---------- Install Dependencies ----------
    COPY requirements.txt .
    
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---------- Copy Project ----------
    COPY . .
    
    # ---------- Collect Static ----------
    RUN python manage.py collectstatic --noinput || true

    COPY entrypoint.sh /app/entrypoint.sh
    RUN chmod +x /app/entrypoint.sh
    ENTRYPOINT ["/app/entrypoint.sh"]

    
    # ---------- Start Gunicorn ----------
    CMD ["gunicorn", "core.wsgi:application", "--config", "gunicorn.conf.py"]
