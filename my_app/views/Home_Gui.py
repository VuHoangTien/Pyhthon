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
from controllers.main_controller import MainController
from controllers.home_controller import HomeController


class HomeGui():
    def __init__(self, master):
        self.master = master
        self.current_content = None  # Lưu nội dung hiện tại
        self.build_home_ui()
        self.show_home()  # Hiển thị trang chủ mặc định

    def show_home(self):
        """Hiển thị trang chủ"""
        if self.current_content:
            self.current_content.destroy()
        self.current_content = HomeController(self)

    def build_home_ui(self):
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
                # Sửa đường dẫn icon - tương tự như cách bạn load background image
                CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
                icon_path = os.path.normpath(os.path.join(CURRENT_DIR, "..", "assets", icon_file))
                
                if os.path.exists(icon_path):
                    print(f"✓ Tìm thấy icon: {icon_path}")
                    icon_raw = Image.open(icon_path)
                    icon_image = CTkImage(light_image=icon_raw, dark_image=icon_raw, size=(20, 20))
                    
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

    def show_login(self):
        """Đăng xuất và quay về trang đăng nhập"""
        # Hiển thị hộp thoại xác nhận đăng xuất
        confirm = messagebox.askyesno(
            "Xác nhận đăng xuất", 
            "Bạn có chắc chắn muốn đăng xuất khỏi hệ thống?",
            icon='question'
        )
        
        # Nếu người dùng chọn "No", không làm gì cả
        if not confirm:
            return
        
        try:
            # Import Login GUI
            from views.Login_Gui import logingui
            
            # Đóng cửa sổ chính hiện tại
            current_window = self.master
            
            # Tạo cửa sổ mới cho đăng nhập
            login_window = tk.Tk()
            login_window.title("Đăng nhập hệ thống quản lý bệnh nhân nhiễm trùng huyết")
            login_window.configure(bg="#fff")
            login_window.resizable(False, False)
            
            # Khởi tạo Login GUI
            login_gui = logingui(master=login_window)
            
            # Đóng cửa sổ chính
            current_window.destroy()
            
            # Hiển thị thông báo đăng xuất thành công
            messagebox.showinfo("Đăng xuất", "Đăng xuất thành công!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể quay về trang đăng nhập: {str(e)}")
    def show_patient_list(self):
        """Hiển thị danh sách bệnh nhân"""
        self.clear_content()
        
        # Tạo frame cho danh sách bệnh nhân
        patient_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        patient_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = patient_frame
        
        # Tiêu đề
        title = tk.Label(patient_frame, text="Danh sách bệnh nhân", font=("Arial", 24, "bold"), 
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)
        
        # Nội dung tạm thời
        content_text = "Trang danh sách bệnh nhân đang được phát triển..."
        content_label = tk.Label(patient_frame, text=content_text, font=("Arial", 12), 
                                bg="#f8f9fa", fg="#333")
        content_label.pack(pady=20)

    def show_staff_list(self):
        """Hiển thị danh sách nhân viên"""
        self.clear_content()
        
        # Tạo frame cho danh sách nhân viên
        staff_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        staff_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = staff_frame
        
        # Tiêu đề
        title = tk.Label(staff_frame, text="Danh sách nhân viên", font=("Arial", 24, "bold"), 
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)
        
        # Nội dung tạm thời
        content_text = "Trang danh sách nhân viên đang được phát triển..."
        content_label = tk.Label(staff_frame, text=content_text, font=("Arial", 12), 
                                bg="#f8f9fa", fg="#333")
        content_label.pack(pady=20)

    def show_account_list(self):
        """Hiển thị danh sách tài khoản"""
        self.clear_content()
        
        # Tạo frame cho danh sách tài khoản
        account_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        account_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = account_frame
        
        # Tiêu đề
        title = tk.Label(account_frame, text="Danh sách tài khoản hệ thống", font=("Arial", 24, "bold"), 
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)
        
        # Nội dung tạm thời
        content_text = "Trang danh sách tài khoản đang được phát triển..."
        content_label = tk.Label(account_frame, text=content_text, font=("Arial", 12), 
                                bg="#f8f9fa", fg="#333")
        content_label.pack(pady=20)

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
