
# Kütüphane Yönetim Sistemi

Bu proje, Django ve Django REST Framework (DRF) kullanılarak geliştirilmiş, ölçeklenebilir, modüler yapıya sahip ve performanslı bir Kütüpane Yönetim Sistemi API'sidir. Projede gelişmiş ORM ilişkileri, konteynerizasyon ve birim testleri gibi modern yazılım geliştirme teknikleri kullanılmıştır.

---

## Proje Genel Bakışı

Kütüpane Yönetim Sistemi API'si aşağıdaki işlevleri sağlar:

- **Kullanıcı Rolleri:**

  - **Yöneticiler:** Kütüphane, kitaplar ve baskıları yönetir.
  - **Üyeler:** Kitap ödünç alır, inceleme yazar ve ödünç alma geçmişini görüntüler.

- **Özellikler:**

  - Kitap yönetimi, birden fazla baskı ve stok takibi.
  - Ödünç alma sistemi (örn. maksimum kitap sınırı, gecikme cezaları).
  - İnceleme sistemi: Üyeler kitaplara yorum yapabilir.
  - Gelişmiş arama, filtreleme, sayfalama ve sıralama.
  - Basic Auth veya Bearer Token kullanılarak kimlik doğrulama.

---

## Yerel Kurulum ve Docker Talimatları

### Ön Koşullar

- Python 3.10+
- Docker & Docker Compose
- Postman (isteğe bağlı olarak API testi için)

### Adımlar

1. **Depoyu Klonlayın:**

   ```bash
   git clone <repository-url>
   cd library_management
   ```

2. **Docker Build ve Container Çalıştırma:**

   Docker container'ları oluşturup çalıştırmak için aşağıdaki komutları kullanın:

   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Veritabanı Göçlerini (Migrations) Çalıştırın:**

   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Seed Komutunu Çalıştırın (Varsayılan Veriler):**

   ```bash
   docker-compose exec web python manage.py seed
   ```

5. **Uygulamaya Erişim:**

   - API Base URL: `http://localhost:8000/api`
   - Admin Panel: `http://localhost:8000/admin`

---

## API Dokümantasyonu

### Kimlik Doğrulama

API, **Basic Auth** veya **Token Authentication** kullanır. Token Authentication kullanmak için aşağıdaki adımları takip edin:

1. **Token Alın:**

   - URL: `http://127.0.0.1:8000/api/token/`
   - Metot: `POST`
   - Payload:
     ```json
     {
       "username": "<your-username>",
       "password": "<your-password>"
     }
     ```
   - Yanıt:
     ```json
     {
       "access": "<access-token>",
       "refresh": "<refresh-token>"
     }
     ```

2. **Bearer Token Kullanımı:**

   Tüm korumalı endpoint'lere erişim için HTTP başlığı ekleyin:

   ```http
   Authorization: Bearer <access-token>
   ```

### Örnek Endpointler

**Kitap Listeleme**

- **URL:** `/api/books/`

- **Metot:** `GET`

- **Filtreleme:** `title`, `author`, `isbn`, `genre`

- **Yanıt:**

  ```json
  [
    {
      "id": 1,
      "title": "Kitap Adı",
      "author": "Yazar Adı",
      "isbn": "1234567890",
      "stock": 5
    }
  ]
  ```

#### Kitap Ödünç Alma

- **URL:** `/api/borrow/`
- **Metot:** `POST`
- **Payload:**
  ```json
  {
    "book_id": 1
  }
  ```
- **Yanıt:**
  ```json
  {
    "message": "Kitap başarıyla ödünç alındı."
  }
  ```

---

## Test Talimatları

1. **Unit Testlerı Çalıştırma:**

   Docker ortamında testleri çalıştırmak için:

   ```bash
   docker-compose exec web python manage.py test library.tests
   ```

2. **Postman Koleksiyonu:**

   - `library_management.postman_collection.json` dosyasını Postman'e aktarın.
   - API'nin temel URL'sini `http://localhost:8000` olarak ayarlayın.
   - Basic Auth veya Bearer Token seçenekleri ile endpoint'leri test edin.
