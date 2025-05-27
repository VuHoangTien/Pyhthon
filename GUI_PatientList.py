import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkScrollbar
from GUI_PatientDetail import PatientDetailGui

class PatientListGui():
    def __init__(self, master, navigation_callback=None):
        self.master = master  # Đây sẽ là content_frame từ GUI_Main
        self.navigation_callback = navigation_callback  # Callback để chuyển màn hình
        self.setup_ui()
 
    def setup_ui(self):
        # Chỉ tạo phần content, không tạo header và menu
        
        # Header của bảng với nút thêm
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(10, 20))

        # Nút thêm bệnh nhân
        add_button = CTkButton(master=table_header, text="➕ Thêm bệnh nhân", width=150, height=35, 
                            fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5,
                            command=self.add_new_patient)
        add_button.pack(side=tk.RIGHT, pady=10)

        # Nút xuất file Json
        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35, 
                            fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
                            command=self.export_json)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Tiêu đề căn giữa
        title_label = tk.Label(table_header, text="Danh sách bệnh nhân", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Frame chứa bảng với scrollbar
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Header của bảng
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["STT", "ID", "Họ tên", "Ngày sinh", "Số điện thoại", "Thao tác"]
        header_widths = [60, 120, 250, 180, 180, 200]

        # Cấu hình trọng số cho các cột
        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, (header, width) in enumerate(zip(headers, header_widths)):
            label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"), 
                            bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

        # Frame chứa Canvas và Scrollbar cho nội dung bảng
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        # Tạo Canvas và Scrollbar
        canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
                         width=12, corner_radius=6,
                         fg_color="white", bg_color="white",
                         button_color="#57a1f8", button_hover_color="#2b8ee0")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        scrollable_frame = CTkFrame(canvas, fg_color="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Data mẫu với thông tin đầy đủ hơn
        self.patients_data = [
            {
                'stt': 1, 'id': 'BN001', 'name': 'Nguyễn Văn A', 'birth_date': '15/03/1985', 'phone': '0901234567',
                'gender': 'Nam', 'email': 'nguyenvana@email.com', 'address': '123 Đường ABC, Q1, TP.HCM',
                'blood_type': 'A', 'height': '170', 'weight': '65', 'medical_history': 'Không có',
                'emergency_name': 'Nguyễn Thị B', 'relationship': 'Vợ', 'emergency_phone': '0912345678'
            },
            {
                'stt': 2, 'id': 'BN002', 'name': 'Trần Thị B', 'birth_date': '22/07/1990', 'phone': '0912345678',
                'gender': 'Nữ', 'email': 'tranthib@email.com', 'address': '456 Đường DEF, Q3, TP.HCM',
                'blood_type': 'B', 'height': '160', 'weight': '55', 'medical_history': 'Tiểu đường',
                'emergency_name': 'Trần Văn C', 'relationship': 'Chồng', 'emergency_phone': '0923456789'
            },
            {
                'stt': 3, 'id': 'BN003', 'name': 'Lê Văn C', 'birth_date': '10/12/1975', 'phone': '0923456789',
                'gender': 'Nam', 'email': 'levanc@email.com', 'address': '789 Đường GHI, Q7, TP.HCM',
                'blood_type': 'O', 'height': '175', 'weight': '70', 'medical_history': 'Cao huyết áp',
                'emergency_name': 'Lê Thị D', 'relationship': 'Vợ', 'emergency_phone': '0934567890'
            },
            {
                'stt': 4, 'id': 'BN004', 'name': 'Phạm Thị D', 'birth_date': '05/09/1988', 'phone': '0934567890',
                'gender': 'Nữ', 'email': 'phamthid@email.com', 'address': '321 Đường JKL, Q5, TP.HCM',
                'blood_type': 'AB', 'height': '165', 'weight': '58', 'medical_history': 'Dị ứng thuốc',
                'emergency_name': 'Phạm Văn E', 'relationship': 'Anh', 'emergency_phone': '0945678901'
            },
            {
                'stt': 5, 'id': 'BN005', 'name': 'Hoàng Văn E', 'birth_date': '18/01/1992', 'phone': '0945678901',
                'gender': 'Nam', 'email': 'hoangvane@email.com', 'address': '654 Đường MNO, Q10, TP.HCM',
                'blood_type': 'A', 'height': '168', 'weight': '62', 'medical_history': 'Không có',
                'emergency_name': 'Hoàng Thị F', 'relationship': 'Mẹ', 'emergency_phone': '0956789012'
            },
            {
                'stt': 6, 'id': 'BN006', 'name': 'Võ Thị F', 'birth_date': '25/06/1983', 'phone': '0956789012',
                'gender': 'Nữ', 'email': 'vothif@email.com', 'address': '789 Đường GHI, Q5, TP.HCM',
                'blood_type': 'B', 'height': '160', 'weight': '55', 'medical_history': 'Tiểu đường',
                'emergency_name': 'Võ Văn G', 'relationship': 'Anh trai', 'emergency_phone': '0911112233'
            },
            {
                'stt': 7, 'id': 'BN007', 'name': 'Đặng Văn G', 'birth_date': '12/11/1979', 'phone': '0967890123',
                'gender': 'Nam', 'email': 'dangvang@email.com', 'address': '321 Đường DEF, Q3, TP.HCM',
                'blood_type': 'O', 'height': '175', 'weight': '70', 'medical_history': 'Cao huyết áp',
                'emergency_name': 'Đặng Thị H', 'relationship': 'Vợ', 'emergency_phone': '0933334455'
            },
            {
                'stt': 8, 'id': 'BN008', 'name': 'Bùi Thị H', 'birth_date': '30/04/1995', 'phone': '0978901234',
                'gender': 'Nữ', 'email': 'buithih@email.com', 'address': '111 Đường ABC, Q2, TP.HCM',
                'blood_type': 'AB', 'height': '162', 'weight': '50', 'medical_history': 'Không có',
                'emergency_name': 'Bùi Văn I', 'relationship': 'Cha', 'emergency_phone': '0922223344'
            },
            {
                'stt': 9, 'id': 'BN009', 'name': 'Lê Thị J', 'birth_date': '09/08/1987', 'phone': '0981234567',
                'gender': 'Nữ', 'email': 'lethij@email.com', 'address': '222 Đường XYZ, Q7, TP.HCM',
                'blood_type': 'A', 'height': '158', 'weight': '48', 'medical_history': 'Hen suyễn',
                'emergency_name': 'Lê Văn K', 'relationship': 'Chồng', 'emergency_phone': '0976543210'
            },
            {
                'stt': 10, 'id': 'BN010', 'name': 'Trần Văn K', 'birth_date': '03/02/1990', 'phone': '0991122334',
                'gender': 'Nam', 'email': 'tranvank@email.com', 'address': '456 Đường UVW, Q1, TP.HCM',
                'blood_type': 'B', 'height': '170', 'weight': '68', 'medical_history': 'Không có',
                'emergency_name': 'Trần Thị L', 'relationship': 'Vợ', 'emergency_phone': '0966667788'
            },
            {
                'stt': 11, 'id': 'BN011', 'name': 'Ngô Thị L', 'birth_date': '20/10/1993', 'phone': '0902233445',
                'gender': 'Nữ', 'email': 'ngothil@email.com', 'address': '777 Đường STU, Q9, TP.HCM',
                'blood_type': 'O', 'height': '165', 'weight': '52', 'medical_history': 'Viêm gan B',
                'emergency_name': 'Ngô Văn M', 'relationship': 'Anh trai', 'emergency_phone': '0944445566'
            },
            {
                'stt': 12, 'id': 'BN012', 'name': 'Phạm Văn M', 'birth_date': '11/03/1980', 'phone': '0913344556',
                'gender': 'Nam', 'email': 'phamvanm@email.com', 'address': '888 Đường RST, Q11, TP.HCM',
                'blood_type': 'AB', 'height': '172', 'weight': '75', 'medical_history': 'Thận yếu',
                'emergency_name': 'Phạm Thị N', 'relationship': 'Vợ', 'emergency_phone': '0932223344'
            },
            {
                'stt': 13, 'id': 'BN013', 'name': 'Nguyễn Thị N', 'birth_date': '07/07/1985', 'phone': '0924455667',
                'gender': 'Nữ', 'email': 'nguyenthin@email.com', 'address': '999 Đường QRS, Q4, TP.HCM',
                'blood_type': 'A', 'height': '159', 'weight': '53', 'medical_history': 'Không có',
                'emergency_name': 'Nguyễn Văn O', 'relationship': 'Chồng', 'emergency_phone': '0955556677'
            },
            {
                'stt': 14, 'id': 'BN014', 'name': 'Trịnh Văn O', 'birth_date': '16/12/1991', 'phone': '0935566778',
                'gender': 'Nam', 'email': 'trinhvano@email.com', 'address': '100 Đường PQR, Q6, TP.HCM',
                'blood_type': 'B', 'height': '178', 'weight': '72', 'medical_history': 'Không có',
                'emergency_name': 'Trịnh Thị P', 'relationship': 'Chị gái', 'emergency_phone': '0988889999'
            },
            {
                'stt': 15, 'id': 'BN015', 'name': 'Nguyễn Văn Q', 'birth_date': '22/02/1988', 'phone': '0912345678',
                'gender': 'Nam', 'email': 'nguyenvanq@email.com', 'address': '123 Đường XYZ, Q1, TP.HCM',
                'blood_type': 'O', 'height': '180', 'weight': '75', 'medical_history': 'Không có',
                'emergency_name': 'Nguyễn Thị R', 'relationship': 'Vợ', 'emergency_phone': '0923456789'
            }

        ]

        # Tạo các dòng dữ liệu
        for i, patient in enumerate(self.patients_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#d0e6ff"  # Màu xanh nhạt khi hover

            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

            # Gán sự kiện hover
            def on_enter(e, frame=row_frame):
                frame.configure(bg=hover_color)
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=hover_color)
                    elif isinstance(widget, tk.Frame):
                        widget.configure(bg=hover_color)

            def on_leave(e, frame=row_frame, color=bg_color):
                frame.configure(bg=color)
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=color)
                    elif isinstance(widget, tk.Frame):
                        widget.configure(bg=color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            row_frame.pack(fill=tk.X)
            
            # Cấu hình trọng số cho các cột của mỗi dòng để khớp với header
            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            # Hiển thị thông tin bệnh nhân (chỉ hiển thị các trường cơ bản trong bảng)
            display_data = [patient['stt'], patient['id'], patient['name'], patient['birth_date'], patient['phone']]
            for j, (data, width) in enumerate(zip(display_data, header_widths[:-1])):
                label = tk.Label(row_frame, text=str(data), font=("Arial", 11), 
                                bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")
            
            # Frame chứa các nút thao tác
            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=len(display_data), padx=5, pady=5)
            
            # Nút xem chi tiết
            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                corner_radius=3, font=("Arial", 9),
                                command=lambda p=patient: self.view_patient_detail(p))
            detail_btn.pack(side=tk.LEFT, padx=2)
            
            # Nút xóa
            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                corner_radius=3, font=("Arial", 9),
                                command=lambda p=patient: self.delete_patient(p))
            delete_btn.pack(side=tk.LEFT, padx=2)

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def view_patient_detail(self, patient_data):
        """Xem chi tiết bệnh nhân"""
        if self.navigation_callback:
            # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
            self.navigation_callback('patient_detail', patient_data)
        else:
            # Mở trực tiếp (dành cho test độc lập)
            self.open_patient_detail_window(patient_data)

    def add_new_patient(self):
        """Thêm bệnh nhân mới"""
        if self.navigation_callback:
            # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
            self.navigation_callback('patient_detail', None)
        else:
            # Mở trực tiếp (dành cho test độc lập)
            self.open_patient_detail_window(None)

    def open_patient_detail_window(self, patient_data):
        """Mở cửa sổ chi tiết bệnh nhân (dành cho test độc lập)"""
        # Xóa nội dung hiện tại
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Tạo PatientDetailGui mới
        detail_gui = PatientDetailGui(self.master, patient_data)

    def delete_patient(self, patient_data):
        """Xóa bệnh nhân"""
        result = messagebox.askyesno("Xác nhận xóa", 
                                   f"Bạn có chắc chắn muốn xóa bệnh nhân '{patient_data['name']}'?\n"
                                   "Hành động này không thể hoàn tác!")
        
        if result:
            try:
                # Xóa khỏi danh sách
                self.patients_data.remove(patient_data)
                
                # Refresh giao diện
                self.refresh_table()
                
                messagebox.showinfo("Thành công", f"Đã xóa bệnh nhân '{patient_data['name']}' thành công!")
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa bệnh nhân: {str(e)}")

    def export_json(self):
        """Xuất dữ liệu ra file JSON"""
        try:
            import json
            from tkinter import filedialog
            
            # Chọn nơi lưu file
            file_path = filedialog.asksaveasfilename(
                title="Lưu file JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                # Xuất dữ liệu
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.patients_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def refresh_table(self):
        """Làm mới bảng dữ liệu"""
        # Xóa nội dung hiện tại và tạo lại
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_ui()

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback


# Test riêng biệt (chỉ dành cho development)
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

    # Test với frame content
    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Khởi tạo giao diện
    patient_list_gui = PatientListGui(content_frame)

    root.mainloop()