import os
import tkinter as tk
from PIL import Image, ImageTk
from LogIn_Event import LoginEvent
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage

class LoginGui():
    def __init__(self,master):
        self.master = master
        self.setup_ui()
    
    def setup_ui(self):

        # Giao diện người dùng
        frame = tk.Frame(root, width=350, height=350, bg="white")
        frame.place(x=480, y=70)
        
        # Tiêu đề
        header = tk.Label(frame, text="Đăng nhập", font=("Arial", 20, "bold"), bg="white", fg="#57a1f8")
        header.place(x=100, y=10)

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

        # Khởi tạo đối tượng LoginEvent với 2 entry
        self.login_event = LoginEvent(self.username_entry, self.password_entry)

        #Nút ẩn hiện mật khẩu
        toggle_btn = tk.Button(frame, text="👁", command=lambda:self.login_event.toggle_password(toggle_btn),bd=0, bg="white", border=0, font=("Arial", 12))
        toggle_btn.place(x=300, y=140)

        # Nút đăng nhập
        login_button = CTkButton(master=frame, text="Đăng nhập", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9", corner_radius=5,command=self.login_event.login)
        login_button.place(x=35, y=204)

        # Nút đăng nhập bằng gmail

        # Đường dẫn ảnh icon Google
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.normpath(os.path.join(CURRENT_DIR, "..", "Python", "icon", "google_icon-icons.com_62736.ico"))
        icon_raw = Image.open(icon_path)
        google_icon = CTkImage(light_image=icon_raw, dark_image=icon_raw, size=(20, 20))

        gmail_button = CTkButton(master=frame, text="Đăng nhập bằng Gmail", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9",corner_radius=5, image=google_icon, compound="right")
        gmail_button.place(x=35, y=250)

        # Lưu biến google_icon tránh bị garbage collector xóa
        gmail_button.image = google_icon

        # Nút quên mật khẩu
        forgot_password = tk.Label(frame, text="Quên mật khẩu?", bg="white", fg="#57a1f8", font=("Arial", 9))
        forgot_password.place(x=70, y=300)
        LoginEvent.apply_hover_effect_text(forgot_password)

        # Nút đăng ký
        register = tk.Label(frame, text="Đăng ký", bg="white", fg="#57a1f8", font=("Arial", 9))
        register.place(x=220, y=300)
        LoginEvent.apply_hover_effect_text(register)


# Tạo cửa sổ chính
root = tk.Tk()
root.title("Đăng nhập hệ thống quản lý bệnh nhân nhiễm trùng huyết")
root.geometry("925x500+300+200")
root.configure(bg="#fff")
root.resizable(False, False)

# Tạo đường dẫn ảnh 
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.normpath(os.path.join(CURRENT_DIR, "..", "Python", "img", "background_form_login.png"))

#Tạo hình ảnh
bg_image_raw = Image.open(IMG_PATH)
bg_image_raw = bg_image_raw.resize((400, 400), Image.Resampling.LANCZOS)  # Resize to fit the window
bg_image = ImageTk.PhotoImage(bg_image_raw)
bg_label = tk.Label(root, image=bg_image, bg="white")
bg_label.place(x=50, y=60)

# Khởi tạo giao diện đăng nhập
login_gui = LoginGui(root)

# Chạy vòng lặp GUI
root.mainloop()











