`<div>` etiketi GitHub'da çalışır, ancak **Markdown içinde HTML kullanmanın bazı kuralları vardır.** Eğer çalışmıyorsa sebebi şunlardan biridir:

1. **Boşluk Hatası:** HTML etiketleri (`<div>` vb.) ile Markdown kodları (örneğin `## Başlık`) arasında **bir satır boşluk** bırakmazsan GitHub bunları tanımaz ve bozuk gösterir.
2. **Kapanmayan Etiket:** `<div>` açtıysan, mutlaka `</div>` ile kapatman gerekir. Yoksa sayfanın geri kalanı tamamen bozulur.
3. **VS Code Önizlemesi:** Bazen VS Code önizlemesi ile GitHub'ın gerçek görüntüsü farklı olabilir.

Senin için **"Hem ortalı (div'li) olsun, hem de bozulmasın"** diyorsan, işte **en garantili hibrit sürüm.**

Sadece **Logo ve Başlık** kısmını HTML (div) ile ortaladım, geri kalan her şeyi **Standart Markdown** yaptım. Bu sayede hem çok şık durur hem de asla bozulmaz.

Bunu kopyala ve yapıştır:

```markdown
<div align="center">

# 🏭 BEM OTOMASYON SİSTEMİ

<img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
<img src="https://img.shields.io/badge/Lisans-MIT-green?style=for-the-badge" />

<br>

**"Üretim süreçlerindeki kaosu bitiren, mühendislik ve maliyet yönetimini<br>tek çatı altında toplayan profesyonel çözüm."**

<br>
</div>

---

## 🧩 Modüller ve Yetenekler

Sistem, üretimdeki darboğazları çözmek için 4 ana modülden oluşur:

| 📁 1. Akıllı Proje Yönetimi | 💰 2. Maliyet & Teklif Robotu |
| :--- | :--- |
| • **Oto-Klasörleme:** Müşteri/Ürün bazlı standart klasör ağacını tek tıkla kurar.<br>• **ERP Mantığı:** Dosyaları otomatik olarak doğru yere kaydeder.<br>• **Düzen:** Dosya karmaşasını %100 engeller. | • **Canlı Kur:** TCMB'den anlık **USD/EUR** çeker.<br>• **Hassas Hesap:** Malzeme ve işçilik karlarını ayrı yönetir.<br>• **PDF Çıktısı:** Teklifi oluşturur ve müşteri klasörüne kaydeder. |

| ✂️ 3. Kesim Optimizasyonu | 📚 4. Mühendislik Kütüphanesi |
| :--- | :--- |
| • **Minimum Fire:** Profilleri en az atık olacak şekilde dizer.<br>• **Görsel Rapor:** Kesim planını grafiksel olarak ekrana çizer.<br>• **Stok Takibi:** Hangi parçanın nereden çıkacağını raporlar. | • **Dijital Katalog:** Cıvata, Rulman, Profil verilerini içerir.<br>• **Hesaplayıcılar:** Kama kanalı, dişli ve segman hesabı yapar.<br>• **Birim Çevirici:** Teknik birimler arası hızlı dönüşüm sağlar. |

---

## 🛠️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için terminale sırasıyla şu komutları yazın:

**1. Projeyi İndirin:**
```bash
git clone [https://github.com/hasanmihalicli23/BEM_Otomasyon.git](https://github.com/hasanmihalicli23/BEM_Otomasyon.git)
cd BEM_Otomasyon

```

**2. Gerekli Kütüphaneleri Yükleyin:**

```bash
pip install -r requirements.txt

```

**3. Programı Başlatın:**

```bash
python main_launcher.py

```

---

## 📂 Proje Dizin Yapısı

```text
BEM_Otomasyon/
├── 📂 apps/                  # MODÜLLERİN KAYNAK KODLARI
│   ├── 📂 proje_klasor_yonetimi/
│   ├── 📂 maliyet_hesaplama/
│   ├── 📂 kesim_optimizasyonu/
│   └── 📂 standart_kutuphane/
├── 📂 assets/                # Arayüz Görselleri
├── 📄 main_launcher.py       # ANA BAŞLATICI
├── 📄 requirements.txt       # Kütüphane Listesi
└── 📄 README.md              # Proje Dökümantasyonu

```

---

<div align="center">

### 📞 İletişim & Geliştirici

Bu proje **Hasan Mıhalıçlı** tarafından geliştirilmiştir.

<a href="https://github.com/hasanmihalicli23">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/GitHub-Follow-181717%3Fstyle%3Dflat%26logo%3Dgithub" />
</a>
<a href="mailto:mail@hasanmihalicli.com">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Email-Contact-D14836%3Fstyle%3Dflat%26logo%3Dgmail%26logoColor%3Dwhite" />
</a>

*Copyright © 2026 BEM Engineering Solutions*

</div>

```

```
