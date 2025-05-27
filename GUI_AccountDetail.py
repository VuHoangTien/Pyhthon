import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from customtkinter import CTkButton, CTkFrame, CTkEntry, CTkLabel, CTkComboBox
from datetime import datetime
import hashlib

class AccountDetailGui():
    def __init__(self, master, account_data=None, navigation_callback=None):
        self.master = master  # Đây sẽ là content_frame từ GUI_Main
        self.account_data = account_data  # Dữ liệu tài khoản (None nếu thêm mới)
        self.navigation_callback = navigation_callback  # Callback để chuyển màn hình
        self.is_editing = False if account_data else True  # Nếu thêm mới thì mặc định là chế độ chỉnh sửa
        self.setup_ui()
        self.load_account_data()
 
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
                            corner_radius=5, command=self.save_account)
        self.save_button.pack(side=tk.RIGHT, padx=5)

        # Nút sửa thông tin
        self.edit_button = CTkButton(master=button_frame, text="✏️ Sửa", width=100, height=35, 
                            fg_color="#ffc107", text_color="white", hover_color="#e0a800", 
                            corner_radius=5, command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.RIGHT, padx=5)

        # Nút xóa thông tin
        self.delete_button = CTkButton(master=button_frame, text="🗑️ Xóa", width=100, height=35, 
                            fg_color="#dc3545", text_color="white", hover_color="#c82333", 
                            corner_radius=5, command=self.delete_account)
        self.delete_button.pack(side=tk.RIGHT, padx=5)

        # Nút reset mật khẩu
        self.reset_button = CTkButton(master=button_frame, text="🔑 Reset MK", width=100, height=35, 
                            fg_color="#17a2b8", text_color="white", hover_color="#138496", 
                            corner_radius=5, command=self.reset_password)
        self.reset_button.pack(side=tk.RIGHT, padx=5)

        # Tiêu đề căn giữa
        title_text = "Tạo tài khoản mới" if not self.account_data else "Chi tiết tài khoản"
        title_label = tk.Label(header_frame, text=title_text, font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Container chính
        main_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Frame chứa toàn bộ nội dung
        content_frame = tk.Frame(main_container, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        # Tạo form thông tin tài khoản
        self.create_account_form(content_frame)

    def create_account_form(self, parent):
        # Thông tin tài khoản
        account_info_frame = CTkFrame(parent, fg_color="#f8f9fa", border_width=1)
        account_info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(account_info_frame, text="THÔNG TIN TÀI KHOẢN", font=("Arial", 14, "bold"), 
                bg="#f8f9fa").pack(pady=(15, 10))

        # Hàng 1: Username và Email
        row1 = tk.Frame(account_info_frame, bg="#f8f9fa")
        row1.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(row1, text="Tên đăng nhập:", font=("Arial", 11), bg="#f8f9fa").pack(side=tk.LEFT)
        self.username_entry = CTkEntry(row1, width=200, height=35, font=("Arial", 11))
        self.username_entry.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(row1, text="Email:", font=("Arial", 11), bg="#f8f9fa").pack(side=tk.LEFT)
        self.email_entry = CTkEntry(row1, width=250, height=35, font=("Arial", 11))
        self.email_entry.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Họ tên và Số điện thoại
        row2 = tk.Frame(account_info_frame, bg="#f8f9fa")
        row2.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(row2, text="Họ và tên:", font=("Arial", 11), bg="#f8f9fa").pack(side=tk.LEFT)
        self.fullname_entry = CTkEntry(row2, width=200, height=35, font=("Arial", 11))
        self.fullname_entry.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(row2, text="Số điện thoại:", font=("Arial", 11), bg="#f8f9fa").pack(side=tk.LEFT)
        self.phone_entry = CTkEntry(row2, width=180, height=35, font=("Arial", 11))
        self.phone_entry.pack(side=tk.LEFT, padx=10)

        # Hàng 3: Mật khẩu (chỉ hiển thị khi tạo mới)
        self.password_row = tk.Frame(account_info_frame, bg="#f8f9fa")
        if not self.account_data:  # Chỉ hiển thị khi tạo mới
            self.password_row.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(self.password_row, text="Mật khẩu:", font=("Arial", 11), bg="#f8f9fa").pack(side=tk.LEFT)
        self.password_entry = CTkEntry(self.password_row, width=200, height=35, font=("Arial", 11), show="*")
        self.password_entry.pack(side=tk.LEFT, padx=(10, 50))

        tk.Label(self.password_row, text="Xác nhận MK:", font=("Arial", 11), bg="#f8f9fa").pack(side=tk.LEFT)
        self.confirm_password_entry = CTkEntry(self.password_row, width=180, height=35, font=("Arial", 11), show="*")
        self.confirm_password_entry.pack(side=tk.LEFT, padx=10)

        # Spacer
        tk.Frame(account_info_frame, bg="#f8f9fa", height=15).pack()

        # Phân quyền và trạng thái
        permission_frame = CTkFrame(parent, fg_color="#e8f4f8", border_width=1)
        permission_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(permission_frame, text="PHÂN QUYỀN VÀ TRẠNG THÁI", font=("Arial", 14, "bold"), 
                bg="#e8f4f8").pack(pady=(15, 10))

        # Hàng 1: Vai trò và Trạng thái
        perm_row1 = tk.Frame(permission_frame, bg="#e8f4f8")
        perm_row1.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(perm_row1, text="Vai trò:", font=("Arial", 11), bg="#e8f4f8").pack(side=tk.LEFT)
        self.role_combo = CTkComboBox(perm_row1, values=["Admin", "Bác sĩ", "Y tá", "Điều dưỡng", "Nhân viên"], 
                                     width=180, height=35, font=("Arial", 11))
        self.role_combo.pack(side=tk.LEFT, padx=(10, 80))

        tk.Label(perm_row1, text="Trạng thái:", font=("Arial", 11), bg="#e8f4f8").pack(side=tk.LEFT)
        self.status_combo = CTkComboBox(perm_row1, values=["Hoạt động", "Tạm khóa", "Vô hiệu hóa"], 
                                       width=150, height=35, font=("Arial", 11))
        self.status_combo.pack(side=tk.LEFT, padx=10)

        # Hàng 2: Ngày tạo và Ngày cập nhật
        perm_row2 = tk.Frame(permission_frame, bg="#e8f4f8")
        perm_row2.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(perm_row2, text="Ngày tạo:", font=("Arial", 11), bg="#e8f4f8").pack(side=tk.LEFT)
        self.created_date_entry = CTkEntry(perm_row2, width=180, height=35, font=("Arial", 11))
        self.created_date_entry.pack(side=tk.LEFT, padx=(10, 80))

        tk.Label(perm_row2, text="Lần đăng nhập cuối:", font=("Arial", 11), bg="#e8f4f8").pack(side=tk.LEFT)
        self.last_login_entry = CTkEntry(perm_row2, width=150, height=35, font=("Arial", 11))
        self.last_login_entry.pack(side=tk.LEFT, padx=10)

        # Spacer
        tk.Frame(permission_frame, bg="#e8f4f8", height=15).pack()

        # Ghi chú
        note_frame = CTkFrame(parent, fg_color="#fff3cd", border_width=1)
        note_frame.pack(fill=tk.X)

        tk.Label(note_frame, text="GHI CHÚ", font=("Arial", 14, "bold"), 
                bg="#fff3cd").pack(pady=(15, 10))

        # Text area cho ghi chú
        note_container = tk.Frame(note_frame, bg="#fff3cd")
        note_container.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.note_text = tk.Text(note_container, width=80, height=4, font=("Arial", 11), 
                                wrap=tk.WORD, bg="white", relief=tk.SOLID, bd=1)
        self.note_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        note_scrollbar = tk.Scrollbar(note_container, orient=tk.VERTICAL, command=self.note_text.yview)
        note_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.note_text.config(yscrollcommand=note_scrollbar.set)

        # Lưu tham chiếu đến các widget để có thể enable/disable
        self.form_widgets = [
            self.username_entry, self.email_entry, self.fullname_entry, self.phone_entry,
            self.password_entry, self.confirm_password_entry, self.role_combo, self.status_combo,
            self.created_date_entry, self.last_login_entry, self.note_text
        ]

    def go_back(self):
        """Quay lại màn hình danh sách tài khoản"""
        if self.navigation_callback:
            self.navigation_callback('account_list')
        else:
            self.back_to_account_list()

    def back_to_account_list(self):
        """Quay lại danh sách tài khoản (dành cho test độc lập)"""
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
                if not self.save_account(show_message=False):
                    return
        
        for widget in self.master.winfo_children():
            widget.destroy()
        
        try:
            from GUI_AccountList import AccountListGui
            account_list_gui = AccountListGui(self.master, self.navigation_callback)
        except ImportError:
            messagebox.showerror("Lỗi", "Không thể import GUI_AccountList!")

    def has_unsaved_changes(self):
        """Kiểm tra xem có thay đổi chưa lưu không"""
        if not self.account_data:
            return (self.username_entry.get().strip() or 
                   self.fullname_entry.get().strip() or
                   self.email_entry.get().strip())
        else:
            return (self.username_entry.get().strip() != self.account_data.get('username', '') or
                   self.fullname_entry.get().strip() != self.account_data.get('fullname', '') or
                   self.email_entry.get().strip() != self.account_data.get('email', ''))

    def load_account_data(self):
        """Tải dữ liệu tài khoản nếu có"""
        if self.account_data:
            self.username_entry.insert(0, self.account_data.get('username', ''))
            self.email_entry.insert(0, self.account_data.get('email', ''))
            self.fullname_entry.insert(0, self.account_data.get('fullname', ''))
            self.phone_entry.insert(0, self.account_data.get('phone', ''))
            self.role_combo.set(self.account_data.get('role', ''))
            self.status_combo.set(self.account_data.get('status', ''))
            self.created_date_entry.insert(0, self.account_data.get('created_date', ''))
            self.last_login_entry.insert(0, self.account_data.get('last_login', ''))
            
            if 'note' in self.account_data:
                self.note_text.insert(tk.END, self.account_data['note'])
        else:
            # Mặc định cho tài khoản mới
            self.status_combo.set("Hoạt động")
            self.created_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
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
        
        # Username không được sửa nếu đã tồn tại
        if self.account_data and self.is_editing:
            self.username_entry.configure(state="disabled")
        
        # Ngày tạo không được sửa
        self.created_date_entry.configure(state="disabled")
        
        # Cập nhật text của nút edit
        if self.is_editing:
            self.edit_button.configure(text="📖 Xem")
        else:
            self.edit_button.configure(text="✏️ Sửa")

    def save_account(self, show_message=True):
        """Lưu thông tin tài khoản"""
        if not self.is_editing:
            if show_message:
                messagebox.showwarning("Cảnh báo", "Vui lòng bấm 'Sửa' để chỉnh sửa thông tin!")
            return False
        
        # Validate dữ liệu
        if not self.username_entry.get().strip():
            if show_message:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập!")
            return False
        
        if not self.fullname_entry.get().strip():
            if show_message:
                messagebox.showerror("Lỗi", "Vui lòng nhập họ tên!")
            return False
        
        if not self.email_entry.get().strip():
            if show_message:
                messagebox.showerror("Lỗi", "Vui lòng nhập email!")
            return False
        
        # Validate password cho tài khoản mới
        if not self.account_data:
            if not self.password_entry.get().strip():
                if show_message:
                    messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu!")
                return False
            
            if self.password_entry.get() != self.confirm_password_entry.get():
                if show_message:
                    messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
                return False
        
        # Thu thập dữ liệu
        account_info = {
            'username': self.username_entry.get().strip(),
            'email': self.email_entry.get().strip(),
            'fullname': self.fullname_entry.get().strip(),
            'phone': self.phone_entry.get().strip(),
            'role': self.role_combo.get(),
            'status': self.status_combo.get(),
            'created_date': self.created_date_entry.get().strip(),
            'last_login': self.last_login_entry.get().strip(),
            'note': self.note_text.get("1.0", tk.END).strip()
        }
        
        # Hash password nếu là tài khoản mới
        if not self.account_data and self.password_entry.get().strip():
            password_hash = hashlib.sha256(self.password_entry.get().encode()).hexdigest()
            account_info['password_hash'] = password_hash
        
        if show_message:
            messagebox.showinfo("Thành công", "Đã lưu thông tin tài khoản thành công!")
        
        self.account_data = account_info
        self.is_editing = False
        self.toggle_form_state()
        
        return True

    def delete_account(self):
        """Xóa tài khoản"""
        if not self.account_data:
            messagebox.showwarning("Cảnh báo", "Không thể xóa tài khoản mới chưa được lưu!")
            return
        
        result = messagebox.askyesno("Xác nhận", 
                                   "Bạn có chắc chắn muốn xóa tài khoản này?\n"
                                   "Hành động này không thể hoàn tác!")
        
        if result:
            messagebox.showinfo("Thành công", "Đã xóa tài khoản!")
            self.go_back()

    def reset_password(self):
        """Reset mật khẩu tài khoản"""
        if not self.account_data:
            messagebox.showwarning("Cảnh báo", "Chức năng này chỉ áp dụng cho tài khoản đã tồn tại!")
            return
        
        result = messagebox.askyesno("Xác nhận", 
                                   f"Bạn có chắc chắn muốn reset mật khẩu cho tài khoản '{self.account_data.get('username', '')}'?\n"
                                   "Mật khẩu mới sẽ được gửi qua email.")
        
        if result:
            # Tạo mật khẩu mới ngẫu nhiên
            import random
            import string
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            messagebox.showinfo("Thành công", 
                              f"Đã reset mật khẩu thành công!\n"
                              f"Mật khẩu mới: {new_password}\n"
                              f"(Đã gửi qua email: {self.account_data.get('email', '')})")

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback


# Test riêng biệt
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Chi tiết tài khoản")
    root.configure(bg="#f8f9fa")
    root.resizable(True, True)

    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Test data
    test_account = {
        'username': 'admin001', 'email': 'admin@hospital.com', 'fullname': 'Nguyễn Văn Admin',
        'phone': '0901234567', 'role': 'Admin', 'status': 'Hoạt động',
        'created_date': '01/01/2024', 'last_login': '28/05/2025 10:30',
        'note': 'Tài khoản quản trị viên hệ thống'
    }

    account_detail_gui = AccountDetailGui(content_frame, test_account)
    root.mainloop()