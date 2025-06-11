# GUI_AccountDetail.py
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from customtkinter import CTkButton, CTkFrame, CTkEntry, CTkLabel, CTkComboBox
from datetime import datetime
import hashlib
import json
import re # Import regex module

class AccountDetailGui():
    def __init__(self, master, account_data=None, navigation_callback=None, all_accounts_data=None, save_callback=None):
        self.master = master  # Đây sẽ là content_frame từ GUI_Main hoặc root nếu chạy độc lập
        self.account_data = account_data # Dữ liệu tài khoản hiện tại (nếu có)
        self.navigation_callback = navigation_callback
        self.accounts_list = all_accounts_data if all_accounts_data is not None else [] # Danh sách tất cả tài khoản
        self.is_editing = False # Ban đầu không ở chế độ chỉnh sửa (nếu là tài khoản đã có)
        self.save_callback = save_callback # Callback để refresh bảng danh sách

        # Load data before setup_ui to ensure self.accounts_list is populated
        self.load_data_account_from_file() 
        self.setup_ui()
        self.load_account_data_into_form() # Đổ dữ liệu của tài khoản hiện tại vào form
        self.toggle_form_state() # Thiết lập trạng thái form ban đầu

        if self.account_data is None: # Nếu là tài khoản mới
            self.is_editing = True
            self.toggle_form_state() # Chuyển sang chế độ chỉnh sửa ngay
            self.username_entry.configure(state="normal") # Cho phép chỉnh sửa username khi thêm mới
            self.role_combobox.set("Staff") # Default role
            self.status_combobox.set("Hoạt động") # Default status
            # Gán giá trị mặc định cho ngày tạo và ngày đăng nhập cuối
            self.created_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.last_login_entry.insert(0, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            # Mật khẩu sẽ hiển thị rõ ràng khi thêm mới
            self.entries["password_hash"].configure(show="")

    # hàm load và save data
    def load_data_account_from_file(self):
        try:
            with open("account.json", "r", encoding="utf-8") as f:
                self.accounts_list = json.load(f)
        except FileNotFoundError:
            self.accounts_list = []
        except json.JSONDecodeError:
            self.accounts_list = [] # Handle empty or malformed JSON

    def save_data_account_to_file(self):
        try:
            with open("account.json", "w", encoding="utf-8") as f:
                json.dump(self.accounts_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)

    def setup_ui(self):
        # Clear existing widgets in the master frame if running standalone or within a managed content_frame
        for widget in self.master.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = CTkFrame(self.master, corner_radius=10, fg_color="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = CTkFrame(main_frame, fg_color="#57a1f8", corner_radius=5)
        header_frame.pack(fill=tk.X, pady=(0, 20), ipady=5)

        title_label = CTkLabel(header_frame, text="CHI TIẾT TÀI KHOẢN", font=("Arial", 20, "bold"), text_color="white")
        title_label.pack(pady=10)

        # Content Frame
        content_frame = CTkFrame(main_frame, fg_color="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Labels and Entries
        fields = [
            ("Tên đăng nhập:", "username"),
            ("Mật khẩu:", "password_hash"),
            ("Họ và tên:", "fullname"),
            ("Email:", "email"),
            ("Số điện thoại:", "phone"),
            ("Chức vụ:", "role"),
            ("Trạng thái:", "status"),
            ("Ngày tạo:", "created_date"),
            ("Lần đăng nhập cuối:", "last_login"),
            ("Ghi chú:", "note"),
        ]

        self.entries = {}
        row_idx = 0
        for i, (label_text, field_name) in enumerate(fields):
            current_row = row_idx + i // 2
            current_col = (i % 2) * 2

            # --- ĐÂY LÀ ĐIỂM CẦN CHÚ Ý ---
            # Thêm hoặc sửa 'text_color' cho các CTkLabel trong content_frame
            CTkLabel(content_frame, text=label_text, font=("Arial", 12), text_color="#333333").grid(row=current_row, column=current_col, sticky="w", padx=10, pady=5)
            
            if field_name in ["role", "status"]:
                values = ["Admin", "Doctor", "Nurse", "Staff", "User"] if field_name == "role" else ["Hoạt động", "Khóa"]
                combobox = CTkComboBox(content_frame, values=values, width=250, height=30, state="readonly")
                combobox.grid(row=current_row, column=current_col + 1, sticky="ew", padx=10, pady=5)
                self.entries[field_name] = combobox
                if field_name == "role":
                    self.role_combobox = combobox
                else:
                    self.status_combobox = combobox
            elif field_name == "password_hash":
                entry = CTkEntry(content_frame, width=250, height=30, show="*" if self.account_data else "")
                entry.grid(row=current_row, column=current_col + 1, sticky="ew", padx=10, pady=5)
                self.entries[field_name] = entry
            else:
                entry = CTkEntry(content_frame, width=250, height=30)
                entry.grid(row=current_row, column=current_col + 1, sticky="ew", padx=10, pady=5)
                self.entries[field_name] = entry
                if field_name == "username":
                    self.username_entry = entry
                elif field_name == "created_date":
                    self.created_date_entry = entry
                    self.created_date_entry.configure(state="readonly")
                elif field_name == "last_login":
                    self.last_login_entry = entry
                    self.last_login_entry.configure(state="readonly")

        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(3, weight=1)

        # Buttons
        button_frame = CTkFrame(main_frame, fg_color="white")
        button_frame.pack(pady=20)

        self.edit_button = CTkButton(button_frame, text="Sửa", width=120, height=40,
                                     fg_color="#007bff", text_color="white", hover_color="#0056b3",
                                     command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.save_button = CTkButton(button_frame, text="Lưu", width=120, height=40,
                                     fg_color="#28a745", text_color="white", hover_color="#218838",
                                     command=self.save_account)
        self.save_button.pack(side=tk.LEFT, padx=10)
        self.save_button.configure(state="disabled")

        cancel_button = CTkButton(button_frame, text="Hủy", width=120, height=40,
                                  fg_color="#6c757d", text_color="white", hover_color="#5a6268",
                                  command=self.cancel_edit)
        cancel_button.pack(side=tk.LEFT, padx=10)

        go_back_button = CTkButton(button_frame, text="Quay lại", width=120, height=40,
                                  fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                  command=self.go_back)
        go_back_button.pack(side=tk.LEFT, padx=10)

    def load_account_data_into_form(self):
        if self.account_data:
            for field, entry_widget in self.entries.items():
                value = self.account_data.get(field, "")
                if isinstance(entry_widget, CTkEntry):
                    entry_widget.delete(0, tk.END)
                    entry_widget.insert(0, value)
                    if field == "password_hash": 
                        entry_widget.configure(show="*") # Mặc định ẩn mật khẩu khi load
                elif isinstance(entry_widget, CTkComboBox):
                    entry_widget.set(value)
        else:
            # Clear all fields for new account creation
            for field, entry_widget in self.entries.items():
                if isinstance(entry_widget, CTkEntry):
                    entry_widget.delete(0, tk.END)
                elif isinstance(entry_widget, CTkComboBox):
                    entry_widget.set("") # Clear combobox selection

    def toggle_form_state(self):
        for field, entry_widget in self.entries.items():
            if field == "username" and self.account_data is not None: # Không cho phép chỉnh sửa username của tài khoản hiện có
                state = "readonly"
            elif field in ["created_date", "last_login"]: # Các trường này luôn là readonly
                state = "readonly"
            elif field == "password_hash": # Trường mật khẩu luôn có thể chỉnh sửa nếu is_editing
                state = "normal" if self.is_editing else "readonly"
                if self.is_editing:
                    entry_widget.configure(show="") # Hiển thị rõ mật khẩu khi đang chỉnh sửa
                else:
                    entry_widget.configure(show="*") # Ẩn mật khẩu khi không chỉnh sửa
            else:
                state = "normal" if self.is_editing else "readonly"
            
            if isinstance(entry_widget, CTkEntry):
                entry_widget.configure(state=state)
            elif isinstance(entry_widget, CTkComboBox):
                entry_widget.configure(state="readonly" if not self.is_editing else "normal")

        if self.is_editing:
            self.edit_button.configure(state="disabled")
            self.save_button.configure(state="normal")
        else:
            self.edit_button.configure(state="normal")
            self.save_button.configure(state="disabled")

    def toggle_edit_mode(self):
        self.is_editing = not self.is_editing
        self.toggle_form_state()
        # Logic hiển thị/ẩn mật khẩu đã được xử lý trong toggle_form_state()

    def validate_input(self, data):
        # Validate fullname
        if not data.get("fullname"):
            messagebox.showerror("Lỗi", "Họ và tên không được để trống.")
            return False
        if not re.fullmatch(r"^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚŨĐàáâãèéêìíòóôõùúũđĂăÂâĐđÊêÔôƠơƯưẠ-ỹ\s]+$", data["fullname"]):
            messagebox.showerror("Lỗi", "Họ và tên chỉ được chứa chữ cái và khoảng trắng.")
            return False

        # Validate phone
        if not data.get("phone"):
            messagebox.showerror("Lỗi", "Số điện thoại không được để trống.")
            return False
        if not re.fullmatch(r"^\d{10}$", data["phone"]):
            messagebox.showerror("Lỗi", "Số điện thoại phải có đúng 10 chữ số.")
            return False

        # Validate email
        if not data.get("email"):
            messagebox.showerror("Lỗi", "Email không được để trống.")
            return False
        if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", data["email"]):
            messagebox.showerror("Lỗi", "Email không đúng định dạng.")
            return False
        
        # Validate password (must not be empty)
        if not data.get("password_hash"):
            messagebox.showerror("Lỗi", "Mật khẩu không được để trống.")
            return False

        return True

    def save_account(self):
        account_new_data = {}
        for field, entry_widget in self.entries.items():
            if isinstance(entry_widget, CTkEntry):
                account_new_data[field] = entry_widget.get().strip()
            elif isinstance(entry_widget, CTkComboBox):
                account_new_data[field] = entry_widget.get()

        if not self.validate_input(account_new_data):
            return

        username = account_new_data.get("username")
        if not username:
            messagebox.showerror("Lỗi", "Tên đăng nhập không được để trống.")
            return

        is_new_account = (self.account_data is None)

        if is_new_account:
            # Check for duplicate username for new accounts
            if any(acc.get("username") == username for acc in self.accounts_list):
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
                return
            self.accounts_list.append(account_new_data)
            messagebox.showinfo("Thành công", "Đã thêm tài khoản mới.")
        else:
            # Update existing account
            found = False
            for i, acc in enumerate(self.accounts_list):
                if acc.get("username") == username:
                    self.accounts_list[i] = account_new_data
                    found = True
                    break
            if not found:
                messagebox.showerror("Lỗi", "Không tìm thấy tài khoản để cập nhật.")
                return
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin tài khoản.")

        self.save_data_account_to_file()
        self.account_data = account_new_data # Update current account_data
        self.is_editing = False
        self.toggle_form_state()

        # Call save_callback to refresh the list GUI
        if self.save_callback:
            self.save_callback()

    def cancel_edit(self):
        if self.account_data: # Existing account
            self.is_editing = False
            self.load_account_data_into_form() # Reload original data
            self.toggle_form_state()
        else: # New account, go back to list
            result = messagebox.askyesno("Xác nhận", "Bạn có muốn hủy tạo tài khoản mới và quay lại không?")
            if result:
                self.go_back()

    def go_back(self):
        if self.navigation_callback:
            # Sử dụng callback để chuyển về màn hình danh sách tài khoản
            self.navigation_callback('account_list')
        else:
            # Nếu không có navigation_callback (chạy độc lập),
            # cần xóa toàn bộ UI hiện tại và tạo lại màn hình danh sách.
            for widget in self.master.winfo_children():
                widget.destroy()
            
            # Import AccountListGui tại đây để tránh import vòng tròn nếu có
            from GUI_AccountList import AccountListGui
            AccountListGui(self.master) # Tạo lại màn hình danh sách

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

    # Tạo một file account.json giả để test
    initial_accounts = [
        {'username': 'admin001', 'email': 'admin@hospital.com', 'fullname': 'Nguyễn Văn Admin',
         'phone': '0901234567', 'role': 'Admin', 'status': 'Hoạt động',
         'created_date': '01/01/2023 10:00:00', 'last_login': '01/06/2024 15:30:00',
         'note': 'Tài khoản quản trị viên', 'password_hash': 'admin123'},
        {'username': 'staff001', 'email': 'staff1@hospital.com', 'fullname': 'Lê Thị Staff',
         'phone': '0987654321', 'role': 'Staff', 'status': 'Hoạt động',
         'created_date': '10/02/2023 09:00:00', 'last_login': '05/06/2024 11:00:00',
         'note': '', 'password_hash': 'staff456'},
    ]
    with open("account.json", "w", encoding="utf-8") as f:
        json.dump(initial_accounts, f, ensure_ascii=False, indent=2)

    # Để test chế độ xem/sửa, dùng dữ liệu mẫu
    test_account = {
        'username': 'admin001', 'email': 'admin@hospital.com', 'fullname': 'Nguyễn Văn Admin',
        'phone': '0901234567', 'role': 'Admin', 'status': 'Hoạt động',
        'created_date': '01/01/2023 10:00:00', 'last_login': '01/06/2024 15:30:00',
        'note': 'Tài khoản quản trị viên', 'password_hash': 'admin123'
    }

    def show_account_list():
        for widget in content_frame.winfo_children():
            widget.destroy()
        from GUI_AccountList import AccountListGui # Import ở đây để tránh import vòng tròn
        AccountListGui(content_frame)

    account_detail_gui = AccountDetailGui(
        content_frame, 
        test_account, 
        navigation_callback=show_account_list, 
        all_accounts_data=initial_accounts, 
        save_callback=show_account_list
    )

    # Để test chế độ thêm mới độc lập, bạn có thể thay đổi dòng trên thành:
    # account_detail_gui = AccountDetailGui(
    #     content_frame, 
    #     None, # Thêm mới tài khoản
    #     navigation_callback=show_account_list, 
    #     all_accounts_data=initial_accounts, # Cần truyền list để có thể thêm ID
    #     save_callback=show_account_list
    # )

    root.mainloop()

    # Dọn dẹp file giả sau khi test
    if os.path.exists("account.json"):
        os.remove("account.json")