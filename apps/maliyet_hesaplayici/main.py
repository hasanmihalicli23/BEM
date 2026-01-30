import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
import requests
import xml.etree.ElementTree as ET
import threading
import re
import json
import os
import sys
import uuid
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A5 
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

# --- 1. DİNAMİK YOL VE AYARLAR ---
def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    FIXED_ROOT = sys.argv[1]
else:
    FIXED_ROOT = os.path.join(os.path.expanduser("~"), "Documents", "BEM_Kayitlari")

if not os.path.exists(FIXED_ROOT): os.makedirs(FIXED_ROOT, exist_ok=True)

DOSYA_ADI = resource_path("katalog.json")
BIRIM_DOSYA_ADI = resource_path("birimler.json")

# --- GLOBAL DEĞİŞKENLER ---
CTK_THEME = "blue"
CTK_APPEARANCE = "Dark"
APP_TITLE = "BEM - Maliyet ve Teklif Yönetimi"
FONT_BOLD = ("Segoe UI", 12, "bold")
FONT_ICON = ("Segoe UI Emoji", 20)

COLOR_PRIMARY = "#1976D2"
COLOR_SECONDARY = "#546E7A"
COLOR_DANGER = "#D32F2F"
COLOR_SUCCESS = "#388E3C"
COLOR_WARNING = "#F57C00" 

proje_verileri = []
oto_kayit_job = None 
ACIK_DOSYA_YOLU = None  
app = None 

# --- DÜZENLEME MODU GLOBAL DEĞİŞKENLERİ ---
duzenleme_modu = False
duzenlenecek_id = None
aktif_duzenleme_tipi = None 

varsayilan_katalog = {
    "Motorlar": ["Asenkron Motor 0.18 kW", "Asenkron Motor 0.37 kW"],
    "Redüktörler": ["Sonsuz Vida 30 Gövde", "Sonsuz Vida 50 Gövde"],
    "Sürücüler": ["Hız Kontrol 0.37 kW", "Hız Kontrol 0.75 kW"],
    "Rulmanlar": ["UCFL 204", "UCFL 205", "6204 ZZ"],
    "Hammadde: Saclar": ["DKP Sac 1mm", "DKP Sac 2mm", "Paslanmaz Sac 1mm"],
    "Hammadde: Profiller": ["Kutu Profil 30x30", "Kutu Profil 40x40"],
    "Civatalar": ["M6 Civata", "M8 Civata", "M10 Civata"],
    "Pnömatik": ["Piston Ø32", "Piston Ø50", "Valf 5/2"],
    "Diğer / Özel Giriş": ["Diğer (Manuel Giriş)"]
}
varsayilan_birimler = ["Adet", "Kg", "Mt", "Tk", "Lt", "Paket", "Plaka", "Hizmet", "Saat"]

# --- 2. YARDIMCI FONKSİYONLAR ---
def format_para(deger):
    try: return f"{float(deger):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except: return "0,00"

def temizle_dosya_adi(isim):
    return re.sub(r'[\\/*?:<>|]', '_', str(isim).strip())

def create_card(parent, title):
    f = ctk.CTkFrame(parent)
    ctk.CTkLabel(f, text=title, font=("Segoe UI", 13, "bold"), text_color="gray").pack(anchor="w", padx=10, pady=5)
    return f

def create_res_card(parent, title, color_theme):
    f = ctk.CTkFrame(parent, fg_color=color_theme)
    ctk.CTkLabel(f, text=title, font=("Segoe UI", 12, "bold"), text_color="#444").pack(anchor="center", pady=(5, 0))
    return f

# --- 3. KLASÖR VE DOSYA YÖNETİMİ ---
def klasor_yapisi_kontrol_ve_olustur():
    m_adi = temizle_dosya_adi(entry_musteri.get())
    p_adi = temizle_dosya_adi(entry_proje_adi.get())
    if not m_adi or not p_adi:
        messagebox.showwarning("Eksik Bilgi", "Lütfen Müşteri ve Proje Adını giriniz.")
        return None
    proje_yolu = os.path.join(FIXED_ROOT, m_adi, p_adi)
    hedef_yol = os.path.join(proje_yolu, "Dökümantasyon", "Teklifler")
    if os.path.exists(hedef_yol): return hedef_yol
    try:
        structure = {
            "Dökümantasyon": ["Görseller", "Malzeme Listeleri", "Teklifler"],
            "Tasarım Dosyaları": ["Ana Montaj", "Mekanik Parçalar", "Sac Parçalar", "Satınalma Parçaları"],
            "Üretim Çıktıları": ["DXF Kesim", "PDF Teknik Resim", "STEP 3D"]
        }
        if not os.path.exists(proje_yolu): os.makedirs(proje_yolu)
        for ana, altlar in structure.items():
            os.makedirs(os.path.join(proje_yolu, ana), exist_ok=True)
            for alt in altlar: os.makedirs(os.path.join(proje_yolu, ana, alt), exist_ok=True)
        return hedef_yol
    except Exception as e:
        messagebox.showerror("Hata", str(e)); return None

def katalog_kaydet(veri):
    try:
        with open(DOSYA_ADI, "w", encoding="utf-8") as f: json.dump(veri, f, ensure_ascii=False, indent=4)
    except: pass

def katalog_yukle():
    if os.path.exists(DOSYA_ADI):
        try:
            with open(DOSYA_ADI, "r", encoding="utf-8") as f: return json.load(f)
        except: return varsayilan_katalog
    else: 
        katalog_kaydet(varsayilan_katalog); return varsayilan_katalog

def birim_kaydet(veri_listesi):
    try:
        with open(BIRIM_DOSYA_ADI, "w", encoding="utf-8") as f: json.dump(veri_listesi, f, ensure_ascii=False, indent=4)
    except: pass

def birim_yukle():
    if os.path.exists(BIRIM_DOSYA_ADI):
        try:
            with open(BIRIM_DOSYA_ADI, "r", encoding="utf-8") as f: return json.load(f)
        except: return varsayilan_birimler
    else:
        birim_kaydet(varsayilan_birimler); return varsayilan_birimler

katalog = katalog_yukle()
birim_katalog = birim_yukle()

# --- 4. İŞ MANTIĞI ---
def tcmb_kur_getir():
    try:
        res = requests.get("https://www.tcmb.gov.tr/kurlar/today.xml", timeout=5)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            for curr in root.findall('Currency'):
                kod = curr.get('Kod')
                if kod == 'USD': 
                    entry_kur_usd.delete(0, 'end'); entry_kur_usd.insert(0, curr.find('ForexSelling').text)
                elif kod == 'EUR': 
                    entry_kur_eur.delete(0, 'end'); entry_kur_eur.insert(0, curr.find('ForexSelling').text)
            lbl_durum.configure(text="Kurlar Güncel ✔", text_color=COLOR_SUCCESS)
    except: lbl_durum.configure(text="Kur Hatası ✘", text_color=COLOR_DANGER)

def baslat_kur_thread(): threading.Thread(target=tcmb_kur_getir, daemon=True).start()

def proje_verilerini_topla():
    return {
        "metadata": {
            "proje_adi": entry_proje_adi.get(), "musteri": entry_musteri.get(),
            "teklif_no": entry_teklif_no.get(), 
            "kur_usd": entry_kur_usd.get(), "kur_eur": entry_kur_eur.get(),
            "kar_malzeme": entry_kar_malzeme.get(), "kar_iscilik": entry_kar_iscilik.get(), "kdv": entry_kdv.get()
        }, "items": proje_verileri
    }

def hesapla():
    try:
        k_usd = float(entry_kur_usd.get().replace(',', '.'))
        k_eur = float(entry_kur_eur.get().replace(',', '.'))
        m_mal = float(entry_kar_malzeme.get().replace(',', '.')) / 100
        m_isc = float(entry_kar_iscilik.get().replace(',', '.')) / 100
        kdv = float(entry_kdv.get().replace(',', '.')) / 100
        
        ham_m = 0; ham_i = 0; satis_m = 0; satis_i = 0
        for v in proje_verileri:
            t = v["tutar"]
            if v["para"] == "TL": t /= k_usd
            elif v["para"] == "EUR": t = (t * k_eur) / k_usd
            
            if v["tip"] == "ISCILIK": ham_i += t; satis_i += t * (1 + m_isc)
            else: ham_m += t; satis_m += t * (1 + m_mal)
        
        total = satis_m + satis_i
        update_card(lbl_ham_toplam_val, ham_m + ham_i, k_usd, k_eur)
        update_card(lbl_satis_toplam_val, total, k_usd, k_eur)
        update_card(lbl_tl_kdvli_val, total * (1 + kdv), k_usd, k_eur)
    except: pass

def update_card(label, val, k_u, k_e):
    label.configure(text=f"$ {format_para(val)}\n€ {format_para(val*k_u/k_e)}\n₺ {format_para(val*k_u)}")

def tabloyu_guncelle():
    for i in tablo.get_children(): tablo.delete(i)
    filtre = cmb_filtre.get() 
    for v in proje_verileri:
        goster = False
        if filtre == "Tümü": goster = True
        elif filtre == "Sadece Malzeme" and v["tip"] == "MALZEME": goster = True
        elif filtre == "Sadece İşçilik" and v["tip"] == "ISCILIK": goster = True
        elif filtre == "Sadece Dış Hizmet" and v["tip"] == "FASON": goster = True
        
        if goster:
            tablo.insert("", "end", iid=v["id"], values=(v["kategori"], v["urun"], f"{v['miktar']:g} {v['birim']}", format_para(v["birim_fiyat"]), v["para"], format_para(v["tutar"]), v["tutar"], v["birim_fiyat"]))

def projeyi_kaydet(sessiz=False):
    global ACIK_DOSYA_YOLU
    veri = proje_verilerini_topla()
    hedef = klasor_yapisi_kontrol_ve_olustur()
    if not hedef: return False
    
    dosya = f"{temizle_dosya_adi(entry_musteri.get())} - {temizle_dosya_adi(entry_proje_adi.get())}.json"
    yol = os.path.join(hedef, dosya)
    
    try:
        with open(yol, "w", encoding="utf-8") as f: json.dump(veri, f, ensure_ascii=False, indent=4)
        ACIK_DOSYA_YOLU = yol
        if not sessiz: messagebox.showinfo("Başarılı", f"Kaydedildi:\n{yol}")
    except Exception as e:
        if not sessiz: messagebox.showerror("Hata", str(e))

def yukle_from_path(dosya_yolu):
    global ACIK_DOSYA_YOLU, proje_verileri
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f: veri = json.load(f)
        meta = veri.get("metadata", {})
        entry_proje_adi.delete(0, 'end'); entry_proje_adi.insert(0, meta.get("proje_adi", ""))
        entry_musteri.delete(0, 'end'); entry_musteri.insert(0, meta.get("musteri", ""))
        entry_teklif_no.delete(0, 'end'); entry_teklif_no.insert(0, meta.get("teklif_no", ""))
        entry_kur_usd.delete(0, 'end'); entry_kur_usd.insert(0, meta.get("kur_usd", "35.50"))
        entry_kur_eur.delete(0, 'end'); entry_kur_eur.insert(0, meta.get("kur_eur", "38.20"))
        entry_kar_malzeme.delete(0, 'end'); entry_kar_malzeme.insert(0, meta.get("kar_malzeme", "30"))
        entry_kar_iscilik.delete(0, 'end'); entry_kar_iscilik.insert(0, meta.get("kar_iscilik", "60"))
        entry_kdv.delete(0, 'end'); entry_kdv.insert(0, meta.get("kdv", "20"))
        
        ham_veri = veri.get("items", [])
        proje_verileri = []
        for item in ham_veri:
            if "id" not in item: item["id"] = str(uuid.uuid4())
            proje_verileri.append(item)

        ACIK_DOSYA_YOLU = dosya_yolu
        tabloyu_guncelle(); hesapla(); messagebox.showinfo("Yüklendi", "Proje yüklendi.")
    except Exception as e: messagebox.showerror("Hata", str(e))

def projeyi_yukle():
    yol = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    if yol: yukle_from_path(yol)

def excele_aktar():
    if not proje_verileri: return
    hedef = klasor_yapisi_kontrol_ve_olustur()
    if not hedef: return
    dosya = f"{temizle_dosya_adi(entry_musteri.get())} - {temizle_dosya_adi(entry_proje_adi.get())}.xlsx"
    yol = os.path.join(hedef, dosya)
    data = []
    for v in proje_verileri:
        t_tl = v["tutar"] if v["para"] == "TL" else 0
        t_usd = v["tutar"] if v["para"] == "USD" else 0
        t_eur = v["tutar"] if v["para"] == "EUR" else 0
        data.append([v["tip"], v["kategori"], v["urun"], v["miktar"], v["birim"], v["birim_fiyat"], v["para"], t_tl, t_usd, t_eur])
    df = pd.DataFrame(data, columns=["Tip", "Kategori", "Ürün", "Miktar", "Birim", "Birim Fiyat", "Para", "TL", "USD", "EUR"])
    hesapla()
    try:
        with pd.ExcelWriter(yol, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Detaylar', index=False)
        if messagebox.askyesno("Excel", f"Kaydedildi: {yol}\nAçmak ister misin?"): os.startfile(hedef)
    except Exception as e: messagebox.showerror("Hata", str(e))

def pdf_olustur_ve_ac():
    if not proje_verileri: return
    hedef = klasor_yapisi_kontrol_ve_olustur()
    if not hedef: return
    dosya = f"{temizle_dosya_adi(entry_musteri.get())} - {temizle_dosya_adi(entry_proje_adi.get())}.pdf"
    yol = os.path.join(hedef, dosya)
    try:
        try:
            pdfmetrics.registerFont(TTFont('TrArial', 'arial.ttf'))
            pdfmetrics.registerFont(TTFont('TrArial-Bold', 'arialbd.ttf'))
            f_n = 'TrArial'; f_b = 'TrArial-Bold'
        except:
            f_n = 'Helvetica'; f_b = 'Helvetica-Bold'
        c = canvas.Canvas(yol, pagesize=A5)
        w, h = A5
        def baslik_ciz():
            c.setFont(f_b, 14)
            c.drawRightString(w-20, h-40, "MALİYET RAPORU")
            c.setFont(f_n, 9)
            c.drawString(20, h-60, f"FİRMA: {entry_musteri.get()}")
            c.drawRightString(w-20, h-60, f"TEKLİF NO: {entry_teklif_no.get()}") 
            c.drawString(20, h-75, f"PROJE: {entry_proje_adi.get()}")
            c.drawString(20, h-90, f"TARİH: {datetime.now().strftime('%d.%m.%Y')}")
            c.setFont(f_b, 8)
            kur_bilgi = f"KUR: USD {entry_kur_usd.get()} | EUR {entry_kur_eur.get()}"
            c.drawString(20, h-105, kur_bilgi)
            y_baslik = h-135
            c.setFont(f_b, 9)
            c.drawString(20, y_baslik, "ÜRÜN / AÇIKLAMA")
            c.drawRightString(w-20, y_baslik, "TUTAR")
            c.setLineWidth(1)
            c.line(20, y_baslik-5, w-20, y_baslik-5)
            return y_baslik - 20 
        y = baslik_ciz()
        c.setFont(f_n, 9)
        for v in proje_verileri:
            urun_text = v["urun"]
            satirlar = simpleSplit(urun_text, f_n, 9, 300)
            satir_sayisi = len(satirlar)
            satir_yuksekligi = satir_sayisi * 12 
            toplam_alan = satir_yuksekligi + 5 
            if y - toplam_alan < 30:
                c.showPage(); y = baslik_ciz(); c.setFont(f_n, 9)
            c.drawRightString(w-20, y, f"{v['para']} {format_para(v['tutar'])}")
            text_y = y
            for satir in satirlar:
                c.drawString(20, text_y, satir)
                text_y -= 12
            y -= toplam_alan
        if y < 100: c.showPage(); y = h-50
        else: y -= 10 
        c.setLineWidth(1); c.line(20, y, w-20, y); y -= 20
        ham_maliyet = lbl_ham_toplam_val.cget('text').replace('\n', '  |  ')
        satis_fiyati = lbl_satis_toplam_val.cget('text').replace('\n', '  |  ')
        kar_oranlari = f"Kâr Oranları: Malzeme %{entry_kar_malzeme.get()}  -  İşçilik %{entry_kar_iscilik.get()}"
        c.setFont(f_n, 9); c.drawRightString(w-20, y, f"HAM MALİYET:  {ham_maliyet}"); y -= 15
        c.setFont(f_n, 8); c.setFillColor(colors.gray); c.drawRightString(w-20, y, kar_oranlari); c.setFillColor(colors.black); y -= 25 
        c.setFont(f_b, 12); c.drawRightString(w-20, y, f"NET TOPLAM:  {satis_fiyati}")
        c.save()
        if messagebox.askyesno("PDF Hazır", f"Kaydedildi: {yol}\nAçmak ister misin?"): os.startfile(yol)
    except Exception as e: messagebox.showerror("Hata", f"PDF Hatası:\n{str(e)}")

def oto_kayit_dongusu(ms):
    global oto_kayit_job
    if cmb_oto_kayit.get() == "Kapalı": return
    if entry_proje_adi.get(): projeyi_kaydet(sessiz=True)
    oto_kayit_job = app.after(ms, lambda: oto_kayit_dongusu(ms))

def oto_kayit_ayar_degisti(e=None):
    global oto_kayit_job
    if oto_kayit_job: app.after_cancel(oto_kayit_job); oto_kayit_job = None
    s = cmb_oto_kayit.get()
    if s != "Kapalı":
        ms = {"30 Saniye": 30000, "1 Dakika": 60000, "5 Dakika": 300000}
        oto_kayit_dongusu(ms.get(s, 60000))

def kategori_degisti(event):
    sec = cmb_kategori.get()
    cmb_urun.configure(values=katalog.get(sec, []))
    if katalog.get(sec): cmb_urun.set(katalog.get(sec)[0])
    manuel_mod_kontrol()

def manuel_mod_kontrol():
    if var_manuel.get() == 1: 
        cmb_urun.configure(state="normal"); cmb_urun.set(""); cmb_urun.focus_set()
        cmb_kategori.configure(state="normal")
    else: 
        cmb_urun.configure(state="readonly"); cmb_kategori.configure(state="readonly") 

def listeden_sil_buton():
    k = cmb_kategori.get(); u = cmb_urun.get()
    if k in katalog and u in katalog[k]:
        if messagebox.askyesno("Sil", f"'{u}' katalogdan silinsin mi?"):
            katalog[k].remove(u); katalog_kaydet(katalog); cmb_urun.configure(values=katalog[k]); cmb_urun.set("")

def kategori_sil_buton():
    k = cmb_kategori.get()
    if k in katalog:
        if messagebox.askyesno("Kategori Sil", f"'{k}' kategorisi ve içindeki tüm ürünler silinsin mi?"):
            del katalog[k]
            katalog_kaydet(katalog)
            cmb_kategori.configure(values=list(katalog.keys()))
            cmb_kategori.set("")
            cmb_urun.configure(values=[]); cmb_urun.set("")

# --- GÜNCELLENEN BUTON YÖNETİMİ ---
def butonlari_sifirla():
    global duzenleme_modu, duzenlenecek_id, aktif_duzenleme_tipi
    duzenleme_modu = False
    duzenlenecek_id = None
    aktif_duzenleme_tipi = None
    
    # Tüm butonları eski haline getir
    btn_malzeme_ekle.configure(text="LİSTEYE EKLE (+)", fg_color=COLOR_PRIMARY, hover_color="#1565C0")
    btn_fason_ekle.configure(text="EKLE (+)", fg_color=COLOR_PRIMARY, hover_color="#1565C0")
    btn_iscilik_ekle.configure(text="EKLE (+)", fg_color=COLOR_PRIMARY, hover_color="#1565C0")

# --- KAYIT / GÜNCELLEME FONKSİYONLARI ---
def malzeme_ekle():
    if not entry_fiyat.get(): return
    kat = cmb_kategori.get(); urun = cmb_urun.get(); birim = cmb_birim.get()
    
    # Katalog Güncelleme
    katalog_guncellendi = False
    if kat not in katalog: katalog[kat] = []; katalog_guncellendi = True
    saf_urun = urun.split(" (")[0] if " (" in urun else urun
    if saf_urun not in katalog[kat]: katalog[kat].append(saf_urun); katalog_guncellendi = True
    if katalog_guncellendi: katalog_kaydet(katalog); cmb_kategori.configure(values=list(katalog.keys()))
    
    if birim and birim not in birim_katalog:
        birim_katalog.append(birim); birim_kaydet(birim_katalog); cmb_birim.configure(values=birim_katalog)

    tedarikci = entry_tedarikci.get()
    urun_tam_ad = f"{saf_urun} ({tedarikci})" if tedarikci else saf_urun
    
    try:
        tutar = float(entry_adet.get().replace(',','.')) * float(entry_fiyat.get().replace(',','.'))
        yeni_veri = {
            "tip": "MALZEME", "kategori": kat, "urun": urun_tam_ad, 
            "miktar": float(entry_adet.get().replace(',','.')), 
            "birim": birim, "birim_fiyat": float(entry_fiyat.get().replace(',','.')), 
            "para": cmb_para.get(), "tutar": tutar
        }
    except: return

    global duzenleme_modu, duzenlenecek_id
    if duzenleme_modu and duzenlenecek_id and aktif_duzenleme_tipi == "MALZEME":
        for item in proje_verileri:
            if item["id"] == duzenlenecek_id:
                item.update(yeni_veri)
                item["id"] = duzenlenecek_id
                break
        butonlari_sifirla()
        messagebox.showinfo("Güncellendi", "Malzeme güncellendi.")
    else:
        yeni_veri["id"] = str(uuid.uuid4())
        proje_verileri.append(yeni_veri)
    
    tabloyu_guncelle(); hesapla()
    entry_adet.delete(0, 'end'); entry_adet.insert(0, "1"); entry_fiyat.delete(0, 'end'); entry_tedarikci.delete(0, 'end')

def otomasyon_ekle():
    try:
        fiyat = float(entry_oto_fiyat.get().replace(',','.'))
        urun_adi = f"{cmb_oto_tur.get()} - {entry_oto_aciklama.get()}"
        yeni_veri = {
            "tip": "FASON", "kategori": "DIŞ HİZMET", "urun": urun_adi, 
            "miktar": 1, "birim": "Hizmet", "birim_fiyat": fiyat, 
            "para": cmb_oto_para.get(), "tutar": fiyat
        }
        
        global duzenleme_modu, duzenlenecek_id
        if duzenleme_modu and duzenlenecek_id and aktif_duzenleme_tipi == "FASON":
            for item in proje_verileri:
                if item["id"] == duzenlenecek_id:
                    item.update(yeni_veri); item["id"] = duzenlenecek_id; break
            butonlari_sifirla()
            messagebox.showinfo("Güncellendi", "Dış hizmet güncellendi.")
        else:
            yeni_veri["id"] = str(uuid.uuid4())
            proje_verileri.append(yeni_veri)
            
        tabloyu_guncelle(); hesapla()
        entry_oto_fiyat.delete(0, 'end'); entry_oto_aciklama.delete(0, 'end')
    except: pass

def iscelik_ekle():
    try:
        tur = cmb_isci_tur.get(); aciklama = entry_isci_aciklama.get() 
        k = float(entry_isci_kisi.get()); s = float(entry_isci_saat.get()); u = float(entry_isci_ucret.get())
        toplam = k * s * u
        urun_adi = f"{tur} - {aciklama} ({int(k)} Kişi)" if aciklama else f"{tur} ({int(k)} Kişi)"
        
        yeni_veri = {
            "tip": "ISCILIK", "kategori": "İŞÇİLİK", "urun": urun_adi, 
            "miktar": k*s, "birim": "Saat", "birim_fiyat": u, 
            "para": cmb_isci_para.get(), "tutar": toplam
        }

        global duzenleme_modu, duzenlenecek_id
        if duzenleme_modu and duzenlenecek_id and aktif_duzenleme_tipi == "ISCILIK":
            for item in proje_verileri:
                if item["id"] == duzenlenecek_id:
                    item.update(yeni_veri); item["id"] = duzenlenecek_id; break
            butonlari_sifirla()
            messagebox.showinfo("Güncellendi", "İşçilik güncellendi.")
        else:
            yeni_veri["id"] = str(uuid.uuid4())
            proje_verileri.append(yeni_veri)

        tabloyu_guncelle(); hesapla()
    except: pass

def sifirla():
    if messagebox.askyesno("Sıfırla", "Liste temizlensin mi?"):
        proje_verileri.clear(); tabloyu_guncelle(); hesapla()

# --- SİLME FONKSİYONU DÜZELTİLDİ ---
def sil():
    sec = tablo.selection()
    if sec and messagebox.askyesno("Sil", "Seçili satırlar silinsin mi?"):
        # HATA DÜZELTİLDİ: Artık seçili öğenin kendisi ID olduğu için doğrudan kullanıyoruz
        ids_to_delete = [s for s in sec]
        
        global proje_verileri
        proje_verileri = [p for p in proje_verileri if p["id"] not in ids_to_delete]
        tabloyu_guncelle(); hesapla()

def sirala(col, rev):
    l = [(tablo.set(k, col), k) for k in tablo.get_children('')]
    l.sort(reverse=rev)
    for i, (val, k) in enumerate(l): tablo.move(k, '', i)
    tablo.heading(col, command=lambda: sirala(col, not rev))

# --- DÜZENLEME FONKSİYONU DÜZELTİLDİ ---
def duzenle_secili():
    global duzenleme_modu, duzenlenecek_id, aktif_duzenleme_tipi
    secili_item = tablo.selection()
    
    if not secili_item:
        messagebox.showwarning("Seçim Yok", "Lütfen düzenlemek istediğiniz satırı seçin.")
        return

    # HATA DÜZELTİLDİ: Seçili öğenin kendisi zaten ID
    item_id = secili_item[0]

    veri = next((item for item in proje_verileri if item["id"] == item_id), None)
    if not veri: return

    # Önce temizlik
    butonlari_sifirla()
    duzenlenecek_id = item_id
    duzenleme_modu = True

    # TİPE GÖRE KUTULARI DOLDUR
    if veri["tip"] == "MALZEME":
        aktif_duzenleme_tipi = "MALZEME"
        cmb_kategori.set(veri["kategori"])
        kategori_degisti(None)
        
        ham_urun = veri["urun"]
        if " (" in ham_urun and ham_urun.endswith(")"):
            p = ham_urun.rsplit(" (", 1)
            cmb_urun.set(p[0]); entry_tedarikci.delete(0, 'end'); entry_tedarikci.insert(0, p[1][:-1])
        else:
            cmb_urun.set(ham_urun)
        
        entry_adet.delete(0, 'end'); entry_adet.insert(0, str(veri["miktar"]))
        cmb_birim.set(veri["birim"])
        entry_fiyat.delete(0, 'end'); entry_fiyat.insert(0, str(veri["birim_fiyat"]))
        cmb_para.set(veri["para"])
        
        btn_malzeme_ekle.configure(text="GÜNCELLE (Kaydet)", fg_color=COLOR_WARNING, hover_color="#EF6C00")
        entry_fiyat.focus_set() 
        entry_fiyat.select_range(0, 'end')

    elif veri["tip"] == "FASON":
        aktif_duzenleme_tipi = "FASON"
        try:
            parca = veri["urun"].split(" - ", 1)
            cmb_oto_tur.set(parca[0])
            entry_oto_aciklama.delete(0, 'end')
            if len(parca) > 1: entry_oto_aciklama.insert(0, parca[1])
        except: pass
        
        entry_oto_fiyat.delete(0, 'end'); entry_oto_fiyat.insert(0, str(veri["birim_fiyat"]))
        cmb_oto_para.set(veri["para"])
        
        btn_fason_ekle.configure(text="GÜNCELLE (Kaydet)", fg_color=COLOR_WARNING, hover_color="#EF6C00")
        entry_oto_fiyat.focus_set()
        entry_oto_fiyat.select_range(0, 'end')

    elif veri["tip"] == "ISCILIK":
        aktif_duzenleme_tipi = "ISCILIK"
        try:
            ham = veri["urun"]
            kisi_sayisi = "1"
            if "(" in ham:
                kisi_part = ham.rsplit("(", 1)[1] 
                kisi_sayisi = kisi_part.split(" ")[0]
                ham = ham.rsplit("(", 1)[0].strip()
            
            if " - " in ham:
                p = ham.split(" - ", 1)
                cmb_isci_tur.set(p[0])
                entry_isci_aciklama.delete(0, 'end'); entry_isci_aciklama.insert(0, p[1])
            else:
                cmb_isci_tur.set(ham)
                entry_isci_aciklama.delete(0, 'end')
            
            entry_isci_kisi.delete(0, 'end'); entry_isci_kisi.insert(0, kisi_sayisi)
        except: pass

        k = float(entry_isci_kisi.get())
        if k == 0: k = 1
        saat = veri["miktar"] / k
        
        entry_isci_saat.delete(0, 'end'); entry_isci_saat.insert(0, f"{saat:g}")
        entry_isci_ucret.delete(0, 'end'); entry_isci_ucret.insert(0, str(veri["birim_fiyat"]))
        cmb_isci_para.set(veri["para"])
        
        btn_iscilik_ekle.configure(text="GÜNCELLE (Kaydet)", fg_color=COLOR_WARNING, hover_color="#EF6C00")
        entry_isci_ucret.focus_set() 
        entry_isci_ucret.select_range(0, 'end')

# --- MAIN GUI ---
def main():
    global app, entry_proje_adi, entry_musteri, lbl_durum, entry_kur_eur, entry_kur_usd
    global cmb_oto_kayit, cmb_kategori, var_manuel, cmb_urun, entry_adet, cmb_birim, entry_fiyat, cmb_para
    global cmb_oto_tur, entry_oto_aciklama, entry_oto_fiyat, cmb_oto_para, entry_tedarikci, entry_teklif_no
    global entry_isci_kisi, entry_isci_saat, entry_isci_ucret, cmb_isci_para, cmb_isci_tur, entry_isci_aciklama, cmb_filtre
    global tablo, entry_kar_malzeme, entry_kar_iscilik, entry_kdv
    global btn_malzeme_ekle, btn_fason_ekle, btn_iscilik_ekle
    global lbl_ham_toplam_val, lbl_satis_toplam_val, lbl_tl_kdvli_val

    ctk.set_appearance_mode(CTK_APPEARANCE); ctk.set_default_color_theme(CTK_THEME)
    app = ctk.CTk(); app.title(APP_TITLE)
    app.after(0, lambda: app.state('zoomed') if os.name == 'nt' else app.geometry("1200x800"))

    main_scroll = ctk.CTkScrollableFrame(app, corner_radius=0, fg_color="transparent")
    main_scroll.pack(fill="both", expand=True)

    style = ttk.Style(); style.theme_use("clam")
    style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=30, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", background="#1f1f1f", foreground="white", relief="flat", font=("Segoe UI", 11, "bold"))
    style.map("Treeview", background=[('selected', '#1f538d')]) 

    frame_head = ctk.CTkFrame(main_scroll, corner_radius=0); frame_head.pack(fill="x")
    f_left = ctk.CTkFrame(frame_head, fg_color="transparent"); f_left.pack(side="left", padx=20, pady=15)
    
    ctk.CTkLabel(f_left, text="PROJE ADI:", font=FONT_BOLD).pack(side="left")
    entry_proje_adi = ctk.CTkEntry(f_left, width=150, placeholder_text="Proje"); entry_proje_adi.pack(side="left", padx=5)
    ctk.CTkLabel(f_left, text="MÜŞTERİ:", font=FONT_BOLD).pack(side="left", padx=(5, 0))
    entry_musteri = ctk.CTkEntry(f_left, width=150, placeholder_text="Firma"); entry_musteri.pack(side="left", padx=5)
    ctk.CTkLabel(f_left, text="TEKLİF NO:", font=FONT_BOLD).pack(side="left", padx=(5, 0))
    entry_teklif_no = ctk.CTkEntry(f_left, width=80, placeholder_text="15/26"); entry_teklif_no.pack(side="left", padx=5)
    
    f_right = ctk.CTkFrame(frame_head, fg_color="transparent"); f_right.pack(side="right", padx=20)
    lbl_durum = ctk.CTkLabel(f_right, text="...", font=("Segoe UI", 14, "bold")); lbl_durum.pack(side="right", padx=10)
    entry_kur_eur = ctk.CTkEntry(f_right, width=60, justify="center"); entry_kur_eur.insert(0, "38.20"); entry_kur_eur.pack(side="right")
    ctk.CTkLabel(f_right, text="EUR", text_color="#FBC02D", font=FONT_BOLD).pack(side="right", padx=5)
    entry_kur_usd = ctk.CTkEntry(f_right, width=60, justify="center"); entry_kur_usd.insert(0, "35.50"); entry_kur_usd.pack(side="right")
    ctk.CTkLabel(f_right, text="USD", text_color="#00E676", font=FONT_BOLD).pack(side="right", padx=5)
    
    f_center = ctk.CTkFrame(frame_head, fg_color="transparent"); f_center.pack(side="left", expand=True)
    ctk.CTkLabel(f_center, text="Oto Kayıt:", font=FONT_BOLD).pack(side="left", padx=5)
    cmb_oto_kayit = ctk.CTkComboBox(f_center, values=["Kapalı", "30 Saniye", "1 Dakika", "5 Dakika"], width=120, command=oto_kayit_ayar_degisti); cmb_oto_kayit.pack(side="left")

    frame_toolbar = ctk.CTkFrame(main_scroll, fg_color="transparent")
    frame_toolbar.pack(fill="x", padx=20, pady=(5, 0)) 
    top_btns = [("📂", projeyi_yukle, COLOR_SECONDARY), ("💾", lambda: projeyi_kaydet(False), COLOR_PRIMARY), ("📄", pdf_olustur_ve_ac, COLOR_PRIMARY), ("📊", excele_aktar, COLOR_PRIMARY)]
    for icon, cmd, col in top_btns: ctk.CTkButton(frame_toolbar, text=icon, command=cmd, fg_color=col, width=50, height=40, font=FONT_ICON).pack(side="left", padx=(0, 10))

    frame_input = ctk.CTkFrame(main_scroll, fg_color="transparent"); frame_input.pack(fill="x", padx=15, pady=10)

    # --- 1. MALZEME ALANI ---
    p_malzeme = create_card(frame_input, "1. Malzeme & Hammadde"); p_malzeme.pack(side="left", fill="both", expand=True, padx=(0,10))
    grid_f = ctk.CTkFrame(p_malzeme, fg_color="transparent"); grid_f.pack(fill="both", expand=True, padx=10, pady=5)
    ctk.CTkLabel(grid_f, text="Kategori:").grid(row=0, column=0, sticky="e", pady=5)
    cmb_kategori = ctk.CTkComboBox(grid_f, values=list(katalog.keys()), width=180, command=kategori_degisti); cmb_kategori.grid(row=0, column=1, sticky="w", padx=5)
    var_manuel = tk.IntVar(); ctk.CTkCheckBox(grid_f, text="Elle Yaz", variable=var_manuel, command=manuel_mod_kontrol, width=20, height=20).grid(row=0, column=2, sticky="w", padx=5)
    ctk.CTkButton(grid_f, text="X", width=30, fg_color=COLOR_DANGER, hover_color="#B71C1C", command=kategori_sil_buton).grid(row=0, column=3, padx=5)
    
    ctk.CTkLabel(grid_f, text="Ürün:").grid(row=1, column=0, sticky="e", pady=5)
    cmb_urun = ctk.CTkComboBox(grid_f, width=250); cmb_urun.grid(row=1, column=1, columnspan=2, sticky="w", padx=5)
    ctk.CTkButton(grid_f, text="X", width=30, fg_color=COLOR_DANGER, hover_color="#B71C1C", command=listeden_sil_buton).grid(row=1, column=3, padx=5)
    
    ctk.CTkLabel(grid_f, text="Tedarikçi:").grid(row=2, column=0, sticky="e", pady=5)
    entry_tedarikci = ctk.CTkEntry(grid_f, width=250, placeholder_text="Tedarikçi Firma / Kişi"); entry_tedarikci.grid(row=2, column=1, columnspan=2, sticky="w", padx=5)
    
    ctk.CTkLabel(grid_f, text="Miktar/Fiyat:").grid(row=3, column=0, sticky="e", pady=5)
    sub_f1 = ctk.CTkFrame(grid_f, fg_color="transparent"); sub_f1.grid(row=3, column=1, columnspan=3, sticky="w")
    entry_adet = ctk.CTkEntry(sub_f1, width=50, justify="center"); entry_adet.insert(0, "1"); entry_adet.pack(side="left", padx=5)
    cmb_birim = ctk.CTkComboBox(sub_f1, values=birim_katalog, width=70); cmb_birim.pack(side="left")
    entry_fiyat = ctk.CTkEntry(sub_f1, width=80, justify="right", placeholder_text="B.Fiyat"); entry_fiyat.pack(side="left", padx=5)
    cmb_para = ctk.CTkComboBox(sub_f1, values=["TL", "USD", "EUR"], width=70); cmb_para.pack(side="left")
    
    btn_malzeme_ekle = ctk.CTkButton(p_malzeme, text="LİSTEYE EKLE (+)", fg_color=COLOR_PRIMARY, hover_color="#1565C0", command=malzeme_ekle)
    btn_malzeme_ekle.pack(fill="x", padx=10, pady=10)
    kategori_degisti(None)

    # --- 2. FASON ALANI ---
    p_fason = create_card(frame_input, "2. Dış Hizmet / Fason"); p_fason.pack(side="left", fill="both", expand=True, padx=(0,10))
    grid_f2 = ctk.CTkFrame(p_fason, fg_color="transparent"); grid_f2.pack(fill="both", expand=True, padx=10, pady=5)
    ctk.CTkLabel(grid_f2, text="İşlem:").grid(row=0, column=0, sticky="e", pady=5)
    cmb_oto_tur = ctk.CTkComboBox(grid_f2, values=["Lazer Kesim", "Abkant", "Taşlama", "Kaplama", "Otomasyon", "Nakliye", "Balans", "Tezgah"], width=180); cmb_oto_tur.grid(row=0, column=1, sticky="w", padx=5)
    ctk.CTkLabel(grid_f2, text="Açıklama:").grid(row=1, column=0, sticky="e", pady=5); entry_oto_aciklama = ctk.CTkEntry(grid_f2, width=180); entry_oto_aciklama.grid(row=1, column=1, sticky="w", padx=5)
    ctk.CTkLabel(grid_f2, text="Fiyat:").grid(row=2, column=0, sticky="e", pady=5)
    sub_f2 = ctk.CTkFrame(grid_f2, fg_color="transparent"); sub_f2.grid(row=2, column=1, sticky="w")
    entry_oto_fiyat = ctk.CTkEntry(sub_f2, width=80, justify="right"); entry_oto_fiyat.pack(side="left", padx=5)
    cmb_oto_para = ctk.CTkComboBox(sub_f2, values=["TL", "USD", "EUR"], width=70); cmb_oto_para.pack(side="left")
    
    btn_fason_ekle = ctk.CTkButton(p_fason, text="EKLE (+)", fg_color=COLOR_PRIMARY, hover_color="#1565C0", command=otomasyon_ekle)
    btn_fason_ekle.pack(fill="x", padx=10, pady=10)

    # --- 3. İŞÇİLİK ALANI ---
    p_iscilik = create_card(frame_input, "3. Atölye İşçilik"); p_iscilik.pack(side="left", fill="both", expand=True)
    grid_f3 = ctk.CTkFrame(p_iscilik, fg_color="transparent"); grid_f3.pack(fill="both", expand=True, padx=10, pady=5)
    ctk.CTkLabel(grid_f3, text="İşçilik Tipi:").grid(row=0, column=0, sticky="e", pady=5)
    cmb_isci_tur = ctk.CTkComboBox(grid_f3, values=["Montaj İşçiliği", "Kaynak İşçiliği", "Torna İşçiliği", "Freze İşçiliği", "Genel İşçilik"], width=140); cmb_isci_tur.grid(row=0, column=1, sticky="w", padx=5)
    ctk.CTkLabel(grid_f3, text="Açıklama:").grid(row=1, column=0, sticky="e", pady=5); entry_isci_aciklama = ctk.CTkEntry(grid_f3, width=140); entry_isci_aciklama.grid(row=1, column=1, sticky="w", padx=5)
    ctk.CTkLabel(grid_f3, text="Kişi x Süre:").grid(row=2, column=0, sticky="e", pady=5)
    sub_row_kisi_saat = ctk.CTkFrame(grid_f3, fg_color="transparent"); sub_row_kisi_saat.grid(row=2, column=1, sticky="w")
    entry_isci_kisi = ctk.CTkEntry(sub_row_kisi_saat, width=50, justify="center"); entry_isci_kisi.insert(0, "1"); entry_isci_kisi.pack(side="left", padx=(5, 5))
    ctk.CTkLabel(sub_row_kisi_saat, text="Kişi   x").pack(side="left")
    entry_isci_saat = ctk.CTkEntry(sub_row_kisi_saat, width=50, justify="center"); entry_isci_saat.pack(side="left", padx=5)
    ctk.CTkLabel(sub_row_kisi_saat, text="Saat").pack(side="left")
    ctk.CTkLabel(grid_f3, text="Saat Ücreti:").grid(row=3, column=0, sticky="e", pady=5)
    sub_f3 = ctk.CTkFrame(grid_f3, fg_color="transparent"); sub_f3.grid(row=3, column=1, sticky="w")
    entry_isci_ucret = ctk.CTkEntry(sub_f3, width=80, justify="right"); entry_isci_ucret.insert(0, "1100"); entry_isci_ucret.pack(side="left", padx=5)
    cmb_isci_para = ctk.CTkComboBox(sub_f3, values=["TL", "USD", "EUR"], width=70); cmb_isci_para.pack(side="left")
    
    btn_iscilik_ekle = ctk.CTkButton(p_iscilik, text="EKLE (+)", fg_color=COLOR_PRIMARY, hover_color="#1565C0", command=iscelik_ekle)
    btn_iscilik_ekle.pack(fill="x", padx=10, pady=10)

    f_ctrl = ctk.CTkFrame(main_scroll, fg_color="transparent"); f_ctrl.pack(fill="x", padx=15, pady=5)
    ctk.CTkLabel(f_ctrl, text="Filtre:", font=("Segoe UI", 12, "bold")).pack(side="left")
    cmb_filtre = ctk.CTkComboBox(f_ctrl, values=["Tümü", "Sadece Malzeme", "Sadece İşçilik", "Sadece Dış Hizmet"], command=lambda e: tabloyu_guncelle()); cmb_filtre.pack(side="left", padx=10)
    
    # --- BUTON SIRALAMASI: MAKAS (Sil) - KALEM (Düzenle) - ÇÖP (Sıfırla) ---
    bottom_btns = [("✂️", sil, COLOR_DANGER), ("✏️", duzenle_secili, COLOR_WARNING), ("🗑️", sifirla, COLOR_DANGER)]
    for icon, cmd, col in bottom_btns: 
        ctk.CTkButton(f_ctrl, text=icon, command=cmd, fg_color=col, width=50, height=35, font=FONT_ICON).pack(side="right", padx=5)

    f_list = ctk.CTkFrame(main_scroll, fg_color="transparent"); f_list.pack(fill="both", expand=True, padx=15, pady=5)
    scroll = ctk.CTkScrollbar(f_list); scroll.pack(side="right", fill="y")
    cols = ("k", "u", "m", "f", "p", "t", "ht", "gbf") 
    headers = ["Kategori", "Ürün / Açıklama", "Miktar", "Birim Fiyat", "Para", "Toplam Tutar", "", ""]
    widths = [150, 400, 100, 120, 80, 150, 0, 0]
    tablo = ttk.Treeview(f_list, columns=cols, show="headings", selectmode="extended", yscrollcommand=scroll.set, height=10); tablo.pack(side="left", fill="both", expand=True)
    scroll.configure(command=tablo.yview)
    for c, t, w in zip(cols, headers, widths): 
        tablo.heading(c, text=t, command=lambda x=c: sirala(x, False))
        tablo.column(c, width=w, anchor="w" if c in ["k","u"] else "center")
    tablo.column("ht", width=0, stretch=False); tablo.column("gbf", width=0, stretch=False)
    
    # Çift tıklama olayını da butondaki fonksiyona bağladık
    tablo.bind("<Double-1>", lambda e: duzenle_secili())

    f_foot = ctk.CTkFrame(main_scroll, height=150); f_foot.pack(fill="x", padx=15, pady=15, side="bottom")
    f_calc = ctk.CTkFrame(f_foot, fg_color="transparent"); f_calc.pack(side="left", padx=20, pady=10)
    ctk.CTkLabel(f_calc, text="Hesaplama Parametreleri", font=("Segoe UI", 12, "bold"), text_color="gray").grid(row=0, column=0, columnspan=2, sticky="w")
    ctk.CTkLabel(f_calc, text="Malzeme %:").grid(row=1, column=0, sticky="e"); entry_kar_malzeme = ctk.CTkEntry(f_calc, width=50); entry_kar_malzeme.insert(0, "30"); entry_kar_malzeme.grid(row=1, column=1, padx=5, pady=2)
    ctk.CTkLabel(f_calc, text="İşçilik %:").grid(row=2, column=0, sticky="e"); entry_kar_iscilik = ctk.CTkEntry(f_calc, width=50); entry_kar_iscilik.insert(0, "60"); entry_kar_iscilik.grid(row=2, column=1, padx=5, pady=2)
    ctk.CTkLabel(f_calc, text="KDV %:").grid(row=3, column=0, sticky="e"); entry_kdv = ctk.CTkEntry(f_calc, width=50); entry_kdv.insert(0, "20"); entry_kdv.grid(row=3, column=1, padx=5, pady=2)
    ctk.CTkButton(f_calc, text="HESAPLA", command=hesapla, fg_color="#F57C00", width=120).grid(row=4, column=0, columnspan=2, pady=5)

    f_res = ctk.CTkFrame(f_foot, fg_color="transparent"); f_res.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    c1 = create_res_card(f_res, "1. Ham Maliyet", "#C8E6C9"); c1.pack(side="left", fill="both", expand=True, padx=5)
    lbl_ham_toplam_val = ctk.CTkLabel(c1, text="...\n...\n...", font=("Consolas", 14, "bold"), text_color="#1B5E20"); lbl_ham_toplam_val.pack(anchor="center", pady=10)
    c2 = create_res_card(f_res, "2. Teklif Fiyatı", "#BBDEFB"); c2.pack(side="left", fill="both", expand=True, padx=5)
    lbl_satis_toplam_val = ctk.CTkLabel(c2, text="...\n...\n...", font=("Consolas", 14, "bold"), text_color="#0D47A1"); lbl_satis_toplam_val.pack(anchor="center", pady=10)
    c3 = create_res_card(f_res, "3. Müşteri Özeti (KDV Dahil)", "#FFE0B2"); c3.pack(side="left", fill="both", expand=True, padx=5)
    lbl_tl_kdvli_val = ctk.CTkLabel(c3, text="...\n...\n...", font=("Consolas", 16, "bold"), text_color="#E65100"); lbl_tl_kdvli_val.pack(anchor="center", pady=10)

    baslat_kur_thread()
    app.mainloop()

if __name__ == "__main__":
    main()