# Temel imaj olarak hafif bir Python sürümü kullanıyoruz
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimleri kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Flask'ın çalışacağı portu dışarı aç
EXPOSE 5000

# Uygulamayı başlat
CMD ["python", "app.py"]
