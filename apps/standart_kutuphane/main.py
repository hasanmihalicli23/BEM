import customtkinter as ctk
import math
import json
import os

# --- TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# MONOCHROME PALET
COLOR_BG = "#0F0F0F"
COLOR_CARD = "#1A1A1A"
COLOR_HEADER = "#2B2B2B"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SUB = "#AAAAAA"
COLOR_ACCENT = "#FFFFFF"

class StandardLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM - Teknik Hesaplama Merkezi")
        self.geometry("1000x750")
        self.configure(fg_color=COLOR_BG)

        # 1. Veritabanını Yükle
        self.load_database()

        # 2. Tab Menüsünü Kur
        self.tabview = ctk.CTkTabview(self, fg_color=COLOR_BG, 
                                      segmented_button_fg_color="#141414",
                                      segmented_button_selected_color="#444444",
                                      segmented_button_selected_hover_color="#555555",
                                      segmented_button_unselected_color="#222222",
                                      text_color="white", corner_radius=8) 
        self.tabview._segmented_button.configure(font=("Arial", 12, "bold"))
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Sekmeler (Dişli Kaldırıldı)
        self.tab_catalog = self.tabview.add(" GENEL KATALOG ")
        self.tab_shaft = self.tabview.add(" MİL & GÖBEK ")
        self.tab_bend = self.tabview.add(" K-FAKTÖRÜ ÇİZELGESİ ")
        self.tab_unit = self.tabview.add(" BİRİM ÇEVİRİCİ ")

        # 3. İçerikleri Doldur
        self.setup_catalog_tab()
        self.setup_shaft_tab()
        self.setup_k_factor_tab()
        self.setup_unit_tab()

    def load_database(self):
        """JSON dosyasını güvenli bir şekilde okur."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "data.json")
        
        self.catalog_data = {}
        self.calc_data = {}

        if not os.path.exists(json_path):
            return # Dosya yoksa sessizce geç, arayüz boş açılır.

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                full_data = json.load(f)
                self.catalog_data = full_data.get("CATALOG", {})
                self.calc_data = full_data.get("CALCULATION_DATA", {})
        except Exception as e:
            print(f"Veri Okuma Hatası: {e}")

    # --- YARDIMCI UI FONKSİYONLARI ---
    def create_stat_row(self, parent, label, value_var):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill="x", pady=5)
        ctk.CTkLabel(f, text=label, font=("Arial", 14), text_color=COLOR_TEXT_SUB).pack(side="left")
        ctk.CTkLabel(f, textvariable=value_var, font=("Arial", 15, "bold"), text_color=COLOR_TEXT_MAIN).pack(side="right")
        return f

    def create_header(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Impact", 24), text_color=COLOR_TEXT_MAIN).pack(pady=(25, 15))

    # =================================================================
    # 1. KATALOG (JSON'dan Dinamik Okur)
    # =================================================================
    def setup_catalog_tab(self):
        f = self.tab_catalog
        f.grid_columnconfigure(0, weight=1); f.grid_columnconfigure(1, weight=3); f.grid_rowconfigure(0, weight=1)

        # SOL: Menü
        f_left = ctk.CTkFrame(f, fg_color=COLOR_CARD, corner_radius=0)
        f_left.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        self.create_header(f_left, "KATALOG")
        
        scroll_cats = ctk.CTkScrollableFrame(f_left, fg_color="transparent")
        scroll_cats.pack(fill="both", expand=True, padx=5, pady=5)

        if not self.catalog_data:
            ctk.CTkLabel(scroll_cats, text="Veri Yok").pack()
        
        # JSON'daki her ana başlık için buton oluştur
        for cat in self.catalog_data.keys():
            ctk.CTkButton(scroll_cats, text=cat, font=("Arial", 11, "bold"), fg_color="transparent", anchor="w",
                          text_color=COLOR_TEXT_SUB, hover_color="#333", 
                          command=lambda c=cat: self.load_cat(c)).pack(fill="x", padx=5, pady=2)

        # SAĞ: İçerik
        f_right = ctk.CTkFrame(f, fg_color="transparent")
        f_right.grid(row=0, column=1, sticky="nsew", pady=10, padx=20)
        
        self.lbl_cat_title = ctk.CTkLabel(f_right, text="KATEGORİ SEÇİNİZ", font=("Impact", 32), text_color=COLOR_TEXT_MAIN, anchor="w")
        self.lbl_cat_title.pack(fill="x", pady=(20, 10))

        self.cmb_cat_item = ctk.CTkComboBox(f_right, values=[], height=40, font=("Arial", 14), command=self.show_cat_data,
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
            ctk.CTkLabel(self.frame_cat_data, text=selected, font=("Arial", 48, "bold"), text_color=COLOR_ACCENT).pack(pady=(50, 30))
            for k, v in data.items():
                row = ctk.CTkFrame(self.frame_cat_data, fg_color="transparent")
                row.pack(fill="x", padx=100, pady=8)
                ctk.CTkLabel(row, text=k, font=("Arial", 16), text_color="gray").pack(side="left")
                ctk.CTkLabel(row, text=v, font=("Arial", 20, "bold"), text_color="white").pack(side="right")

    # =================================================================
    # 2. MİL & GÖBEK (JSON Verisi ile Hesapla)
    # =================================================================
    def setup_shaft_tab(self):
        f = self.tab_shaft
        in_panel = ctk.CTkFrame(f, fg_color=COLOR_CARD, corner_radius=10)
        in_panel.pack(fill="x", padx=50, pady=30)
        ctk.CTkLabel(in_panel, text="MİL ÇAPI (mm):", font=("Impact", 24)).pack(side="left", padx=30, pady=25)
        self.entry_shaft = ctk.CTkEntry(in_panel, width=120, font=("Arial", 24), justify="center", fg_color="#111", border_color="#555")
        self.entry_shaft.pack(side="left", padx=10)
        self.entry_shaft.bind("<KeyRelease>", self.calc_shaft)

        res_panel = ctk.CTkFrame(f, fg_color="transparent"); res_panel.pack(fill="both", expand=True, padx=20)
        res_panel.columnconfigure(0, weight=1); res_panel.columnconfigure(1, weight=1)

        # Kama Kartı
        card_key = ctk.CTkFrame(res_panel, fg_color=COLOR_CARD, border_width=1, border_color="#333")
        card_key.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(card_key, text="KAMA KANALI (DIN 6885)", font=("Arial", 16, "bold"), text_color="white").pack(pady=20)
        self.key_vars = {k: ctk.StringVar(value="-") for k in ["b", "h", "t1", "t2"]}
        for k, v in self.key_vars.items(): self.create_stat_row(card_key, k, v).pack(padx=30, pady=5)

        # Segman Kartı
        card_cir = ctk.CTkFrame(res_panel, fg_color=COLOR_CARD, border_width=1, border_color="#333")
        card_cir.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(card_cir, text="SEGMAN KANALI (DIN 471)", font=("Arial", 16, "bold"), text_color="white").pack(pady=20)
        self.cir_vars = {k: ctk.StringVar(value="-") for k in ["d2", "m", "s"]}
        for k, v in self.cir_vars.items(): self.create_stat_row(card_cir, k, v).pack(padx=30, pady=5)

    def calc_shaft(self, event=None):
        try:
            d_val = float(self.entry_shaft.get())
            
            # --- 1. KAMA ---
            keyway_list = self.calc_data.get("KEYWAY_DIN6885", [])
            k_res = None
            for item in keyway_list:
                if item["min"] < d_val <= item["max"]:
                    k_res = item
                    break
            
            if k_res:
                self.key_vars["b"].set(f"{k_res['b']} mm")
                self.key_vars["h"].set(f"{k_res['h']} mm")
                self.key_vars["t1"].set(f"{k_res['t1']} mm")
                self.key_vars["t2"].set(f"{k_res['t2']} mm")
            else:
                for v in self.key_vars.values(): v.set("-")

            # --- 2. SEGMAN ---
            circlip_dict = self.calc_data.get("CIRCLIP_DIN471", {})
            search_key = str(int(d_val)) 
            
            if search_key in circlip_dict:
                s_res = circlip_dict[search_key]
                self.cir_vars["d2"].set(f"{s_res['d2']} mm")
                self.cir_vars["m"].set(f"{s_res['m']} mm")
                self.cir_vars["s"].set(f"{s_res['s']} mm")
            else:
                for v in self.cir_vars.values(): v.set("-")

        except ValueError:
            pass

    # =================================================================
    # 3. K-FAKTÖRÜ (JSON Table)
    # =================================================================
    def setup_k_factor_tab(self):
        f = self.tab_bend
        self.create_header(f, "90° BÜKÜM İÇİN K-FAKTÖRÜ & MİN. BÜKÜM BOYU")
        ctk.CTkLabel(f, text="(DKP ve Paslanmaz Saclar İçin)", text_color="gray").pack(pady=(0, 20))

        header_frame = ctk.CTkFrame(f, fg_color=COLOR_HEADER, height=45, corner_radius=5)
        header_frame.pack(fill="x", padx=100)
        cols = ["KALINLIK (mm)", "K FAKTÖRÜ", "UZAMA (mm)", "MİN. BÜKÜM BOYU"]
        for col in cols: ctk.CTkLabel(header_frame, text=col, font=("Arial", 13, "bold"), text_color="white").pack(side="left", expand=True)

        table_body = ctk.CTkFrame(f, fg_color="transparent")
        table_body.pack(fill="both", expand=True, padx=100, pady=5)

        k_table = self.calc_data.get("K_FACTOR_TABLE", [])

        for i, row_data in enumerate(k_table):
            bg = COLOR_CARD if i % 2 == 0 else "#252525"
            rf = ctk.CTkFrame(table_body, fg_color=bg, corner_radius=0, height=35)
            rf.pack(fill="x", pady=1)
            rf.pack_propagate(False)
            
            vals = [row_data.get("thick"), row_data.get("k"), row_data.get("elong"), row_data.get("min_bend")]
            for item in vals: ctk.CTkLabel(rf, text=item, font=("Arial", 13), text_color="#DDD").pack(side="left", expand=True)

    # =================================================================
    # 4. BİRİM ÇEVİRİCİ
    # =================================================================
    def setup_unit_tab(self):
        f = self.tab_unit
        self.create_header(f, "HIZLI BİRİM ÇEVİRİCİ")
        
        self.sv_val = ctk.StringVar(); self.sv_val.trace_add("write", self.convert_unit)
        frame_conv = ctk.CTkFrame(f, fg_color=COLOR_CARD, corner_radius=15); frame_conv.pack(pady=20, padx=150, fill="x")
        frame_conv.columnconfigure((0,1,3), weight=2); frame_conv.columnconfigure(2, weight=1)
        
        self.entry_u = ctk.CTkEntry(frame_conv, textvariable=self.sv_val, placeholder_text="0", height=50, font=("Arial", 22), justify="center", fg_color="#111", border_color="#555", text_color="white")
        self.entry_u.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.units = ["mm", "inch", "m", "kg", "lb", "bar", "psi", "kW", "HP"]
        self.cmb_f = ctk.CTkComboBox(frame_conv, values=self.units, height=50, font=("Arial", 16, "bold"), justify="center", command=self.convert_unit); self.cmb_f.set("inch"); self.cmb_f.grid(row=0, column=1, padx=10, sticky="ew")
        ctk.CTkLabel(frame_conv, text="➜", font=("Arial", 30)).grid(row=0, column=2)
        self.cmb_t = ctk.CTkComboBox(frame_conv, values=self.units, height=50, font=("Arial", 16, "bold"), justify="center", command=self.convert_unit); self.cmb_t.set("mm"); self.cmb_t.grid(row=0, column=3, padx=20, sticky="ew")
        
        self.lbl_u_res = ctk.CTkLabel(f, text="0.0000", font=("Arial", 72, "bold"), text_color="white"); self.lbl_u_res.pack(pady=(40, 10))

    def convert_unit(self, *args):
        try:
            val = float(self.sv_val.get().replace(',', '.') or 0)
            u_f, u_t = self.cmb_f.get(), self.cmb_t.get()
            if u_f == u_t: self.lbl_u_res.configure(text=f"{val:.4f}"); return
            
            factors = {"mm":("L",1), "m":("L",1000), "inch":("L",25.4), "kg":("M",1), "lb":("M",0.453592), "bar":("P",1), "psi":("P",0.0689), "kW":("W",1), "HP":("W",0.7457)}
            tf, ff = factors.get(u_f, (None,0)); tt, ft = factors.get(u_t, (None,0))
            
            if tf != tt: self.lbl_u_res.configure(text="---", text_color="red"); return
            res = (val * ff) / ft
            self.lbl_u_res.configure(text=f"{res:.4f}", text_color="white")
        except: self.lbl_u_res.configure(text="0.0000")

if __name__ == "__main__":
    app = StandardLibraryApp()
    app.mainloop()