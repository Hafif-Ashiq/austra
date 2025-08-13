FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    curl unzip gnupg2 libnss3 libgconf-2-4 libxi6 libxcursor1 \
    libxcomposite1 libasound2 libxdamage1 libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

# Installer les paquets Python requis
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
