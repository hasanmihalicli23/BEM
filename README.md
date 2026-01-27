```markdown
# 🏭 BEM Otomasyon - Entegre Üretim & Proje Yönetim Sistemi

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-indigo?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**BEM Otomasyon**, mühendislik ve üretim süreçlerini dijitalleştirmek için geliştirilmiş; klasör yönetiminden maliyet analizine, kesim optimizasyonundan teknik hesaplamalara kadar uçtan uca çözüm sunan Python tabanlı bir masaüstü yazılımıdır.

---

## 🚀 Modüller ve Temel Özellikler

Sistem, birbirine entegre çalışan 4 ana modülden oluşur:

### 📁 1. Akıllı Proje & Klasör Yönetimi
Proje süreçlerinin standartlaşmasını sağlar.
- **Otomatik Yapılandırma:** Müşteri ve Ürün adına göre standart klasör ağacını (Dökümantasyon, Tasarım, Üretim) saniyeler içinde kurar.
- **Standart İsimlendirme:** Dosya ve klasör isimlerini bozuk karakterlerden arındırarak sistemli bir arşiv oluşturur.
- **ERP Entegrasyon Mantığı:** Tüm modüller bu ana dizin yapısını baz alarak çalışır.

### 💰 2. Maliyet Analizi & Otomatik Teklif
Hammadde, işçilik ve fason giderlerini hesaplayarak profesyonel teklifler hazırlar.
- **Anlık Döviz Kuru:** TCMB entegrasyonu ile USD/EUR kurlarını canlı çeker.
- **Dinamik Hesaplama:** Malzeme, İşçilik ve Genel Gider marjlarını ayrı ayrı yönetir.
- **Raporlama:** Teklifi PDF formatında oluşturur ve ilgili projenin `01-Dökümantasyon/Teklifler` klasörüne otomatik kaydeder.
- **Çoklu Para Birimi:** Sonuçları TL, USD ve EUR bazında anlık gösterir.

### ✂️ 3. Kesim Optimizasyonu (1D Nesting)
Üretim firelerini minimize etmek için matematiksel algoritmalar kullanır.
- **Fire Analizi:** Girilen parça listesini stok boyuna göre en verimli şekilde dizer.
- **Görselleştirme:** Kesim planını grafiksel olarak ekrana çizer.
- **PDF Raporu:** Kesim operatörü için detaylı imalat planını PDF olarak verir.

### 📚 4. Teknik Kütüphane & Hesaplayıcı
Mühendislik hesaplamaları için dijital bir el kitabıdır.
- **Dinamik Katalog:** Cıvata, Rulman, Profil gibi standart elemanların verilerini içerir (JSON tabanlı, güncellenebilir).
- **Mühendislik Hesapları:** Kama kanalı, segman yuvası ölçüleri ve dişli hesaplarını yapar.
- **Birim Çevirici:** Teknik birimler arasında hızlı dönüşüm sağlar.

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel makinenize kurmak için aşağıdaki adımları izleyin:

### Gereksinimler
- Python 3.10 veya üzeri
- Git

### 1. Projeyi Klonlayın
```bash
git clone [https://github.com/KULLANICI_ADIN/BEM_Otomasyon.git](https://github.com/KULLANICI_ADIN/BEM_Otomasyon.git)
cd BEM_Otomasyon

```

### 2. Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt

```

### 3. Uygulamayı Başlatın

```bash
python main_launcher.py

```

---

## 📂 Proje Dizin Yapısı

```text
BEM_Otomasyon/
├── apps/
│   ├── proje_klasor_yonetimi/   # Modül 1 Kaynak Kodları
│   ├── maliyet_hesaplama/       # Modül 2 Kaynak Kodları (PDF & TCMB)
│   ├── kesim_optimizasyonu/     # Modül 3 Kaynak Kodları (Nesting)
│   └── standart_kutuphane/      # Modül 4 Kaynak Kodları (Data)
├── assets/                      # İkonlar ve görseller
├── main_launcher.py             # Ana Menü (Başlatıcı)
├── requirements.txt             # Bağımlılıklar
└── README.md                    # Dökümantasyon

```

## 📞 İletişim & Geliştirici

Bu proje **[HASAN MIHALIÇLI]** tarafından geliştirilmiştir.

* **GitHub:** [github.com/hasanmihalicil23](https://www.google.com/search?q=https://github.com/hasanmihalicli23)
* **Email:** [mail@hasanmihalicli.com]

---

*Copyright © 2026 BEM Engineering Solutions.*

```

---

### 2. Dosya: `requirements.txt` (Kütüphane Listesi)
Bu dosya, projeyi başka bir bilgisayara kurarken hangi modüllerin gerekli olduğunu söyler. Proje ana dizinine bu isimle kaydet:

```text
customtkinter==5.2.2
pandas>=2.0.0
openpyxl>=3.1.0
reportlab>=4.0.0
requests>=2.31.0
Pillow>=10.0.0

```

---

### 3. Dosya: `.gitignore` (Gereksiz Dosya Engelleyici)

Bu dosya, gereksiz sistem dosyalarının GitHub'a yüklenmesini engeller. Proje ana dizinine `.gitignore` adıyla (nokta ile başlar) kaydet:

```text
# Python derleme dosyaları
__pycache__/
*.pyc
*.pyo
*.pyd

# Sanal ortam klasörleri
venv/
env/
.env

# IDE ayar dosyaları
.vscode/
.idea/

# Windows sistem dosyaları
Thumbs.db
Desktop.ini

# Proje çıktıları (Kullanıcı verisi içerdiği için yüklenmez)
*.pdf
*.xlsx
katalog.json
bem_folder_config.json

```

---

### Son Adım: GitHub'a Gönder 🚀

Bu dosyaları oluşturup kaydettikten sonra terminali aç ve şu komutlarla gönder:

```bash
git add .
git commit -m "Proje dökümantasyonu, lisans ve gereksinimler eklendi"
git push

```

