import customtkinter as ctk
import os
import json
import subprocess
from tkinter import filedialog, messagebox

# --- TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# MONOCHROME AYARLAR
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT = "#FFFFFF"
COLOR_BTN_BG = "#E0E0E0"        # Buton Arka Planı
COLOR_BTN_TEXT = "#000000"      # Buton Yazısı
COLOR_BTN_HOVER = "#FFFFFF"     # Hover Rengi

CONFIG_FILE = "bem_folder_config.json"

class ProjectFolderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM")
        self.geometry("600x700")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        self.root_dir = self.load_config()

        # --- BAŞLIK ---
        self.frame_head = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_head.pack(pady=(40, 20))
        ctk.CTkLabel(self.frame_head, text="PROJE", font=("Impact", 32), text_color="#FFFFFF").pack()
        ctk.CTkLabel(self.frame_head, text="Standart Klasör Yapılandırması", font=("Arial", 12), text_color="gray").pack()

        # --- KART 1: ANA KLASÖR SEÇİMİ ---
        self.frame_root = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=15, border_width=1, border_color="#333")
        self.frame_root.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(self.frame_root, text="ÇALIŞMA YILI / ANA DİZİN", font=("Arial", 12, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(15, 5))

        self.lbl_root_path = ctk.CTkLabel(self.frame_root, text=self.root_dir if self.root_dir else "Seçili Değil", 
                                          font=("Consolas", 11), text_color="#FFFFFF" if self.root_dir else "red", anchor="w")
        self.lbl_root_path.pack(fill="x", padx=20, pady=5)

        btn_root = self.create_white_btn(self.frame_root, "ANA KLASÖRÜ DEĞİŞTİR", self.select_root_directory)
        btn_root.configure(height=35, font=("Arial", 11, "bold")) # Bu buton biraz daha kibar olsun
        btn_root.pack(pady=(5, 20), padx=20, fill="x")

        # --- KART 2: PROJE DETAYLARI ---
        self.frame_inputs = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=15, border_width=1, border_color="#333")
        self.frame_inputs.pack(pady=10, padx=30, fill="x")

        # Firma Seçimi
        ctk.CTkLabel(self.frame_inputs, text="FİRMA ADI", font=("Arial", 12, "bold"), text_color="white").pack(anchor="w", padx=20, pady=(20, 5))
        self.combo_cust = ctk.CTkComboBox(self.frame_inputs, height=40, variable=ctk.StringVar(),
                                          fg_color=COLOR_BG, border_color="#444", button_color="#444", text_color="white", dropdown_fg_color="#222")
        self.combo_cust.pack(fill="x", padx=20, pady=5)
        self.combo_cust.set("") 

        # Proje Adı
        ctk.CTkLabel(self.frame_inputs, text="PROJE / ÜRÜN ADI", font=("Arial", 12, "bold"), text_color="white").pack(anchor="w", padx=20, pady=(15, 5))
        self.entry_proj = ctk.CTkEntry(self.frame_inputs, placeholder_text="Örn: Twistoff Kavanoz Temizleme", height=40,
                                       fg_color=COLOR_BG, border_color="#444", text_color="white")
        self.entry_proj.pack(fill="x", padx=20, pady=(5, 25))

        # --- OLUŞTUR BUTONU ---
        self.btn_create = self.create_white_btn(self, "PROJE KLASÖRLERİNİ OLUŞTUR", self.create_project)
        self.btn_create.configure(height=60, font=("Arial", 15, "bold"))
        self.btn_create.pack(pady=30, padx=30, fill="x")

        # Durum Çubuğu
        self.lbl_status = ctk.CTkLabel(self, text="Hazır...", text_color="gray")
        self.lbl_status.pack(side="bottom", pady=15)

        if self.root_dir: self.refresh_customers()

    def create_white_btn(self, master, text, command):
        """Özel Beyaz Buton (Batch Exporter ile aynı)"""
        return ctk.CTkButton(master, text=text, font=("Arial", 13, "bold"),
                             height=45, fg_color=COLOR_BTN_BG, text_color=COLOR_BTN_TEXT,
                             hover_color=COLOR_BTN_HOVER, corner_radius=10,
                             command=command)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f: return json.load(f).get("root_dir", "")
            except: return ""
        return ""

    def save_config(self, path):
        with open(CONFIG_FILE, "w") as f: json.dump({"root_dir": path}, f)

    def select_root_directory(self):
        path = filedialog.askdirectory(title="Çalışılacak YIL klasörünü seçin (Örn: BEM/2026)")
        if path:
            self.root_dir = path
            self.save_config(path)
            self.lbl_root_path.configure(text=path, text_color="#29B6F6")
            self.refresh_customers()

    def refresh_customers(self):
        if not self.root_dir or not os.path.exists(self.root_dir): return
        try:
            customers = [d for d in os.listdir(self.root_dir) if os.path.isdir(os.path.join(self.root_dir, d))]
            customers.sort()
            self.combo_cust.configure(values=customers)
        except Exception as e: self.lbl_status.configure(text=f"Hata: {e}")

    def format_title(self, text):
        """Metni 'İlk Harfler Büyük' formatına çevirir (Title Case)."""
        if not text: return ""
        return text.strip().title()

    def create_project(self):
        if not self.root_dir:
            messagebox.showerror("Hata", "Lütfen önce Ana Klasör (Yıl) seçin!")
            return

        raw_cust = self.combo_cust.get()
        raw_proj = self.entry_proj.get()

        cust_name = self.format_title(raw_cust)
        proj_name = self.format_title(raw_proj)

        if not cust_name: messagebox.showwarning("Eksik", "Firma adı girmediniz."); return
        if not proj_name: messagebox.showwarning("Eksik", "Proje/Ürün adı girmediniz."); return

        # Hedef Yol
        target_path = os.path.join(self.root_dir, cust_name, proj_name)

        if os.path.exists(target_path):
            messagebox.showerror("Hata", f"Bu proje klasörü zaten var!\n\n{target_path}")
            return

        # --- NUMARASIZ, SADE KLASÖR YAPISI (SENİN İSTEDİĞİN GİBİ) ---
        subfolders = [
            "Tasarım Dosyaları/Ana Montaj",
            "Tasarım Dosyaları/Sac Parçalar",
            "Tasarım Dosyaları/Mekanik Parçalar",
            "Tasarım Dosyaları/Satınalma Parçaları",
            
            "Üretim Çıktıları/DXF Kesim",
            "Üretim Çıktıları/PDF Teknik Resim",
            "Üretim Çıktıları/STEP 3D",
            
            "Dökümantasyon/Teklifler",
            "Dökümantasyon/Malzeme Listeleri",
            "Dökümantasyon/Görseller"
        ]

        try:
            os.makedirs(target_path)
            for sub in subfolders:
                os.makedirs(os.path.join(target_path, sub))

            self.lbl_status.configure(text=f"Oluşturuldu: {proj_name}", text_color="#66BB6A")
            
            msg_box = messagebox.askyesno("Başarılı", f"Proje yapısı kuruldu:\n\n{cust_name} / {proj_name}\n\nKlasörü şimdi açmak ister misin?")
            if msg_box: os.startfile(target_path)

            self.refresh_customers()
            self.entry_proj.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Kritik Hata", f"Klasör oluşturulamadı:\n{e}")

if __name__ == "__main__":
    app = ProjectFolderApp()
    app.mainloop()