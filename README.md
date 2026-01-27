```markdown
# BEM Otomasyon

BEM Otomasyon, üretim ve mühendislik süreçlerini dijitalleştirmek, proje yönetimini standartlaştırmak ve maliyet analizlerini otomatize etmek için geliştirilmiş Python tabanlı bir masaüstü yazılımıdır.

## Özellikler ve Modüller

Sistem 4 ana modülden oluşmaktadır:

**1. Proje Klasör Yönetimi**
* Müşteri ve ürün bazlı standart klasör ağacını otomatik oluşturur.
* Dökümantasyon, Tasarım ve Üretim klasörlerini standartlaştırır.
* Dosya arşivleme düzenini sağlar.

**2. Maliyet Analizi ve Teklif**
* Hammadde, işçilik ve fason giderlerini hesaplar.
* TCMB entegrasyonu ile anlık döviz kurlarını çeker.
* Teklifleri PDF formatında oluşturur ve ilgili proje klasörüne kaydeder.

**3. Kesim Optimizasyonu (Nesting)**
* Profil ve boru kesimlerinde minimum fire hesabını yapar.
* Kesim planını görselleştirir ve raporlar.

**4. Teknik Kütüphane**
* Standart makine elemanları (Cıvata, Rulman, Profil) veritabanı.
* Mühendislik hesaplama araçları (Kama, Dişli, Birim Çevirme).

## Kurulum ve Kullanım

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları uygulayın.

1. Projeyi indirin:
```bash
git clone [https://github.com/hasanmihalicli23/BEM_Otomasyon.git](https://github.com/hasanmihalicli23/BEM_Otomasyon.git)
cd BEM_Otomasyon

```

2. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt

```

3. Uygulamayı başlatın:

```bash
python main_launcher.py

```

## Proje Yapısı

* **apps/**: Modüllerin kaynak kodları (Maliyet, Klasörleme, Kesim, Kütüphane).
* **assets/**: Arayüz dosyaları.
* **main_launcher.py**: Ana giriş ekranı.
* **requirements.txt**: Gerekli Python kütüphaneleri listesi.

## İletişim

Geliştirici: Hasan Mıhalıçlı
GitHub: https://github.com/hasanmihalicli23

```

```
