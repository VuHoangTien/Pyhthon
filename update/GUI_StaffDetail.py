# import os
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# from PIL import Image, ImageTk
# from customtkinter import CTkButton, CTkFrame, CTkEntry, CTkLabel, CTkComboBox
# from datetime import datetime
# import json

# class StaffDetailGui():
#     def __init__(self, master, staff_data=None, navigation_callback=None):
#         self.master = master  # Đây sẽ là content_frame từ GUI_Main
#         self.staff_data = staff_data  # Dữ liệu nhân viên (None nếu thêm mới)
#         self.navigation_callback = navigation_callback  # Callback để chuyển màn hình
#         self.image_path = None
#         self.photo_label = None
#         self.is_editing = False if staff_data else True  # Nếu thêm mới thì mặc định là chế độ chỉnh sửa
#         self.setup_ui()
#         self.load_data_staff_from_file()
#         self.staffs_data = []

        
 
#     def setup_ui(self):
#         # Header với tiêu đề và các nút chức năng
#         header_frame = tk.Frame(self.master, bg="white", height=60)
#         header_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

#         # Nút quay lại
#         back_button = CTkButton(master=header_frame, text="← Quay lại", width=100, height=35, 
#                             fg_color="#6c757d", text_color="white", hover_color="#5a6268", 
#                             corner_radius=5, command=self.go_back)
#         back_button.pack(side=tk.LEFT, pady=10)

#         # Các nút chức năng bên phải
#         button_frame = tk.Frame(header_frame, bg="white")
#         button_frame.pack(side=tk.RIGHT, pady=10)

#         # Nút lưu thông tin
#         self.save_button = CTkButton(master=button_frame, text="💾 Lưu", width=100, height=35, 
#                             fg_color="#28a745", text_color="white", hover_color="#218838", 
#                             corner_radius=5, command=self.save_staff)
#         self.save_button.pack(side=tk.RIGHT, padx=5)

#         # Nút sửa thông tin
#         self.edit_button = CTkButton(master=button_frame, text="✏️ Sửa", width=100, height=35, 
#                             fg_color="#ffc107", text_color="white", hover_color="#e0a800", 
#                             corner_radius=5, command=self.toggle_edit_mode)
#         self.edit_button.pack(side=tk.RIGHT, padx=5)

#         # Nút xóa thông tin
#         self.delete_button = CTkButton(master=button_frame, text="🗑️ Xóa", width=100, height=35, 
#                             fg_color="#dc3545", text_color="white", hover_color="#c82333", 
#                             corner_radius=5, command=self.delete_staff)
#         self.delete_button.pack(side=tk.RIGHT, padx=5)

#         # Tiêu đề căn giữa
#         title_text = "Thêm nhân viên mới" if not self.staff_data else "Chi tiết nhân viên"
#         title_label = tk.Label(header_frame, text=title_text, font=("Arial", 16, "bold"), bg="white")
#         title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#         # Container chính
#         main_container = CTkFrame(self.master, border_width=1, corner_radius=10)
#         main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

#         # Frame chứa toàn bộ nội dung với scroll
#         scroll_container = tk.Frame(main_container, bg="white")
#         scroll_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         # Canvas cho scroll
#         canvas = tk.Canvas(scroll_container, bg="white")
#         scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
#         scrollable_frame = tk.Frame(canvas, bg="white")

#         scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )

#         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)

#         scrollbar.pack(side="right", fill="y")
#         canvas.pack(side="left", fill="both", expand=True)

#         # Nội dung chính
#         content_frame = tk.Frame(scrollable_frame, bg="white")
#         content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

#         # Phần hình ảnh (bên trái)
#         left_frame = tk.Frame(content_frame, bg="white")
#         left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 30))

#         # Khung hình ảnh 3x4
#         photo_frame = CTkFrame(left_frame, width=240, height=320, border_width=2)
#         photo_frame.pack(pady=10)
#         photo_frame.pack_propagate(False)

#         # Label hiển thị hình ảnh
#         self.photo_label = tk.Label(photo_frame, text="Chưa có ảnh\n📷", font=("Arial", 14), 
#                                    bg="#f8f9fa", fg="#6c757d", justify=tk.CENTER)
#         self.photo_label.pack(fill=tk.BOTH, expand=True)

#         # Nút chọn ảnh
#         self.upload_button = CTkButton(master=left_frame, text="📁 Chọn ảnh", width=240, height=35,
#                                       fg_color="#17a2b8", text_color="white", hover_color="#138496",
#                                       corner_radius=5, command=self.upload_image)
#         self.upload_button.pack(pady=10)

#         # Phần thông tin (bên phải)
#         right_frame = tk.Frame(content_frame, bg="white")
#         right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#         # Tạo form thông tin
#         self.create_staff_form(right_frame)

#         # Bind mousewheel
#         def _on_mousewheel(event):
#             canvas.yview_scroll(int(-1*(event.delta/120)), "units")
#         canvas.bind_all("<MouseWheel>", _on_mousewheel)

#     def create_staff_form(self, parent):
#         # Thông tin cơ bản
#         basic_info_frame = CTkFrame(parent, fg_color="#f8f9fa", border_width=1)
#         basic_info_frame.pack(fill=tk.X, pady=(0, 20))

#         tk.Label(basic_info_frame, text="THÔNG TIN CƠ BẢN", font=("Arial", 12, "bold"), 
#                 bg="#f8f9fa").pack(pady=(10, 5))

#         # Hàng 1: ID và Họ tên
#         row1 = tk.Frame(basic_info_frame, bg="#f8f9fa")
#         row1.pack(fill=tk.X, padx=15, pady=5)

#         tk.Label(row1, text="ID nhân viên:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
#         self.staff_id_entry = CTkEntry(row1, width=150, height=30)
#         self.staff_id_entry.pack(side=tk.LEFT, padx=(10, 50))

#         tk.Label(row1, text="Họ và tên:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
#         self.fullname_entry = CTkEntry(row1, width=250, height=30)
#         self.fullname_entry.pack(side=tk.LEFT, padx=10)

#         # Hàng 2: Ngày sinh và Giới tính
#         row2 = tk.Frame(basic_info_frame, bg="#f8f9fa")
#         row2.pack(fill=tk.X, padx=15, pady=5)

#         tk.Label(row2, text="Ngày sinh:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
#         self.birth_date_entry = CTkEntry(row2, width=150, height=30, placeholder_text="dd/mm/yyyy")
#         self.birth_date_entry.pack(side=tk.LEFT, padx=(10, 50))

#         tk.Label(row2, text="Giới tính:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
#         self.gender_combo = CTkComboBox(row2, values=["Nam", "Nữ", "Khác"], width=150, height=30)
#         self.gender_combo.pack(side=tk.LEFT, padx=10)

#         # Hàng 3: Số điện thoại và Email
#         row3 = tk.Frame(basic_info_frame, bg="#f8f9fa")
#         row3.pack(fill=tk.X, padx=15, pady=5)

#         tk.Label(row3, text="Số điện thoại:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
#         self.phone_entry = CTkEntry(row3, width=150, height=30)
#         self.phone_entry.pack(side=tk.LEFT, padx=(10, 30))

#         tk.Label(row3, text="Email:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
#         self.email_entry = CTkEntry(row3, width=250, height=30)
#         self.email_entry.pack(side=tk.LEFT, padx=10)

#         # Hàng 4: Địa chỉ
#         row4 = tk.Frame(basic_info_frame, bg="#f8f9fa")
#         row4.pack(fill=tk.X, padx=15, pady=(5, 15))

#         tk.Label(row4, text="Địa chỉ:", font=("Arial", 10), bg="#f8f9fa").pack(side=tk.LEFT)
#         self.address_entry = CTkEntry(row4, width=500, height=30)
#         self.address_entry.pack(side=tk.LEFT, padx=10)

#         # Thông tin công việc
#         work_info_frame = CTkFrame(parent, fg_color="#e8f4f8", border_width=1)
#         work_info_frame.pack(fill=tk.X, pady=(0, 20))

#         tk.Label(work_info_frame, text="THÔNG TIN CÔNG VIỆC", font=("Arial", 12, "bold"), 
#                 bg="#e8f4f8").pack(pady=(10, 5))

#         # Hàng 1: Chức vụ và Khoa/Phòng ban
#         work_row1 = tk.Frame(work_info_frame, bg="#e8f4f8")
#         work_row1.pack(fill=tk.X, padx=15, pady=5)

#         tk.Label(work_row1, text="Chức vụ:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
#         self.position_combo = CTkComboBox(work_row1, values=["Bác sĩ", "Y tá", "Điều dưỡng", "Kỹ thuật viên", "Hành chính", "Khác"], width=150, height=30)
#         self.position_combo.pack(side=tk.LEFT, padx=(10, 50))

#         tk.Label(work_row1, text="Khoa/Phòng ban:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
#         self.department_combo = CTkComboBox(work_row1, values=["Nội khoa", "Ngoại khoa", "Nhi khoa", "Sản khoa", "Tim mạch", "Thần kinh", "Hành chính", "Khác"], width=200, height=30)
#         self.department_combo.pack(side=tk.LEFT, padx=10)

#         # Hàng 2: Ngày vào làm và Trình độ
#         work_row2 = tk.Frame(work_info_frame, bg="#e8f4f8")
#         work_row2.pack(fill=tk.X, padx=15, pady=5)

#         tk.Label(work_row2, text="Ngày vào làm:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
#         self.start_date_entry = CTkEntry(work_row2, width=150, height=30, placeholder_text="dd/mm/yyyy")
#         self.start_date_entry.pack(side=tk.LEFT, padx=(10, 30))

#         tk.Label(work_row2, text="Trình độ:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
#         self.education_combo = CTkComboBox(work_row2, values=["Trung cấp", "Cao đẳng", "Đại học", "Thạc sĩ", "Tiến sĩ"], width=150, height=30)
#         self.education_combo.pack(side=tk.LEFT, padx=10)

#         # Hàng 3: Số giấy phép hành nghề và Lương
#         work_row3 = tk.Frame(work_info_frame, bg="#e8f4f8")
#         work_row3.pack(fill=tk.X, padx=15, pady=(5, 15))

#         tk.Label(work_row3, text="Số GPHHN:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
#         self.license_entry = CTkEntry(work_row3, width=200, height=30)
#         self.license_entry.pack(side=tk.LEFT, padx=(10, 50))

#         tk.Label(work_row3, text="Lương (VNĐ):", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
#         self.salary_entry = CTkEntry(work_row3, width=150, height=30)
#         self.salary_entry.pack(side=tk.LEFT, padx=10)

#         # Thông tin liên hệ khẩn cấp
#         emergency_frame = CTkFrame(parent, fg_color="#fff3cd", border_width=1)
#         emergency_frame.pack(fill=tk.X)

#         tk.Label(emergency_frame, text="THÔNG TIN LIÊN HỆ KHẨN CẤP", font=("Arial", 12, "bold"), 
#                 bg="#fff3cd").pack(pady=(10, 5))

#         # Hàng 1: Tên người liên hệ và Mối quan hệ
#         em_row1 = tk.Frame(emergency_frame, bg="#fff3cd")
#         em_row1.pack(fill=tk.X, padx=15, pady=5)

#         tk.Label(em_row1, text="Tên người liên hệ:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
#         self.emergency_name_entry = CTkEntry(em_row1, width=200, height=30)
#         self.emergency_name_entry.pack(side=tk.LEFT, padx=(10, 30))

#         tk.Label(em_row1, text="Mối quan hệ:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
#         self.relationship_combo = CTkComboBox(em_row1, values=["Cha", "Mẹ", "Vợ/Chồng", "Con", "Anh/Chị/Em", "Bạn", "Khác"], 
#                                             width=150, height=30)
#         self.relationship_combo.pack(side=tk.LEFT, padx=10)

#         # Hàng 2: Số điện thoại khẩn cấp
#         em_row2 = tk.Frame(emergency_frame, bg="#fff3cd")
#         em_row2.pack(fill=tk.X, padx=15, pady=(5, 15))

#         tk.Label(em_row2, text="Số điện thoại:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
#         self.emergency_phone_entry = CTkEntry(em_row2, width=200, height=30)
#         self.emergency_phone_entry.pack(side=tk.LEFT, padx=10)

#         # Lưu tham chiếu đến các widget để có thể enable/disable
#         self.form_widgets = [
#             self.staff_id_entry, self.fullname_entry, self.birth_date_entry, self.gender_combo,
#             self.phone_entry, self.email_entry, self.address_entry, self.position_combo,
#             self.department_combo, self.start_date_entry, self.education_combo, self.license_entry,
#             self.salary_entry, self.emergency_name_entry, self.relationship_combo, self.emergency_phone_entry
#         ]

#     def go_back(self):
#         """Quay lại màn hình danh sách nhân viên"""
#         if self.navigation_callback:
#             self.navigation_callback('staff_list')
#         else:
#             self.back_to_staff_list()

#     def back_to_staff_list(self):
#         """Quay lại danh sách nhân viên (dành cho test độc lập)"""
#         if self.is_editing and self.has_unsaved_changes():
#             result = messagebox.askyesnocancel("Xác nhận", 
#                                              "Bạn có thay đổi chưa được lưu.\n"
#                                              "Bạn có muốn lưu trước khi quay lại không?\n\n"
#                                              "Nhấn 'Có' để lưu và quay lại\n"
#                                              "Nhấn 'Không' để bỏ qua thay đổi\n"
#                                              "Nhấn 'Hủy' để tiếp tục chỉnh sửa")
            
#             if result is None:
#                 return
#             elif result:
#                 if not self.save_staff(show_message=False):
#                     return
        
#         for widget in self.master.winfo_children():
#             widget.destroy()
        
#         try:
#             from GUI_StaffList import StaffListGui
#             staff_list_gui = StaffListGui(self.master, self.navigation_callback)
#         except ImportError:
#             messagebox.showerror("Lỗi", "Không thể import GUI_StaffList!")

#     def has_unsaved_changes(self):
#         """Kiểm tra xem có thay đổi chưa lưu không"""
#         if not self.staff_data:
#             # Bệnh nhân mới - kiểm tra có dữ liệu đã nhập không
#             return (self.staff_id_entry.get().strip() or 
#                    self.fullname_entry.get().strip() or
#                    self.phone_entry.get().strip())
#         else:
#             # Bệnh nhân có sẵn - kiểm tra có thay đổi so với dữ liệu gốc không
#             return (self.staff_id_entry.get().strip() != self.staff_data.get('id', '') or
#                    self.fullname_entry.get().strip() != self.staff_data.get('name', '') or
#                    self.phone_entry.get().strip() != self.staff_data.get('phone', ''))

#     def upload_image(self):
#         if not self.is_editing:
#             messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để thay đổi hình ảnh!")
#             return
            
#         file_path = filedialog.askopenfilename(
#             title="Chọn ảnh nhân viên",
#             filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
#         )
        
#         if file_path:
#             try:
#                 image = Image.open(file_path)
#                 image = image.resize((220, 300), Image.Resampling.LANCZOS)
#                 photo = ImageTk.PhotoImage(image)
                
#                 self.photo_label.configure(image=photo, text="")
#                 self.photo_label.image = photo
#                 self.image_path = file_path
                
#             except Exception as e:
#                 messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")

#     def load_staff_data(self):
#         """Tải dữ liệu nhân viên nếu có"""
#         if self.staff_data:
#             self.staff_id_entry.insert(0, self.staff_data.get('id', ''))
#             self.fullname_entry.insert(0, self.staff_data.get('name', ''))
#             self.birth_date_entry.insert(0, self.staff_data.get('birth_date', ''))
#             self.gender_combo.set(self.staff_data.get('gender', ''))
#             self.phone_entry.insert(0, self.staff_data.get('phone', ''))
#             self.email_entry.insert(0, self.staff_data.get('email', ''))
#             self.address_entry.insert(0, self.staff_data.get('address', ''))
#             self.position_combo.set(self.staff_data.get('position', ''))
#             self.department_combo.set(self.staff_data.get('department', ''))
#             self.start_date_entry.insert(0, self.staff_data.get('start_date', ''))
#             self.education_combo.set(self.staff_data.get('education', ''))
#             self.license_entry.insert(0, self.staff_data.get('license', ''))
#             self.salary_entry.insert(0, self.staff_data.get('salary', ''))
#             self.emergency_name_entry.insert(0, self.staff_data.get('emergency_name', ''))
#             self.relationship_combo.set(self.staff_data.get('relationship', ''))
#             self.emergency_phone_entry.insert(0, self.staff_data.get('emergency_phone', ''))
            
#             if 'image_path' in self.staff_data and self.staff_data['image_path']:
#                 try:
#                     image = Image.open(self.staff_data['image_path'])
#                     image = image.resize((220, 300), Image.Resampling.LANCZOS)
#                     photo = ImageTk.PhotoImage(image)
#                     self.photo_label.configure(image=photo, text="")
#                     self.photo_label.image = photo
#                     self.image_path = self.staff_data['image_path']
#                 except:
#                     pass
        
#         self.toggle_form_state()

#     def toggle_edit_mode(self):
#         """Chuyển đổi giữa chế độ xem và chỉnh sửa"""
#         self.is_editing = not self.is_editing
#         self.toggle_form_state()

#     def toggle_form_state(self):
#         """Bật/tắt khả năng chỉnh sửa form"""
#         state = "normal" if self.is_editing else "disabled"
        
#         for widget in self.form_widgets:
#             if hasattr(widget, 'configure'):
#                 widget.configure(state=state)
        
#         if self.is_editing:
#             self.edit_button.configure(text="📖 Xem")
#             self.upload_button.configure(state="normal")
#         else:
#             self.edit_button.configure(text="✏️ Sửa")
#             self.upload_button.configure(state="disabled")
            
#     # hàm load và save data
#     def load_data_staff_from_file(self):
#         try:
#             with open("staffs.json", "r", encoding="utf-8") as f:
#                 self.staffs_data = json.load(f)  # ✅ đúng: load vào danh sách
#         except FileNotFoundError:
#             self.staffs_data = []

       
#     def save_data_staff_to_file(self):
#         try:
#             with open("staffs.json", "w", encoding="utf-8") as f:
#                 json.dump(self.staffs_data, f, ensure_ascii=False, indent=2)
#         except Exception as e:
#             print("Lỗi khi ghi file:", e)


#     def save_staff(self, show_message=True):
#         """Lưu thông tin nhân viên"""
#         if not self.is_editing:
#             if show_message:
#                 messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để chỉnh sửa thông tin!")
#             return False
        
#         if not self.staff_id_entry.get().strip():
#             if show_message:
#                 messagebox.showerror("Lỗi", "Vui lòng nhập ID nhân viên!")
#             return False
        
#         if not self.fullname_entry.get().strip():
#             if show_message:
#                 messagebox.showerror("Lỗi", "Vui lòng nhập họ tên nhân viên!")
#             return False
        
#         staff_info = {
#             'id': self.staff_id_entry.get().strip(),
#             'name': self.fullname_entry.get().strip(),
#             'birth_date': self.birth_date_entry.get().strip(),
#             'gender': self.gender_combo.get(),
#             'phone': self.phone_entry.get().strip(),
#             'email': self.email_entry.get().strip(),
#             'address': self.address_entry.get().strip(),
#             'position': self.position_combo.get(),
#             'department': self.department_combo.get(),
#             'start_date': self.start_date_entry.get().strip(),
#             'education': self.education_combo.get(),
#             'license': self.license_entry.get().strip(),
#             'salary': self.salary_entry.get().strip(),
#             'emergency_name': self.emergency_name_entry.get().strip(),
#             'relationship': self.relationship_combo.get(),
#             'emergency_phone': self.emergency_phone_entry.get().strip(),
#             'image_path': self.image_path
#         }
        
#         # Tải dữ liệu hiện có để đảm bảo chúng ta đang làm việc với dữ liệu mới nhất
#         self.load_data_staff_from_file() # Đảm bảo staffs_data được cập nhật

#         found = False # Cờ để kiểm tra xem nhân viên có tồn tại hay không
#         # Nếu đang chỉnh sửa một nhân viên hiện có, tìm và cập nhật
#         for i, staff in enumerate(self.staffs_data): # Lặp qua dữ liệu nhân viên hiện có
#             if staff["id"] == staff_info["id"]: # Kiểm tra xem ID nhân viên hiện tại có khớp với ID hiện có hay không
#                 self.staffs_data[i] = staff_info # Cập nhật dữ liệu của nhân viên hiện có
#                 found = True # Đặt cờ thành true vì nhân viên đã được tìm thấy và cập nhật
#                 break # Thoát vòng lặp sau khi cập nhật
        
#         if not found: # Nếu không tìm thấy nhân viên (nhân viên mới)
#             self.staffs_data.append(staff_info) # Thêm nhân viên mới vào danh sách

#         # Lưu toàn bộ danh sách đã cập nhật trở lại tệp
#         self.save_data_staff_to_file() # Lưu tất cả dữ liệu nhân viên vào tệp

#         # Cập nhật dữ liệu nhân viên hiện tại cho phiên bản GUI
#         self.staff_data = staff_info # Cập nhật thuộc tính staff_data với thông tin mới

#         if show_message:
#             messagebox.showinfo("Thành công", "Đã lưu thông tin nhân viên thành công!") # Hiển thị thông báo thành công

#         # Trở lại chế độ xem
#         self.is_editing = False # Đặt chế độ chỉnh sửa thành false
#         self.toggle_form_state() # Cập nhật trạng thái của biểu mẫu
        
#         return True # Trả về true cho biết đã lưu thành công

#     def delete_staff(self):
#         """Xóa nhân viên"""
#         if not self.staff_data:
#             messagebox.showwarning("Cảnh báo", "Không thể xóa nhân viên mới chưa được lưu!")
#             return
        
#         result = messagebox.askyesno("Xác nhận", 
#                                    "Bạn có chắc chắn muốn xóa thông tin nhân viên này?\n"
#                                    "Hành động này không thể hoàn tác!")
        
#         if result:
#             staff_id = self.staff_data.get("id")
#             if not staff_id:
#                 messagebox.showerror("Lỗi", "Không tìm thấy ID nhân viên để xóa.")
#                 return

#             # Xóa khỏi danh sách self.staff_data
#             self.patients_data = [p for p in self.staff_data if p.get("id") != staff_id]

#             # Ghi lại vào file JSON
#             self.save_data_staff_to_file()

#             # Thông báo
#             messagebox.showinfo("Thành công", f"Đã xóa nhân viên ID: {staff_id} khỏi hệ thống.")
            
#             # Quay lại danh sách sau khi xóa
#             self.go_back()

#     def set_navigation_callback(self, callback):
#         """Thiết lập callback cho navigation"""
#         self.navigation_callback = callback


# # Test riêng biệt
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Test Chi tiết nhân viên")
#     root.configure(bg="#f8f9fa")
#     root.resizable(True, True)

#     window_width = 1200
#     window_height = 700
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     center_x = int((screen_width - window_width) / 2)
#     center_y = int((screen_height - window_height) / 3)
#     root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

#     content_frame = tk.Frame(root, bg="#f8f9fa")
#     content_frame.pack(expand=True, fill=tk.BOTH)

#     # Test data
#     test_staff = {
#         'id': 'NV001', 'name': 'Nguyễn Văn A', 'birth_date': '15/03/1985', 'phone': '0901234567',
#         'gender': 'Nam', 'email': 'nguyenvana@hospital.com', 'address': '123 Đường ABC, Q1, TP.HCM',
#         'position': 'Bác sĩ', 'department': 'Nội khoa', 'start_date': '01/01/2020', 'education': 'Đại học',
#         'license': 'BS123456', 'salary': '15000000', 'emergency_name': 'Nguyễn Thị B', 
#         'relationship': 'Vợ', 'emergency_phone': '0912345678'
#     }

#     staff_detail_gui = StaffDetailGui(content_frame, test_staff)
#     root.mainloop()


# GUI_StaffDetail.py
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from customtkinter import CTkButton, CTkFrame, CTkEntry, CTkLabel, CTkComboBox
from datetime import datetime
import json

class StaffDetailGui():
    def __init__(self, master, staff_data=None, navigation_callback=None):
        self.master = master
        self.staff_data = staff_data
        self.navigation_callback = navigation_callback
        self.image_path = None
        self.photo_label = None
        self.is_editing = False if staff_data else True
        self.staffs_data = [] # Khởi tạo chỉ một lần

        self.setup_ui()
        self.load_data_staff_from_file() # Tải dữ liệu tổng thể trước
        self.load_staff_data() # Sau đó tải dữ liệu của staff cụ thể (nếu có) và thiết lập trạng thái form

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

        # Hàng 1: Chức vụ và Khoa/Phòng ban
        work_row1 = tk.Frame(work_info_frame, bg="#e8f4f8")
        work_row1.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(work_row1, text="Chức vụ:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.position_combo = CTkComboBox(work_row1, values=["Bác sĩ", "Y tá", "Điều dưỡng", "Kỹ thuật viên", "Hành chính", "Khác"], width=150, height=30)
        self.position_combo.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(work_row1, text="Khoa/Phòng ban:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.department_combo = CTkComboBox(work_row1, values=["Nội khoa", "Ngoại khoa", "Nhi khoa", "Sản khoa", "Tim mạch", "Thần kinh", "Hành chính", "Khác"], width=200, height=30)
        self.department_combo.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Ngày vào làm và Trình độ
        work_row2 = tk.Frame(work_info_frame, bg="#e8f4f8")
        work_row2.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(work_row2, text="Ngày vào làm:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.start_date_entry = CTkEntry(work_row2, width=150, height=30, placeholder_text="dd/mm/yyyy")
        self.start_date_entry.pack(side=tk.LEFT, padx=(10, 30))

        tk.Label(work_row2, text="Trình độ:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.education_combo = CTkComboBox(work_row2, values=["Trung cấp", "Cao đẳng", "Đại học", "Thạc sĩ", "Tiến sĩ"], width=150, height=30)
        self.education_combo.pack(side=tk.LEFT, padx=10)

        # Hàng 3: Số giấy phép hành nghề và Lương
        work_row3 = tk.Frame(work_info_frame, bg="#e8f4f8")
        work_row3.pack(fill=tk.X, padx=15, pady=(5, 15))

        tk.Label(work_row3, text="Số GPHHN:", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.license_entry = CTkEntry(work_row3, width=200, height=30)
        self.license_entry.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(work_row3, text="Lương (VNĐ):", font=("Arial", 10), bg="#e8f4f8").pack(side=tk.LEFT)
        self.salary_entry = CTkEntry(work_row3, width=150, height=30)
        self.salary_entry.pack(side=tk.LEFT, padx=10)

        # Thông tin liên hệ khẩn cấp
        emergency_frame = CTkFrame(parent, fg_color="#fff3cd", border_width=1)
        emergency_frame.pack(fill=tk.X)

        tk.Label(emergency_frame, text="THÔNG TIN LIÊN HỆ KHẨN CẤP", font=("Arial", 12, "bold"),
                bg="#fff3cd").pack(pady=(10, 5))

        # Hàng 1: Tên người liên hệ và Mối quan hệ
        em_row1 = tk.Frame(emergency_frame, bg="#fff3cd")
        em_row1.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(em_row1, text="Tên người liên hệ:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
        self.emergency_name_entry = CTkEntry(em_row1, width=200, height=30)
        self.emergency_name_entry.pack(side=tk.LEFT, padx=(10, 30))

        tk.Label(em_row1, text="Mối quan hệ:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
        self.relationship_combo = CTkComboBox(em_row1, values=["Cha", "Mẹ", "Vợ/Chồng", "Con", "Anh/Chị/Em", "Bạn", "Khác"],
                                            width=150, height=30)
        self.relationship_combo.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Số điện thoại khẩn cấp
        em_row2 = tk.Frame(emergency_frame, bg="#fff3cd")
        em_row2.pack(fill=tk.X, padx=15, pady=(5, 15))

        tk.Label(em_row2, text="Số điện thoại:", font=("Arial", 10), bg="#fff3cd").pack(side=tk.LEFT)
        self.emergency_phone_entry = CTkEntry(em_row2, width=200, height=30)
        self.emergency_phone_entry.pack(side=tk.LEFT, padx=10)

        # Lưu tham chiếu đến các widget để có thể enable/disable
        self.form_widgets = [
            self.staff_id_entry, self.fullname_entry, self.birth_date_entry, self.gender_combo,
            self.phone_entry, self.email_entry, self.address_entry, self.position_combo,
            self.department_combo, self.start_date_entry, self.education_combo, self.license_entry,
            self.salary_entry, self.emergency_name_entry, self.relationship_combo, self.emergency_phone_entry
        ]

    def go_back(self):
        """Quay lại màn hình danh sách nhân viên"""
        if self.navigation_callback:
            self.navigation_callback('staff_list')
        else:
            self.back_to_staff_list()

    def back_to_staff_list(self):
        """Quay lại danh sách nhân viên (dành cho test độc lập)"""
        if self.is_editing and self.has_unsaved_changes():
            result = messagebox.askyesnocancel("Xác nhận",
                                             "Bạn có thay đổi chưa được lưu.\n"
                                             "Bạn có muốn lưu trước khi quay lại không?\n\n"
                                             "Nhấn 'Có' để lưu và quay lại\n"
                                             "Nhấn 'Không' để bỏ qua thay đổi\n"
                                             "Nhấn 'Hủy' để tiếp tục chỉnh sửa")

            if result is None:
                return
            elif result:
                if not self.save_staff(show_message=False):
                    return

        for widget in self.master.winfo_children():
            widget.destroy()

        try:
            from GUI_StaffList import StaffListGui
            staff_list_gui = StaffListGui(self.master, self.navigation_callback)
        except ImportError:
            messagebox.showerror("Lỗi", "Không thể import GUI_StaffList!")

    def has_unsaved_changes(self):
        """Kiểm tra xem có thay đổi chưa lưu không"""
        if not self.staff_data:
            # Nhân viên mới - kiểm tra có dữ liệu đã nhập không
            return (self.staff_id_entry.get().strip() or
                   self.fullname_entry.get().strip() or
                   self.phone_entry.get().strip())
        else:
            # Nhân viên có sẵn - kiểm tra có thay đổi so với dữ liệu gốc không
            return (self.staff_id_entry.get().strip() != self.staff_data.get('id', '') or
                   self.fullname_entry.get().strip() != self.staff_data.get('name', '') or
                   self.birth_date_entry.get().strip() != self.staff_data.get('birth_date', '') or
                   self.gender_combo.get() != self.staff_data.get('gender', '') or
                   self.phone_entry.get().strip() != self.staff_data.get('phone', '') or
                   self.email_entry.get().strip() != self.staff_data.get('email', '') or
                   self.address_entry.get().strip() != self.staff_data.get('address', '') or
                   self.position_combo.get() != self.staff_data.get('position', '') or
                   self.department_combo.get() != self.staff_data.get('department', '') or
                   self.start_date_entry.get().strip() != self.staff_data.get('start_date', '') or
                   self.education_combo.get() != self.staff_data.get('education', '') or
                   self.license_entry.get().strip() != self.staff_data.get('license', '') or
                   self.salary_entry.get().strip() != self.staff_data.get('salary', '') or
                   self.emergency_name_entry.get().strip() != self.staff_data.get('emergency_name', '') or
                   self.relationship_combo.get() != self.staff_data.get('relationship', '') or
                   self.emergency_phone_entry.get().strip() != self.staff_data.get('emergency_phone', '') or
                   self.image_path != self.staff_data.get('image_path', None))


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
                image = Image.open(file_path)
                image = image.resize((220, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.photo_label.configure(image=photo, text="")
                self.photo_label.image = photo
                self.image_path = file_path

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")

    def load_staff_data(self):
        """Tải dữ liệu nhân viên nếu có và thiết lập trạng thái form ban đầu"""
        if self.staff_data:
            self.staff_id_entry.insert(0, self.staff_data.get('id', ''))
            self.fullname_entry.insert(0, self.staff_data.get('name', ''))
            self.birth_date_entry.insert(0, self.staff_data.get('birth_date', ''))
            self.gender_combo.set(self.staff_data.get('gender', ''))
            self.phone_entry.insert(0, self.staff_data.get('phone', ''))
            self.email_entry.insert(0, self.staff_data.get('email', ''))
            self.address_entry.insert(0, self.staff_data.get('address', ''))
            self.position_combo.set(self.staff_data.get('position', ''))
            self.department_combo.set(self.staff_data.get('department', ''))
            self.start_date_entry.insert(0, self.staff_data.get('start_date', ''))
            self.education_combo.set(self.staff_data.get('education', ''))
            self.license_entry.insert(0, self.staff_data.get('license', ''))
            self.salary_entry.insert(0, self.staff_data.get('salary', ''))
            self.emergency_name_entry.insert(0, self.staff_data.get('emergency_name', ''))
            self.relationship_combo.set(self.staff_data.get('relationship', ''))
            self.emergency_phone_entry.insert(0, self.staff_data.get('emergency_phone', ''))

            if 'image_path' in self.staff_data and self.staff_data['image_path'] and os.path.exists(self.staff_data['image_path']):
                try:
                    image = Image.open(self.staff_data['image_path'])
                    image = image.resize((220, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.photo_label.configure(image=photo, text="")
                    self.photo_label.image = photo
                    self.image_path = self.staff_data['image_path']
                except Exception as e:
                    print(f"Không thể tải ảnh từ đường dẫn '{self.staff_data['image_path']}': {e}")
                    pass # Bỏ qua lỗi nếu ảnh không tồn tại hoặc bị hỏng

        # Thiết lập trạng thái form sau khi tải dữ liệu
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

        if self.is_editing:
            self.edit_button.configure(text="📖 Xem")
            self.upload_button.configure(state="normal")
            self.save_button.configure(state="normal") # Cho phép lưu khi đang chỉnh sửa
        else:
            self.edit_button.configure(text="✏️ Sửa")
            self.upload_button.configure(state="disabled")
            self.save_button.configure(state="disabled") # Tắt nút lưu khi ở chế độ xem

    # hàm load và save data
    def load_data_staff_from_file(self):
        try:
            with open("staffs.json", "r", encoding="utf-8") as f:
                self.staffs_data = json.load(f)
        except FileNotFoundError:
            self.staffs_data = []

    def save_data_staff_to_file(self):
        try:
            with open("staffs.json", "w", encoding="utf-8") as f:
                json.dump(self.staffs_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)


    def save_staff(self, show_message=True):
        """Lưu thông tin nhân viên"""
        if not self.is_editing:
            if show_message:
                messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để chỉnh sửa thông tin!")
            return False

        if not self.staff_id_entry.get().strip():
            if show_message:
                messagebox.showerror("Lỗi", "Vui lòng nhập ID nhân viên!")
            return False

        if not self.fullname_entry.get().strip():
            if show_message:
                messagebox.showerror("Lỗi", "Vui lòng nhập họ tên nhân viên!")
            return False

        staff_info = {
            'id': self.staff_id_entry.get().strip(),
            'name': self.fullname_entry.get().strip(),
            'birth_date': self.birth_date_entry.get().strip(),
            'gender': self.gender_combo.get(),
            'phone': self.phone_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'address': self.address_entry.get().strip(),
            'position': self.position_combo.get(),
            'department': self.department_combo.get(),
            'start_date': self.start_date_entry.get().strip(),
            'education': self.education_combo.get(),
            'license': self.license_entry.get().strip(),
            'salary': self.salary_entry.get().strip(),
            'emergency_name': self.emergency_name_entry.get().strip(),
            'relationship': self.relationship_combo.get(),
            'emergency_phone': self.emergency_phone_entry.get().strip(),
            'image_path': self.image_path
        }

        # Tải dữ liệu hiện có để đảm bảo chúng ta đang làm việc với dữ liệu mới nhất
        self.load_data_staff_from_file()

        found = False
        # Nếu đang chỉnh sửa một nhân viên hiện có, tìm và cập nhật
        for i, staff in enumerate(self.staffs_data):
            if staff["id"] == staff_info["id"]:
                self.staffs_data[i] = staff_info
                found = True
                break

        if not found: # Nếu không tìm thấy nhân viên (nhân viên mới)
            self.staffs_data.append(staff_info)

        # Lưu toàn bộ danh sách đã cập nhật trở lại tệp
        self.save_data_staff_to_file()

        # Cập nhật dữ liệu nhân viên hiện tại cho phiên bản GUI
        self.staff_data = staff_info

        if show_message:
            messagebox.showinfo("Thành công", "Đã lưu thông tin nhân viên thành công!")

        # Trở lại chế độ xem
        self.is_editing = False
        self.toggle_form_state()

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
            self.load_data_staff_from_file() # Tải lại dữ liệu để đảm bảo là mới nhất
            # Lọc danh sách, loại bỏ nhân viên có ID trùng khớp với nhân viên hiện tại
            self.staffs_data = [s for s in self.staffs_data if s.get("id") != self.staff_data.get("id")]
            self.save_data_staff_to_file()

            messagebox.showinfo("Thành công", "Đã xóa nhân viên khỏi hệ thống.")
            self.go_back() # Quay lại danh sách nhân viên sau khi xóa


# Test riêng biệt (chỉ dành cho development)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Chi tiết nhân viên") # Đổi tiêu đề
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

    # Ví dụ dữ liệu nhân viên để test
    # test_staff_data = {
    #     'id': 'NV001',
    #     'name': 'Nguyễn Văn A',
    #     'birth_date': '01/01/1990',
    #     'gender': 'Nam',
    #     'phone': '0912345678',
    #     'email': 'vana@example.com',
    #     'address': '123 Đường ABC, Quận 1, TP.HCM',
    #     'position': 'Bác sĩ',
    #     'department': 'Nội khoa',
    #     'start_date': '15/03/2015',
    #     'education': 'Đại học',
    #     'license': 'GPHHN12345',
    #     'salary': '20000000',
    #     'emergency_name': 'Nguyễn Thị B',
    #     'relationship': 'Vợ/Chồng',
    #     'emergency_phone': '0987654321',
    #     'image_path': None # Thay bằng đường dẫn ảnh thật nếu có
    # }

    # Để test chế độ thêm mới, dùng None
    staff_detail_gui = StaffDetailGui(content_frame, None)
    # Để test chế độ xem/sửa, dùng dữ liệu mẫu
    # staff_detail_gui = StaffDetailGui(content_frame, test_staff_data)

    root.mainloop()