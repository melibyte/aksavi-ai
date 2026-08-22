# AKSAVİ AI Assistant

AKSAVİ AI Assistant, Cloud ve DevOps alanında kullanıcıların temel ihtiyaçlarını analiz etmek, sorularını yapay zekâ destekli olarak yanıtlamak ve iletişim taleplerini kayıt altına almak amacıyla geliştirilmiş bir web uygulaması prototipidir.

Proje, Human Ports Proje Uzmanı Yetiştirme Programı online dönem çalışmaları kapsamında hazırlanmıştır.

AKSAVİ, Cloud & DevOps Solutions alanında hizmet sunan bir marka olarak kurgulanmıştır. Sistem; Python ve Flask tabanlı backend, Groq AI, SQLite, Render, Wix Studio ve Velo bileşenlerinden oluşmaktadır.

---

## Projenin Amacı

Projenin amacı, kullanıcıların Cloud ve DevOps alanındaki sorularına yapay zekâ destekli yanıtlar sunmak ve potansiyel müşteri iletişim taleplerini kayıt altına almaktır.

Sistem özellikle aşağıdaki konulara yönelik kullanılmak üzere geliştirilmiştir:

- CI/CD süreçleri
- Bulut altyapısı
- DevOps uygulamaları
- Otomasyon
- Konteyner teknolojileri
- Monitoring ve izleme
- Yazılım dağıtım süreçleri

Kullanıcılar yapay zekâ asistanına soru sorabilmekte, isim ve telefon bilgilerini bırakarak iletişim talebi oluşturabilmektedir. Bu talepler veritabanına kaydedilmekte ve Yönetim Paneli üzerinden görüntülenebilmektedir.

---

## Temel Özellikler

- Cloud ve DevOps odaklı yapay zekâ asistanı
- Groq API entegrasyonu
- Flask REST API
- SQLite tabanlı iletişim talebi yönetimi
- Kullanıcı bilgilerinin kaydedilmesi
- İletişim taleplerinin API üzerinden listelenmesi
- Wix Studio AI Assistant arayüzü
- Wix Studio Yönetim Paneli
- Velo ile Flask API entegrasyonu
- Render üzerinde backend deployment
- Health Check endpoint'i
- Git ve GitHub ile versiyon kontrolü

---

## Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|---|---|
| Python | Backend geliştirme |
| Flask | REST API |
| SQLite | İletişim taleplerinin saklanması |
| Groq API | Yapay zekâ yanıtlarının oluşturulması |
| Flask-CORS | Frontend-backend iletişimi |
| Gunicorn | Deployment sunucusu |
| Render | Backend deployment |
| Wix Studio | Kullanıcı arayüzü |
| Velo / JavaScript | Wix ve Flask bağlantısı |
| Git / GitHub | Versiyon kontrolü |

---

## Sistem Mimarisi

### AI Assistant

```text
Kullanıcı
   |
   v
Wix Studio
   |
   v
POST /api/sohbet
   |
   v
Flask Backend
   |
   v
Groq AI
   |
   v
AI Yanıtı
```

### İletişim Talebi

```text
Wix Form
   |
   v
POST /api/leads
   |
   v
Flask Backend
   |
   v
SQLite
```

### Yönetim Paneli

```text
Wix Yönetim Paneli
   |
   v
GET /api/leads
   |
   v
Flask Backend
   |
   v
SQLite
   |
   v
Wix Repeater
```

---

## Proje Klasör Yapısı

```text
aksavi-ai/
|
|-- app/
|   |-- __init__.py
|   |-- database.py
|   |-- routes.py
|   |
|   |-- services/
|   |   |-- __init__.py
|   |   |-- ai_service.py
|   |
|   |-- templates/
|       |-- index.html
|       |-- dashboard.html
|
|-- config.py
|-- requirements.txt
|-- run.py
|-- .gitignore
|-- README.md
```

---

## API Endpointleri

### Health Check

Backend servisinin çalışıp çalışmadığını kontrol eder.

```http
GET /health
```

Örnek yanıt:

```json
{
  "status": "ok"
}
```

Canlı endpoint:

```text
https://aksavi-ai.onrender.com/health
```

### AI Sohbet

Kullanıcının mesajını yapay zekâ servisine gönderir.

```http
POST /api/sohbet
```

Örnek istek:

```json
{
  "mesaj": "CI/CD ve bulut altyapısı hakkında bilgi almak istiyorum.",
  "gecmis": []
}
```

### İletişim Talebi Oluşturma

Kullanıcının iletişim bilgilerini veritabanına kaydeder.

```http
POST /api/leads
```

Örnek istek:

```json
{
  "isim": "Test Kullanıcısı",
  "telefon": "05555555555",
  "mesaj": "CI/CD ve bulut altyapısı hakkında bilgi almak istiyorum."
}
```

### İletişim Taleplerini Listeleme

Kayıtlı iletişim taleplerini listeler.

```http
GET /api/leads
```

Örnek yanıt:

```json
{
  "basarili": true,
  "leads": [
    {
      "id": 1,
      "isim": "Test Kullanıcısı",
      "telefon": "05555555555",
      "mesaj": "CI/CD ve bulut altyapısı hakkında bilgi almak istiyorum.",
      "tarih": "2026-08-22 19:05:30"
    }
  ]
}
```

---

## Wix Studio Entegrasyonu

Frontend tarafında AI Assistant ve Yönetim Paneli olmak üzere iki temel ekran hazırlanmıştır.

### AI Assistant

Kullanıcı sorusunu girdikten sonra Velo kodu `/api/sohbet` endpoint'ine POST isteği gönderir. Flask backend, Groq AI üzerinden yanıt üretir ve cevap Wix arayüzünde kullanıcıya gösterilir.

Aynı ekrandan kullanıcı isim ve telefon bilgilerini girerek iletişim talebi oluşturabilir. Bu bilgiler `/api/leads` endpoint'ine gönderilerek veritabanına kaydedilir.

Başarılı kayıt sonucunda kullanıcıya:

```text
Talebiniz başarıyla kaydedildi.
```

mesajı gösterilir.

### Yönetim Paneli

Yönetim Paneli `/api/leads` endpoint'inden kayıtları alır ve Wix Repeater bileşeninde gösterir.

Her kayıt için aşağıdaki bilgiler görüntülenmektedir:

- İsim
- Telefon
- Mesaj
- Tarih

Repeater içerisinde her kayıt için benzersiz `_id` oluşturulmakta ve `$item` kullanılarak ilgili veriler ekrana aktarılmaktadır.

---

## Kurulum

Repository'yi klonlayın:

```bash
git clone https://github.com/melibyte/aksavi-ai.git
cd aksavi-ai
```

Sanal ortam oluşturun:

```powershell
python -m venv venv
```

Bağımlılıkları yükleyin:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Proje kök dizininde `.env` dosyası oluşturun:

```env
APP_ENV=development
AI_PROVIDER=groq
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

API anahtarları kaynak kod içerisinde tutulmamalı ve `.env` dosyası GitHub'a yüklenmemelidir.

Uygulamayı çalıştırmak için:

```powershell
.\venv\Scripts\python.exe run.py
```

Lokal adres:

```text
http://127.0.0.1:5000
```

Health Check:

```text
http://127.0.0.1:5000/health
```

---

## Deployment

Backend uygulaması Render üzerinde deploy edilmiştir.

Backend:

```text
https://aksavi-ai.onrender.com
```

Health Check:

```text
https://aksavi-ai.onrender.com/health
```

Lead API:

```text
https://aksavi-ai.onrender.com/api/leads
```

Render deployment işleminde GitHub repository kaynak olarak kullanılmıştır.

---

## Yapılan Testler

Proje geliştirme sürecinde aşağıdaki testler gerçekleştirilmiştir:

- Flask uygulamasının lokal ortamda çalıştırılması
- Lokal ve Render Health Check testi
- Groq API bağlantı testi
- AI sohbet endpoint testi
- Türkçe karakter testi
- POST `/api/leads` testi
- GET `/api/leads` testi
- SQLite kayıt testi
- Wix AI Assistant testi
- Wix üzerinden AI yanıtı alma testi
- Wix üzerinden iletişim talebi oluşturma testi
- Wix Yönetim Paneli testi
- Wix Repeater veri gösterimi

Testler sonucunda oluşturulan iletişim talebinin backend üzerinde kaydedildiği ve Yönetim Panelinde başarıyla görüntülendiği doğrulanmıştır.

---

## Güvenlik

Projede API anahtarları doğrudan kaynak kod içerisinde tutulmamaktadır.

Hassas bilgiler ortam değişkenleri üzerinden yönetilmektedir.

- `.env` GitHub'a yüklenmemektedir.
- Groq API anahtarı paylaşılmamaktadır.
- `.gitignore` kullanılmaktadır.
- Sanal ortam dosyaları repository dışında tutulmaktadır.

---

## Bilinen Sınırlamalar ve Gelecek Geliştirmeler

Bu proje online dönem kapsamında çalışan bir prototip olarak geliştirilmiştir.

Mevcut sürümde SQLite kullanılmaktadır. Production ortamında daha kalıcı ve ölçeklenebilir bir yapı için PostgreSQL gibi harici bir veritabanına geçilmesi planlanabilir.

Gelecek geliştirmelerde:

- PostgreSQL entegrasyonu
- Yönetim paneli yetkilendirmesi
- Kullanıcı giriş sistemi
- Sohbet geçmişi
- Lead durum yönetimi
- E-posta bildirimleri
- Monitoring ve loglama
- Docker desteği
- CI/CD pipeline
- AKSAVİ kurumsal web sitesi ile tam entegrasyon

eklenebilir.

---

## GitHub Repository

```text
https://github.com/melibyte/aksavi-ai
```

---

## Proje Durumu

- Flask backend tamamlandı.
- Groq AI entegrasyonu tamamlandı.
- SQLite veritabanı oluşturuldu.
- AI sohbet endpoint'i tamamlandı.
- Lead kayıt ve listeleme endpointleri tamamlandı.
- GitHub repository oluşturuldu.
- Render deployment tamamlandı.
- Wix AI Assistant entegrasyonu tamamlandı.
- Wix Yönetim Paneli tamamlandı.
- Repeater ile kayıt listeleme tamamlandı.
- Fonksiyonel testler tamamlandı.

---

## Sonuç

AKSAVİ AI Assistant kapsamında yapay zekâ destekli bir Cloud ve DevOps danışmanlık prototipi geliştirilmiştir.

Python ve Flask ile geliştirilen backend Groq AI ile entegre edilmiş, kullanıcı talepleri SQLite veritabanına kaydedilmiş ve Render üzerinde deploy edilmiştir.

Wix Studio ve Velo entegrasyonu sayesinde kullanıcıların yapay zekâ asistanına soru sorması, iletişim talebi oluşturması ve oluşturulan kayıtların Yönetim Panelinde görüntülenmesi sağlanmıştır.

---

## Geliştirici

Melisa Akbulut

Bilgisayar Mühendisliği

AKSAVİ  
Cloud & DevOps Solutions
