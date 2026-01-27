```markdown
<div align="center">

  # 🏭 BEM Otomasyon - Entegre Üretim Yönetim Sistemi
  
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-007ACC?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Stable-success?style=for-the-badge" />

  <br />
  <br />

  > **İmalat ve mühendislik süreçlerini dijitalleştirmek için geliştirilmiş; <br /> proje yönetimi, maliyet analizi, kesim optimizasyonu ve teknik hesaplamaları <br /> tek çatı altında toplayan profesyonel masaüstü otomasyonu.**

  <br />

</div>

---

## 🚀 Proje Hakkında

Üretim sektöründe verimliliği düşüren en büyük etkenler; karmaşık dosya yapıları, manuel yapılan maliyet hesapları ve malzeme fireleridir.

**BEM Otomasyon**, bu karmaşayı bitirmek için tasarlanmıştır. Sistem, müşteri klasörlerini otomatik oluşturur, TCMB'den canlı kur çekerek maliyet hesaplar, kesim firelerini minimize eder ve mühendislik hesaplarını saniyeler içinde çözer.

---

## 🌟 Modüller ve Özellikler

Proje, birbirine entegre çalışan 4 ana güç merkezinden oluşur:

| Modül | Açıklama |
| :--- | :--- |
| **📂 Akıllı Klasör Yönetimi** | Müşteri ve Ürün adına göre standart `Dökümantasyon`, `Tasarım`, `Üretim` klasör ağacını tek tıkla kurar. |
| **💰 Maliyet & Teklif** | Malzeme, işçilik ve fason giderlerini hesaplar. TCMB'den **canlı kur** çeker ve **otomatik PDF teklif** oluşturur. |
| **✂️ Kesim Optimizasyonu** | Profil ve boru kesimlerinde (1D Nesting) en az fire verecek yerleşimi matematiksel olarak hesaplar ve görselleştirir. |
| **📚 Teknik Kütüphane** | Cıvata, Rulman, Profil gibi standart elemanların verilerini ve mühendislik hesaplayıcılarını (Kama, Dişli) içerir. |

---

## 🛠️ Kurulum ve Çalıştırma Rehberi

Projeyi kendi bilgisayarınızda çalıştırmak ve geliştirmek için aşağıdaki adımları sırasıyla uygulayabilirsiniz.

> **Ön Bilgi:** Bu proje **Python** ile geliştirilmiştir. Bilgisayarınızda Python'un yüklü olduğundan emin olun.

### Adım 1: Projeyi Bilgisayarınıza İndirin

Öncelikle terminalinizi (veya CMD) açın ve projeyi klonlamak için şu komutu yapıştırın:

```bash
git clone [https://github.com/hasanmihalicli23/BEM_Otomasyon.git](https://github.com/hasanmihalicli23/BEM_Otomasyon.git)

```

Ardından proje klasörünün içine girin:

```bash
cd BEM_Otomasyon

```

### Adım 2: Gerekli Kütüphaneleri Yükleyin

Projenin çalışması için gerekli modern arayüz ve hesaplama paketlerini yükleyin:

```bash
pip install -r requirements.txt

```

### Adım 3: Uygulamayı Başlatın 🚀

Her şey hazır! Ana kontrol panelini (Launcher) başlatmak için:

```bash
python main_launcher.py

```

---

## 📂 Proje Dizin Yapısı

```text
BEM_Otomasyon/
├── apps/                        # MODÜL KAYNAK KODLARI
│   ├── proje_klasor_yonetimi/   # Modül 1: Klasör Yapılandırma
│   ├── maliyet_hesaplama/       # Modül 2: Maliyet & PDF & TCMB
│   ├── kesim_optimizasyonu/     # Modül 3: Nesting Algoritması
│   └── standart_kutuphane/      # Modül 4: Teknik Veri & Hesap
├── assets/                      # İkonlar ve Arayüz Görselleri
├── main_launcher.py             # Ana Başlatıcı
├── requirements.txt             # Kütüphane Listesi
└── README.md                    # Dökümantasyon

```

---

<div align="center">

### 👨‍💻 Geliştirici

**Hasan Mıhalıçlı**

<a href="https://www.linkedin.com/in/hasanmihalicli23/" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin" />
</a>
<a href="https://github.com/hasanmihalicli23" target="_blank">
<img src="https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github" />
</a>

<br />
<br />

*Copyright © 2026 BEM Engineering Solutions.*

</div>

```

```
