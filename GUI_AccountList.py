import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkScrollbar

class AccountListGui():
    def __init__(self, master):
        self.master = master  # Đây sẽ là content_frame từ GUI_Main
        self.setup_ui()
 
    def setup_ui(self):
        # Chỉ tạo phần content, không tạo header và menu
        
        # Header của bảng với nút thêm
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        # Nút thêm tài khoản
        add_button = CTkButton(master=table_header, text="➕ Thêm tài khoản", width=150, height=35, 
                            fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5)
        add_button.pack(side=tk.RIGHT, pady=10)

        # Nút xuất file Json
        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35, 
                            fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Tiêu đề căn giữa
        title_label = tk.Label(table_header, text="Danh sách tài khoản hệ thống", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Frame chứa bảng với scrollbar
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Header của bảng
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["STT", "Tên đăng nhập", "Mật khẩu", "Gmail", "Số điện thoại", "Thao tác"]
        header_widths = [60, 150, 120, 250, 150, 180]

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

        # Data mẫu cho tài khoản
        accounts_data = [
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

        # Tạo các dòng dữ liệu
        for i, account in enumerate(accounts_data):
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

            # Hiển thị thông tin tài khoản
            for j, (data, width) in enumerate(zip(account, header_widths[:-1])):
                # Ẩn mật khẩu bằng dấu *
                if j == 2:  # Cột mật khẩu
                    display_text = "*" * len(str(data))
                else:
                    display_text = str(data)
                    
                label = tk.Label(row_frame, text=display_text, font=("Arial", 11), 
                                bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")
            
            # Frame chứa các nút thao tác
            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=len(account), padx=5, pady=5)
            
            # Nút xem chi tiết
            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                corner_radius=3, font=("Arial", 9))
            detail_btn.pack(side=tk.LEFT, padx=2)
            
            # Nút sửa
            edit_btn = CTkButton(master=action_frame, text="Sửa", width=50, height=28,
                                fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                                corner_radius=3, font=("Arial", 9))
            edit_btn.pack(side=tk.LEFT, padx=2)
            
            # Nút xóa
            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                corner_radius=3, font=("Arial", 9))
            delete_btn.pack(side=tk.LEFT, padx=2)

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)


# Test riêng biệt (chỉ dành cho development)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách tài khoản")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)

    window_width = 1100
    window_height = 600
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