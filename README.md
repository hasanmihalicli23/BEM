```markdown
# 🏭 BEM Otomasyon - Entegre Üretim & Proje Yönetim Sistemi

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-indigo?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

**BEM Otomasyon**, üretim ve mühendislik süreçlerini dijitalleştirmek, hata payını sıfıra indirmek ve proje yönetimini standartlaştırmak için geliştirilmiş kapsamlı bir masaüstü yazılımıdır.

---

## 🚀 Modüller ve Özellikler

Sistem, birbirine tam entegre çalışan 4 ana modülden oluşur:

### 📁 1. Akıllı Proje & Klasör Yönetimi
- **Otomatik Yapılandırma:** Müşteri ve Proje adına göre standart klasör ağacını (Dökümantasyon, Tasarım, Üretim) tek tıkla kurar.
- **Standartlaşma:** Karmaşık ve düzensiz dosya yapısını engeller.
- **Entegrasyon:** Diğer tüm modüller bu dosya yapısını baz alarak çalışır.

### 💰 2. Maliyet Analizi & Otomatik Teklif
- **Gider Hesaplama:** Hammadde, işçilik, fason ve genel giderleri detaylı analiz eder.
- **Canlı Döviz:** TCMB üzerinden anlık USD/EUR kurlarını çeker ve TL karşılıklarını hesaplar.
- **Akıllı Kayıt:** Teklifi PDF formatında oluşturur ve otomatik olarak ilgili projenin `Dökümantasyon/Teklifler` klasörüne kaydeder.
- **Çoklu Para Birimi:** Sonuç ekranında USD, EUR ve TL maliyetlerini aynı anda gösterir.

### ✂️ 3. Kesim Optimizasyonu (1D Nesting)
- **Fire Analizi:** Profil ve boru kesimlerinde en az fire verecek yerleşimi matematiksel olarak hesaplar.
- **Görsel Rapor:** Hangi parçanın hangi stoktan kesileceğini grafiksel olarak çizer.
- **PDF Çıktısı:** Kesim operatörü için detaylı iş emri oluşturur.

### 📚 4. Teknik Kütüphane & Hesaplayıcı
- **Dijital Katalog:** Cıvata, Rulman, Profil gibi standart makine elemanlarının verilerini içerir (JSON tabanlı, güncellenebilir).
- **Mühendislik Hesapları:** Kama kanalı, segman yuvası ve dişli hesaplarını otomatik yapar.
- **Birim Çevirici:** Teknik birimler arasında hızlı dönüşüm sağlar.

---

## 🛠️ Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Projeyi İndirin (Klonlayın)
Terminali açın ve şu komutu yazarak projeyi bilgisayarınıza çekin:
```bash
git clone [https://github.com/hasanmihalicli23/BEM_Otomasyon.git](https://github.com/hasanmihalicli23/BEM_Otomasyon.git)
cd BEM_Otomasyon

```

### 2. Gerekli Kütüphaneleri Yükleyin

Projenin çalışması için gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt

```

### 3. Uygulamayı Başlatın

Kurulum bittikten sonra ana menüyü açmak için:

```bash
python main_launcher.py

```

---

## 📂 Proje Dizin Yapısı

```text
BEM_Otomasyon/
├── apps/
│   ├── proje_klasor_yonetimi/   # Modül 1: Klasör Yapılandırma
│   ├── maliyet_hesaplama/       # Modül 2: Maliyet & PDF & TCMB
│   ├── kesim_optimizasyonu/     # Modül 3: Nesting Algoritması
│   └── standart_kutuphane/      # Modül 4: Teknik Veri & Hesap
├── assets/                      # İkonlar ve görseller
├── main_launcher.py             # Ana Başlatıcı (Menü)
├── requirements.txt             # Kütüphane Listesi
└── README.md                    # Dökümantasyon Dosyası

```

---

## 📞 İletişim

Geliştirici: **[HASAN MIHALIÇLI]**
GitHub Profilim: [github.com/hasanmihalicli23](https://www.google.com/search?q=https://github.com/hasanmihalicli23)

---

*Copyright © 2026 BEM Engineering Solutions.*

```

```
