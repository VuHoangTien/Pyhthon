import tkinter as tk
from tkinter import messagebox
from models.data_models import load_users

class MainController:
    def __init__(self, view):
        self.view = view
        self.users = load_users()
        self.is_password_visible = tk.BooleanVar(value=False)

    def handle_login(self):
        
        """Xử lý sự kiện đăng nhập."""
        print(f"Users data type: {type(self.users)}")
        print(f"Users data: {self.users}")

        username = self.view.username_entry.get()
        password = self.view.password_entry.get()

        if username == "Tên đăng nhập" or password == "Mật khẩu":
            messagebox.showerror("Login", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        user = next((u for u in self.users if u["username"] == username), None)
        if user and user["password"] == password:
            messagebox.showinfo("Login", "Login successful!")
            self.open_home_gui()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    #Hàm xử lý placeholder động
    @staticmethod
    def setup_placeholder(entry, placeholder_text, is_password=False):
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
    def toggle_password(self,password_entry, toggle_button):
        current_text = password_entry.get()
        if current_text == "Mật khẩu":
            return
        if self.is_password_visible.get(): 
            password_entry.config(show="*")
            toggle_button.config(text="👁")
            self.is_password_visible.set(False)
        else:
            password_entry.config(show="")
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

    def open_home_gui(self):
        """Mở giao diện chính sau khi đăng nhập thành công"""
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
