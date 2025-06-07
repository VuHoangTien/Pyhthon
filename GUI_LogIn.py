import os
import tkinter as tk
from PIL import Image, ImageTk
from LogIn_Event import LoginEvent
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
import sys


def resource_path(relative_path):
    """Trả về đường dẫn phù hợp cả khi chạy script lẫn .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class LoginGui():
    def __init__(self,master):
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):

        # Giao diện người dùng
        frame = tk.Frame(self.master, width=350, height=350, bg="white")  # Sửa root thành self.master
        frame.place(x=480, y=70)
        
        # Tiêu đề
        header = tk.Label(frame, text="Đăng nhập", font=("Arial", 20, "bold"), bg="white", fg="#57a1f8")
        header.place(relx=0.5, y=20, anchor=tk.CENTER)

        # Tạo các trường nhập liệu
        # Tên đăng nhập
        self.username_entry = tk.Entry(frame, width=30 ,fg="black", border=0, bg="white", font=("Arial", 12))
        self.username_entry.place(x=30, y=80)
        LoginEvent.setup_placeholder(self.username_entry, 'Tên đăng nhập')
        frame_username = tk.Frame(frame, width=300, height=2, bg="black").place(x=25, y=105)

        # Mật khẩu
        self.password_entry = tk.Entry(frame, width=30, fg="black", border=0, bg="white", font=("Arial", 12), show="*")
        self.password_entry.place(x=30, y=150)
        LoginEvent.setup_placeholder(self.password_entry, 'Mật khẩu', is_password=True)
        frame_password = tk.Frame(frame, width=300, height=2, bg="black").place(x=25, y=175)

        # Khởi tạo đối tượng LoginEvent với 2 entry và master
        self.login_event = LoginEvent(self.username_entry, self.password_entry, self.master)

        #Nút ẩn hiện mật khẩu
        toggle_btn = tk.Button(frame, text="👁", command=lambda:self.login_event.toggle_password(toggle_btn),bd=0, bg="white", border=0, font=("Arial", 12))
        toggle_btn.place(x=300, y=140)

        # Nút đăng nhập
        login_button = CTkButton(master=frame, text="Đăng nhập", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9", corner_radius=5,command=self.login_event.login)
        login_button.place(x=35, y=204)

        # Nút đăng nhập bằng gmail
        # Sử dụng resource_path cho Google icon
        icon_path = resource_path("google_icon-icons.com_62736.ico")
        
        try:
            if os.path.exists(icon_path):
                icon_raw = Image.open(icon_path)
                google_icon = CTkImage(light_image=icon_raw, dark_image=icon_raw, size=(20, 20))
                
                gmail_button = CTkButton(master=frame, text="Đăng nhập bằng Gmail", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9",corner_radius=5, image=google_icon, compound="right")
                gmail_button.place(x=35, y=250)
                
                # Lưu biến google_icon tránh bị garbage collector xóa
                gmail_button.image = google_icon
            else:
                # Tạo button không có icon nếu không tìm thấy file
                gmail_button = CTkButton(master=frame, text="Đăng nhập bằng Gmail", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9",corner_radius=5)
                gmail_button.place(x=35, y=250)
                print(f"Warning: Google icon not found at {icon_path}")
        except Exception as e:
            # Tạo button không có icon nếu có lỗi
            gmail_button = CTkButton(master=frame, text="Đăng nhập bằng Gmail", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9",corner_radius=5)
            gmail_button.place(x=35, y=250)
            print(f"Error loading Google icon: {e}")

        # Nút quên mật khẩu
        forgot_password = tk.Label(frame, text="Quên mật khẩu?", bg="white", fg="#57a1f8", font=("Arial", 9))
        forgot_password.place(relx=0.5, y=300, anchor=tk.CENTER)
        LoginEvent.apply_hover_effect_text(forgot_password)


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Đăng nhập hệ thống quản lý bệnh nhân nhiễm trùng huyết")
root.configure(bg="#fff")
root.resizable(False, False)

# Kích thước cửa sổ
window_width = 925
window_height = 500

# Lấy kích thước màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Tính toán vị trí để căn giữa
center_x = int((screen_width - window_width) / 2)
center_y = int((screen_height - window_height) / 2)

root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Tạo hình ảnh background với xử lý lỗi
IMG_PATH = resource_path("background_form_login.png")

try:
    if os.path.exists(IMG_PATH):
        bg_image_raw = Image.open(IMG_PATH)
        bg_image_raw = bg_image_raw.resize((400, 400), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image_raw)
        bg_label = tk.Label(root, image=bg_image, bg="white")
        bg_label.place(x=50, y=60)
        
        # Lưu reference để tránh garbage collection
        root.bg_image = bg_image
    else:
        print(f"Warning: Background image not found at {IMG_PATH}")
        # Tạo một label thay thế nếu không có hình
        bg_label = tk.Label(root, text="HOSPITAL\nMANAGEMENT\nSYSTEM", 
                           font=("Arial", 24, "bold"), 
                           bg="lightblue", fg="white",
                           width=20, height=15)
        bg_label.place(x=50, y=60)
        
except Exception as e:
    print(f"Error loading background image: {e}")
    # Tạo một label thay thế nếu có lỗi
    bg_label = tk.Label(root, text="HOSPITAL\nMANAGEMENT\nSYSTEM", 
                       font=("Arial", 24, "bold"), 
                       bg="lightblue", fg="white",
                       width=20, height=15)
    bg_label.place(x=50, y=60)

# Khởi tạo giao diện đăng nhập
login_gui = LoginGui(root)

# Chạy vòng lặp GUI
root.mainloop()