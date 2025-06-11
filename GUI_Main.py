import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkScrollbar
import GUI_xetnghiem

# Import các GUI khác
try:
    from GUI_PatientList import PatientListGui
    from GUI_StaffList import StaffListGui
    from GUI_AccountList import AccountListGui
    print("✓ Tất cả các GUI đã được import thành công.")
except ImportError as e:
    print(f"Lỗi import GUI: {e}")

class MainGui():
    def __init__(self, master, user_role=None): # Thêm tham số user_role
        self.master = master
        self.user_role = user_role # Lưu vai trò người dùng
        self.current_content = None
        self.setup_ui()
        self.show_home()

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
                                 corner_radius=5, command=self.logout_and_show_login) # Thay đổi command
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
        """Tạo các nút menu với sự kiện click và phân quyền"""
        menu_items = [
            ("Trang chủ", "home.png", self.show_home),
            ("Khám bệnh", "check-list.png", self.show_xetnghiem),
            ("Danh sách bệnh nhân", "check-list.png", self.show_patient_list),
            ("Danh sách nhân viên", "check-list.png", self.show_staff_list),
            # "Danh sách tài khoản hệ thống" chỉ hiển thị cho Admin
            ("Cài đặt", "gear.png", self.show_settings)
        ]

        if self.user_role == "Admin": # Chỉ hiển thị nút này nếu người dùng là Admin
            menu_items.insert(4, ("Danh sách tài khoản hệ thống", "profile.png", self.show_account_list)) # Chèn vào vị trí mong muốn

        for item in menu_items:
            name, icon_file, command = item
            try:
                # Tạo đường dẫn icon (giả sử thư mục 'icon' nằm ngang hàng với script)
                icon_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "icon", icon_file))

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

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        """Hiển thị trang chủ"""
        self.clear_content()

        home_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        home_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = home_frame

        title = tk.Label(home_frame, text="Trang chủ", font=("Arial", 24, "bold"),
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)

        welcome_text = f"""
        Chào mừng bạn đến với Hệ thống quản lý bệnh nhân nhiễm trùng huyết!
        Bạn đang đăng nhập với vai trò: {self.user_role if self.user_role else "Khách"}

        Hệ thống cung cấp các chức năng:
        • Quản lý danh sách bệnh nhân
        • Quản lý danh sách nhân viên y tế
        • Quản lý tài khoản hệ thống (chỉ dành cho Admin)
        • Báo cáo và thống kê

        Vui lòng chọn menu bên trái để bắt đầu sử dụng.
        """

        content_label = tk.Label(home_frame, text=welcome_text, font=("Arial", 12),
                                bg="#f8f9fa", fg="#333", justify=tk.LEFT)
        content_label.pack(pady=20)

        stats_frame = tk.Frame(home_frame, bg="#f8f9fa")
        stats_frame.pack(pady=20)

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

    from GUI_xetnghiem import XetNghiemFrame

    def show_xetnghiem(self):
        if hasattr(self, 'current_content') and self.current_content:
            self.current_content.destroy()

        xetnghiem_frame = GUI_xetnghiem.XetNghiemFrame(self.content_frame)
        xetnghiem_frame.pack(expand=True, fill="both")

        self.current_content = xetnghiem_frame
        self.xetnghiem_gui = xetnghiem_frame

    def show_patient_list(self):
        """Hiển thị danh sách bệnh nhân"""
        self.clear_content()
        try:
            patient_gui = PatientListGui(self.content_frame)
            self.current_content = self.content_frame.winfo_children()[-1] if self.content_frame.winfo_children() else None
        except Exception as e:
            self.show_error("Lỗi tải danh sách bệnh nhân", str(e))

    def logout_and_show_login(self):
        """Đăng xuất và hiển thị lại trang đăng nhập."""
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"):
            self.master.destroy()  # Đóng cửa sổ MainGui
            # Mở lại cửa sổ đăng nhập
            import GUI_LogIn # Import lại GUI_LogIn
            login_root = tk.Tk()
            login_gui = GUI_LogIn.LoginGui(login_root) # Tạo lại đối tượng LoginGui với root mới
            # Thiết lập lại kích thước và vị trí cửa sổ đăng nhập như ban đầu
            login_root.title("Đăng nhập hệ thống quản lý bệnh nhân nhiễm trùng huyết")
            login_root.configure(bg="#fff")
            login_root.resizable(False, False)
            window_width = 925
            window_height = 500
            screen_width = login_root.winfo_screenwidth()
            screen_height = login_root.winfo_screenheight()
            center_x = int((screen_width - window_width) / 2)
            center_y = int((screen_height - window_height) / 2)
            login_root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

            # Tải lại ảnh nền cho form login
            CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
            IMG_PATH = os.path.normpath(os.path.join(CURRENT_DIR, "background_form_login.png"))
            bg_image_raw = Image.open(IMG_PATH)
            bg_image_raw = bg_image_raw.resize((400, 400), Image.Resampling.LANCZOS)
            bg_image = ImageTk.PhotoImage(bg_image_raw)
            bg_label = tk.Label(login_root, image=bg_image, bg="white")
            bg_label.place(x=50, y=60)
            bg_label.image = bg_image # Giữ tham chiếu để tránh bị garbage collected
            login_root.mainloop()


    def show_staff_list(self):
        """Hiển thị danh sách nhân viên"""
        self.clear_content()
        try:
            staff_gui = StaffListGui(self.content_frame)
            self.current_content = self.content_frame.winfo_children()[-1] if self.content_frame.winfo_children() else None
        except Exception as e:
            self.show_error("Lỗi tải danh sách nhân viên", str(e))

    def show_account_list(self):
        """Hiển thị danh sách tài khoản (chỉ dành cho Admin)"""
        if self.user_role == "Admin":
            self.clear_content()
            try:
                account_gui = AccountListGui(self.content_frame)
                self.current_content = self.content_frame.winfo_children()[-1] if self.content_frame.winfo_children() else None
            except Exception as e:
                self.show_error("Lỗi tải danh sách tài khoản", str(e))
        else:
            messagebox.showwarning("Quyền truy cập", "Bạn không có quyền truy cập chức năng này.")
            self.show_home() # Quay về trang chủ nếu không có quyền

    def show_settings(self):
        """Hiển thị trang cài đặt"""
        self.clear_content()

        settings_frame = tk.Frame(self.content_frame, bg="#f8f9fa")
        settings_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.current_content = settings_frame

        title = tk.Label(settings_frame, text="Cài đặt hệ thống", font=("Arial", 24, "bold"),
                        bg="#f8f9fa", fg="#57a1f8")
        title.pack(pady=20)

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

# Phần này không chạy khi GUI_Main được import, chỉ chạy khi nó là main script
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hệ thống quản lý bệnh nhân nhiễm trùng huyết")
    root.configure(bg="#fff")
    root.resizable(False, False)

    window_width = 1400
    window_height = 700

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)

    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Khi chạy trực tiếp GUI_Main.py, không có user_role ban đầu.
    # Trong môi trường thực, MainGui sẽ được khởi tạo sau khi đăng nhập thành công.
    main_gui = MainGui(root, user_role="Admin") # Ví dụ: giả định vai trò Admin khi chạy độc lập để test
    # Nếu bạn muốn test mà không có vai trò, hãy dùng: main_gui = MainGui(root)

    root.mainloop()