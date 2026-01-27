import customtkinter as ctk
import os
import subprocess
import sys
import json
from tkinter import filedialog, messagebox

# --- MODÜLLERİN IMPORT EDİLMESİ (EXE İÇİN GEREKLİ) ---
try:
    import apps.proje_yonetimi.main as mod_proje
    import apps.batch_exporter.main as mod_exporter
    import apps.maliyet_hesaplayici.main as mod_maliyet
    import apps.kutle_hesaplayici.main as mod_kutle
    import apps.kesim_optimizasyonu.main as mod_kesim
    import apps.standart_kutuphane.main as mod_standart
except ImportError as e:
    print(f"Modül import uyarısı: {e}")

# --- AYARLAR YÖNETİMİ ---
SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"workspace_path": ""}

def save_settings(path):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({"workspace_path": path}, f, indent=4)

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SUB = "#9E9E9E"

class MainLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM - Ana Panel")
        self.geometry("550x880")
        self.configure(fg_color=COLOR_BG)
        self.resizable(False, False)

        self.settings = load_settings()
        self.workspace_path = self.settings.get("workspace_path", "")

        if not self.workspace_path or not os.path.exists(self.workspace_path):
            self.select_workspace(first_run=True)

        self.setup_ui()

    def select_workspace(self, first_run=False):
        path = filedialog.askdirectory(title="Çalışma Klasörünü Seçin")
        if path:
            self.workspace_path = path
            save_settings(path)
            if hasattr(self, 'lbl_path_val'): self.lbl_path_val.configure(text=path)
        elif first_run:
            self.workspace_path = os.path.join(os.path.expanduser("~"), "Documents", "BEM_Kayitlari")
            os.makedirs(self.workspace_path, exist_ok=True)
            save_settings(self.workspace_path)

    def setup_ui(self):
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(pady=(30, 10))
        ctk.CTkLabel(self.frame_header, text="BURSA ELİF MAKİNA", font=("Impact", 40), text_color=COLOR_TEXT_MAIN).pack()
        ctk.CTkLabel(self.frame_header, text="MÜHENDİSLİK YÖNETİM PANELİ", font=("Arial", 12, "bold"), text_color="gray").pack(pady=(5, 0))

        self.frame_path = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        self.frame_path.pack(pady=10, padx=35, fill="x")
        ctk.CTkLabel(self.frame_path, text="AKTİF ÇALIŞMA DİZİNİ:", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(5, 0))
        self.lbl_path_val = ctk.CTkLabel(self.frame_path, text=self.workspace_path, font=("Consolas", 10), text_color="#00E676", wraplength=450)
        self.lbl_path_val.pack(pady=(0, 5))
        ctk.CTkButton(self.frame_path, text="KLASÖRÜ DEĞİŞTİR", font=("Arial", 9, "bold"), height=20, fg_color="#333", command=self.select_workspace).pack(pady=5)

        # Kartlar
        self.create_mono_card("PROJE YÖNETİCİSİ", "Klasör yapılandırması.", "📂", "--run-proje")
        self.create_mono_card("ÜRETİM ÇIKTILARI", "Toplu DXF / STEP.", "⚙️", "--run-exporter")
        self.create_mono_card("MALİYET HESAPLAYICI", "Teklif analizi.", "💰", "--run-maliyet")
        self.create_mono_card("KÜTLE HESAPLAYICI", "Ağırlık hesabı.", "⚖️", "--run-kutle")
        self.create_mono_card("KESİM OPTİMİZASYONU", "Profil kesim planı.", "✂️", "--run-kesim")
        self.create_mono_card("STANDART ELEMANLAR", "Teknik kütüphane.", "🔩", "--run-standart")

        ctk.CTkLabel(self, text="| Bursa Elif Makina - 2026", font=("Arial", 10), text_color="#333").pack(side="bottom", pady=10)

    def create_mono_card(self, title, desc, icon, flag):
        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=15, cursor="hand2", border_width=1, border_color="#2B2B2B")
        card.pack(pady=6, padx=35, fill="x")
        
        def command():
            try:
                # DÜZELTME BURADA YAPILDI: sys.argv[0] eklendi
                # Bu sayede komut: python.exe main_launcher.py --run-proje "C:/Yol" şeklinde çalışır.
                script_path = sys.argv[0]
                subprocess.Popen([sys.executable, script_path, flag, self.workspace_path])
            except Exception as e:
                messagebox.showerror("Hata", str(e))

        def on_enter(e): card.configure(border_color="#FFFFFF", fg_color="#252525")
        def on_leave(e): card.configure(border_color="#2B2B2B", fg_color=COLOR_CARD)
        def on_click(e): command()

        card.bind("<Enter>", on_enter); card.bind("<Leave>", on_leave); card.bind("<Button-1>", on_click)
        
        lbl_icon = ctk.CTkLabel(card, text=icon, font=("Arial", 28))
        lbl_icon.pack(side="left", padx=(25, 15), pady=15)
        frame_text = ctk.CTkFrame(card, fg_color="transparent")
        frame_text.pack(side="left", fill="both", expand=True, pady=10)
        lbl_title = ctk.CTkLabel(frame_text, text=title, font=("Arial", 14, "bold"), text_color=COLOR_TEXT_MAIN, anchor="w")
        lbl_title.pack(fill="x")
        lbl_desc = ctk.CTkLabel(frame_text, text=desc, font=("Arial", 10), text_color=COLOR_TEXT_SUB, anchor="w")
        lbl_desc.pack(fill="x")
        
        for w in [lbl_icon, lbl_title, lbl_desc, frame_text]:
            w.bind("<Enter>", on_enter); w.bind("<Leave>", on_leave); w.bind("<Button-1>", on_click)

# --- ANA GİRİŞ NOKTASI (DAĞITICI) ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        komut = sys.argv[1]
        
        # Yol argümanını al (eğer varsa 3. argümandır)
        path_arg = sys.argv[2] if len(sys.argv) > 2 else None

        if komut == "--run-proje":
            if path_arg: mod_proje.ROOT_DIR = path_arg
            app = mod_proje.ProjectFolderApp()
            app.mainloop()
            
        elif komut == "--run-exporter":
            # Batch exporter direkt klasör seçtirdiği için path zorunlu değil ama ekleyelim
            app = mod_exporter.BatchExporterApp()
            app.mainloop()
            
        elif komut == "--run-maliyet":
            if path_arg: mod_maliyet.FIXED_ROOT = path_arg
            mod_maliyet.main() # Maliyet modülünü başlat
            
        elif komut == "--run-kutle":
            if path_arg: mod_kutle.WORKSPACE_PATH = path_arg
            app = mod_kutle.MassCalculatorApp()
            app.mainloop()
            
        elif komut == "--run-kesim":
            if path_arg: mod_kesim.WORKSPACE_PATH = path_arg
            app = mod_kesim.CuttingOptimizerApp()
            app.mainloop()
            
        elif komut == "--run-standart":
            if path_arg: mod_standart.WORKSPACE_PATH = path_arg
            app = mod_standart.StandardLibraryApp()
            app.mainloop()

    # Argüman yoksa (Çift tıklama ile açıldıysa) Ana Menü
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and not sys.argv[1].startswith("--")):
        app = MainLauncher()
        app.mainloop()