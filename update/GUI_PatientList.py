import os
import tkinter as tk
from tkinter import messagebox, filedialog
from customtkinter import CTkButton, CTkFrame, CTkScrollbar
from GUI_PatientDetail import PatientDetailGui
import json

class PatientListGui():
    def __init__(self, master, navigation_callback=None):
        self.master = master
        self.navigation_callback = navigation_callback
        self.setup_ui()

    def load_data_from_file(self):
        try:
            with open("patients.json", "r", encoding="utf-8") as f:
                self.patients_data = json.load(f)
        except FileNotFoundError:
            self.patients_data = []

    def save_data_to_file(self):
        try:
            with open("patients.json", "w", encoding="utf-8") as f:
                json.dump(self.patients_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)

    def setup_ui(self):
        # Header
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(10, 20))

        add_button = CTkButton(master=table_header, text="➕ Thêm bệnh nhân", width=150, height=35,
                               fg_color="#28a745", text_color="white", hover_color="#218838",
                               corner_radius=5, command=self.add_new_patient)
        add_button.pack(side=tk.RIGHT, pady=10)

        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
                                  fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                                  corner_radius=5, command=self.export_json)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        title_label = tk.Label(table_header, text="Danh sách bệnh nhân", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Container
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["ID", "Họ tên", "Ngày sinh", "Số điện thoại", "Thao tác"]
        header_widths = [80, 200, 150, 180, 200]

        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=1, minsize=width)

        for i, header in enumerate(headers):
            label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"),
                             bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="nsew")

        # Scrollable content
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
                                 width=12, corner_radius=6, fg_color="white", bg_color="white",
                                 button_color="#57a1f8", button_hover_color="#2b8ee0")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = CTkFrame(canvas, fg_color="white")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.load_data_from_file()

        for i, patient in enumerate(self.patients_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#d0e6ff"

            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)
            row_frame.pack(fill=tk.X, expand=True, pady=1)

            def on_enter(e, frame=row_frame):
                frame.configure(bg=hover_color)
                for w in frame.winfo_children():
                    if isinstance(w, (tk.Label, tk.Frame)):
                        w.configure(bg=hover_color)

            def on_leave(e, frame=row_frame, color=bg_color):
                frame.configure(bg=color)
                for w in frame.winfo_children():
                    if isinstance(w, (tk.Label, tk.Frame)):
                        w.configure(bg=color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)

            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=1, minsize=width)

            display_data = [patient.get("id", ""), patient.get("name", ""), patient.get("birth_date", ""), patient.get("phone", "")]
            for j, data in enumerate(display_data):
                label = tk.Label(row_frame, text=data, font=("Arial", 11),
                                 bg=bg_color, anchor="w")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="nsew")

            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=4, padx=5, pady=5)

            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                   fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda p=patient: self.view_patient_detail(p))
            detail_btn.pack(side=tk.LEFT, padx=2)

            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                   fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda p_id=patient.get('id'): self.delete_patient_by_id(p_id)) # Truyền ID thay vì đối tượng
            delete_btn.pack(side=tk.LEFT, padx=2)

        # Mousewheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def view_patient_detail(self, patient_data):
        if self.navigation_callback:
            self.navigation_callback('patient_detail', patient_data)
        else:
            self.open_patient_detail_window(patient_data)

    def add_new_patient(self):
        if self.navigation_callback:
            self.navigation_callback('patient_detail', None)
        else:
            self.open_patient_detail_window(None)

    def open_patient_detail_window(self, patient_data):
        # Đây là phương thức được sử dụng khi chạy độc lập hoặc khi navigation_callback không được thiết lập.
        # Trong môi trường tích hợp với GUI_Main, navigation_callback sẽ được ưu tiên.
        for widget in self.master.winfo_children():
            widget.destroy()
        detail_gui = PatientDetailGui(self.master, patient_data)
        detail_gui.pack(fill=tk.BOTH, expand=True)

    def delete_patient_by_id(self, patient_id):
        """Xóa bệnh nhân dựa trên ID của họ."""
        if not self.patients_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xóa.")
            return

        # Tìm bệnh nhân cần xóa để hiển thị tên trong thông báo xác nhận
        patient_name = "N/A"
        for p in self.patients_data:
            if p.get("id") == patient_id:
                patient_name = p.get("name", "Bệnh nhân không tên")
                break
        
        result = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa bệnh nhân '{patient_name}' (ID: {patient_id})?\nHành động này không thể hoàn tác!")
        if result:
            # Xóa bệnh nhân dựa trên ID
            self.patients_data = [p for p in self.patients_data if p.get("id") != patient_id]

            # Ghi lại vào file JSON
            self.save_data_to_file()

            # Cập nhật giao diện
            self.refresh_table()

            messagebox.showinfo("Thành công", f"Đã xóa bệnh nhân '{patient_name}' khỏi hệ thống.")


    def export_json(self):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Lưu file JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.patients_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Thành công", f"Đã lưu tại:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

    def refresh_table(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_ui()

    def set_navigation_callback(self, callback):
        self.navigation_callback = callback


# Chạy test độc lập
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách bệnh nhân")
    root.configure(bg="#f8f9fa")
    root.resizable(True, True)

    window_width = 1200
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    app = PatientListGui(content_frame)
    root.mainloop()