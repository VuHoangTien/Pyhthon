import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkScrollbar

# Import các GUI khác
try:
    from GUI_PatientList import PatientListGui
    from GUI_StaffList import StaffListGui
    from GUI_AccountList import AccountListGui
    print("✓ Tất cả các GUI đã được import thành công.")
except ImportError as e:
    print(f"Lỗi import GUI: {e}")

class MainGui():
    def __init__(self, master):
        self.master = master
        self.current_content = None  # Lưu nội dung hiện tại
        self.setup_ui()
        self.show_home()  # Hiển thị trang chủ mặc định
 
    def setup_ui(self):
        # Header frame
        self.header_frame = tk.Frame(self.master, width=1400, height=70, bg="#57a1f8")
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)
       
        # Tiêu đề
        header = tk.Label(self.header_frame, text="Hệ thống quản lý bệnh nhân nhiễm trùng huyết", 
                         font=("Arial", 20, "bold"), bg="#57a1f8", fg="white")
        header.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Nút đăng xuất
        logout_button = CTkButton(master=self.header_frame, text="Đăng xuất", width=100, height=30, 
                                 fg_color="#fff", text_color="#57a1f8", hover_color="#e0e0e0", 
                                 corner_radius=5, command=self.show_login)
        logout_button.configure(command=self.show_login)  # Gọi hàm show_login khi nhấn nút
        logout_button.place(x=1250, y=20)

        # Container chính
        main_container = tk.Frame(self.master, bg="white")
        main_container.pack(expand=True, fill=tk.BOTH)

        # Menu bên trái
        self.menu_frame = tk.Frame(main_container, width=300, bg="white")
        self.menu_frame.pack(fill=tk.Y, side=tk.LEFT)
        self.menu_frame.pack_propagate(False)

        # Tiêu đề menu
        menu_label = tk.Label(self.menu_frame, text="Menu", font=("Arial", 14, "bold"), bg="white")
        menu_label.pack(pady=10) 

        # Đường phân cách
        menu_separator = tk.Frame(self.menu_frame, width=200, height=2, bg="#e0e0e0")
        menu_separator.place(x=50, y=40)

        # Tạo các nút menu với command
        self.create_menu_buttons()

        # Content frame bên phải
        self.content_frame = tk.Frame(main_container, bg="#f8f9fa")
        self.content_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

    def create_menu_buttons(self):
        """Tạo các nút menu với sự kiện click"""
        menu_items = [
            ("Trang chủ", "home.png", self.show_home),
            ("Danh sách bệnh nhân", "check-list.png", self.show_patient_list),
            ("Danh sách nhân viên", "check-list.png", self.show_staff_list),
            ("Danh sách tài khoản hệ thống", "profile.png", self.show_account_list),
            ("Cài đặt", "gear.png", self.show_settings)
        ]
        
        for item in menu_items:
            name, icon_file, command = item
            try:
                # Tạo đường dẫn icon
                icon_path = os.path.join("icon", icon_file)
                
                if os.path.exists(icon_path):
                    print(f"✓ Tìm thấy icon: {icon_path}")
                    icon_image = CTkImage(Image.open(icon_path), size=(20, 20))
                    
                    btn = CTkButton(master=self.menu_frame, text=name, width=250, height=40, 
                                   fg_color="#fff", text_color="#57a1f8", hover_color="#e0e0e0", 
                                   corner_radius=5, anchor="w", image=icon_image, compound="left",
                                   command=command)
                else:
                    print(f"✗ Không tìm thấy icon: {icon_path}")
                    btn = CTkButton(master=self.menu_frame, text=name, width=250, height=40, 
                                   fg_color="#fff", text_color="#57a1f8", hover_color="#e0e0e0", 
                                   corner_radius=5, anchor="w", command=command)
                
                btn.pack(pady=5, padx=10, fill=tk.X)
                
            except Exception as e:
                print(f"Lỗi tạo menu {name}: {e}")
                btn = CTkButton(master=self.menu_frame, text=name, width=250, height=40, 
                               fg_color="#fff", text_color="#57a1f8", hover_color="#e0e0e0", 
                               corner_radius=5, anchor="w", command=command)
                btn.pack(pady=5, padx=10, fill=tk.X)

    def clear_content(self):
        """Xóa nội dung hiện tại trong content_frame"""
        if self.current_content:
            self.current_content.destroy()
            self.current_content = None
        
        # Xóa tất cả widget con trong content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Hiển thị trang chủ"""
        self.clear_content()
        
        # Tạo frame cho trang chủ
        home_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        home_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = home_frame
        
        # Tiêu đề trang chủ
        title = tk.Label(home_frame, text="Trang chủ", font=("Arial", 24, "bold"), 
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)
        
        # Nội dung chào mừng
        welcome_text = """
        Chào mừng bạn đến với Hệ thống quản lý bệnh nhân nhiễm trùng huyết!
        
        Hệ thống cung cấp các chức năng:
        • Quản lý danh sách bệnh nhân
        • Quản lý danh sách nhân viên y tế
        • Quản lý tài khoản hệ thống
        • Báo cáo và thống kê
        
        Vui lòng chọn menu bên trái để bắt đầu sử dụng.
        """
        
        content_label = tk.Label(home_frame, text=welcome_text, font=("Arial", 12), 
                                bg="#f8f9fa", fg="#333", justify=tk.LEFT)
        content_label.pack(pady=20)
        
        # Thống kê nhanh
        stats_frame = tk.Frame(home_frame, bg="#f8f9fa")
        stats_frame.pack(pady=20)
        
        # Các thẻ thống kê
        stats = [
            ("Tổng bệnh nhân", "156", "#28a745"),
            ("Nhân viên", "45", "#17a2b8"),
            ("Tài khoản", "23", "#ffc107")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_card = CTkFrame(stats_frame, fg_color=color, corner_radius=10)
            stat_card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            value_label = tk.Label(stat_card, text=value, font=("Arial", 20, "bold"), 
                                  bg=color, fg="white")
            value_label.pack(pady=5)
            
            label_text = tk.Label(stat_card, text=label, font=("Arial", 12), 
                                 bg=color, fg="white")
            label_text.pack(pady=(0, 10))

    def show_patient_list(self):
        """Hiển thị danh sách bệnh nhân"""
        self.clear_content()
        try:
            # Tạo instance của PatientListGui trong content_frame
            patient_gui = PatientListGui(self.content_frame)
            self.current_content = self.content_frame.winfo_children()[-1] if self.content_frame.winfo_children() else None
        except Exception as e:
            self.show_error("Lỗi tải danh sách bệnh nhân", str(e))

    def show_login(self):
        """Hiển thị trang đăng nhập"""
        self.master()
        
        # Tạo frame cho đăng nhập
        login_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        login_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = login_frame
        
        # Tiêu đề
        title = tk.Label(login_frame, text="Đăng nhập", font=("Arial", 24, "bold"), 
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)
        
        # Nội dung đăng nhập
        login_text = """
        Vui lòng nhập thông tin đăng nhập để truy cập hệ thống.
        
        Nếu bạn chưa có tài khoản, vui lòng liên hệ quản trị viên.
        """
        
        content_label = tk.Label(login_frame, text=login_text, font=("Arial", 12), 
                                bg="#f8f9fa", fg="#333", justify=tk.LEFT)
        content_label.pack(pady=20)

    def show_staff_list(self):
        """Hiển thị danh sách nhân viên"""
        self.clear_content()
        try:
            # Tạo instance của StaffListGui trong content_frame  
            staff_gui = StaffListGui(self.content_frame)
            self.current_content = self.content_frame.winfo_children()[-1] if self.content_frame.winfo_children() else None
        except Exception as e:
            self.show_error("Lỗi tải danh sách nhân viên", str(e))

    def show_account_list(self):
        """Hiển thị danh sách tài khoản"""
        self.clear_content()
        try:
            # Tạo instance của AccountListGui trong content_frame
            account_gui = AccountListGui(self.content_frame)
            self.current_content = self.content_frame.winfo_children()[-1] if self.content_frame.winfo_children() else None
        except Exception as e:
            self.show_error("Lỗi tải danh sách tài khoản", str(e))

    def show_settings(self):
        """Hiển thị trang cài đặt"""
        self.clear_content()
        
        # Tạo frame cho cài đặt
        settings_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        settings_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = settings_frame
        
        # Tiêu đề
        title = tk.Label(settings_frame, text="Cài đặt hệ thống", font=("Arial", 24, "bold"), 
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)
        
        # Nội dung cài đặt
        settings_text = """
        Trang cài đặt đang được phát triển...
        
        Các tính năng sắp có:
        • Cài đặt thông tin hệ thống
        • Quản lý quyền truy cập
        • Sao lưu và phục hồi dữ liệu
        • Cấu hình báo cáo
        """
        
        content_label = tk.Label(settings_frame, text=settings_text, font=("Arial", 12), 
                                bg="#f8f9fa", fg="#333", justify=tk.LEFT)
        content_label.pack(pady=20)

    def show_error(self, title, message):
        """Hiển thị thông báo lỗi"""
        error_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        error_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = error_frame
        
        error_title = tk.Label(error_frame, text=title, font=("Arial", 18, "bold"), 
                              bg="#f8f9fa", fg="#dc3545")
        error_title.pack(pady=20)
        
        error_message = tk.Label(error_frame, text=message, font=("Arial", 12), 
                                bg="#f8f9fa", fg="#666")
        error_message.pack(pady=10)

# Chạy ứng dụng chính
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hệ thống quản lý bệnh nhân nhiễm trùng huyết")
    root.configure(bg="#fff")
    root.resizable(False, False)

    # Kích thước cửa sổ
    window_width = 1400
    window_height = 700

    # Lấy kích thước màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Tính toán vị trí để căn giữa
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)

    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Khởi tạo giao diện chính
    main_gui = MainGui(root)

    # Chạy vòng lặp chính
    root.mainloop()