# GUI_StaffDetail.py
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from customtkinter import CTkButton, CTkFrame, CTkEntry, CTkLabel, CTkComboBox
from datetime import datetime
import json
import re

class StaffDetailGui():
    def __init__(self, master, staff_data=None, navigation_callback=None, save_callback=None, all_staffs_data=None):
        self.master = master
        self.staff_data = staff_data
        self.navigation_callback = navigation_callback
        self.image_path = None
        self.photo_label = None
        self.is_editing = False if staff_data else True
        self.save_callback = save_callback
        self.staffs_data = all_staffs_data if all_staffs_data is not None else [] # Dữ liệu tất cả nhân viên

        self.setup_ui()
        self.load_data_staff_from_file() # Tải dữ liệu tổng thể trước để có thể tạo ID
        self.load_staff_data() # Sau đó tải dữ liệu của staff cụ thể (nếu có) và thiết lập trạng thái form

        if not self.staff_data:  # If adding a new staff, generate ID
            self.staff_id_entry.configure(state="normal") # Temporarily enable to insert
            self.staff_id_entry.delete(0, tk.END)
            self.staff_id_entry.insert(0, self.generate_new_staff_id())
            self.staff_id_entry.configure(state="disabled") # Disable after inserting
            self.edit_button.configure(state="disabled") # Disable edit button for new staff
            self.delete_button.configure(state="disabled") # Disable delete button for new staff

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
                            corner_radius=5, command=self.save_staff)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        # Nút sửa thông tin
        self.edit_button = CTkButton(master=button_frame, text="✏️ Sửa", width=100, height=35,
                            fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                            corner_radius=5, command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.RIGHT, padx=5)

        # Nút xóa thông tin
        self.delete_button = CTkButton(master=button_frame, text="🗑️ Xóa", width=100, height=35,
                            fg_color="#dc3545", text_color="white", hover_color="#c82333",
                            corner_radius=5, command=self.delete_staff)
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        # Tiêu đề căn giữa
        title_text = "Thêm nhân viên mới" if not self.staff_data else "Chi tiết nhân viên"
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
        photo_frame.pack_propagate(False)

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
        self.create_staff_form(right_frame)

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_staff_form(self, parent):
        # Thông tin cơ bản
        basic_info_frame = CTkFrame(parent, fg_color="#f8f9fa", border_width=1)
        basic_info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(basic_info_frame, text="THÔNG TIN CƠ BẢN", font=("Arial", 12, "bold"),
                bg="#f8f9fa").pack(pady=(10, 5))

        # Hàng 1: ID và Họ tên
        row1 = tk.Frame(basic_info_frame, bg="#f8f9fa")
        row1.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(row1, text="ID nhân viên:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
        self.staff_id_entry = CTkEntry(row1, width=150, height=30)
        self.staff_id_entry.pack(side=tk.LEFT, padx=(10, 50))
        # ID entry should be read-only for existing staff, managed by toggle_form_state

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

        # Thông tin công việc
        work_info_frame = CTkFrame(parent, fg_color="#e8f4f8", border_width=1)
        work_info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(work_info_frame, text="THÔNG TIN CÔNG VIỆC", font=("Arial", 12, "bold"),
                bg="#e8f4f8").pack(pady=(10, 5))

        # Hàng 1: Chức vụ và Phòng ban
        work_row1 = tk.Frame(work_info_frame, bg="#e8f4f8")
        work_row1.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(work_row1, text="Chức vụ:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.position_entry = CTkEntry(work_row1, width=200, height=30)
        self.position_entry.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(work_row1, text="Phòng ban:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.department_entry = CTkEntry(work_row1, width=200, height=30)
        self.department_entry.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Ngày bắt đầu làm việc và Lương
        work_row2 = tk.Frame(work_info_frame, bg="#e8f4f8")
        work_row2.pack(fill=tk.X, padx=15, pady=(5, 15))

        tk.Label(work_row2, text="Ngày bắt đầu:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.start_date_entry = CTkEntry(work_row2, width=150, height=30, placeholder_text="dd/mm/yyyy")
        self.start_date_entry.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(work_row2, text="Lương:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.salary_entry = CTkEntry(work_row2, width=150, height=30)
        self.salary_entry.pack(side=tk.LEFT, padx=10)

        # Lưu tham chiếu đến các widget để có thể enable/disable
        self.form_widgets = [
            self.fullname_entry, self.birth_date_entry, self.gender_combo,
            self.phone_entry, self.email_entry, self.address_entry,
            self.position_entry, self.department_entry, self.start_date_entry, self.salary_entry
        ]

    def go_back(self):
        """Quay lại màn hình danh sách nhân viên"""
        if self.navigation_callback:
            # Sử dụng callback để chuyển về màn hình danh sách
            self.navigation_callback('staff_list')
        else:
            # Quay lại trực tiếp (dành cho test độc lập)
            self.back_to_staff_list()

    def back_to_staff_list(self):
        """Quay lại danh sách nhân viên (dành cho test độc lập)"""
        # Kiểm tra nếu có thay đổi chưa lưu
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
                if not self.save_staff(show_message=False):
                    return  # Lưu thất bại, không quay lại

        # Xóa nội dung hiện tại
        for widget in self.master.winfo_children():
            widget.destroy()

        # Import và tạo StaffListGui
        try:
            from GUI_StaffList import StaffListGui
            staff_list_gui = StaffListGui(self.master, self.navigation_callback)
        except ImportError:
            messagebox.showerror("Lỗi", "Không thể import GUI_StaffList!")

    def has_unsaved_changes(self):
        """Kiểm tra xem có thay đổi chưa lưu không"""
        current_data = self.get_current_form_data()
        if not self.staff_data: # New staff
            # Check if any main fields are filled
            return any(current_data[key].strip() for key in ['id', 'name', 'phone'])
        else: # Existing staff
            # Compare current data with original staff_data
            for key in current_data:
                if key == 'image_path':
                    if current_data['image_path'] != self.staff_data.get('image_path', ''):
                        return True
                elif current_data[key].strip() != self.staff_data.get(key, '').strip():
                    return True
            return False

    def upload_image(self):
        if not self.is_editing:
            messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để thay đổi hình ảnh!")
            return

        file_path = filedialog.askopenfilename(
            title="Chọn ảnh nhân viên",
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

    def load_data_staff_from_file(self):
        """Tải toàn bộ dữ liệu nhân viên từ file JSON."""
        try:
            with open("staffs.json", "r", encoding="utf-8") as f:
                self.staffs_data = json.load(f)
        except FileNotFoundError:
            self.staffs_data = []
        except json.JSONDecodeError:
            self.staffs_data = [] # Handle empty or malformed JSON

    def save_data_staff_to_file(self):
        """Ghi toàn bộ dữ liệu nhân viên vào file JSON."""
        try:
            with open("staffs.json", "w", encoding="utf-8") as f:
                json.dump(self.staffs_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi ghi file: {e}")

    def load_staff_data(self):
        """Tải dữ liệu nhân viên cụ thể nếu có và điền vào form."""
        if self.staff_data:
            # Điền dữ liệu vào form
            self.staff_id_entry.insert(0, self.staff_data.get('id', ''))
            self.fullname_entry.insert(0, self.staff_data.get('name', ''))
            self.birth_date_entry.insert(0, self.staff_data.get('birth_date', ''))
            self.gender_combo.set(self.staff_data.get('gender', ''))
            self.phone_entry.insert(0, self.staff_data.get('phone', ''))
            self.email_entry.insert(0, self.staff_data.get('email', ''))
            self.address_entry.insert(0, self.staff_data.get('address', ''))
            self.position_entry.insert(0, self.staff_data.get('position', ''))
            self.department_entry.insert(0, self.staff_data.get('department', ''))
            self.start_date_entry.insert(0, self.staff_data.get('start_date', ''))
            self.salary_entry.insert(0, self.staff_data.get('salary', ''))

            # Tải ảnh nếu có
            if 'image_path' in self.staff_data and self.staff_data['image_path'] and os.path.exists(self.staff_data['image_path']):
                try:
                    image = Image.open(self.staff_data['image_path'])
                    image = image.resize((220, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.photo_label.configure(image=photo, text="")
                    self.photo_label.image = photo
                    self.image_path = self.staff_data['image_path']
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

        # Staff ID is always disabled for manual input
        self.staff_id_entry.configure(state="disabled")

        # Cập nhật text của nút edit
        if self.is_editing:
            self.edit_button.configure(text="📖 Xem")
            self.save_button.configure(state="normal")
            self.upload_button.configure(state="normal")
        else:
            self.edit_button.configure(text="✏️ Sửa")
            self.save_button.configure(state="disabled")
            self.upload_button.configure(state="disabled")

    def generate_new_staff_id(self):
        """Sinh ID nhân viên tự động dạng NVxxx"""
        self.load_data_staff_from_file() # Ensure self.staffs_data is up-to-date
        existing_ids = [s["id"] for s in self.staffs_data if "id" in s]

        max_number = 0
        for id_str in existing_ids:
            if id_str.startswith("NV") and id_str[2:].isdigit():
                max_number = max(max_number, int(id_str[2:]))

        new_number = max_number + 1
        return f"NV{new_number:03d}"

    def get_current_form_data(self):
        return {
            'id': self.staff_id_entry.get().strip(),
            'name': self.fullname_entry.get().strip(),
            'birth_date': self.birth_date_entry.get().strip(),
            'gender': self.gender_combo.get(),
            'phone': self.phone_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'address': self.address_entry.get().strip(),
            'position': self.position_entry.get().strip(),
            'department': self.department_entry.get().strip(),
            'start_date': self.start_date_entry.get().strip(),
            'salary': self.salary_entry.get().strip(),
            'image_path': self.image_path
        }

    def validate_input(self, staff_info, show_message=True):
        """Validate all input fields."""

        # Full Name validation
        if not staff_info['name']:
            if show_message: messagebox.showerror("Lỗi", "Vui lòng nhập Họ và tên nhân viên!")
            return False
        if not all(c.isalpha() or c.isspace() for c in staff_info['name']):
            if show_message:
                messagebox.showerror("Lỗi", "Tên bệnh nhân chỉ được chứa chữ cái và khoảng trắng!")
            return False


        # Birth Date validation (dd/mm/yyyy)
        if staff_info['birth_date']:
            try:
                datetime.strptime(staff_info['birth_date'], '%d/%m/%Y')
            except ValueError:
                if show_message: messagebox.showerror("Lỗi", "Ngày sinh không đúng định dạng. Vui lòng nhập theo dd/mm/yyyy!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập ngày sinh.")

        # Phone number validation (10 digits)
        if not staff_info['phone']:
            if show_message: messagebox.showerror("Lỗi", "Vui lòng nhập số điện thoại!")
            return False
        if not re.fullmatch(r"^\d{10}$", staff_info['phone']):
            if show_message: messagebox.showerror("Lỗi", "Số điện thoại phải có đúng 10 chữ số!")
            return False

        # Email validation
        if staff_info['email']:
            if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", staff_info['email']):
                if show_message: messagebox.showerror("Lỗi", "Địa chỉ email không hợp lệ!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập email.")

        # Address validation
        if not staff_info['address']:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập địa chỉ.")

        # Position validation
        if not staff_info['position']:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập chức vụ.")
        
        # Department validation
        if not staff_info['department']:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập phòng ban.")

        # Start Date validation (dd/mm/yyyy)
        if staff_info['start_date']:
            try:
                datetime.strptime(staff_info['start_date'], '%d/%m/%Y')
            except ValueError:
                if show_message: messagebox.showerror("Lỗi", "Ngày bắt đầu làm việc không đúng định dạng. Vui lòng nhập theo dd/mm/yyyy!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập ngày bắt đầu làm việc.")

        # Salary validation (numeric, optional but recommended)
        if staff_info['salary']:
            try:
                salary_value = float(staff_info['salary'])
                if salary_value < 0:
                    if show_message: messagebox.showerror("Lỗi", "Lương không thể là số âm!")
                    return False
            except ValueError:
                if show_message: messagebox.showerror("Lỗi", "Lương phải là một số!")
                return False
        else:
            if show_message: messagebox.showwarning("Cảnh báo", "Bạn chưa nhập lương.")

        return True

    def save_staff(self, show_message=True):
        """Lưu thông tin nhân viên"""
        if not self.is_editing:
            if show_message:
                messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để chỉnh sửa thông tin!")
            return False

        staff_info = self.get_current_form_data()

        # Validate data
        if not self.validate_input(staff_info, show_message):
            return False

        # Check for duplicate ID if adding a new staff (should be handled by auto-gen, but good for robustness)
        if not self.staff_data: # Only check for new staff
            if any(s['id'] == staff_info['id'] for s in self.staffs_data):
                if show_message:
                    messagebox.showerror("Lỗi", "ID nhân viên đã tồn tại. Vui lòng thử lại hoặc liên hệ quản trị.")
                return False

        # Update self.staffs_data (danh sách nhân viên)
        found_existing = False
        for i, s in enumerate(self.staffs_data):
            if s['id'] == staff_info['id']:
                self.staffs_data[i] = staff_info
                found_existing = True
                break

        if not found_existing:
            # If it's a new staff, add to the list
            self.staffs_data.append(staff_info)

        # Ghi file JSON
        self.save_data_staff_to_file()

        # Cập nhật dữ liệu hiện tại
        self.staff_data = staff_info

        if show_message:
            messagebox.showinfo("Thành công", "Đã lưu thông tin nhân viên thành công!")

        # Trở lại chế độ xem
        self.is_editing = False
        self.toggle_form_state()

        if self.save_callback: # Notify the parent (StaffListGui) to refresh
            self.save_callback()

        return True

    def delete_staff(self):
        """Xóa nhân viên"""
        if not self.staff_data:
            messagebox.showwarning("Cảnh báo", "Không thể xóa nhân viên mới chưa được lưu!")
            return

        result = messagebox.askyesno("Xác nhận",
                                   "Bạn có chắc chắn muốn xóa thông tin nhân viên này?\n"
                                   "Hành động này không thể hoàn tác!")

        if result:
            staff_id = self.staff_data.get("id")
            if not staff_id:
                messagebox.showerror("Lỗi", "Không tìm thấy ID nhân viên để xóa.")
                return

            # Xóa khỏi danh sách self.staffs_data
            self.staffs_data = [s for s in self.staffs_data if s.get("id") != staff_id]

            # Ghi lại vào file JSON
            self.save_data_staff_to_file()

            # Thông báo
            messagebox.showinfo("Thành công", f"Đã xóa nhân viên ID: {staff_id} khỏi hệ thống.")

            # Quay lại danh sách sau khi xóa
            self.go_back()

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback


# Test riêng biệt (chỉ dành cho development)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Chi tiết nhân viên")
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

    # # Example staffs_data for testing ID generation and existence - REMOVED/COMMENTED OUT
    # initial_staffs = [
    #     {'id': 'NV001', 'name': 'Lê Văn Luyện', 'birth_date': '10/05/1980', 'phone': '0901111222',
    #      'gender': 'Nam', 'email': 'luyenlv@example.com', 'address': '123 Đường ABC, Q1, TP.HCM',
    #      'position': 'Bác sĩ', 'department': 'Nội khoa', 'start_date': '01/01/2010', 'salary': '20000000', 'image_path': ''},
    #     {'id': 'NV002', 'name': 'Trần Thị Thu', 'birth_date': '25/11/1992', 'phone': '0983333444',
    #      'gender': 'Nữ', 'email': 'thuttt@example.com', 'address': '456 Đường XYZ, Q2, TP.HCM',
    #      'position': 'Y tá', 'department': 'Phòng khám', 'start_date': '15/07/2015', 'salary': '12000000', 'image_path': ''},
    # ]

    # # Create a dummy staffs.json for testing - REMOVED/COMMENTED OUT
    # with open("staffs.json", "w", encoding="utf-8") as f:
    #     json.dump(initial_staffs, f, ensure_ascii=False, indent=2)

    # Test data for an existing staff (can still be used if you want to explicitly load one for testing)
    # This data should ideally come from your staffs.json if it exists
    test_staff = {
        'id': 'NV001', 'name': 'nguyễn thị thanh hằng', 'birth_date': '11/08/2006', 'phone': '09842323256',
        'gender': 'Nữ', 'email': 'ngtthang@gmail.com', 'address': '',
        'position': 'Bác sĩ', 'department': 'Nội khoa', 'start_date': '', 'salary': '',
        'image_path': None # Assuming no image for this test
    }

    # Load all staff data to simulate the main app's behavior
    all_staff_data_from_file = []
    try:
        with open("staffs.json", "r", encoding="utf-8") as f:
            all_staff_data_from_file = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_staff_data_from_file = [] # Handle if file doesn't exist or is empty/corrupt

    # Khởi tạo giao diện (test với dữ liệu có sẵn từ file hoặc tạo mới)
    # To test adding new staff, pass staff_data=None
    # staff_detail_gui = StaffDetailGui(content_frame, staff_data=None, all_staffs_data=all_staff_data_from_file)
    # To test editing existing staff, pass test_staff (ensure it's in all_staff_data_from_file)
    staff_detail_gui = StaffDetailGui(content_frame, staff_data=test_staff, all_staffs_data=all_staff_data_from_file)

    root.mainloop()

    # # Clean up the dummy staffs.json after testing - REMOVED/COMMENTED OUT
    # if os.path.exists("staffs.json"):
    #     os.remove("staffs.json")