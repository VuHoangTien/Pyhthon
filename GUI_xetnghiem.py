# GUI_xetnghiem.py

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import joblib

class XetNghiemFrame(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Load model và scaler
        self.final_model = joblib.load("final_model.pkl")
        self.scaler = joblib.load("scaler.pkl")

        # Load ảnh nền
        self.bg_image = Image.open("nurst.png")

        # Xây dựng UI
        self.build_ui()

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

        # resize giữ tỉ lệ
        img_w, img_h = 280, 400
        resized = ImageOps.contain(self.bg_image, (img_w, img_h), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized)

        ttk.Label(left, image=self.bg_photo).pack(pady=(10,5))
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

    def classify_patient(self):
        try:
            data = [float(self.entries[k].get()) for k in
                    ["prg","pl","pr","sk","ts","m11","bd2"]]
            data += [int(self.entries["age"].get()), int(self.entries["insurance"].get())]
            pred = self.final_model.predict(self.scaler.transform([data]))[0]
            if pred==1:
                self.result_label.config(text="🛑 Có khả năng nhiễm trùng máu!", foreground="#dc3545")
            else:
                self.result_label.config(text="✅ Không có dấu hiệu nhiễm trùng máu.", foreground="#198754")
        except Exception as e:
            self.result_label.config(text=f"⚠️ Lỗi: {e}", foreground="orange")


# Hàm demo: khi chạy trực tiếp file này
def demo():
    root = tk.Tk()
    root.title("Demo Form Chính")
    root.geometry("900x600")

    # Ví dụ nhúng XetNghiemFrame vào khung chính
    frame = XetNghiemFrame(root)
    frame.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    demo()
