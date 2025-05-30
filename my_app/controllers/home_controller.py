import tkinter as tk
from tkinter import messagebox
from models.data_models import load_users

class HomeController:
    def __init__(self, view):
        self.view = view
        self.users = load_users()
        self.is_password_visible = tk.BooleanVar(value=False)

    def open_home_gui(self):
        try:
            from views.Home_Gui import HomeGui
            
            # Đóng cửa sổ đăng nhập hiện tại
            login_window = self.view.master

            # Tạo cửa sổ mới cho HomeGui
            main_window = tk.Tk()
            main_window.title("Hệ thống quản lý bệnh nhân nhiễm trùng huyết")
            main_window.configure(bg="#fff")
            main_window.resizable(False, False)
            
            # Kích thước cửa sổ
            window_width = 1400
            window_height = 700

            # Lấy kích thước màn hình
            screen_width = main_window.winfo_screenwidth()
            screen_height = main_window.winfo_screenheight()

            # Tính toán vị trí để căn giữa
            center_x = int((screen_width - window_width) / 2)
            center_y = int((screen_height - window_height) / 3)

            main_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

            # Khởi tạo HomeGui
            home_gui = HomeGui(main_window)

            # Đóng cửa sổ đăng nhập
            login_window.destroy()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở giao diện chính: {str(e)}")

