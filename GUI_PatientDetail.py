# GUI_PatientDetail.py
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from customtkinter import CTkButton, CTkFrame, CTkEntry, CTkLabel, CTkComboBox
from datetime import datetime
import json
import re # Import regex module

class PatientDetailGui():
    def __init__(self, master, patient_data=None, navigation_callback=None, save_callback=None, all_patients_data=None):
        self.master = master  # Đây sẽ là content_frame từ GUI_Main
        self.patient_data = patient_data  # Dữ liệu bệnh nhân (None nếu thêm mới)
        self.navigation_callback = navigation_callback  # Callback để chuyển màn hình
        self.image_path = None
        self.photo_label = None
        self.is_editing = False if patient_data else True  # Nếu thêm mới thì mặc định là chế độ chỉnh sửa
        self.save_callback = save_callback
        self.patients_data = all_patients_data if all_patients_data is not None else [] # Dữ liệu tất cả bệnh nhân
        self.load_data_from_file()   # Tải dữ liệu tổng thể trước để có thể tạo ID
        self.setup_ui()
        self.load_patient_data() # Sau đó tải dữ liệu của patient cụ thể (nếu có) và thiết lập trạng thái form

        if not self.patient_data:  # If adding a new patient, generate ID
            self.patient_id_entry.configure(state="normal") # Temporarily enable to insert
            self.patient_id_entry.delete(0, tk.END)
            self.patient_id_entry.insert(0, self.generate_new_patient_id())
            self.patient_id_entry.configure(state="disabled") # Disable after inserting
            self.edit_button.configure(state="disabled") # Disable edit button for new patient
            self.delete_button.configure(state="disabled") # Disable delete button for new patient

    def setup_ui(self):
        # Header với tiêu đề và các nút chức năng
        header_frame = tk.Frame(self.master, bg="white", height=60)
        header_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

        # Nút quay lại
        back_button = CTkButton(master=header_frame, text="← Quay lại", width=100, height=35,
                            fg_color="#6c757d", text_color="white", hover_color="#5a6268",
                            corner_radius=5, command=self.go_back)
        back_button.pack(side=tk.LEFT, pady=10)

        # Các nút chức năng bên phải
        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side=tk.RIGHT, pady=10)

        # Nút lưu thông tin
        self.save_button = CTkButton(master=button_frame, text="💾 Lưu", width=100, height=35,
                            fg_color="#28a745", text_color="white", hover_color="#218838",
                            corner_radius=5, command=self.save_patient)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        # Nút sửa thông tin
        self.edit_button = CTkButton(master=button_frame, text="✏️ Sửa", width=100, height=35,
                            fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                            corner_radius=5, command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.RIGHT, padx=5)

        # Nút xóa thông tin
        self.delete_button = CTkButton(master=button_frame, text="🗑️ Xóa", width=100, height=35,
                            fg_color="#dc3545", text_color="white", hover_color="#c82333",
                            corner_radius=5, command=self.delete_patient)
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        # Tiêu đề căn giữa
        title_text = "Thêm bệnh nhân mới" if not self.patient_data else "Chi tiết bệnh nhân"
        title_label = tk.Label(header_frame, text=title_text, font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Container chính
        main_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Frame chứa toàn bộ nội dung với scroll
        scroll_container = tk.Frame(main_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas cho scroll
        canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Nội dung chính
        content_frame = tk.Frame(scrollable_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Phần hình ảnh (bên trái)
        left_frame = tk.Frame(content_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 30))

        # Khung hình ảnh 3x4
        photo_frame = CTkFrame(left_frame, width=240, height=320, border_width=2)
        photo_frame.pack(pady=10)
        photo_frame.pack_propagate(False) # Ngăn không cho frame co dãn theo nội dung

        # Label hiển thị hình ảnh
        self.photo_label = tk.Label(photo_frame, text="Chưa có ảnh\n📷", font=("Arial", 14),
                                   bg="#f8f9fa", fg="#6c757d", justify=tk.CENTER)
        self.photo_label.pack(fill=tk.BOTH, expand=True)

        # Nút chọn ảnh
        self.upload_button = CTkButton(master=left_frame, text="📁 Chọn ảnh", width=240, height=35,
                                      fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                      corner_radius=5, command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Phần thông tin (bên phải)
        right_frame = tk.Frame(content_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Tạo form thông tin
        self.create_patient_form(right_frame)

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)


    def create_patient_form(self, parent):
        # Thông tin cơ bản
        basic_info_frame = CTkFrame(parent, fg_color="#f8f9fa", border_width=1)
        basic_info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(basic_info_frame, text="THÔNG TIN CƠ BẢN", font=("Arial", 12, "bold"),
                bg="#f8f9fa").pack(pady=(10, 5))

        # Hàng 1: ID và Họ tên
        row1 = tk.Frame(basic_info_frame, bg="#f8f9fa")
        row1.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(row1, text="ID bệnh nhân:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.patient_id_entry = CTkEntry(row1, width=150, height=30)
        self.patient_id_entry.pack(side=tk.LEFT, padx=(10, 50))
        # Patient ID entry should be read-only for existing patient, managed by toggle_form_state

        tk.Label(row1, text="Họ và tên:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.fullname_entry = CTkEntry(row1, width=250, height=30)
        self.fullname_entry.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Ngày sinh và Giới tính
        row2 = tk.Frame(basic_info_frame, bg="#f8f9fa")
        row2.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(row2, text="Ngày sinh:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.birth_date_entry = CTkEntry(row2, width=150, height=30, placeholder_text="dd/mm/yyyy")
        self.birth_date_entry.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(row2, text="Giới tính:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.gender_combo = CTkComboBox(row2, values=["Nam", "Nữ", "Khác"], width=150, height=30)
        self.gender_combo.pack(side=tk.LEFT, padx=10)

        # Hàng 3: Số điện thoại và Email
        row3 = tk.Frame(basic_info_frame, bg="#f8f9fa")
        row3.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(row3, text="Số điện thoại:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.phone_entry = CTkEntry(row3, width=150, height=30)
        self.phone_entry.pack(side=tk.LEFT, padx=(10, 30))

        tk.Label(row3, text="Email:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.email_entry = CTkEntry(row3, width=250, height=30)
        self.email_entry.pack(side=tk.LEFT, padx=10)

        # Hàng 4: Địa chỉ
        row4 = tk.Frame(basic_info_frame, bg="#f8f9fa")
        row4.pack(fill=tk.X, padx=15, pady=(5, 15))

        tk.Label(row4, text="Địa chỉ:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.address_entry = CTkEntry(row4, width=500, height=30)
        self.address_entry.pack(side=tk.LEFT, padx=10)

        # Thông tin sức khỏe
        medical_info_frame = CTkFrame(parent, fg_color="#e8f4f8", border_width=1)
        medical_info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(medical_info_frame, text="THÔNG TIN SỨC KHỎE", font=("Arial", 12, "bold"),
                bg="#e8f4f8").pack(pady=(10, 5))

        # Hàng 1: Nhóm máu và Chiều cao
        med_row1 = tk.Frame(medical_info_frame, bg="#e8f4f8")
        med_row1.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(med_row1, text="Nhóm máu:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.blood_type_combo = CTkComboBox(med_row1, values=["A", "B", "AB", "O"], width=100, height=30)
        self.blood_type_combo.pack(side=tk.LEFT, padx=(10, 30))

        tk.Label(med_row1, text="Chiều cao (cm):", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.height_entry = CTkEntry(med_row1, width=100, height=30)
        self.height_entry.pack(side=tk.LEFT, padx=(10, 30))

        tk.Label(med_row1, text="Cân nặng (kg):", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.weight_entry = CTkEntry(med_row1, width=100, height=30)
        self.weight_entry.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Tiền sử bệnh án
        med_row2 = tk.Frame(medical_info_frame, bg="#e8f4f8")
        med_row2.pack(fill=tk.X, padx=15, pady=(5, 15))

        tk.Label(med_row2, text="Tiền sử bệnh án:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.medical_history_entry = CTkEntry(med_row2, width=500, height=30)
        self.medical_history_entry.pack(side=tk.LEFT, padx=10)

        # Thông tin liên hệ khẩn cấp
        emergency_info_frame = CTkFrame(parent, fg_color="#fff3cd", border_width=1)
        emergency_info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(emergency_info_frame, text="LIÊN HỆ KHẨN CẤP", font=("Arial", 12, "bold"),
                bg="#fff3cd").pack(pady=(10, 5))

        # Hàng 1: Tên người liên hệ khẩn cấp và Quan hệ
        emg_row1 = tk.Frame(emergency_info_frame, bg="#fff3cd")
        emg_row1.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(emg_row1, text="Tên người liên hệ:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
        self.emergency_name_entry = CTkEntry(emg_row1, width=250, height=30)
        self.emergency_name_entry.pack(side=tk.LEFT, padx=(10, 30))

        tk.Label(emg_row1, text="Quan hệ:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
        self.relationship_entry = CTkEntry(emg_row1, width=150, height=30)
        self.relationship_entry.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Số điện thoại khẩn cấp
        emg_row2 = tk.Frame(emergency_info_frame, bg="#fff3cd")
        emg_row2.pack(fill=tk.X, padx=15, pady=(5, 15))

        tk.Label(emg_row2, text="SĐT khẩn cấp:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
        self.emergency_phone_entry = CTkEntry(emg_row2, width=150, height=30)
        self.emergency_phone_entry.pack(side=tk.LEFT, padx=10)

        # Lưu tham chiếu đến các widget để có thể enable/disable
        self.form_widgets = [
            self.fullname_entry, self.birth_date_entry, self.gender_combo,
            self.phone_entry, self.email_entry, self.address_entry,
            self.blood_type_combo, self.height_entry, self.weight_entry,
            self.medical_history_entry, self.emergency_name_entry,
            self.relationship_entry, self.emergency_phone_entry
        ]

    def go_back(self):
        """Quay lại màn hình danh sách bệnh nhân"""
        if self.navigation_callback:
            self.navigation_callback('patient_list')
        else:
            self.back_to_patient_list()

    def back_to_patient_list(self):
        """Quay lại danh sách bệnh nhân (dành cho test độc lập)"""
        if self.is_editing and self.has_unsaved_changes():
            result = messagebox.askyesnocancel("Xác nhận",
                                             "Bạn có thay đổi chưa được lưu.\n"
                                             "Bạn có muốn lưu trước khi quay lại không?\n\n"
                                             "Nhấn 'Có' để lưu và quay lại\n"
                                             "Nhấn 'Không' để bỏ qua thay đổi\n"
                                             "Nhấn 'Hủy' để tiếp tục chỉnh sửa")

            if result is None:  # Cancel
                return
            elif result:  # Yes - Save
                if not self.save_patient(show_message=False):
                    return  # Lưu thất bại, không quay lại

        # Xóa nội dung hiện tại
        for widget in self.master.winfo_children():
            widget.destroy()

        # Import và tạo PatientListGui
        try:
            from GUI_PatientList import PatientListGui
            patient_list_gui = PatientListGui(self.master, self.navigation_callback)
        except ImportError:
            messagebox.showerror("Lỗi", "Không thể import GUI_PatientList!")

    def has_unsaved_changes(self):
        """Kiểm tra xem có thay đổi chưa lưu không"""
        current_data = self.get_current_form_data()
        if not self.patient_data: # New patient
            # Check if any main fields are filled
            return any(current_data[key].strip() for key in ['id', 'name', 'phone'])
        else: # Existing patient
            # Compare current data with original patient_data
            for key in current_data:
                if key == 'image_path':
                    if current_data['image_path'] != self.patient_data.get('image_path', ''):
                        return True
                elif current_data[key].strip() != self.patient_data.get(key, '').strip():
                    return True
            return False

    def upload_image(self):
        if not self.is_editing:
            messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để thay đổi hình ảnh!")
            return

        file_path = filedialog.askopenfilename(
            title="Chọn ảnh bệnh nhân",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )

        if file_path:
            try:
                # Mở và resize ảnh về tỷ lệ 3:4
                image = Image.open(file_path)
                image = image.resize((220, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                # Hiển thị ảnh
                self.photo_label.configure(image=photo, text="")
                self.photo_label.image = photo  # Giữ reference
                self.image_path = file_path

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")

    def load_data_from_file(self):
        """Tải toàn bộ dữ liệu bệnh nhân từ file JSON."""
        try:
            with open("patients.json", "r", encoding="utf-8") as f:
                self.patients_data = json.load(f)
        except FileNotFoundError:
            self.patients_data = []
        except json.JSONDecodeError:
            self.patients_data = [] # Handle empty or malformed JSON

    def save_data_to_file(self):
        """Ghi toàn bộ dữ liệu bệnh nhân vào file JSON."""
        try:
            with open("patients.json", "w", encoding="utf-8") as f:
                json.dump(self.patients_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi ghi file: {e}")

    def load_patient_data(self):
        """Tải dữ liệu bệnh nhân cụ thể nếu có và điền vào form."""
        if self.patient_data:
            # Điền dữ liệu vào form
            self.patient_id_entry.insert(0, self.patient_data.get('id', ''))
            self.fullname_entry.insert(0, self.patient_data.get('name', ''))
            self.birth_date_entry.insert(0, self.patient_data.get('birth_date', ''))
            self.gender_combo.set(self.patient_data.get('gender', ''))
            self.phone_entry.insert(0, self.patient_data.get('phone', ''))
            self.email_entry.insert(0, self.patient_data.get('email', ''))
            self.address_entry.insert(0, self.patient_data.get('address', ''))
            self.blood_type_combo.set(self.patient_data.get('blood_type', ''))
            self.height_entry.insert(0, self.patient_data.get('height', ''))
            self.weight_entry.insert(0, self.patient_data.get('weight', ''))
            self.medical_history_entry.insert(0, self.patient_data.get('medical_history', ''))
            self.emergency_name_entry.insert(0, self.patient_data.get('emergency_name', ''))
            self.relationship_entry.insert(0, self.patient_data.get('relationship', ''))
            self.emergency_phone_entry.insert(0, self.patient_data.get('emergency_phone', ''))

            # Tải ảnh nếu có
            if 'image_path' in self.patient_data and self.patient_data['image_path'] and os.path.exists(self.patient_data['image_path']):
                try:
                    image = Image.open(self.patient_data['image_path'])
                    image = image.resize((220, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.photo_label.configure(image=photo, text="")
                    self.photo_label.image = photo
                    self.image_path = self.patient_data['image_path']
                except Exception as e:
                    print(f"Error loading image: {e}")
                    pass  # Không load được ảnh, giữ nguyên placeholder
            else:
                self.image_path = None # Reset image path if file does not exist

        # Thiết lập trạng thái ban đầu
        self.toggle_form_state()

    def toggle_edit_mode(self):
        """Chuyển đổi giữa chế độ xem và chỉnh sửa"""
        self.is_editing = not self.is_editing
        self.toggle_form_state()

    def toggle_form_state(self):
        """Bật/tắt khả năng chỉnh sửa form"""
        state = "normal" if self.is_editing else "disabled"

        for widget in self.form_widgets:
            if hasattr(widget, 'configure'):
                widget.configure(state=state)

        # Patient ID is always disabled for manual input
        self.patient_id_entry.configure(state="disabled")

        # Cập nhật text của nút edit
        if self.is_editing:
            self.edit_button.configure(text="📖 Xem")
            self.save_button.configure(state="normal")
            self.upload_button.configure(state="normal")
        else:
            self.edit_button.configure(text="✏️ Sửa")
            self.save_button.configure(state="disabled")
            self.upload_button.configure(state="disabled")

    def generate_new_patient_id(self):
        """Sinh ID bệnh nhân tự động dạng BNxxx"""
        self.load_data_from_file() # Ensure self.patients_data is up-to-date
        existing_ids = [p["id"] for p in self.patients_data if "id" in p]

        max_number = 0
        for id_str in existing_ids:
            if id_str.startswith("BN") and id_str[2:].isdigit():
                max_number = max(max_number, int(id_str[2:]))

        new_number = max_number + 1
        return f"BN{new_number:03d}"

    def get_current_form_data(self):
        return {
            'id': self.patient_id_entry.get().strip(),
            'name': self.fullname_entry.get().strip(),
            'birth_date': self.birth_date_entry.get().strip(),
            'gender': self.gender_combo.get(),
            'phone': self.phone_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'address': self.address_entry.get().strip(),
            'blood_type': self.blood_type_combo.get(),
            'height': self.height_entry.get().strip(),
            'weight': self.weight_entry.get().strip(),
            'medical_history': self.medical_history_entry.get().strip(),
            'emergency_name': self.emergency_name_entry.get().strip(),
            'relationship': self.relationship_entry.get().strip(),
            'emergency_phone': self.emergency_phone_entry.get().strip(),
            'image_path': self.image_path
        }

    def validate_input(self, patient_info, show_message=True):
        """Validate all input fields."""

        # Full Name validation
        if not patient_info['name']:
            if show_message: messagebox.showerror("Lỗi", "Vui lòng nhập Họ và tên bệnh nhân!")
            return False
        if not all(c.isalpha() or c.isspace() for c in patient_info['name']):
            if show_message:
                messagebox.showerror("Lỗi", "Tên bệnh nhân chỉ được chứa chữ cái và khoảng trắng!")
            return False

        # Birth Date validation (dd/mm/yyyy)
        if patient_info['birth_date']:
            try:
                datetime.strptime(patient_info['birth_date'], '%d/%m/%Y')
            except ValueError:
                if show_message: messagebox.showerror("Lỗi", "Ngày sinh không đúng định dạng. Vui lòng nhập theo dd/mm/yyyy!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập ngày sinh.")

        # Phone number validation (10 digits)
        if not patient_info['phone']:
            if show_message: messagebox.showerror("Lỗi", "Vui lòng nhập số điện thoại!")
            return False
        if not re.fullmatch(r"^\d{10}$", patient_info['phone']):
            if show_message: messagebox.showerror("Lỗi", "Số điện thoại phải có đúng 10 chữ số!")
            return False

        # Email validation
        if patient_info['email']:
            if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", patient_info['email']):
                if show_message: messagebox.showerror("Lỗi", "Địa chỉ email không hợp lệ!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập email.")

        # Address validation
        if not patient_info['address']:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập địa chỉ.")

        # Height validation (numeric, optional)
        if patient_info['height']:
            try:
                height_value = float(patient_info['height'])
                if height_value <= 0:
                    if show_message: messagebox.showerror("Lỗi", "Chiều cao phải là số dương!")
                    return False
            except ValueError:
                if show_message: messagebox.showerror("Lỗi", "Chiều cao phải là một số!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập chiều cao.")

        # Weight validation (numeric, optional)
        if patient_info['weight']:
            try:
                weight_value = float(patient_info['weight'])
                if weight_value <= 0:
                    if show_message: messagebox.showerror("Lỗi", "Cân nặng phải là số dương!")
                    return False
            except ValueError:
                if show_message: messagebox.showerror("Lỗi", "Cân nặng phải là một số!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập cân nặng.")

        # Emergency Contact Name
        if not patient_info['emergency_name']:
            if show_message: messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên người liên hệ khẩn cấp.")
        
        # Emergency Phone
        if not patient_info['emergency_phone']:
            if show_message: messagebox.showwarning("Cảnh báo", "Vui lòng nhập số điện thoại khẩn cấp.")
        elif not re.fullmatch(r"^\d{10}$", patient_info['emergency_phone']):
            if show_message: messagebox.showerror("Lỗi", "Số điện thoại khẩn cấp phải có đúng 10 chữ số!")
            return False


        return True

    def save_patient(self, show_message=True):
        """Lưu thông tin bệnh nhân"""
        if not self.is_editing:
            if show_message:
                messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để chỉnh sửa thông tin!")
            return False

        patient_info = self.get_current_form_data()

        # Validate data
        if not self.validate_input(patient_info, show_message):
            return False

        # Check for duplicate ID if adding a new patient (should be handled by auto-gen, but good for robustness)
        if not self.patient_data: # Only check for new patient
            if any(p['id'] == patient_info['id'] for p in self.patients_data):
                if show_message:
                    messagebox.showerror("Lỗi", "ID bệnh nhân đã tồn tại. Vui lòng thử lại hoặc liên hệ quản trị.")
                return False

        # Update self.patients_data (danh sách bệnh nhân)
        found_existing = False
        for i, p in enumerate(self.patients_data):
            if p['id'] == patient_info['id']:
                self.patients_data[i] = patient_info
                found_existing = True
                break

        if not found_existing:
            # If it's a new patient, add to the list
            self.patients_data.append(patient_info)

        # Ghi file JSON
        self.save_data_to_file()

        # Cập nhật dữ liệu hiện tại
        self.patient_data = patient_info

        if show_message:
            messagebox.showinfo("Thành công", "Đã lưu thông tin bệnh nhân thành công!")

        # Trở lại chế độ xem
        self.is_editing = False
        self.toggle_form_state()

        if self.save_callback: # Notify the parent (PatientListGui) to refresh
            self.save_callback()

        return True

    def delete_patient(self):
        """Xóa bệnh nhân"""
        if not self.patient_data:
            messagebox.showwarning("Cảnh báo", "Không thể xóa bệnh nhân mới chưa được lưu!")
            return

        result = messagebox.askyesno("Xác nhận",
                                   "Bạn có chắc chắn muốn xóa thông tin bệnh nhân này?\n"
                                   "Hành động này không thể hoàn tác!")

        if result:
            patient_id = self.patient_data.get("id")
            if not patient_id:
                messagebox.showerror("Lỗi", "Không tìm thấy ID bệnh nhân để xóa.")
                return

            # Xóa khỏi danh sách self.patients_data
            self.patients_data = [p for p in self.patients_data if p.get("id") != patient_id]

            # Ghi lại vào file JSON
            self.save_data_to_file()

            # Thông báo
            messagebox.showinfo("Thành công", f"Đã xóa bệnh nhân ID: {patient_id} khỏi hệ thống.")

            # Quay lại danh sách sau khi xóa
            self.go_back()

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback


# Test riêng biệt (chỉ dành cho development)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Chi tiết bệnh nhân")
    root.configure(bg="#f8f9fa")
    root.resizable(True, True)

    window_width = 1000
    window_height = 800
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    # # Example patients_data for testing ID generation and existence - REMOVED/COMMENTED OUT
    # initial_patients = [
    #     {'id': 'BN001', 'name': 'Nguyễn Văn A', 'birth_date': '15/03/1985', 'phone': '0901234567',
    #      'gender': 'Nam', 'email': 'nguyenvana@email.com', 'address': '123 Đường ABC, Q1, TP.HCM',
    #      'blood_type': 'A', 'height': '170', 'weight': '65', 'medical_history': 'Không có',
    #      'emergency_name': 'Nguyễn Thị B', 'relationship': 'Vợ', 'emergency_phone': '0912345678', 'image_path': ''},
    #     {'id': 'BN002', 'name': 'Lê Thị C', 'birth_date': '20/07/1990', 'phone': '0987654321',
    #      'gender': 'Nữ', 'email': 'lethic@email.com', 'address': '456 Đường XYZ, Q2, TP.HCM',
    #      'blood_type': 'B', 'height': '160', 'weight': '55', 'medical_history': 'Tiểu đường',
    #      'emergency_name': 'Trần Văn D', 'relationship': 'Cha', 'emergency_phone': '0976543210', 'image_path': ''},
    # ]

    # # Create a dummy patients.json for testing - REMOVED/COMMENTED OUT
    # with open("patients.json", "w", encoding="utf-8") as f:
    #     json.dump(initial_patients, f, ensure_ascii=False, indent=2)

    # Test data for an existing patient (can still be used if you want to explicitly load one for testing)
    # This data should ideally come from your patients.json if it exists
    test_patient = {
        'id': 'BN001', 'name': 'Nguyễn Văn Thanh', 'birth_date': '15/03/1985', 'phone': '0901234567',
        'gender': 'Nam', 'email': 'nguyenvana@email.com', 'address': '123 Đường ABC, Q1, TP.HCM',
        'blood_type': 'A', 'height': '170', 'weight': '65', 'medical_history': 'Không có',
        'emergency_name': 'Nguyễn Thị B', 'relationship': 'Vợ', 'emergency_phone': '0912345678',
        'image_path': '' # Add image_path to the test patient data
    }

    # Load all patient data to simulate the main app's behavior
    all_patient_data_from_file = []
    try:
        with open("patients.json", "r", encoding="utf-8") as f:
            all_patient_data_from_file = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_patient_data_from_file = [] # Handle if file doesn't exist or is empty/corrupt

    # Khởi tạo giao diện (test với dữ liệu có sẵn hoặc tạo mới)
    # To test adding new patient, pass patient_data=None
    # patient_detail_gui = PatientDetailGui(content_frame, patient_data=None, all_patients_data=all_patient_data_from_file)
    # To test editing existing patient, pass test_patient (ensure it's in all_patients_data_from_file)
    patient_detail_gui = PatientDetailGui(content_frame, patient_data=test_patient, all_patients_data=all_patient_data_from_file)

    root.mainloop()

    # # Clean up the dummy patients.json after testing - REMOVED/COMMENTED OUT
    # if os.path.exists("patients.json"):
    #     os.remove("patients.json")