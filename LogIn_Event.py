import json
import tkinter as tk
from tkinter import messagebox
# import hashlib # KHÔNG CẦN THIẾT NỮA KHI KHÔNG BĂM MẬT KHẨU

class LoginEvent:
    def __init__(self, username_entry, password_entry, master):
        self.username_entry = username_entry
        self.password_entry = password_entry
        self.master = master
        self.password_visible = False

    @staticmethod
    def setup_placeholder(entry, placeholder, is_password=False):
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='black')
                if is_password:
                    entry.config(show='*')

        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg='grey')
                if is_password:
                    entry.config(show='')

        entry.insert(0, placeholder)
        entry.config(fg='grey')
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def toggle_password(self, toggle_btn):
        if self.password_visible:
            self.password_entry.config(show="*")
            toggle_btn.config(text="👁")
            self.password_visible = False
        else:
            self.password_entry.config(show="")
            toggle_btn.config(text="👁")
            self.password_visible = True

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get() # Lấy mật khẩu nguyên bản từ Entry

        if username == "Tên đăng nhập" or password == "Mật khẩu":
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        try:
            with open("account.json", "r") as f:
                accounts_data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file tài khoản (account.json).")
            return

        authenticated = False
        user_role = None
        for account in accounts_data:
            # So sánh trực tiếp mật khẩu
            if account.get("username") == username and account.get("password_hash") == password:
                authenticated = True
                user_role = account.get("role")
                break


        if authenticated:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.master.destroy()

            import GUI_Main
            main_root = tk.Tk()
            main_app = GUI_Main.MainGui(main_root, user_role)

            window_width = 1400
            window_height = 700

            screen_width = main_root.winfo_screenwidth()
            screen_height = main_root.winfo_screenheight()

            center_x = int((screen_width - window_width) / 2)
            center_y = int((screen_height - window_height) / 3)

            main_root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
            main_root.mainloop()

        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    @staticmethod
    def apply_hover_effect_text(widget):
        def on_enter(event):
            widget.config(fg="blue")

        def on_leave(event):
            widget.config(fg="#57a1f8")

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)