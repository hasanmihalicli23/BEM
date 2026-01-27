import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import sys
import subprocess

# --- EXE UYUMLU KAYNAK YOLU ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
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

# MONOCHROME PALET
COLOR_BG = "#0F0F0F"
COLOR_CARD = "#1A1A1A"
COLOR_TEXT_MAIN = "#FFFFFF"
COLOR_TEXT_SUB = "#AAAAAA"
COLOR_BTN_BG = "#E0E0E0"
COLOR_BTN_TEXT = "#000000"
COLOR_ACCENT_RED = "#FF5252"

class CuttingOptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM - Kesim Optimizasyonu")
        self.geometry("1050x750")
        self.configure(fg_color=COLOR_BG)

        self.parts_list = [] 
        self.inputs = {}
        self.last_result = None 

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === SOL PANEL (GİRİŞLER) ===
        self.frame_left = ctk.CTkFrame(self, width=350, fg_color=COLOR_CARD, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_left.grid_propagate(False)

        ctk.CTkLabel(self.frame_left, text="KESİM AYARLARI", font=("Impact", 24), text_color=COLOR_TEXT_MAIN).pack(pady=(30, 20))

        # Stok Girişi
        self.create_input_group("STOK BİLGİLERİ", [("Stok Boyu (mm):", "6000"), ("Testere Payı (mm):", "3")])

        # Parça Ekleme Alanı
        self.frame_add = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        self.frame_add.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(self.frame_add, text="PARÇA LİSTESİ", font=("Arial", 12, "bold"), text_color="gray").pack(anchor="w")
        
        self.entry_len = ctk.CTkEntry(self.frame_add, placeholder_text="Uzunluk (mm)", height=40, fg_color=COLOR_BG, border_color="#444", text_color="white")
        self.entry_len.pack(fill="x", pady=(5, 5))
        
        self.entry_qty = ctk.CTkEntry(self.frame_add, placeholder_text="Adet", height=40, fg_color=COLOR_BG, border_color="#444", text_color="white")
        self.entry_qty.pack(fill="x", pady=5)
        
        self.btn_add = ctk.CTkButton(self.frame_add, text="LİSTEYE EKLE", font=("Arial", 12, "bold"), height=40,
                                     fg_color="#333", hover_color="#444", command=self.add_part)
        self.btn_add.pack(fill="x", pady=10)

        # Liste Görünümü
        self.scroll_parts = ctk.CTkScrollableFrame(self.frame_left, fg_color=COLOR_BG, height=200)
        self.scroll_parts.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        # Hesapla Butonu
        self.btn_calc = ctk.CTkButton(self.frame_left, text="HESAPLA", font=("Arial", 14, "bold"), height=50,
                                      fg_color=COLOR_BTN_BG, text_color=COLOR_BTN_TEXT, hover_color="white",
                                      command=self.optimize)
        self.btn_calc.pack(fill="x", padx=20, pady=(0, 10))

        # === SAĞ PANEL (SONUÇLAR) ===
        self.frame_right = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Üst Başlık ve PDF Butonu
        head_frame = ctk.CTkFrame(self.frame_right, fg_color="transparent")
        head_frame.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(head_frame, text="KESİM PLANI", font=("Impact", 32), text_color=COLOR_TEXT_MAIN).pack(side="left")
        
        self.btn_pdf = ctk.CTkButton(head_frame, text="PDF RAPOR İNDİR", font=("Arial", 12, "bold"), height=40,
                                     fg_color="#CFD8DC", text_color="black", hover_color="#B0BEC5", state="disabled", command=self.export_pdf)
        self.btn_pdf.pack(side="right")

        # Özet Bilgi
        self.lbl_summary = ctk.CTkLabel(self.frame_right, text="Henüz hesaplama yapılmadı...", font=("Arial", 14), text_color=COLOR_TEXT_SUB)
        self.lbl_summary.pack(anchor="w", pady=(0, 20))

        # Sonuç Listesi
        self.scroll_results = ctk.CTkScrollableFrame(self.frame_right, fg_color=COLOR_CARD, corner_radius=15)
        self.scroll_results.pack(fill="both", expand=True)

    def create_input_group(self, title, fields):
        frame = ctk.CTkFrame(self.frame_left, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame, text=title, font=("Arial", 12, "bold"), text_color="gray").pack(anchor="w")
        for label, default in fields:
            f = ctk.CTkFrame(frame, fg_color="transparent")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=label, width=120, anchor="w", font=("Arial", 12)).pack(side="left")
            entry = ctk.CTkEntry(f, height=30, fg_color=COLOR_BG, border_color="#444", text_color="white")
            entry.pack(side="right", expand=True, fill="x")
            entry.insert(0, default)
            self.inputs[label] = entry

    def add_part(self):
        try:
            l_val = self.entry_len.get().replace(',', '.')
            q_val = self.entry_qty.get()
            if not l_val or not q_val: return
            length = float(l_val); qty = int(q_val)
            if length <= 0 or qty <= 0: return
            self.parts_list.append({'len': length, 'qty': qty})
            self.refresh_parts_list()
            self.entry_len.delete(0, 'end'); self.entry_qty.delete(0, 'end'); self.entry_len.focus()
        except ValueError: messagebox.showerror("Hata", "Lütfen sayısal değer girin.")

    def refresh_parts_list(self):
        for w in self.scroll_parts.winfo_children(): w.destroy()
        for i, item in enumerate(self.parts_list):
            f = ctk.CTkFrame(self.scroll_parts, fg_color="#222", corner_radius=5)
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{item['len']} mm", font=("Arial", 12, "bold"), width=80, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"x {item['qty']} Adet", font=("Arial", 12), width=80).pack(side="left")
            ctk.CTkButton(f, text="X", width=30, height=20, fg_color=COLOR_ACCENT_RED, command=lambda idx=i: self.delete_part(idx)).pack(side="right", padx=5, pady=5)

    def delete_part(self, index):
        del self.parts_list[index]; self.refresh_parts_list()

    def optimize(self):
        if not self.parts_list: messagebox.showwarning("Uyarı", "Listeniz boş!"); return
        try:
            stock_len = float(self.inputs["Stok Boyu (mm):"].get())
            kerf = float(self.inputs["Testere Payı (mm):"].get())
        except: messagebox.showerror("Hata", "Stok verileri hatalı!"); return

        all_pieces = []
        for p in self.parts_list: all_pieces.extend([p['len']] * p['qty'])
        all_pieces.sort(reverse=True)

        if any(p > stock_len for p in all_pieces): messagebox.showerror("Hata", "Stok boyundan uzun parça var!"); return

        bars = [] 
        for piece in all_pieces:
            placed = False
            for bar in bars:
                current_len = sum(bar) + (len(bar) * kerf)
                needed = piece + (kerf if bar else 0)
                if (current_len + needed) <= stock_len:
                    bar.append(piece); placed = True; break
            if not placed: bars.append([piece])

        self.last_result = {"bars": bars, "stock": stock_len, "kerf": kerf}
        self.btn_pdf.configure(state="normal", fg_color="#CFD8DC")
        self.show_results(bars, stock_len, kerf)

    def show_results(self, bars, stock_len, kerf):
        for w in self.scroll_results.winfo_children(): w.destroy()
        total_waste = 0; total_used_len = 0
        
        for i, bar in enumerate(bars):
            used = sum(bar) + (len(bar) - 1) * kerf
            waste = stock_len - used
            total_waste += waste; total_used_len += stock_len

            card = ctk.CTkFrame(self.scroll_results, fg_color="#222", corner_radius=8)
            card.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(card, text=f"STOK #{i+1}", font=("Arial", 12, "bold"), text_color="white").pack(anchor="w", padx=10, pady=(5,0))
            
            prog = ctk.CTkProgressBar(card, height=15, corner_radius=5, progress_color="#4FC3F7")
            prog.set(used / stock_len)
            prog.pack(fill="x", padx=10, pady=5)
            
            cuts_str = " + ".join([f"{p:.0f}" for p in bar])
            info = f"Kesimler: {cuts_str}\nDolu: {used:.1f} mm | Fire: {waste:.1f} mm"
            ctk.CTkLabel(card, text=info, font=("Consolas", 11), text_color="#BBB", justify="left").pack(anchor="w", padx=10, pady=(0, 10))

        verim = ((total_used_len - total_waste) / total_used_len) * 100 if total_used_len > 0 else 0
        self.lbl_summary.configure(text=f"Toplam {len(bars)} Boy Stok | Fire: {total_waste:.1f} mm | Verim: %{verim:.1f}", text_color=COLOR_TEXT_MAIN)

    # --- GELİŞMİŞ PDF ÇIKTISI ---
    def export_pdf(self):
        if not self.last_result: return
        bars = self.last_result["bars"]
        stock_len = self.last_result["stock"]
        kerf = self.last_result["kerf"]

        # Varsayılan klasör olarak WORKSPACE_PATH'i ayarla
        path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                            initialdir=WORKSPACE_PATH,
                                            filetypes=[("PDF Dosyası", "*.pdf")], 
                                            title="Raporu Kaydet")
        if not path: return

        try:
            c = canvas.Canvas(path, pagesize=A4)
            width, height = A4
            
            # --- BAŞLIK ---
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 24)
            c.drawString(30, height - 50, "BEM")
            
            # Tarih
            c.setFont("Helvetica", 10)
            date_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            c.drawRightString(width - 30, height - 50, f"Tarih: {date_str}")
            
            # Çizgi
            c.setStrokeColor(colors.black)
            c.setLineWidth(2)
            c.line(30, height - 60, width - 30, height - 60)

            # --- ÖZET KUTUSU ---
            total_bars = len(bars)
            total_waste = 0
            total_len = total_bars * stock_len
            for b in bars: total_waste += stock_len - (sum(b) + (len(b)-1)*kerf)
            efficiency = ((total_len - total_waste) / total_len) * 100

            c.setLineWidth(1)
            c.rect(30, height - 120, width - 60, 50, stroke=1, fill=0)
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, height - 90, "PROJE :")
            
            c.setFont("Helvetica", 11)
            summary_text = f"Toplam Stok: {total_bars} Adet ({stock_len:.0f} mm)   |   Toplam Fire: {total_waste:.1f} mm   |   Verimlilik: %{efficiency:.1f}"
            c.drawString(40, height - 105, summary_text)

            # --- ÇUBUK ÇİZİMLERİ ---
            y = height - 160
            bar_draw_width = width - 60 
            bar_height = 15
            
            for i, bar in enumerate(bars):
                if y < 60:
                    c.showPage()
                    y = height - 50
                
                used_len = sum(bar) + (len(bar)-1)*kerf
                waste = stock_len - used_len
                
                c.setFillColor(colors.black)
                c.setFont("Helvetica-Bold", 10)
                c.drawString(30, y + 20, f"STOK #{i+1}")
                c.setFont("Helvetica", 10)
                c.drawRightString(width - 30, y + 20, f"Fire: {waste:.1f} mm")

                c.setStrokeColor(colors.black)
                c.rect(30, y, bar_draw_width, bar_height)
                
                current_x = 30
                for piece in bar:
                    piece_w_px = (piece / stock_len) * bar_draw_width
                    
                    c.setFillColor(colors.lightgrey)
                    c.rect(current_x, y, piece_w_px, bar_height, fill=1, stroke=1)
                    
                    if piece_w_px > 15: 
                        c.setFillColor(colors.black)
                        c.setFont("Helvetica", 8)
                        c.drawCentredString(current_x + piece_w_px/2, y + 4, f"{piece:.0f}")
                    
                    kerf_w_px = (kerf / stock_len) * bar_draw_width
                    current_x += piece_w_px + kerf_w_px
                
                waste_w_px = (waste / stock_len) * bar_draw_width
                if waste_w_px > 0:
                    c.setFillColor(colors.Color(1, 0.8, 0.8)) 
                    c.rect(current_x - kerf_w_px, y, width - 30 - (current_x - kerf_w_px), bar_height, fill=1, stroke=1)
                    c.setFillColor(colors.red)
                    c.setFont("Helvetica-Oblique", 8)
                    if waste_w_px > 20:
                        c.drawCentredString((current_x - kerf_w_px) + waste_w_px/2, y + 4, "FIRE")

                c.setFillColor(colors.black)
                c.setFont("Helvetica", 9)
                text_list = " + ".join([f"{p:.0f}" for p in bar])
                c.drawString(30, y - 12, f"Kesimler: {text_list}")

                y -= 60 

            c.save()
            messagebox.showinfo("Başarılı", "PDF Raporu başarıyla oluşturuldu!")
            
            # Cross-platform dosya açma
            if sys.platform == "win32":
                os.startfile(path)
            else:
                subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', path])

        except Exception as e:
            messagebox.showerror("Hata", f"PDF Hatası: {e}")

if __name__ == "__main__":
    app = CuttingOptimizerApp()
    app.mainloop()