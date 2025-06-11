# GUI_xetnghiem.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import joblib
import os
import sys

def resource_path(relative_path):
    """Trả về đường dẫn phù hợp cả khi chạy script lẫn .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class XetNghiemFrame(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Load model và scaler với xử lý lỗi
        self.final_model = None
        self.scaler = None
        self.bg_photo = None
        
        self.load_models()
        self.load_background_image()
        
        # Xây dựng UI
        self.build_ui()

    def load_models(self):
        """Load model và scaler với xử lý lỗi"""
        try:
            model_path = resource_path("final_model.pkl")
            scaler_path = resource_path("scaler.pkl")
            
            if os.path.exists(model_path):
                self.final_model = joblib.load(model_path)
                print("Model loaded successfully")
            else:
                print(f"Warning: Model file not found at {model_path}")
                
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                print("Scaler loaded successfully")
            else:
                print(f"Warning: Scaler file not found at {scaler_path}")
                
        except Exception as e:
            print(f"Error loading models: {e}")
            self.final_model = None
            self.scaler = None

    def load_background_image(self):
        """Load ảnh nền với xử lý lỗi"""
        try:
            img_path = resource_path("nurst.png")
            
            if os.path.exists(img_path):
                self.bg_image = Image.open(img_path)
                print("Background image loaded successfully")
            else:
                print(f"Warning: Background image not found at {img_path}")
                # Tạo ảnh mặc định nếu không tìm thấy
                self.bg_image = Image.new('RGB', (280, 400), color='lightblue')
                
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Tạo ảnh mặc định nếu có lỗi
            self.bg_image = Image.new('RGB', (280, 400), color='lightblue')

    def build_ui(self):
        # Style chung
        style = ttk.Style()
        style.configure("TFrame", background="#f2f4f8")
        style.configure("TLabel", background="#f2f4f8", font=("Segoe UI", 12))
        style.configure("TEntry", font=("Segoe UI", 12), padding=5)
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=5)

        # Bố cục 2 cột: trái (ảnh + kết quả), phải (form nhập)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # --- CỘT TRÁI: Ảnh + Dòng kết quả ---
        left = ttk.Frame(self, style="TFrame", padding=10)
        left.grid(row=0, column=0, sticky="nsew")

        # resize giữ tỉ lệ với xử lý lỗi
        try:
            img_w, img_h = 280, 400
            resized = ImageOps.contain(self.bg_image, (img_w, img_h), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)
            ttk.Label(left, image=self.bg_photo).pack(pady=(10,5))
        except Exception as e:
            print(f"Error creating background photo: {e}")
            # Tạo label thay thế nếu không load được ảnh
            placeholder_label = ttk.Label(left, text="🏥\nHỆ THỐNG\nXÉT NGHIỆM", 
                                        font=("Segoe UI", 16, "bold"),
                                        foreground="#0d6efd")
            placeholder_label.pack(pady=(10,5))

        self.result_label = ttk.Label(left, text="", font=("Segoe UI", 12, "bold"),
                                      foreground="#dc3545", wraplength=250, justify="center")
        self.result_label.pack(pady=(0,20))

        # --- CỘT PHẢI: Form nhập liệu ---
        right = ttk.Frame(self, style="TFrame", padding=20)
        right.grid(row=0, column=1, sticky="nsew")

        ttk.Label(right, text="🧬 Dự đoán nhiễm trùng máu",
                  font=("Segoe UI", 16, "bold"), foreground="#0d6efd").grid(row=0, column=0, columnspan=2, pady=(0,20))

        self.entries = {}
        fields = [("PRG","prg"),("PL","pl"),("PR","pr"),("SK","sk"),
                  ("TS","ts"),("M11","m11"),("BD2","bd2"),("Tuổi","age"),("Bảo hiểm","insurance")]

        for i,(lab,key) in enumerate(fields, start=1):
            ttk.Label(right, text=f"{lab}:").grid(row=i, column=0, sticky="e", pady=5, padx=(0,10))
            ent = ttk.Entry(right, width=25)
            ent.grid(row=i, column=1, sticky="w", pady=5)
            self.entries[key] = ent

        ttk.Button(right, text="🔍 Chẩn đoán", command=self.classify_patient)\
           .grid(row=len(fields)+1, column=0, columnspan=2, pady=20)

        # Hiển thị trạng thái model
        if self.final_model is None or self.scaler is None:
            status_label = ttk.Label(right, text="⚠️ Model chưa được tải. Chức năng dự đoán không khả dụng.", 
                                   foreground="orange", font=("Segoe UI", 10))
            status_label.grid(row=len(fields)+2, column=0, columnspan=2, pady=5)

    def classify_patient(self):
        # Kiểm tra model có được load không
        if self.final_model is None or self.scaler is None:
            self.result_label.config(text="⚠️ Model không khả dụng!", foreground="orange")
            return
            
        try:
            # Kiểm tra tất cả các trường đã được nhập
            for key, entry in self.entries.items():
                if not entry.get().strip():
                    self.result_label.config(text=f"⚠️ Vui lòng nhập {key}!", foreground="orange")
                    return
            
            # Lấy dữ liệu từ các trường nhập
            data = []
            
            # Các trường số thực
            float_fields = ["prg","pl","pr","sk","ts","m11","bd2"]
            for key in float_fields:
                try:
                    value = float(self.entries[key].get())
                    data.append(value)
                except ValueError:
                    self.result_label.config(text=f"⚠️ {key} phải là số!", foreground="orange")
                    return
            
            # Các trường số nguyên
            int_fields = ["age", "insurance"]
            for key in int_fields:
                try:
                    value = int(self.entries[key].get())
                    data.append(value)
                except ValueError:
                    self.result_label.config(text=f"⚠️ {key} phải là số nguyên!", foreground="orange")
                    return
            
            # Thực hiện dự đoán
            scaled_data = self.scaler.transform([data])
            pred = self.final_model.predict(scaled_data)[0]
            
            if pred == 1:
                self.result_label.config(text="🛑 Có khả năng nhiễm trùng máu!", foreground="#dc3545")
            else:
                self.result_label.config(text="✅ Không có dấu hiệu nhiễm trùng máu.", foreground="#198754")
                
        except Exception as e:
            self.result_label.config(text=f"⚠️ Lỗi: {str(e)}", foreground="orange")
            print(f"Classification error: {e}")


# Hàm demo: khi chạy trực tiếp file này
def demo():
    root = tk.Tk()
    root.title("Demo Form Chính")
    root.geometry("900x600")
    root.configure(bg="#f2f4f8")

    # Ví dụ nhúng XetNghiemFrame vào khung chính
    frame = XetNghiemFrame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    demo()
