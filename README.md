```markdown
<div align="center">

  # 🏭 BEM OTOMASYON SİSTEMİ
  ### Entegre Üretim, Maliyet Analizi ve Proje Yönetim Çözümü

  <p>
    <img src="https://img.shields.io/badge/VERSION-V5.3-blue?style=for-the-badge&logo=appveyor" />
    <img src="https://img.shields.io/badge/PYTHON-3.10%2B-F7D100?style=for-the-badge&logo=python&logoColor=black" />
    <img src="https://img.shields.io/badge/PLATFORM-WINDOWS-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
    <img src="https://img.shields.io/badge/LISANS-MIT-green?style=for-the-badge" />
  </p>

  <p>
    <strong>BEM Otomasyon</strong>, üretim süreçlerindeki kaosu bitirmek için tasarlandı. <br>
    Klasörlemeden maliyet analizine, teknik hesaplamalardan kesim optimizasyonuna kadar her şey tek bir arayüzde.
  </p>

  <br>

</div>

---

## 🧩 MODÜLLER VE YETENEKLER

Proje, birbirine entegre çalışan 4 ana güç merkezinden oluşur.

| 📁 1. Akıllı Proje Yönetimi | 💰 2. Maliyet & Teklif Robotu |
| :--- | :--- |
| • **Oto-Klasörleme:** Müşteri ve Ürün adına göre standart `Dökümantasyon`, `Tasarım`, `Üretim` ağacını saniyeler içinde kurar.<br>• **ERP Mantığı:** Tüm dosyaları doğru yere, standart isimlendirme ile kaydeder.<br>• **Düzen:** Yanlış yere dosya kaydetmeyi imkansız kılar. | • **Canlı Kur:** TCMB'den anlık **USD/EUR** çeker.<br>• **Hassas Hesap:** Malzeme, İşçilik ve Fason giderlerini ayrı marjlarla hesaplar.<br>• **PDF Çıktısı:** Profesyonel teklif formunu oluşturur ve ilgili klasöre atar.<br>• **Çoklu Para:** Maliyeti aynı anda TL, USD ve EUR gösterir. |

| ✂️ 3. Kesim Optimizasyonu (Nesting) | 📚 4. Dijital Mühendislik Kütüphanesi |
| :--- | :--- |
| • **Minumum Fire:** Profil ve boru kesimlerinde en az fire verecek kombinasyonu hesaplar.<br>• **Görsel Rapor:** Hangi parçanın hangi stoktan kesileceğini grafiksel çizer.<br>• **Stok Takibi:** Kullanılan ve kalan parçaları raporlar. | • **Canlı Katalog:** Cıvata, Rulman, Profil gibi elemanların teknik verilerini içerir.<br>• **Hesaplayıcılar:** Kama kanalı, dişli hesabı ve birim çevirici.<br>• **Genişletilebilir:** JSON tabanlı veritabanı sayesinde kolayca yeni ürün eklenir. |

## 🛠️ KURULUM VE ÇALIŞTIRMA

Bilgisayarınıza kurmak için aşağıdaki adımları terminale (CMD) sırasıyla yapıştırın:

### 1. İndirme
```bash
git clone [https://github.com/hasanmihalicli23/BEM_Otomasyon.git](https://github.com/hasanmihalicli23/BEM_Otomasyon.git)
cd BEM_Otomasyon

```

### 2. Yükleme

```bash
pip install -r requirements.txt

```

### 3. Başlatma

```bash
python main_launcher.py

```

---

<div align="center">

### 📂 PROJE DİZİN YAPISI

```text
BEM_Otomasyon/
├── 📂 apps/                  # Modül Kaynak Kodları
│   ├── proje_klasor_yonetimi/
│   ├── maliyet_hesaplama/
│   ├── kesim_optimizasyonu/
│   └── standart_kutuphane/
├── 📂 assets/                # Arayüz Görselleri
├── 📄 main_launcher.py       # Ana Kontrol Paneli
├── 📄 requirements.txt       # Kütüphane Listesi
└── 📄 README.md              # Bu Dosya

```

**Geliştirici:** [HASAN MIHALIÇLI]

*Copyright © 2026 BEM Engineering Solutions*

</div>
