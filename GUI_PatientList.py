# GUI_PatientList.py
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
        self.patients_data = []
        self.load_data_from_file() # Load data before setting up UI
        self.setup_ui()


    def load_data_from_file(self):
        try:
            with open("patients.json", "r", encoding="utf-8") as f:
                self.patients_data = json.load(f)
        except FileNotFoundError:
            self.patients_data = []
        except json.JSONDecodeError:
            self.patients_data = [] # Handle empty or malformed JSON

    def save_data_to_file(self):
        try:
            with open("patients.json", "w", encoding="utf-8") as f:
                json.dump(self.patients_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)

    def setup_ui(self):
        # Clear existing widgets before setting up UI
        for widget in self.master.winfo_children():
            widget.destroy()

        # Header
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        add_button = CTkButton(master=table_header, text="➕ Thêm bệnh nhân", width=150, height=35,
                               fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5,
                               command=self.add_new_patient)
        add_button.pack(side=tk.RIGHT, pady=10)

        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
                                  fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
                                  command=self.export_json)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        title_label = tk.Label(table_header, text="Danh sách bệnh nhân", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Table container
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Header row
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["ID", "Họ tên", "Giới tính", "Số điện thoại", "Tiền sử bệnh án", "Thao tác"]
        header_widths = [80, 180, 100, 150, 200, 180] # Adjusted widths

        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, header in enumerate(headers):
            label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"),
                             bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

        # Scrollable area
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
                                 width=12, corner_radius=6,
                                 fg_color="white", bg_color="white",
                                 button_color="#57a1f8", button_hover_color="#2b8ee0")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = CTkFrame(canvas, fg_color="white")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.populate_table(scrollable_frame, header_widths)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def populate_table(self, scrollable_frame, header_widths):
        """Populates the table with patient data."""
        self.load_data_from_file() # Ensure the data is fresh when populating

        for i, patient in enumerate(self.patients_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#d0e6ff"

            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

            def on_enter(e, frame=row_frame):
                frame.configure(bg=hover_color)
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Frame)):
                        widget.configure(bg=hover_color)

            def on_leave(e, frame=row_frame, color=bg_color):
                frame.configure(bg=color)
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Frame)):
                        widget.configure(bg=color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            row_frame.pack(fill=tk.X)

            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            display_data = [
                patient.get("id", ""),
                patient.get("name", ""),
                patient.get("gender", ""),
                patient.get("phone", ""),
                patient.get("medical_history", "")
            ]

            for j, text in enumerate(display_data):
                label = tk.Label(row_frame, text=text, font=("Arial", 11),
                                 bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=5, padx=5, pady=5) # Column 5 for actions

            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                   fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda p=patient: self.view_patient_detail(p))
            detail_btn.pack(side=tk.LEFT, padx=2)

            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                   fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda p_id=patient.get('id'): self.delete_patient_by_id(p_id))
            delete_btn.pack(side=tk.LEFT, padx=2)

    def view_patient_detail(self, patient_data):
        if self.navigation_callback:
            # Pass all_patients_data and a refresh callback
            self.navigation_callback('patient_detail', patient_data, self.patients_data, self.refresh_table)
        else:
            self.open_patient_detail_window(patient_data)

    def add_new_patient(self):
        if self.navigation_callback:
            # Pass None for patient_data and all_patients_data for ID generation, plus refresh callback
            self.navigation_callback('patient_detail', None, self.patients_data, self.refresh_table)
        else:
            self.open_patient_detail_window(None)

    def open_patient_detail_window(self, patient_data):
        for widget in self.master.winfo_children():
            widget.destroy()
        # For standalone testing, pass a dummy all_patients_data or load it here
        detail_gui = PatientDetailGui(self.master, patient_data, all_patients_data=self.patients_data, save_callback=self.refresh_table)
        # In a real integrated app, you'd navigate without packing it directly
        # detail_gui.pack(fill=tk.BOTH, expand=True) # This line would be in the main app's navigation


    def delete_patient_by_id(self, patient_id):
        self.load_data_from_file() # Ensure data is fresh before deletion attempt

        if not self.patients_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xóa.")
            return

        patient_name = "N/A"
        for p in self.patients_data:
            if p.get("id") == patient_id:
                patient_name = p.get("name", "Bệnh nhân không tên")
                break

        result = messagebox.askyesno("Xác nhận",
                                     f"Bạn có chắc chắn muốn xóa bệnh nhân '{patient_name}' (ID: {patient_id})?\nHành động này không thể hoàn tác!")
        if result:
            self.patients_data = [p for p in self.patients_data if p.get("id") != patient_id]
            self.save_data_to_file()
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
        # Reload data and re-setup UI to reflect changes
        self.load_data_from_file()
        self.setup_ui()

    def set_navigation_callback(self, callback):
        self.navigation_callback = callback

# Test độc lập
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách bệnh nhân")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)

    window_width = 1100
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    # # Create a dummy patients.json for testing - REMOVED/COMMENTED OUT
    # # initial_patients_for_list = [
    # #     {'id': 'BN001', 'name': 'Nguyễn Văn A', 'birth_date': '15/03/1985', 'phone': '0901234567',
    # #      'gender': 'Nam', 'email': 'nguyenvana@email.com', 'address': '123 Đường ABC, Q1, TP.HCM',
    # #      'blood_type': 'A', 'height': '170', 'weight': '65', 'medical_history': 'Không có',
    # #      'emergency_name': 'Nguyễn Thị B', 'relationship': 'Vợ', 'emergency_phone': '0912345678', 'image_path': ''},
    # #     {'id': 'BN002', 'name': 'Lê Thị C', 'birth_date': '20/07/1990', 'phone': '0987654321',
    # #      'gender': 'Nữ', 'email': 'lethic@email.com', 'address': '456 Đường XYZ, Q2, TP.HCM',
    # #      'blood_type': 'B', 'height': '160', 'weight': '55', 'medical_history': 'Tiểu đường',
    # #      'emergency_name': 'Trần Văn D', 'relationship': 'Cha', 'emergency_phone': '0976543210', 'image_path': ''},
    # # ]
    # # with open("patients.json", "w", encoding="utf-8") as f:
    # #     json.dump(initial_patients_for_list, f, ensure_ascii=False, indent=2)

    app = PatientListGui(content_frame)
    root.mainloop()

    # # Clean up the dummy patients.json after testing - REMOVED/COMMENTED OUT
    # if os.path.exists("patients.json"):
    #     os.remove("patients.json")