import customtkinter as ctk
import math
import json
import os
import sys
from tkinter import messagebox

# --- EXE UYUMLU KAYNAK YOLU ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# --- ANA MENÜDEN GELEN YOLU YAKALA ---
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    WORKSPACE_PATH = sys.argv[1]
else:
    WORKSPACE_PATH = os.path.join(os.path.expanduser("~"), "Documents", "BEM_Kayitlari")

# --- TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# PRO PALET (Sumatra PDF Tarzı Minimalist Dark)
COLOR_BG = "#121212"           # Ana Arka Plan
COLOR_CARD = "#1E1E1E"         # Kartlar (Satır A)
COLOR_CARD_ALT = "#252525"     # Alternatif Satır (Satır B)
COLOR_HEADER = "#000000"       # Tablo Başlığı (Simsiyah)
COLOR_TEXT_MAIN = "#E0E0E0"    # Ana Metin (Kırık Beyaz)
COLOR_TEXT_SUB = "#9E9E9E"     # Alt Metin (Gri)
COLOR_ACCENT = "#3B8ED0"       # Vurgu Rengi

class StandardLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM - Teknik Hesaplama Merkezi")
        self.geometry("1200x800") 
        self.configure(fg_color=COLOR_BG)

        self.load_database()

        # Tab Menüsü
        self.tabview = ctk.CTkTabview(self, fg_color=COLOR_BG, 
                                      segmented_button_fg_color="#181818",
                                      segmented_button_selected_color="#333333",
                                      segmented_button_selected_hover_color="#444444",
                                      segmented_button_unselected_color="#181818",
                                      text_color="#E0E0E0", corner_radius=8) 
        self.tabview._segmented_button.configure(font=("Segoe UI", 12, "bold"))
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.tab_catalog = self.tabview.add(" GENEL KATALOG ")
        self.tab_shaft = self.tabview.add(" MİL & GÖBEK ")
        self.tab_bend = self.tabview.add(" K-FAKTÖRÜ ÇİZELGESİ ")
        self.tab_unit = self.tabview.add(" BİRİM ÇEVİRİCİ ")

        self.setup_catalog_tab()
        self.setup_shaft_tab()
        self.setup_k_factor_tab()
        self.setup_unit_tab()

    def load_database(self):
        json_path = resource_path("data.json")
        self.catalog_data = {}
        self.calc_data = {}

        if not os.path.exists(json_path):
            return

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                full_data = json.load(f)
                self.catalog_data = full_data.get("CATALOG", {})
                self.calc_data = full_data.get("CALCULATION_DATA", {})
        except Exception as e:
            messagebox.showerror("Hata", f"Veri Okuma Hatası:\n{e}")

    def create_stat_row(self, parent, label, value_var):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=5)
        ctk.CTkLabel(f, text=label, font=("Segoe UI", 14), text_color=COLOR_TEXT_SUB).pack(side="left")
        ctk.CTkLabel(f, textvariable=value_var, font=("Consolas", 15, "bold"), text_color=COLOR_TEXT_MAIN).pack(side="right")
        return f

    def create_header(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Segoe UI", 24, "bold"), text_color=COLOR_TEXT_MAIN).pack(pady=(25, 15))

    # --- 1. KATALOG ---
    def setup_catalog_tab(self):
        f = self.tab_catalog
        f.grid_columnconfigure(0, weight=1); f.grid_columnconfigure(1, weight=3); f.grid_rowconfigure(0, weight=1)
        
        f_left = ctk.CTkFrame(f, fg_color=COLOR_CARD, corner_radius=0)
        f_left.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        self.create_header(f_left, "KATALOG")
        
        scroll_cats = ctk.CTkScrollableFrame(f_left, fg_color="transparent")
        scroll_cats.pack(fill="both", expand=True, padx=5, pady=5)

        if not self.catalog_data: ctk.CTkLabel(scroll_cats, text="Veri Yok").pack()
        
        for cat in self.catalog_data.keys():
            ctk.CTkButton(scroll_cats, text=cat, font=("Segoe UI", 12), fg_color="transparent", anchor="w",
                          text_color=COLOR_TEXT_SUB, hover_color="#333", 
                          command=lambda c=cat: self.load_cat(c)).pack(fill="x", padx=5, pady=2)

        f_right = ctk.CTkFrame(f, fg_color="transparent")
        f_right.grid(row=0, column=1, sticky="nsew", pady=10, padx=20)
        
        self.lbl_cat_title = ctk.CTkLabel(f_right, text="KATEGORİ SEÇİNİZ", font=("Segoe UI", 32, "bold"), text_color=COLOR_TEXT_MAIN, anchor="w")
        self.lbl_cat_title.pack(fill="x", pady=(20, 10))

        self.cmb_cat_item = ctk.CTkComboBox(f_right, values=[], height=40, font=("Segoe UI", 14), command=self.show_cat_data,
                                            fg_color=COLOR_CARD, border_color="#444", text_color="white", dropdown_fg_color="#222")
        self.cmb_cat_item.pack(fill="x", pady=(0, 20))
        
        self.frame_cat_data = ctk.CTkFrame(f_right, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color="#333")
        self.frame_cat_data.pack(fill="both", expand=True)

    def load_cat(self, cat):
        self.lbl_cat_title.configure(text=cat)
        items = list(self.catalog_data[cat].keys())
        self.cmb_cat_item.configure(values=items)
        if items:
            self.cmb_cat_item.set(items[0])
            self.show_cat_data(items[0])

    def show_cat_data(self, selected):
        for w in self.frame_cat_data.winfo_children(): w.destroy()
        cat = self.lbl_cat_title.cget("text")
        if cat in self.catalog_data and selected in self.catalog_data[cat]:
            data = self.catalog_data[cat][selected]
            ctk.CTkLabel(self.frame_cat_data, text=selected, font=("Segoe UI", 36, "bold"), text_color=COLOR_ACCENT).pack(pady=(40, 30))
            for k, v in data.items():
                row = ctk.CTkFrame(self.frame_cat_data, fg_color="transparent")
                row.pack(fill="x", padx=80, pady=8)
                ctk.CTkLabel(row, text=k, font=("Segoe UI", 16), text_color="gray").pack(side="left")
                ctk.CTkLabel(row, text=v, font=("Consolas", 18, "bold"), text_color="white").pack(side="right")

    # --- 2. MİL & GÖBEK ---
    def setup_shaft_tab(self):
        f = self.tab_shaft
        in_panel = ctk.CTkFrame(f, fg_color=COLOR_CARD, corner_radius=10)
        in_panel.pack(fill="x", padx=50, pady=30)
        ctk.CTkLabel(in_panel, text="MİL ÇAPI (mm):", font=("Segoe UI", 24, "bold")).pack(side="left", padx=30, pady=25)
        self.entry_shaft = ctk.CTkEntry(in_panel, width=120, font=("Consolas", 24, "bold"), justify="center", fg_color="#111", border_color="#555")
        self.entry_shaft.pack(side="left", padx=10)
        self.entry_shaft.bind("<KeyRelease>", self.calc_shaft)

        res_panel = ctk.CTkFrame(f, fg_color="transparent"); res_panel.pack(fill="both", expand=True, padx=20)
        res_panel.columnconfigure(0, weight=1); res_panel.columnconfigure(1, weight=1)

        card_key = ctk.CTkFrame(res_panel, fg_color=COLOR_CARD, border_width=1, border_color="#333")
        card_key.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(card_key, text="KAMA KANALI (DIN 6885)", font=("Segoe UI", 16, "bold"), text_color="white").pack(pady=20)
        self.key_vars = {k: ctk.StringVar(value="-") for k in ["b", "h", "t1", "t2"]}
        for k, v in self.key_vars.items(): self.create_stat_row(card_key, k, v).pack(padx=30, pady=5)

        card_cir = ctk.CTkFrame(res_panel, fg_color=COLOR_CARD, border_width=1, border_color="#333")
        card_cir.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(card_cir, text="SEGMAN KANALI (DIN 471)", font=("Segoe UI", 16, "bold"), text_color="white").pack(pady=20)
        self.cir_vars = {k: ctk.StringVar(value="-") for k in ["d2", "m", "s"]}
        for k, v in self.cir_vars.items(): self.create_stat_row(card_cir, k, v).pack(padx=30, pady=5)

    def calc_shaft(self, event=None):
        try:
            d_val = float(self.entry_shaft.get())
            keyway_list = self.calc_data.get("KEYWAY_DIN6885", [])
            k_res = None
            for item in keyway_list:
                if item["min"] < d_val <= item["max"]:
                    k_res = item; break
            if k_res:
                self.key_vars["b"].set(f"{k_res['b']} mm"); self.key_vars["h"].set(f"{k_res['h']} mm")
                self.key_vars["t1"].set(f"{k_res['t1']} mm"); self.key_vars["t2"].set(f"{k_res['t2']} mm")
            else:
                for v in self.key_vars.values(): v.set("-")

            circlip_dict = self.calc_data.get("CIRCLIP_DIN471", {})
            search_key = str(int(d_val)) 
            if search_key in circlip_dict:
                s_res = circlip_dict[search_key]
                self.cir_vars["d2"].set(f"{s_res['d2']} mm"); self.cir_vars["m"].set(f"{s_res['m']} mm"); self.cir_vars["s"].set(f"{s_res['s']} mm")
            else:
                for v in self.cir_vars.values(): v.set("-")
        except ValueError: pass

    # --- 3. K-FAKTÖRÜ (YENİ TASARIM: Minimalist Grid) ---
    def setup_k_factor_tab(self):
        f = self.tab_bend
        
        # Başlık Alanı
        title_box = ctk.CTkFrame(f, fg_color="transparent")
        title_box.pack(pady=(10, 20))
        ctk.CTkLabel(title_box, text="90° BÜKÜM TABLOSU", font=("Segoe UI", 26, "bold"), text_color="white").pack()
        ctk.CTkLabel(title_box, text="DKP ve Paslanmaz Saclar İçin Referans Değerler", font=("Segoe UI", 12), text_color="gray").pack()

        # Tablo Konteyneri (Kenarlıklı)
        table_container = ctk.CTkFrame(f, fg_color="transparent", border_width=0)
        table_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

        # Sütun Ayarları (Sabit Genişlikler - Piksel)
        col_widths = [110, 110, 110, 110, 140, 140]
        cols = ["KALINLIK", "K FAKTÖRÜ", "UZAMA", "RADÜS", "KALIP GENİŞLİĞİ", "BÜKÜM BOYU"]

        # 1. Başlık Satırı (Siyah Arka Plan)
        header_frame = ctk.CTkFrame(table_container, fg_color=COLOR_HEADER, height=45, corner_radius=6)
        header_frame.pack(fill="x", pady=(0, 5))
        
        for i, col in enumerate(cols):
            ctk.CTkLabel(header_frame, text=col, width=col_widths[i], 
                         font=("Segoe UI", 11, "bold"), text_color="#FFFFFF", 
                         anchor="center").pack(side="left", padx=2, fill="y")

        # 2. Veri Alanı (Kaydırılabilir)
        scroll_body = ctk.CTkScrollableFrame(table_container, fg_color="transparent", corner_radius=0)
        scroll_body.pack(fill="both", expand=True)

        k_table = self.calc_data.get("K_FACTOR_TABLE", [])

        for i, row_data in enumerate(k_table):
            # Sumatra PDF Tarzı: Satırlar arasında belirgin kontrast
            bg_color = COLOR_CARD if i % 2 == 0 else COLOR_CARD_ALT
            
            row_frame = ctk.CTkFrame(scroll_body, fg_color=bg_color, corner_radius=4, height=40)
            row_frame.pack(fill="x", pady=2)
            
            # Veriler
            vals = [
                row_data.get("thick", "-"),        
                row_data.get("k", "-"),            
                row_data.get("elong", "-"),        
                row_data.get("radius", "-"),       
                row_data.get("die_width", "-"),    
                row_data.get("min_bend", "-")      
            ]
            
            for j, item in enumerate(vals): 
                # Veri Yazı Tipi: Consolas (Hizalamayı mükemmel yapar)
                # Renk: Parlak beyaz (#FFF)
                ctk.CTkLabel(row_frame, text=str(item), width=col_widths[j], 
                             font=("Consolas", 13), text_color="#E0E0E0", 
                             anchor="center").pack(side="left", padx=2)

    # --- 4. BİRİM ÇEVİRİCİ ---
    def setup_unit_tab(self):
        f = self.tab_unit
        self.create_header(f, "HIZLI BİRİM ÇEVİRİCİ")
        self.sv_val = ctk.StringVar(); self.sv_val.trace_add("write", self.convert_unit)
        
        frame_conv = ctk.CTkFrame(f, fg_color=COLOR_CARD, corner_radius=15)
        frame_conv.pack(pady=30, padx=150, fill="x")
        frame_conv.columnconfigure((0,1,3), weight=2); frame_conv.columnconfigure(2, weight=1)
        
        self.entry_u = ctk.CTkEntry(frame_conv, textvariable=self.sv_val, placeholder_text="0", height=60, font=("Consolas", 28), justify="center", fg_color="#111", border_color="#444", text_color="white")
        self.entry_u.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.units = ["mm", "inch", "m", "kg", "lb", "bar", "psi", "kW", "HP"]
        self.cmb_f = ctk.CTkComboBox(frame_conv, values=self.units, height=50, font=("Segoe UI", 16, "bold"), justify="center", command=self.convert_unit); self.cmb_f.set("inch"); self.cmb_f.grid(row=0, column=1, padx=10, sticky="ew")
        
        ctk.CTkLabel(frame_conv, text="➜", font=("Arial", 30), text_color="gray").grid(row=0, column=2)
        
        self.cmb_t = ctk.CTkComboBox(frame_conv, values=self.units, height=50, font=("Segoe UI", 16, "bold"), justify="center", command=self.convert_unit); self.cmb_t.set("mm"); self.cmb_t.grid(row=0, column=3, padx=20, sticky="ew")
        
        self.lbl_u_res = ctk.CTkLabel(f, text="0.0000", font=("Consolas", 72, "bold"), text_color=COLOR_ACCENT); self.lbl_u_res.pack(pady=(40, 10))

    def convert_unit(self, *args):
        try:
            val = float(self.sv_val.get().replace(',', '.') or 0)
            u_f, u_t = self.cmb_f.get(), self.cmb_t.get()
            if u_f == u_t: self.lbl_u_res.configure(text=f"{val:.4f}"); return
            factors = {"mm":("L",1), "m":("L",1000), "inch":("L",25.4), "kg":("M",1), "lb":("M",0.453592), "bar":("P",1), "psi":("P",0.0689), "kW":("W",1), "HP":("W",0.7457)}
            tf, ff = factors.get(u_f, (None,0)); tt, ft = factors.get(u_t, (None,0))
            if tf != tt: self.lbl_u_res.configure(text="---", text_color="red"); return
            res = (val * ff) / ft
            self.lbl_u_res.configure(text=f"{res:.4f}", text_color=COLOR_ACCENT)
        except: self.lbl_u_res.configure(text="0.0000", text_color="gray")

if __name__ == "__main__":
    app = StandardLibraryApp()
    app.mainloop()