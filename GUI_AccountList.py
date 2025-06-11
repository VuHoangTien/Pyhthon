# GUI_AccountList.py
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from customtkinter import CTkButton, CTkFrame, CTkScrollbar
import json
from GUI_AccountDetail import AccountDetailGui # Import AccountDetailGui

class AccountListGui():
    def __init__(self, master, navigation_callback=None):
        self.master = master
        self.navigation_callback = navigation_callback
        self.account_data = [] # Khởi tạo danh sách tài khoản
        self.load_data_account_from_file()
        self.setup_ui()

    def load_data_account_from_file(self):
        try:
            with open("account.json", "r", encoding="utf-8") as f:
                self.account_data = json.load(f)
        except FileNotFoundError:
            self.account_data = []
        except json.JSONDecodeError:
            self.account_data = [] # Handle empty or malformed JSON

    def save_data_account_to_file(self):
        try:
            with open("account.json", "w", encoding="utf-8") as f:
                json.dump(self.account_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)

    def setup_ui(self):
        # KHÔNG XÓA TOÀN BỘ self.master.winfo_children() ở đây nữa
        # Việc dọn dẹp master frame nên được xử lý bởi navigation_callback
        # khi chuyển đổi giữa các màn hình chính.
        # Nếu chạy độc lập, self.master ban đầu sẽ trống.

        # Header
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        add_button = CTkButton(master=table_header, text="➕ Thêm tài khoản", width=150, height=35,
                               fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5,
                               command=self.add_new_account)
        add_button.pack(side=tk.RIGHT, pady=10)

        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
                                  fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
                                  command=self.export_json)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        title_label = tk.Label(table_header, text="Danh sách tài khoản", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Table container
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Header row (table columns)
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        self.headers = ["Tên đăng nhập", "Họ và tên", "Email", "Số điện thoại", "Chức vụ", "Trạng thái", "Thao tác"]
        self.header_widths = [120, 180, 180, 120, 100, 100, 120] 

        for i, width in enumerate(self.header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, header in enumerate(self.headers):
            label = tk.Label(header_frame, text=header, font=("Arial", 12, "bold"),
                             bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

        # Scrollable area
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=self.canvas.yview,
                                 width=12, corner_radius=6,
                                 fg_color="white", bg_color="white",
                                 button_color="#57a1f8", button_hover_color="#2b8ee0")
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = CTkFrame(self.canvas, fg_color="white")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.populate_table(self.scrollable_frame, self.header_widths)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _clear_table_rows(self):
        """Xóa tất cả các widget hàng hiện có trong scrollable_frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def populate_table(self, scrollable_frame, header_widths):
        # Dữ liệu đã được tải bởi refresh_table hoặc __init__

        for i, account in enumerate(self.account_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#d0e6ff"

            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

            def on_enter(e, frame=row_frame, current_bg_color=bg_color):
                frame.configure(bg=hover_color)
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Frame)):
                        widget.configure(bg=hover_color)

            def on_leave(e, frame=row_frame, current_bg_color=bg_color):
                frame.configure(bg=current_bg_color)
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Frame)):
                        widget.configure(bg=current_bg_color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            row_frame.pack(fill=tk.X)

            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            display_data = [
                account.get("username", ""),
                account.get("fullname", ""),
                account.get("email", ""),
                account.get("phone", ""),
                account.get("role", ""),
                account.get("status", "")
            ]

            for j, text in enumerate(display_data):
                label = tk.Label(row_frame, text=text, font=("Arial", 11),
                                 bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=6, padx=5, pady=5)

            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                   fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda acc=account: self.view_account_detail(acc))
            detail_btn.pack(side=tk.LEFT, padx=2)

            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                   fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda uname=account.get('username'): self.delete_account_by_username(uname))
            delete_btn.pack(side=tk.LEFT, padx=2)

    def view_account_detail(self, account_data):
        if self.navigation_callback:
            # Nếu có navigation_callback, chuyển màn hình thông qua nó
            self.navigation_callback('account_detail', account_data, self.account_data, self.refresh_table)
        else:
            # Nếu chạy độc lập, mở cửa sổ chi tiết mới
            self.open_account_detail_window(account_data)

    def add_new_account(self):
        if self.navigation_callback:
            self.navigation_callback('account_detail', None, self.account_data, self.refresh_table)
        else:
            self.open_account_detail_window(None)

    def open_account_detail_window(self, account_data):
        # Khi chuyển sang màn hình chi tiết trong chế độ độc lập,
        # cần xóa các widget hiện tại của màn hình danh sách.
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Khởi tạo AccountDetailGui với master là self.master (content_frame)
        # và truyền callback để refresh lại AccountList khi dữ liệu được lưu
        account_detail_gui = AccountDetailGui(self.master, account_data, 
                                              all_accounts_data=self.account_data, 
                                              save_callback=self.refresh_table)

    def delete_account_by_username(self, username):
        self.load_data_account_from_file() # Tải lại dữ liệu để đảm bảo cập nhật nhất

        if not self.account_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xóa.")
            return

        acc_fullname = "N/A"
        for acc in self.account_data:
            if acc.get("username") == username:
                acc_fullname = acc.get("fullname", "Tài khoản không tên")
                break

        result = messagebox.askyesno("Xác nhận",
                                     f"Bạn có chắc chắn muốn xóa tài khoản '{acc_fullname}' (Username: {username})?\nHành động này không thể hoàn tác!")
        if result:
            self.account_data = [acc for acc in self.account_data if acc.get("username") != username]
            self.save_data_account_to_file()
            self.refresh_table() # Làm mới bảng sau khi xóa
            messagebox.showinfo("Thành công", f"Đã xóa tài khoản '{acc_fullname}' khỏi hệ thống.")

    def export_json(self):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Lưu file JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.account_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def refresh_table(self):
        """Làm mới lại toàn bộ UI của bảng để hiển thị dữ liệu mới"""
        self.load_data_account_from_file() # Tải lại dữ liệu mới nhất
        self._clear_table_rows() # Xóa các hàng cũ
        self.populate_table(self.scrollable_frame, self.header_widths) # Vẽ lại các hàng mới

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback


# Chạy test độc lập
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách tài khoản")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False) # Có thể đổi thành True nếu muốn thay đổi kích thước

    window_width = 1100
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Tạo một file account.json giả để test
    initial_accounts_for_list = [
        {'username': 'admin', 'email': 'admin@hospital.com', 'fullname': 'Nguyễn Văn Admin',
         'phone': '0901234567', 'role': 'Admin', 'status': 'Hoạt động', 'password_hash': 'admin123'},
        {'username': 'user01', 'email': 'user01@hospital.com', 'fullname': 'Trần Thị User',
         'phone': '0912345678', 'role': 'User', 'status': 'Hoạt động', 'password_hash': 'user123'},
    ]
    with open("account.json", "w", encoding="utf-8") as f:
        json.dump(initial_accounts_for_list, f, ensure_ascii=False, indent=2)

    app = AccountListGui(content_frame) # Truyền content_frame vào làm master
    root.mainloop()

    # Dọn dẹp file giả sau khi test
    if os.path.exists("account.json"):
        os.remove("account.json")