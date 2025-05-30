import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkScrollbar
from models.data_models import load_users

class AccountListGui():
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.setup_ui()
 
    def setup_ui(self):
        """Tạo giao diện danh sách tài khoản"""
        # Tạo frame chính cho trang tài khoản
        self.account_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        self.account_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Tiêu đề trang
        title = tk.Label(self.account_frame, text="Danh sách tài khoản hệ thống", 
                        font=("Arial", 24, "bold"), bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=(0, 20))
        
        # Header của bảng với các nút chức năng
        table_header = tk.Frame(self.account_frame, bg="#f8f9fa", height=60)
        table_header.pack(fill=tk.X, pady=(0, 10))

        # Nút thêm tài khoản
        add_button = CTkButton(master=table_header, text="➕ Thêm tài khoản", width=150, height=35, 
                            fg_color="#28a745", text_color="white", hover_color="#218838", 
                            corner_radius=5, command=self.add_account)
        add_button.pack(side=tk.RIGHT, pady=10)

        # Nút xuất file JSON
        export_button = CTkButton(master=table_header, text="📄 Xuất JSON", width=130, height=35, 
                            fg_color="#ffc107", text_color="white", hover_color="#e0a800", 
                            corner_radius=5, command=self.export_json)
        export_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        # Nút làm mới
        refresh_button = CTkButton(master=table_header, text="🔄 Làm mới", width=120, height=35, 
                            fg_color="#6c757d", text_color="white", hover_color="#5a6268", 
                            corner_radius=5, command=self.refresh_data)
        refresh_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        # Frame chứa bảng với scrollbar
        table_container = CTkFrame(self.account_frame, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True)

        # Header của bảng
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=50)
        header_frame.pack(fill=tk.X)

        headers = ["STT", "Tên đăng nhập", "Mật khẩu", "Email", "Số điện thoại", "Thao tác"]
        header_widths = [80, 180, 120, 280, 150, 200]

        # Cấu hình trọng số cho các cột
        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, (header, width) in enumerate(zip(headers, header_widths)):
            label = tk.Label(header_frame, text=header, font=("Arial", 12, "bold"), 
                            bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=2, pady=10, sticky="ew")

        # Frame chứa Canvas và Scrollbar cho nội dung bảng
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        # Tạo Canvas và Scrollbar
        self.canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=self.canvas.yview,
                         width=15, corner_radius=6,
                         fg_color="#f8f9fa", bg_color="#f8f9fa",
                         button_color="#57a1f8", button_hover_color="#4a8bc9")
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollable_frame = CTkFrame(self.canvas, fg_color="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Load dữ liệu
        self.load_accounts_data()

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def load_accounts_data(self):
        """Load và hiển thị dữ liệu tài khoản"""
        # Data mẫu cho tài khoản
        self.accounts_data = [
            (1, "admin", "admin123", "admin@hospital.com", "0901234567"),
            (2, "doctor01", "doc123456", "doctor1@hospital.com", "0912345678"),
            (3, "nurse01", "nurse123", "nurse1@hospital.com", "0923456789"),
            (4, "manager", "manager456", "manager@hospital.com", "0934567890"),
            (5, "doctor02", "doc789012", "doctor2@hospital.com", "0945678901"),
            (6, "nurse02", "nurse456", "nurse2@hospital.com", "0956789012"),
            (7, "technician", "tech123", "tech@hospital.com", "0967890123"),
            (8, "pharmacist", "pharm789", "pharmacist@hospital.com", "0978901234"),
            (9, "receptionist", "recep123", "reception@hospital.com", "0989012345"),
            (10, "staff01", "staff456", "staff1@hospital.com", "0990123456"),
            (11, "doctor03", "docpass789", "doctor3@hospital.com", "0901122334"),
            (12, "nurse03", "nursepass", "nurse3@hospital.com", "0912233445")
        ]

        header_widths = [80, 180, 120, 280, 150, 200]

        # Xóa dữ liệu cũ nếu có
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Tạo các dòng dữ liệu
        for i, account in enumerate(self.accounts_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#e3f2fd"  # Màu xanh nhạt khi hover

            row_frame = tk.Frame(self.scrollable_frame, bg=bg_color, height=50)
            row_frame.pack(fill=tk.X, padx=2, pady=1)
            
            # Cấu hình trọng số cho các cột của mỗi dòng để khớp với header
            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            # Hiển thị thông tin tài khoản
            for j, (data, width) in enumerate(zip(account, header_widths[:-1])):
                # Ẩn mật khẩu bằng dấu *
                if j == 2:  # Cột mật khẩu
                    display_text = "*" * len(str(data))
                else:
                    display_text = str(data)
                    
                label = tk.Label(row_frame, text=display_text, font=("Arial", 10), 
                                bg=bg_color, anchor="center", wraplength=width-10)
                label.grid(row=0, column=j, padx=2, pady=10, sticky="ew")
            
            # Frame chứa các nút thao tác
            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=len(account), padx=5, pady=8)
            
            # Nút xem chi tiết
            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=55, height=30,
                                fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                corner_radius=4, font=("Arial", 9),
                                command=lambda acc=account: self.view_detail(acc))
            detail_btn.pack(side=tk.LEFT, padx=1)
            
            # Nút sửa
            edit_btn = CTkButton(master=action_frame, text="Sửa", width=45, height=30,
                                fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                                corner_radius=4, font=("Arial", 9),
                                command=lambda acc=account: self.edit_account(acc))
            edit_btn.pack(side=tk.LEFT, padx=1)
            
            # Nút xóa
            delete_btn = CTkButton(master=action_frame, text="Xóa", width=45, height=30,
                                fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                corner_radius=4, font=("Arial", 9),
                                command=lambda acc=account: self.delete_account(acc))
            delete_btn.pack(side=tk.LEFT, padx=1)

            # Gán sự kiện hover cho cả dòng
            self.bind_hover_events(row_frame, bg_color, hover_color)

    def bind_hover_events(self, row_frame, bg_color, hover_color):
        """Gán sự kiện hover cho dòng"""
        def on_enter(e):
            row_frame.configure(bg=hover_color)
            for widget in row_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=hover_color)
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=hover_color)

        def on_leave(e):
            row_frame.configure(bg=bg_color)
            for widget in row_frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=bg_color)
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=bg_color)

        row_frame.bind("<Enter>", on_enter)
        row_frame.bind("<Leave>", on_leave)

    def add_account(self):
        """Thêm tài khoản mới"""
        messagebox.showinfo("Thêm tài khoản", "Chức năng thêm tài khoản đang được phát triển...")

    def edit_account(self, account):
        """Sửa thông tin tài khoản"""
        messagebox.showinfo("Sửa tài khoản", f"Chỉnh sửa tài khoản: {account[1]}")

    def delete_account(self, account):
        """Xóa tài khoản"""
        confirm = messagebox.askyesno(
            "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa tài khoản '{account[1]}'?\n\nHành động này không thể hoàn tác!",
            icon='warning'
        )
        if confirm:
            messagebox.showinfo("Xóa tài khoản", f"Đã xóa tài khoản: {account[1]}")
            # TODO: Thực hiện xóa thực tế từ database

    def view_detail(self, account):
        """Xem chi tiết tài khoản"""
        detail_info = f"""
Thông tin chi tiết tài khoản:

STT: {account[0]}
Tên đăng nhập: {account[1]}
Email: {account[3]}
Số điện thoại: {account[4]}
Trạng thái: Hoạt động
Ngày tạo: 01/01/2024
Lần đăng nhập cuối: 30/05/2025
        """
        messagebox.showinfo("Chi tiết tài khoản", detail_info)

    def export_json(self):
        """Xuất dữ liệu ra file JSON"""
        messagebox.showinfo("Xuất JSON", "Chức năng xuất file JSON đang được phát triển...")

    def refresh_data(self):
        """Làm mới dữ liệu"""
        self.load_accounts_data()
        messagebox.showinfo("Làm mới", "Dữ liệu đã được cập nhật!")


# Test riêng biệt (chỉ dành cho development)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách tài khoản")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)

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
    account_list_gui = AccountListGui(content_frame)

    root.mainloop()