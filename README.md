# Lorenza — Tek Sayfa Web Sitesi

Django ile hazırlanmış, aşağı kaydırmalı tek sayfa site (Lorenza).

## Özellikler

- **Navbar**: Anasayfa, Hakkımızda, Galeri, İletişim linkleri; tıklanınca ilgili bölüme smooth scroll
- **Anasayfa**: Veritabanından çekilen resimlerle slider; her resim yaklaşık 8 saniye gösterilir, sonra otomatik geçiş
- **Hakkımızda**: Admin panelinden düzenlenebilir metin
- **Galeri**: Yapılan işlere ait resim, başlık ve açıklama; lightbox ve büyüteç ile inceleme
- **İletişim**: Adres, telefon, e-posta (admin’den düzenlenir)

## Kurulum

### 1. Sanal ortam ve bağımlılıklar

```bash
cd C:\Users\halim\Desktop\ugur
python -m venv venv
venv\Scripts\activate
cd ugur
pip install -r requirements.txt
```

### 2. MySQL veritabanı

MySQL’de bir veritabanı oluşturun (SQLite kullanıyorsanız bu adımı atlayın):

```sql
CREATE DATABASE lorenza_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lorenza_user'@'localhost' IDENTIFIED BY 'sifreniz';
GRANT ALL ON lorenza_db.* TO 'lorenza_user'@'localhost';
FLUSH PRIVILEGES;
```

Proje kökünde `.env` dosyası oluşturun (isteğe göre):

```
USE_SQLITE=true
MYSQL_DATABASE=lorenza_db
MYSQL_USER=lorenza_user
MYSQL_PASSWORD=sifreniz
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

### 3. Migrasyonlar ve çalıştırma

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Tarayıcıda: http://127.0.0.1:8000/  
Admin panel: http://127.0.0.1:8000/admin/

## Admin paneli

- **Slider resimleri**: Anasayfa slider’a resim, başlık, alt başlık ekleyin; sıra numarası verin.
- **Hakkımızda**: Bir kayıt oluşturup başlık ve içerik girin.
- **Galeri öğeleri**: Her iş için resim, başlık, açıklama ve sıra ekleyin.
- **İletişim bilgileri**: Adres, telefon, e-posta girin.

Yerel geliştirmede resimler `static/media/slider/` ve `static/media/gallery/`
altında saklanır. Canlı ortamda bilgisayardan yüklenen resimlerin deploy veya
sunucu yeniden başlatmasında kaybolmaması için Cloudinary kullanılır.

Render servisinin **Environment** bölümüne Cloudinary hesabınızdan aldığınız
tek bir değişken ekleyin:

```
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Sonraki deploy'dan itibaren admin panelinden seçilen yeni resimler kalıcı olarak
Cloudinary'ye yüklenir. GitHub'da bulunan eski resimler de aynı şekilde görünmeye
devam eder. `CLOUDINARY_URL` değerini GitHub'a veya `.env` dosyasını repoya
yüklemeyin.
