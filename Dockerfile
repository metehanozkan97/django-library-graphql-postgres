# Python resmi imajını kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Gereksinim dosyalarını kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Django migration'larını otomatik çalıştırmak için ortam değişkeni
ENV DJANGO_SETTINGS_MODULE=library_management.settings

# Django uygulamasını başlat
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "library_management.wsgi:application"]
