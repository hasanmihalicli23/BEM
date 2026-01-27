import customtkinter as ctk
import math
from tkinter import messagebox
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Örnek kullanım: 
# logo = Image.open(resource_path("assets/logo.png"))

# Örnek kullanım: 
# logo = Image.open(resource_path("assets/logo.png"))
# --- TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# MONOCHROME PALET
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SUB = "#9E9E9E"
COLOR_BTN_BG = "#E0E0E0"
COLOR_BTN_TEXT = "#000000"
COLOR_BTN_HOVER = "#FFFFFF"
COLOR_ACCENT_GREEN = "#00E676" # Sonuç Rengi
COLOR_ACCENT_RED = "#FF5252"   # Silme Rengi

class MassCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM - Kütle Toplayıcı")
        self.geometry("1000x700") # Geniş ekran
        self.configure(fg_color=COLOR_BG)

        self.cart_items = [] # Sepet Listesi

        # --- DÜZEN (SOL / SAĞ) ---
        self.grid_columnconfigure(0, weight=1) # Sol (Hesap)
        self.grid_columnconfigure(1, weight=1) # Sağ (Liste)
        self.grid_rowconfigure(0, weight=1)

        # ========================================================
        # SOL PANEL: HESAPLAMA MOTORU
        # ========================================================
        self.frame_left = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Başlık
        ctk.CTkLabel(self.frame_left, text="HESAPLAMA", font=("Impact", 28), text_color=COLOR_TEXT_MAIN).pack(anchor="w", pady=(10, 20))

        # 1. ANLIK SONUÇ KARTI
        self.frame_result = ctk.CTkFrame(self.frame_left, fg_color=COLOR_CARD, corner_radius=15)
        self.frame_result.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(self.frame_result, text="TEK PARÇA AĞIRLIĞI", font=("Arial", 11, "bold"), text_color="gray").pack(pady=(15, 0))
        self.lbl_current_weight = ctk.CTkLabel(self.frame_result, text="0.00 kg", font=("Arial", 40, "bold"), text_color=COLOR_ACCENT_GREEN)
        self.lbl_current_weight.pack(pady=(0, 15))

        # 2. GİRİŞLER
        self.frame_inputs = ctk.CTkFrame(self.frame_left, fg_color=COLOR_CARD, corner_radius=15)
        self.frame_inputs.pack(fill="x", pady=0)

        # Değişkenler (Dinamik Takip)
        self.sv_boy = ctk.StringVar()
        self.sv_olcu1 = ctk.StringVar()
        self.sv_olcu2 = ctk.StringVar()
        self.sv_adet = ctk.StringVar(value="1") # Varsayılan 1 adet

        for sv in [self.sv_boy, self.sv_olcu1, self.sv_olcu2, self.sv_adet]:
            sv.trace_add("write", self.calculate)

        # Malzeme Seçimi
        ctk.CTkLabel(self.frame_inputs, text="MALZEME", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(15, 5))
        self.malzemeler = [
            "DKP Sac", "HRP (Siyah) Sac", "Galvaniz Sac", "Çelik (İmalat)", 
            "Paslanmaz 304", "Paslanmaz 316", "Alüminyum", "Pirinç (Sarı)", 
            "Bronz", "Bakır", "Döküm (Pik)", "Titanyum", 
            "Kestamid", "PEEK", "Delrin (POM)", "Polyamid 6", "Teflon (PTFE)"
        ]
        self.cmb_malzeme = ctk.CTkComboBox(self.frame_inputs, values=self.malzemeler, height=35, 
                                           fg_color=COLOR_BG, border_color="#444", text_color="white", dropdown_fg_color="#222",
                                           command=self.calculate)
        self.cmb_malzeme.set("DKP Sac")
        self.cmb_malzeme.pack(fill="x", padx=20, pady=5)

        # Geometri Seçimi
        ctk.CTkLabel(self.frame_inputs, text="GEOMETRİ", font=("Arial", 11, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(15, 5))
        self.geometriler = [
            "Sac / Levha", "Kare (Dolu)", "Daire (Mil)", "Altıköşe", 
            "Dikdörtgen (Lama)", "Boru", "Kare Profil (Kutu)"
        ]
        self.cmb_geometri = ctk.CTkComboBox(self.frame_inputs, values=self.geometriler, height=35,
                                            fg_color=COLOR_BG, border_color="#444", text_color="white", dropdown_fg_color="#222",
                                            command=self.update_ui_and_calculate)
        self.cmb_geometri.set("Sac / Levha")
        self.cmb_geometri.pack(fill="x", padx=20, pady=5)

        # Ölçü Girişleri (Grid)
        self.frame_dims = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_dims.pack(fill="x", padx=10, pady=10)
        self.frame_dims.columnconfigure(1, weight=1)

        self.lbl_boy, self.entry_boy = self.create_entry(self.frame_dims, 0, "Uzunluk (mm):", self.sv_boy)
        self.lbl_olcu1, self.entry_olcu1 = self.create_entry(self.frame_dims, 1, "Genişlik (mm):", self.sv_olcu1)
        self.lbl_olcu2, self.entry_olcu2 = self.create_entry(self.frame_dims, 2, "Kalınlık (mm):", self.sv_olcu2)
        
        # Adet Girişi
        self.lbl_adet, self.entry_adet = self.create_entry(self.frame_dims, 3, "Adet:", self.sv_adet)

        # EKLE BUTONU
        self.btn_add = ctk.CTkButton(self.frame_left, text="LİSTEYE EKLE  ➡️", font=("Arial", 14, "bold"), height=50,
                                     fg_color=COLOR_BTN_BG, text_color=COLOR_BTN_TEXT, hover_color=COLOR_BTN_HOVER,
                                     command=self.add_to_list)
        self.btn_add.pack(fill="x", pady=20)


        # ========================================================
        # SAĞ PANEL: LİSTE VE TOPLAM
        # ========================================================
        self.frame_right = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=0)
        self.frame_right.grid(row=0, column=1, sticky="nsew") # Köşeli olsun sağ taraf tam yaslansın

        ctk.CTkLabel(self.frame_right, text="PARÇA LİSTESİ", font=("Impact", 24), text_color=COLOR_TEXT_MAIN).pack(anchor="w", padx=20, pady=(30, 10))

        # Scroll Listesi
        self.scroll_list = ctk.CTkScrollableFrame(self.frame_right, fg_color="#181818")
        self.scroll_list.pack(fill="both", expand=True, padx=20, pady=10)

        # Alt Toplam Kartı
        self.frame_total = ctk.CTkFrame(self.frame_right, fg_color="transparent")
        self.frame_total.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(self.frame_total, text="GENEL TOPLAM AĞIRLIK", font=("Arial", 12, "bold"), text_color="gray").pack(anchor="e")
        self.lbl_grand_total = ctk.CTkLabel(self.frame_total, text="0.00 kg", font=("Arial", 36, "bold"), text_color=COLOR_TEXT_MAIN)
        self.lbl_grand_total.pack(anchor="e")

        # Temizle Butonu
        ctk.CTkButton(self.frame_right, text="LİSTEYİ TEMİZLE", font=("Arial", 11), height=30,
                      fg_color="transparent", text_color=COLOR_ACCENT_RED, hover_color="#333", border_width=1, border_color=COLOR_ACCENT_RED,
                      command=self.clear_list).pack(fill="x", padx=50, pady=(0, 30))

        # Başlangıç Ayarı
        self.update_ui_and_calculate("Sac / Levha")


    # --- YARDIMCILAR ---
    def create_entry(self, parent, row, text, var):
        lbl = ctk.CTkLabel(parent, text=text, font=("Arial", 12), text_color="#DDD", anchor="w")
        lbl.grid(row=row, column=0, pady=5, padx=10, sticky="w")
        ent = ctk.CTkEntry(parent, textvariable=var, height=35, fg_color=COLOR_BG, border_color="#444", text_color="white")
        ent.grid(row=row, column=1, pady=5, padx=10, sticky="ew")
        return lbl, ent

    def update_ui_and_calculate(self, choice):
        # Varsayılanlar
        self.lbl_boy.configure(text="Uzunluk (mm):")
        self.lbl_olcu1.configure(text="Çap / Kenar (mm):")
        
        # 2. Ölçüyü Göster
        self.lbl_olcu2.grid()
        self.entry_olcu2.grid()

        if choice == "Sac / Levha":
            self.lbl_olcu1.configure(text="Genişlik (mm):")
            self.lbl_olcu2.configure(text="Kalınlık (mm):")
        elif choice in ["Boru", "Kare Profil (Kutu)"]:
            self.lbl_olcu1.configure(text="Dış Çap / Kenar:")
            self.lbl_olcu2.configure(text="Et Kalınlığı:")
        elif choice == "Dikdörtgen (Lama)":
            self.lbl_olcu1.configure(text="Genişlik (mm):")
            self.lbl_olcu2.configure(text="Kalınlık (mm):")
        else: # Tek Ölçülüler
            self.lbl_olcu2.grid_remove() 
            self.entry_olcu2.grid_remove()

        self.calculate()

    def get_float(self, var):
        try: return float(var.get().replace(',', '.') or 0)
        except: return 0.0

    def calculate(self, *args):
        malzeme = self.cmb_malzeme.get()
        sekil = self.cmb_geometri.get()
        boy = self.get_float(self.sv_boy)
        olcu1 = self.get_float(self.sv_olcu1)
        olcu2 = self.get_float(self.sv_olcu2)
        adet = self.get_float(self.sv_adet)
        
        if adet < 1: adet = 1

        ozkutleler = {
            "DKP Sac": 7.85, "HRP (Siyah) Sac": 7.85, "Galvaniz Sac": 7.85, "Çelik (İmalat)": 7.85,
            "Paslanmaz 304": 7.90, "Paslanmaz 316": 7.98, "Alüminyum": 2.70, "Pirinç (Sarı)": 8.50,
            "Bronz": 8.80, "Bakır": 8.96, "Döküm (Pik)": 7.20, "Titanyum": 4.43, "Kestamid": 1.15,
            "PEEK": 1.32, "Delrin (POM)": 1.42, "Polyamid 6": 1.13, "Teflon (PTFE)": 2.20
        }
        rho = ozkutleler.get(malzeme, 7.85)
        
        alan_mm2 = 0
        if sekil == "Sac / Levha": alan_mm2 = olcu1 * olcu2
        elif sekil == "Kare (Dolu)": alan_mm2 = olcu1 * olcu1
        elif sekil == "Daire (Mil)": alan_mm2 = math.pi * ((olcu1/2) ** 2)
        elif sekil == "Altıköşe": alan_mm2 = 0.866 * (olcu1 ** 2)
        elif sekil == "Dikdörtgen (Lama)": alan_mm2 = olcu1 * olcu2
        elif sekil == "Boru":
            r_dis = olcu1 / 2; r_ic = r_dis - olcu2
            if r_ic > 0: alan_mm2 = (math.pi * (r_dis**2)) - (math.pi * (r_ic**2))
        elif sekil == "Kare Profil (Kutu)":
            ic = olcu1 - (2 * olcu2)
            if ic > 0: alan_mm2 = (olcu1**2) - (ic**2)

        # Tek parça ağırlığı
        birim_agirlik = (alan_mm2 * boy / 1_000_000) * rho
        
        self.lbl_current_weight.configure(text=f"{birim_agirlik:.3f} kg")
        return birim_agirlik, adet

    def add_to_list(self):
        agirlik, adet = self.calculate()
        if agirlik <= 0: return

        toplam_agirlik = agirlik * adet
        
        # Bilgileri Kaydet
        item = {
            "malzeme": self.cmb_malzeme.get(),
            "sekil": self.cmb_geometri.get(),
            "detay": f"{self.sv_olcu1.get()}x{self.sv_boy.get()} mm",
            "adet": int(adet),
            "toplam": toplam_agirlik
        }
        self.cart_items.append(item)
        
        # Listeyi Güncelle
        self.update_list_ui()

    def update_list_ui(self):
        # Temizle
        for w in self.scroll_list.winfo_children(): w.destroy()
        
        grand_total = 0
        
        for i, item in enumerate(self.cart_items):
            grand_total += item["toplam"]
            
            # Kart
            card = ctk.CTkFrame(self.scroll_list, fg_color="#222", corner_radius=5)
            card.pack(fill="x", pady=2)
            
            # Sol: Bilgi
            info = f"{item['malzeme']} | {item['sekil']}\n{item['detay']}"
            ctk.CTkLabel(card, text=info, font=("Arial", 11), text_color="#DDD", justify="left").pack(side="left", padx=10, pady=5)
            
            # Orta: Adet
            ctk.CTkLabel(card, text=f"x{item['adet']}", font=("Arial", 12, "bold"), text_color="white").pack(side="left", padx=20)
            
            # Sağ: Ağırlık ve Sil
            ctk.CTkButton(card, text="X", width=25, height=20, fg_color=COLOR_ACCENT_RED, hover_color="#D32F2F",
                          command=lambda idx=i: self.delete_item(idx)).pack(side="right", padx=10)
            
            ctk.CTkLabel(card, text=f"{item['toplam']:.2f} kg", font=("Arial", 12, "bold"), text_color=COLOR_ACCENT_GREEN).pack(side="right", padx=10)

        self.lbl_grand_total.configure(text=f"{grand_total:.2f} kg")

    def delete_item(self, index):
        del self.cart_items[index]
        self.update_list_ui()

    def clear_list(self):
        self.cart_items = []
        self.update_list_ui()

if __name__ == "__main__":
    app = MassCalculatorApp()
    app.mainloop()