import customtkinter as ctk
import os
import subprocess
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox

# --- AYARLAR VE HAFIZA YÖNETİMİ ---
SETTINGS_FILE = "settings.json"

def load_settings():
    """Daha önce seçilen klasör yolunu dosyadan yükler."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"workspace_path": ""}

def save_settings(path):
    """Seçilen yolu settings.json dosyasına kaydeder."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump({"workspace_path": path}, f, indent=4)

# --- EVRENSEL YOL FONKSİYONU ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- TEMA AYARLARI ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") 

COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SUB = "#9E9E9E"

class MainLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM")
        self.geometry("550x880") 
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        # 1. Hafızadaki yolu yükle
        self.settings = load_settings()
        self.workspace_path = self.settings.get("workspace_path", "")

        # 2. Eğer yol yoksa, ilk açılışta bir kez sor
        if not self.workspace_path or not os.path.exists(self.workspace_path):
            self.select_workspace(first_run=True)

        self.setup_ui()

    def select_workspace(self, first_run=False):
        """Kullanıcıya klasör seçtirir ve kaydeder."""
        path = filedialog.askdirectory(title="Projelerin Kaydedileceği Ana Klasörü Seçin")
        
        if path:
            self.workspace_path = path
            save_settings(path)
            if hasattr(self, 'lbl_path_val'):
                self.lbl_path_val.configure(text=path)
        else:
            # İptal edilirse ve ilk açılışsa varsayılan ata
            if first_run:
                self.workspace_path = os.path.join(os.path.expanduser("~"), "Documents", "BEM_Kayitlari")
                os.makedirs(self.workspace_path, exist_ok=True)
                save_settings(self.workspace_path)

    def setup_ui(self):
        # --- ÜST BAŞLIK ---
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(pady=(30, 10))
        
        self.lbl_title = ctk.CTkLabel(self.frame_header, text="BURSA ELİF MAKİNA", font=("Impact", 40), text_color=COLOR_TEXT_MAIN)
        self.lbl_title.pack()
        
        self.lbl_sub = ctk.CTkLabel(self.frame_header, text="MÜHENDİSLİK YÖNETİM PANELİ", font=("Arial", 12, "bold"), text_color="gray")
        self.lbl_sub.pack(pady=(5, 0))

        # --- ÇALIŞMA ALANI BİLGİSİ ---
        self.frame_path = ctk.CTkFrame(self, fg_color="#181818", corner_radius=10)
        self.frame_path.pack(pady=10, padx=35, fill="x")

        self.lbl_path_title = ctk.CTkLabel(self.frame_path, text="AKTİF ÇALIŞMA DİZİNİ:", font=("Arial", 10, "bold"), text_color="gray")
        self.lbl_path_title.pack(pady=(5, 0))

        self.lbl_path_val = ctk.CTkLabel(self.frame_path, text=self.workspace_path, font=("Consolas", 10), text_color="#00E676", wraplength=450)
        self.lbl_path_val.pack(pady=(0, 5))

        self.btn_change_path = ctk.CTkButton(self.frame_path, text="KLASÖRÜ DEĞİŞTİR", font=("Arial", 9, "bold"), 
                                            height=20, fg_color="#333", command=self.select_workspace)
        self.btn_change_path.pack(pady=5)

        # --- MODÜL KARTLARI ---
        self.create_mono_card("PROJE YÖNETİCİSİ", "Klasör yapılandırması ve proje kurulumu.", "📂", self.run_folder_manager)
        self.create_mono_card("ÜRETİM ÇIKTILARI", "Toplu DXF / STEP dönüştürme merkezi.", "⚙️", self.run_exporter)
        self.create_mono_card("MALİYET HESAPLAYICI", "Malzeme ve işçilik teklif analizi.", "💰", self.run_cost_calc)
        self.create_mono_card("KÜTLE HESAPLAYICI", "Ağırlık ve malzeme yoğunluk hesabı.", "⚖️", self.run_mass_calc)
        self.create_mono_card("KESİM OPTİMİZASYONU", "Profil ve boru kesim planlama (Nesting).", "✂️", self.run_cutting_opt)
        self.create_mono_card("STANDART ELEMANLAR", "Cıvata, somun, rulman ve kütüphane.", "🔩", self.run_std_lib)

        # --- ALT BİLGİ ---
        self.lbl_footer = ctk.CTkLabel(self, text="| Bursa Elif Makina - 2026", font=("Arial", 10), text_color="#333")
        self.lbl_footer.pack(side="bottom", pady=10)

    def create_mono_card(self, title, desc, icon, command):
        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=15, cursor="hand2", border_width=1, border_color="#2B2B2B")
        card.pack(pady=6, padx=35, fill="x")

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

    def run_process(self, relative_path):
        base_path = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_path, relative_path)
        
        if os.path.exists(script_path):
            try:
                # KRİTİK: Workspace yolunu alt programa "argüman" olarak atıyoruz.
                subprocess.Popen([sys.executable, script_path, self.workspace_path], cwd=os.path.dirname(script_path))
            except Exception as e:
                messagebox.showerror("Hata", f"Program başlatılamadı:\n{e}")
        else:
            messagebox.showerror("Dosya Yok", f"Modül dosyası bulunamadı:\n{script_path}")

    # Modül Yolları
    def run_folder_manager(self): self.run_process("apps/proje_yonetimi/main.py")
    def run_exporter(self): self.run_process("apps/batch_exporter/main.py")
    def run_cost_calc(self): self.run_process("apps/maliyet_hesaplayici/main.py")
    def run_mass_calc(self): self.run_process("apps/kutle_hesaplayici/main.py")
    def run_cutting_opt(self): self.run_process("apps/kesim_optimizasyonu/main.py")
    def run_std_lib(self): self.run_process("apps/standart_kutuphane/main.py")

if __name__ == "__main__":
    app = MainLauncher()
    app.mainloop()