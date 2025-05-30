import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from controllers.main_controller import MainController

class logingui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Đăng nhập hệ thống quản lý bệnh nhân nhiễm trùng huyết")
        self.master.configure(bg="#fff")
        self.master.resizable(False, False)
        self.controller = MainController(self)
        self.center_window(width=925, height=500)
        self.load_background_image()
        self.build_login_ui()

    def center_window(self,width=925,height=500):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def load_background_image(self):
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        IMG_PATH = os.path.normpath(os.path.join(CURRENT_DIR, "..", "assets", "background_form_login.png"))

        if os.path.exists(IMG_PATH):
            bg_image_raw = Image.open(IMG_PATH)
            bg_image_raw = bg_image_raw.resize((400, 400), Image.Resampling.LANCZOS)  # Resize to fit the window
            self.bg_image = ImageTk.PhotoImage(bg_image_raw)
            bg_label = tk.Label(self.master, image=self.bg_image, bg="white")
            bg_label.place(x=50, y=60)
        else:
            messagebox.showerror("Error", "Background image not found.")

    def build_login_ui(self):

         # Giao diện người dùng
        frame = tk.Frame(self.master, width=350, height=350, bg="white")
        frame.place(x=480, y=70)
        
        # Tiêu đề
        header = tk.Label(frame, text="Đăng nhập", font=("Arial", 20, "bold"), bg="white", fg="#57a1f8")
        header.place(relx=0.5, y=20, anchor=tk.CENTER)

        # Tạo các trường nhập liệu
        # Tên đăng nhập
        self.username_entry = tk.Entry(frame, width=30 ,fg="black", border=0, bg="white", font=("Arial", 12))
        self.username_entry.place(x=30, y=80)
        self.controller.setup_placeholder(self.username_entry, 'Tên đăng nhập')
        frame_username = tk.Frame(frame, width=300, height=2, bg="black").place(x=25, y=105)

        # Mật khẩu
        self.password_entry = tk.Entry(frame, width=30, fg="black", border=0, bg="white", font=("Arial", 12), show="*")
        self.password_entry.place(x=30, y=150)
        self.controller.setup_placeholder(self.password_entry, 'Mật khẩu', is_password=True)
        frame_password = tk.Frame(frame, width=300, height=2, bg="black").place(x=25, y=175)

        #Nút ẩn hiện mật khẩu
        toggle_btn = tk.Button(frame, text="👁", command=lambda:self.controller.toggle_password(self.password_entry, toggle_btn),bd=0, bg="white", border=0, font=("Arial", 12))
        toggle_btn.place(x=300, y=140)

        # Nút đăng nhập
        login_button = CTkButton(master=frame, text="Đăng nhập", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9", corner_radius=5,command=self.controller.handle_login)
        login_button.place(x=35, y=204)

        # Nút đăng nhập bằng gmail

        # Đường dẫn ảnh icon Google
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.normpath(os.path.join(CURRENT_DIR, "..","assets", "google_icon-icons.com_62736.ico"))
        icon_raw = Image.open(icon_path)
        google_icon = CTkImage(light_image=icon_raw, dark_image=icon_raw, size=(20, 20))

        gmail_button = CTkButton(master=frame, text="Đăng nhập bằng Gmail", width=280, height=35, fg_color="#57a1f8", text_color="white",hover_color="#4a8bc9",corner_radius=5, image=google_icon, compound="right")
        gmail_button.place(x=35, y=250)

        # Lưu biến google_icon tránh bị garbage collector xóa
        gmail_button.image = google_icon

        # Nút quên mật khẩu
        forgot_password = tk.Label(frame, text="Quên mật khẩu?", bg="white", fg="#57a1f8", font=("Arial", 9))
        forgot_password.place(relx=0.5, y=300, anchor=tk.CENTER)
        self.controller.apply_hover_effect_text(forgot_password)


        

     