import customtkinter as ctk
import os
import time
import win32com.client
import pythoncom
import threading
from tkinter import filedialog, messagebox
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Örnek kullanım: 
# logo = Image.open(resource_path("assets/logo.png"))

# --- ezdxf KONTROLÜ ---
try: import ezdxf
except ImportError: pass

# --- TEMA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# MONOCHROME AYARLAR (SİYAH/BEYAZ PRESTİJ TEMASI)
COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_BTN_BG = "#E0E0E0"        
COLOR_BTN_TEXT = "#000000"      
COLOR_BTN_HOVER = "#FFFFFF"     

# --- SW SABİTLERİ ---
swDocPART = 1
swDocASSEMBLY = 2
swSaveAsCurrentVersion = 0
swSaveAsOptions_Silent = 1
swOpenDocOptions_Silent = 1

class BatchExporterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BEM")
        self.geometry("600x750")
        self.configure(fg_color=COLOR_BG)

        # BAŞLIK
        self.frame_head = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_head.pack(pady=(30, 20))
        ctk.CTkLabel(self.frame_head, text="ÜRETİM", font=("Impact", 32), text_color="#FFFFFF").pack()
        ctk.CTkLabel(self.frame_head, text="SolidWorks Toplu Dönüştürme Merkezi", font=("Arial", 12), text_color="gray").pack()

        # AYARLAR KARTI
        self.frame_opts = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=15, border_width=1, border_color="#333")
        self.frame_opts.pack(pady=10, padx=30, fill="x")
        
        ctk.CTkLabel(self.frame_opts, text="ÇIKTI FORMATLARI", font=("Arial", 12, "bold"), text_color="gray").pack(pady=(15, 10))

        # Checkbox Alanı
        self.frame_checks = ctk.CTkFrame(self.frame_opts, fg_color="transparent")
        self.frame_checks.pack(pady=(0, 20))
        
        # DXF
        self.chk_dxf = ctk.CTkCheckBox(self.frame_checks, text="DXF (Lazer)", font=("Arial", 14, "bold"), 
                                       fg_color="white", checkmark_color="black", text_color="white")
        self.chk_dxf.pack(side="left", padx=20)
        self.chk_dxf.select()
        
        # STEP
        self.chk_step = ctk.CTkCheckBox(self.frame_checks, text="STEP (3D Katı)", font=("Arial", 14, "bold"), 
                                        fg_color="white", checkmark_color="black", text_color="white")
        self.chk_step.pack(side="left", padx=20)
        self.chk_step.select()

        # GİZLİ "Zorla Al" MANTIĞI:
        # Kodun orijinalinde self.chk_force_dxf vardı.
        # Şimdi onu UI'dan kaldırdım ama aşağıda process_part içinde hep True kabul edeceğim.

        # TABLAR
        self.tabview = ctk.CTkTabview(self, width=500, height=300, 
                                      fg_color=COLOR_CARD, 
                                      segmented_button_fg_color=COLOR_BG,
                                      segmented_button_selected_color="white",
                                      segmented_button_selected_hover_color="#EEE",
                                      segmented_button_unselected_hover_color="#333",
                                      text_color="black") 
        self.tabview.pack(pady=20, padx=30, fill="x")

        self.tab_folder = self.tabview.add("  KLASÖR TARA  ")
        self.tab_active = self.tabview.add("  AKTİF DOSYA  ")

        self.setup_folder_tab()
        self.setup_active_tab()

        # LOG
        self.txt_log = ctk.CTkTextbox(self, height=150, font=("Consolas", 11), 
                                      fg_color="#000000", text_color="#00FF00", border_color="#333", border_width=1)
        self.txt_log.pack(pady=20, padx=30, fill="x")

    def log(self, message):
        print(message)
        self.txt_log.insert("end", "> " + message + "\n")
        self.txt_log.see("end")

    def create_white_btn(self, master, text, command):
        """Özel Beyaz Buton"""
        return ctk.CTkButton(master, text=text, font=("Arial", 13, "bold"),
                             height=45, fg_color=COLOR_BTN_BG, text_color=COLOR_BTN_TEXT,
                             hover_color=COLOR_BTN_HOVER, corner_radius=8,
                             command=command)

    def setup_folder_tab(self):
        self.tab_folder.grid_columnconfigure(0, weight=1)
        self.entry_filter = ctk.CTkEntry(self.tab_folder, placeholder_text="Filtre (Örn: sac, gövde)", width=300, 
                                         fg_color=COLOR_BG, border_color="#444", text_color="white")
        self.entry_filter.grid(row=0, column=0, pady=(30, 15))
        
        btn = self.create_white_btn(self.tab_folder, "KLASÖR SEÇ VE BAŞLAT", self.start_folder_process)
        btn.grid(row=1, column=0, pady=10, sticky="ew", padx=50)

    def setup_active_tab(self):
        self.tab_active.grid_columnconfigure(0, weight=1)
        
        # Orijinal koddaki tek parça butonu
        btn1 = self.create_white_btn(self.tab_active, "TEK PARÇA İŞLE (Sadece Açık Olan)", self.start_single_process)
        btn1.grid(row=0, column=0, pady=(40, 10), sticky="ew", padx=50)

        # Orijinal koddaki montaj butonu
        btn2 = self.create_white_btn(self.tab_active, "MONTAJI TARA (Tüm Bileşenler)", self.start_active_process)
        btn2.grid(row=1, column=0, pady=10, sticky="ew", padx=50)

    # ==========================================
    # --- ORİJİNAL ÇALIŞAN MANTIK (V17 Core) ---
    # ==========================================
    def get_sw_app(self):
        return win32com.client.Dispatch("SldWorks.Application")

    def call_safe(self, obj, attr_name):
        try:
            val = getattr(obj, attr_name)
            if callable(val): return val()
            return val
        except: return None

    def open_doc_safe(self, app, path):
        try:
            res = app.OpenDoc6(path, swDocPART, swOpenDocOptions_Silent, "", 0, 0)
            if res: return res
        except: pass
        try:
            res = app.OpenDoc(path, swDocPART)
            if res: return res
        except: pass
        return None

    def is_sheet_metal(self, model):
        try:
            feat = model.FirstFeature()
            while feat:
                type_name = str(self.call_safe(feat, "GetTypeName2") or "")
                user_name = str(self.call_safe(feat, "Name") or "")
                keywords = ["SheetMetal", "Sac-Levha", "Sac", "FlatPattern", "Yassı-Çoğaltma"]
                if any(k in type_name for k in keywords) or any(k in user_name for k in keywords):
                    try: return round(feat.GetDefinition().Thickness * 1000, 2)
                    except: return 0.0
                feat = feat.GetNextFeature()
            return None 
        except: return None

    def process_with_ezdxf(self, file_path):
        if 'ezdxf' not in globals(): return False
        try:
            time.sleep(0.1) 
            doc = ezdxf.readfile(file_path)
            msp = doc.modelspace()
            modified = False
            for entity in msp:
                if entity.dxftype() in ['LINE', 'CIRCLE', 'ARC', 'LWPOLYLINE']:
                    ltype = str(entity.dxf.linetype).upper()
                    layer = str(entity.dxf.layer).upper()
                    if any(x in ltype for x in ['ISO', 'DASH', 'HIDDEN', 'AM_', 'CENTER']) or "BEND" in layer or "BÜKÜM" in layer:
                        entity.dxf.linetype = 'CONTINUOUS'; entity.dxf.color = 1; modified = True
            if modified: doc.save()
            return True
        except: return False

    def process_part(self, swApp, model, output_dirs, close_after=False):
        filename = "Bilinmeyen"
        try:
            path = self.call_safe(model, "GetPathName")
            if not path: return
            path = os.path.normpath(path)
            filename = os.path.splitext(os.path.basename(path))[0]
            dxf_dir, step_dir = output_dirs

            # DXF
            if self.chk_dxf.get():
                thickness = self.is_sheet_metal(model)
                
                # --- GİZLİ MANTIK ---
                # Orijinal kodda self.chk_force_dxf.get() vardı.
                # Burada onu sabit True yapıyorum ki hep zorlasın.
                force_dxf = True 
                
                if force_dxf or (thickness is not None):
                    th_str = str(int(thickness)) if (thickness and thickness.is_integer()) else str(thickness or "Levha")
                    if not thickness: dxf_name = f"{filename}.dxf"
                    else: dxf_name = f"{th_str}mm - {filename}.dxf"
                    
                    dxf_path = os.path.join(dxf_dir, dxf_name)
                    if not os.path.exists(dxf_path):
                        data_alignment = [0.0] * 12
                        var_alignment = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, data_alignment)
                        
                        # 1. Yöntem: Sac Açınımı
                        res = model.ExportToDWG2(dxf_path, path, 1, True, var_alignment, False, False, 5, None)
                        
                        # 2. Yöntem (V17 Orijinalinde yoktu ama V16'da vardı, eklememi ister misin? 
                        # Şimdilik orijinal V17'ye sadık kalıyorum sadece ExportToDWG2 deniyor)
                        
                        if res: 
                            self.log(f"-> DXF: {dxf_name}")
                            self.process_with_ezdxf(dxf_path)
                        else: self.log(f"-> DXF BAŞARISIZ: {filename}")
                else: self.log(f"   (Atlandı: Sac Değil)")

            # STEP
            if self.chk_step.get():
                step_path = os.path.join(step_dir, filename + ".step")
                if not os.path.exists(step_path):
                    model.SaveAs3(step_path, 0, 0)
                    self.log(f"-> STEP: {filename}")

        except Exception as e:
            self.log(f"Hata ({filename}): {e}")
        
        finally:
            if close_after and swApp and filename != "Bilinmeyen":
                try: swApp.CloseDoc(os.path.basename(path))
                except: pass

    # --- THREAD BAŞLATICILAR ---
    def start_folder_process(self):
        path = filedialog.askdirectory()
        if path: threading.Thread(target=self.run_folder_logic, args=(path,)).start()

    def start_active_process(self):
        threading.Thread(target=self.run_assembly_logic).start()

    def start_single_process(self):
        threading.Thread(target=self.run_single_logic).start()

    # --- 1. KLASÖR MODU (HAYALET + FİLTRE) ---
    def run_folder_logic(self, folder_path):
        pythoncom.CoInitialize()
        # self.btn_select_folder artık yok, yerel değişkende kaldı ama sorun değil
        self.txt_log.delete("1.0", "end")
        
        filter_text = self.entry_filter.get().strip().lower()
        
        try:
            folder_path = os.path.normpath(folder_path)
            self.log(f"Klasör: {folder_path}")
            if filter_text: self.log(f"Filtre: '{filter_text}'")
            
            swApp = self.get_sw_app()
            swApp.Visible = False; swApp.UserControl = False

            all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".sldprt")]
            
            files_to_process = []
            if filter_text:
                for f in all_files:
                    if filter_text in f.lower(): files_to_process.append(f)
            else: files_to_process = all_files

            self.log(f"{len(files_to_process)} parça işlenecek.\n")

            dxf_dir = os.path.join(folder_path, "DXF_BEM")
            step_dir = os.path.join(folder_path, "STEP_BEM")
            if self.chk_dxf.get() and not os.path.exists(dxf_dir): os.makedirs(dxf_dir)
            if self.chk_step.get() and not os.path.exists(step_dir): os.makedirs(step_dir)
            
            for i, f in enumerate(files_to_process):
                self.log(f"[{i+1}/{len(files_to_process)}] {f}")
                full_path = os.path.abspath(os.path.join(folder_path, f))
                res = self.open_doc_safe(swApp, full_path)
                model = res[0] if isinstance(res, tuple) else res
                if model: 
                    self.process_part(swApp, model, (dxf_dir, step_dir), close_after=True)
                else: 
                    self.log(f"   AÇILAMADI: {f}")

            self.log("\nBİTTİ.")
            swApp.Visible = True; swApp.UserControl = True
            messagebox.showinfo("Bitti", "Tamamlandı.")
            
        except Exception as e: 
            self.log(f"GENEL HATA: {e}")
            try: swApp.Visible = True; swApp.UserControl = True
            except: pass

    # --- 2. TEK PARÇA MODU ---
    def run_single_logic(self):
        pythoncom.CoInitialize()
        self.txt_log.delete("1.0", "end")
        try:
            swApp = self.get_sw_app()
            Model = swApp.ActiveDoc
            if not Model: self.log("HATA: Hiçbir dosya açık değil!"); return

            doc_type = self.call_safe(Model, "GetType")
            if doc_type != swDocPART:
                 self.log("HATA: Bu mod sadece PARÇA içindir."); return

            path = self.call_safe(Model, "GetPathName")
            if not path: self.log("HATA: Dosya kaydedilmemiş!"); return
            
            self.log(f"Tek Parça İşleniyor: {os.path.basename(path)}")
            
            base_dir = os.path.dirname(path)
            dxf_dir = os.path.join(base_dir, "DXF_BEM")
            step_dir = os.path.join(base_dir, "STEP_BEM")
            if self.chk_dxf.get() and not os.path.exists(dxf_dir): os.makedirs(dxf_dir)
            if self.chk_step.get() and not os.path.exists(step_dir): os.makedirs(step_dir)

            self.process_part(swApp, Model, (dxf_dir, step_dir), close_after=False)
            
            self.log("\nBİTTİ.")
            messagebox.showinfo("Bitti", "Tek parça tamamlandı.")

        except Exception as e: self.log(f"HATA: {e}")

    # --- 3. MONTAJ MODU ---
    def run_assembly_logic(self):
        pythoncom.CoInitialize()
        self.txt_log.delete("1.0", "end")
        try:
            swApp = self.get_sw_app()
            Model = swApp.ActiveDoc
            if not Model: self.log("Dosya yok!"); return

            doc_type = self.call_safe(Model, "GetType")
            if doc_type != swDocASSEMBLY:
                self.log("HATA: Bu mod sadece MONTAJ içindir."); return

            path = self.call_safe(Model, "GetPathName")
            base_dir = os.path.dirname(path) if path else os.path.expanduser("~/Desktop")
            
            dxf_dir = os.path.join(base_dir, "DXF_BEM")
            step_dir = os.path.join(base_dir, "STEP_BEM")
            if self.chk_dxf.get() and not os.path.exists(dxf_dir): os.makedirs(dxf_dir)
            if self.chk_step.get() and not os.path.exists(step_dir): os.makedirs(step_dir)

            comps = Model.GetComponents(False)
            self.log(f"Montaj Taranıyor: {len(comps)} bileşen...")
            self.log("NOT: DXF için parçalar arka planda açılıp kapatılacak.\n")

            processed_paths = [] 

            for i, comp in enumerate(comps):
                try:
                    if self.call_safe(comp, "GetSuppression") == 0: continue 
                    comp_path = self.call_safe(comp, "GetPathName")
                    
                    if comp_path and os.path.exists(comp_path) and comp_path.lower().endswith(".sldprt"):
                        if comp_path in processed_paths: continue 
                        
                        processed_paths.append(comp_path)
                        self.log(f"[{i+1}] {comp.Name2}")

                        res = self.open_doc_safe(swApp, comp_path)
                        part_doc = res[0] if isinstance(res, tuple) else res
                        
                        if part_doc:
                            self.process_part(swApp, part_doc, (dxf_dir, step_dir), close_after=True)
                        else:
                            self.log("   (Açılamadı)")
                            
                except: continue
            
            self.log("\nBİTTİ.")
            messagebox.showinfo("Bitti", "Montaj işlemi tamamlandı.")
        except Exception as e: self.log(f"GENEL HATA: {e}")

if __name__ == "__main__":
    app = BatchExporterApp()
    app.mainloop()