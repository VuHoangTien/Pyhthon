import tkinter as tk
from tkinter import messagebox

class LoginEvent:
    # Thông tin đăng nhập giả lập
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "admin123"

    def __init__(self, username_entry, password_entry):
        self.username_entry = username_entry
        self.password_entry = password_entry

        #Biến trạng thái ẩn hiện
        self.is_password_visible = tk.BooleanVar(value=False)

    #Hàm xử lý đăng nhập
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.VALID_USERNAME and password == self.VALID_PASSWORD:
            messagebox.showinfo("Đăng nhập thành công", "Chào mừng bạn đến với hệ thống quản lý bệnh nhân!")
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng.")

    #Hàm xử lý placeholder động
    @staticmethod 
    def setup_placeholder(entry, placeholder_text,is_password=False):
        def on_entry_click(event):
            """Xóa placeholder khi nhấp vào trường nhập liệu."""
            if event.widget.get() == placeholder_text:
                event.widget.delete(0, "end")  # Xóa nội dung
                event.widget.config(fg='black')  # Đặt màu chữ thành đen
                if is_password:
                    event.widget.config(show="*")

        def on_focus_out(event):
            """Đặt lại placeholder nếu trường nhập liệu trống."""
            if event.widget.get() == "":
                event.widget.insert(0, placeholder_text)
                event.widget.config(fg='grey')  # Đặt màu chữ thành xám
                if is_password:
                    event.widget.config(show="")
            else:
                # Khi có dữ liệu, nếu là password, thì ẩn ký tự
                if is_password:
                    entry.config(show="*")
                entry.config(fg='black')
               
            # Khởi tạo placeholder
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')

        if is_password:
            entry.config(show="")  # không ẩn ký tự khi hiển thị placeholder

        # Gắn sự kiện
        entry.bind("<FocusIn>", on_entry_click)
        entry.bind("<FocusOut>", on_focus_out)

    #Biến trạng thái hiện ẩn 
    def toggle_password(self, toggle_button):
        current_text = self.password_entry.get()
        if current_text == "Mật khẩu":
            return
        if self.is_password_visible.get(): 
            self.password_entry.config(show="*")
            toggle_button.config(text="👁")
            self.is_password_visible.set(False)
        else:
            self.password_entry.config(show="")
            toggle_button.config(text="Ẩn")
            self.is_password_visible.set(True)
            
    # Tạo hiệu ứng khi di chuột qua text
    @staticmethod
    def apply_hover_effect_text(label, hover_color="red", normal_color="#57a1f8"):
        def on_enter(e):
            label['fg'] = hover_color

        def on_leave(e):
            label['fg'] = normal_color

        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)