import customtkinter as ctk
import os
import subprocess
import sys
from tkinter import messagebox

# --- TEMA AYARLARI ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") 

# MONOCHROME PALET (PRESTİJ)
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SUB = "#9E9E9E"
COLOR_ACCENT = "#FFFFFF"

class MainLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM")
        self.geometry("550x850") # Biraz daha uzattık (5. modül için)
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        # --- ÜST BAŞLIK ---
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(pady=(30, 20))
        
        self.lbl_title = ctk.CTkLabel(self.frame_header, text="BURSA ELİF MAKİNA", font=("Impact", 40), text_color=COLOR_TEXT_MAIN)
        self.lbl_title.pack()
        
        self.lbl_sub = ctk.CTkLabel(self.frame_header, text="MÜHENDİSLİK YÖNETİM PANELİ", font=("Arial", 12, "bold"), text_color="gray")
        self.lbl_sub.pack(pady=(5, 0))

        # --- MODÜLLER ---
        
        # 1. PROJE
        self.create_mono_card(
            title="PROJE YÖNETİCİSİ",
            desc="Klasör yapılandırması ve proje kurulumu.",
            icon="📂", 
            command=self.run_folder_manager
        )

        # 2. DXF/STEP
        self.create_mono_card(
            title="ÜRETİM ÇIKTILARI",
            desc="Toplu DXF / STEP dönüştürme merkezi.",
            icon="⚙️", 
            command=self.run_exporter
        )

        # 3. MALİYET
        self.create_mono_card(
            title="MALİYET HESAPLAYICI",
            desc="Malzeme ve işçilik teklif analizi.",
            icon="💰", 
            command=self.run_cost_calc
        )

        # 4. KÜTLE
        self.create_mono_card(
            title="KÜTLE HESAPLAYICI",
            desc="Ağırlık ve malzeme yoğunluk hesabı.",
            icon="⚖️", 
            command=self.run_mass_calc
        )

        # 5. KESİM OPTİMİZASYONU (YENİ)
        self.create_mono_card(
            title="KESİM OPTİMİZASYONU",
            desc="Profil ve boru kesim planlama (Nesting).",
            icon="✂️", 
            command=self.run_cutting_opt
        )

        # 6. STANDART KÜTÜPHANE
        self.create_mono_card(
            title="STANDART ELEMANLAR",
            desc="Cıvata, somun, rulman ve kama ölçü kütüphanesi.",
            icon="🔩", 
            command=self.run_std_lib
        )

        # --- ALT BİLGİ ---
        self.lbl_footer = ctk.CTkLabel(self, text="| Bursa Elif Makina", font=("Arial", 10), text_color="#333")
        self.lbl_footer.pack(side="bottom", pady=20)

    # --- KART OLUŞTURUCU FONKSİYON (HATANIN KAYNAĞI BUYDU, ŞİMDİ EKLENDİ) ---
    def create_mono_card(self, title, desc, icon, command):
        """Siyah-Beyaz-Gri Kart Tasarımı"""
        
        # Kart (Antrasit)
        card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=15, cursor="hand2", border_width=1, border_color="#2B2B2B")
        card.pack(pady=8, padx=35, fill="x")

        # Hover Efektleri
        def on_enter(e): card.configure(border_color="#FFFFFF", fg_color="#252525")
        def on_leave(e): card.configure(border_color="#2B2B2B", fg_color=COLOR_CARD)
        def on_click(e): command()

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", on_click)

        # İKON & BAŞLIK
        lbl_icon = ctk.CTkLabel(card, text=icon, font=("Arial", 28))
        lbl_icon.pack(side="left", padx=(25, 15), pady=20)
        
        frame_text = ctk.CTkFrame(card, fg_color="transparent")
        frame_text.pack(side="left", fill="both", expand=True, pady=15)

        lbl_title = ctk.CTkLabel(frame_text, text=title, font=("Arial", 15, "bold"), text_color=COLOR_TEXT_MAIN, anchor="w")
        lbl_title.pack(fill="x")

        lbl_desc = ctk.CTkLabel(frame_text, text=desc, font=("Arial", 11), text_color=COLOR_TEXT_SUB, anchor="w")
        lbl_desc.pack(fill="x")

        # Tıklama olaylarını alt elemanlara da yay
        for w in [lbl_icon, lbl_title, lbl_desc, frame_text]:
            w.bind("<Enter>", on_enter); w.bind("<Leave>", on_leave); w.bind("<Button-1>", on_click)

    # --- ÇALIŞTIRMA MANTIĞI ---
    def run_process(self, relative_path):
        base_path = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_path, relative_path)
        
        if os.path.exists(script_path):
            try:
                # Programı kendi klasöründe başlat (cwd parametresi önemli)
                subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path))
            except Exception as e:
                messagebox.showerror("Hata", f"Program başlatılamadı:\n{e}")
        else:
            messagebox.showerror("Dosya Yok", f"Modül dosyası bulunamadı:\n{script_path}\n\nLütfen klasör adlarını kontrol edin.")

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