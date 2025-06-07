
# import os
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import messagebox
# from customtkinter import CTkButton, CTkImage, CTkFrame, CTkScrollbar
# import json
# from GUI_AccountDetail import AccountDetailGui

# class AccountListGui():
#     def __init__(self, master, navigation_callback=None):
#         self.master = master
#         self.navigation_callback = navigation_callback
#         self.account_data = [] # Khởi tạo danh sách tài khoản
#         self.setup_ui()

#     def load_data_account_from_file(self):
#         try:
#             with open("account.json", "r", encoding="utf-8") as f:
#                 self.account_data = json.load(f)
#         except FileNotFoundError:
#             self.account_data = []

#     def save_data_account_to_file(self):
#         try:
#             with open("account.json", "w", encoding="utf-8") as f:
#                 json.dump(self.account_data, f, ensure_ascii=False, indent=2)
#         except Exception as e:
#             print("Lỗi khi ghi file:", e)

#     def setup_ui(self):
#         # Header
#         table_header = tk.Frame(self.master, bg="white", height=60)
#         table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

#         add_button = CTkButton(master=table_header, text="➕ Thêm tài khoản", width=150, height=35,
#                                fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5, command=self.add_new_account)
#         add_button.pack(side=tk.RIGHT, pady=10)

#         export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
#                                   fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
#                                   command=self.export_json) # Thêm command
#         export_button.pack(side=tk.RIGHT, padx=10, pady=10)

#         title_label = tk.Label(table_header, text="Danh sách tài khoản hệ thống", font=("Arial", 16, "bold"), bg="white")
#         title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#         # Container
#         table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
#         table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

#         # Header row
#         header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
#         header_frame.pack(fill=tk.X)

#         headers = ["Tên đăng nhập", "Mật khẩu", "Email", "Số điện thoại", "Thao tác"] # Sửa "Gmail" thành "Email"
#         header_widths = [180, 160, 250, 150, 200]

#         for i, width in enumerate(header_widths):
#             header_frame.grid_columnconfigure(i, weight=0, minsize=width)

#         for i, header in enumerate(headers):
#             label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"),
#                              bg="#57a1f8", fg="white", anchor="center")
#             label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

#         # Scrollable area
#         scroll_container = tk.Frame(table_container, bg="white")
#         scroll_container.pack(fill=tk.BOTH, expand=True)

#         canvas = tk.Canvas(scroll_container, bg="white")
#         scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
#                                  width=12, corner_radius=6,
#                                  fg_color="white", bg_color="white",
#                                  button_color="#57a1f8", button_hover_color="#2b8ee0")
#         scrollbar.pack(side="right", fill="y")
#         canvas.pack(side="left", fill="both", expand=True)

#         scrollable_frame = CTkFrame(canvas, fg_color="white")
#         scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
#         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)

#         # Load and show data
#         self.load_data_account_from_file()

#         # Xóa các widget hiện có trong scrollable_frame để tránh trùng lặp khi refresh
#         for widget in scrollable_frame.winfo_children():
#             widget.destroy()

#         for i, account in enumerate(self.account_data):
#             bg_color = "#f8f9fa" if i % 2 == 1 else "white"
#             hover_color = "#d0e6ff"

#             row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

#             def on_enter(e, frame=row_frame):
#                 frame.configure(bg=hover_color)
#                 for widget in frame.winfo_children():
#                     if isinstance(widget, (tk.Label, tk.Frame)):
#                         widget.configure(bg=hover_color)

#             def on_leave(e, frame=row_frame, color=bg_color):
#                 frame.configure(bg=color)
#                 for widget in frame.winfo_children():
#                     if isinstance(widget, (tk.Label, tk.Frame)):
#                         widget.configure(bg=color)

#             row_frame.bind("<Enter>", on_enter)
#             row_frame.bind("<Leave>", on_leave)
#             # Dùng pack thay vì grid cho row_frame trực tiếp trong scrollable_frame
#             row_frame.pack(fill=tk.X)

#             for j, width in enumerate(header_widths):
#                 row_frame.grid_columnconfigure(j, weight=0, minsize=width)

#             display_data = [
#                 account.get('username', ''),
#                 '********' if 'password_hash' in account and account.get('password_hash') else '', # Hiển thị 8 dấu * cố định
#                 account.get('email', ''),
#                 account.get('phone', '')
#             ]

#             for j, text in enumerate(display_data):
#                 label = tk.Label(row_frame, text=text, font=("Arial", 11),
#                                  bg=bg_color, anchor="center")
#                 label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

#             # Action buttons
#             action_frame = tk.Frame(row_frame, bg=bg_color)
#             action_frame.grid(row=0, column=4, padx=5, pady=5)

#             detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
#                                    fg_color="#17a2b8", text_color="white", hover_color="#138496",
#                                    corner_radius=3, font=("Arial", 9),
#                                    command=lambda acc=account: self.view_account_detail(acc)) # Đổi p thành acc
#             detail_btn.pack(side=tk.LEFT, padx=2)

#             edit_btn = CTkButton(master=action_frame, text="Sửa", width=50, height=28,
#                                  fg_color="#ffc107", text_color="white", hover_color="#e0a800",
#                                  corner_radius=3, font=("Arial", 9),
#                                  command=lambda acc=account: self.edit_account(acc)) # Thêm command
#             edit_btn.pack(side=tk.LEFT, padx=2)

#             delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
#                                    fg_color="#dc3545", text_color="white", hover_color="#c82333",
#                                    corner_radius=3, font=("Arial", 9),
#                                    command=lambda acc=account: self.delete_account(acc)) # Thêm command
#             delete_btn.pack(side=tk.LEFT, padx=2)

#         # Mouse scroll
#         def _on_mousewheel(event):
#             canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

#         canvas.bind_all("<MouseWheel>", _on_mousewheel)

#     def open_account_detail_window(self, account_data): # Đổi patient_data thành account_data
#         """Mở cửa sổ chi tiết account (dành cho test độc lập)"""
#         # Xóa nội dung hiện tại
#         for widget in self.master.winfo_children():
#             widget.destroy()

#         # Tạo AccountDetailGui mới
#         detail_gui = AccountDetailGui(self.master, account_data, self.navigation_callback)
#         detail_gui.pack(fill=tk.BOTH, expand=True) # Thêm dòng này để hiển thị GUI_AccountDetail

#     def view_account_detail(self, account_data): # Đổi patient_data thành account_data
#         """Xem chi tiết tài khoản"""
#         if self.navigation_callback:
#             self.navigation_callback('account_detail', account_data) # Sửa staffs_detail thành account_detail
#         else:
#             self.open_account_detail_window(account_data)

#     def add_new_account(self):
#         """Thêm tài khoản mới"""
#         if self.navigation_callback:
#             self.navigation_callback('account_detail', None)
#         else:
#             self.open_account_detail_window(None)

#     def edit_account(self, account_data):
#         """Chỉnh sửa tài khoản hiện có"""
#         if self.navigation_callback:
#             self.navigation_callback('account_detail', account_data)
#         else:
#             self.open_account_detail_window(account_data)

#     def delete_account(self, account_data):
#         """Xóa tài khoản đã chọn khỏi danh sách và file"""
#         if not self.account_data:
#             messagebox.showwarning("Cảnh báo", "Không có dữ liệu tài khoản để xóa!")
#             return

#         result = messagebox.askyesno("Xác nhận",
#                                  f"Bạn có chắc chắn muốn xóa tài khoản '{account_data.get('username', '')}'?\n"
#                                  "Hành động này không thể hoàn tác!")

#         if result:
#             # Lọc tài khoản cần xóa
#             self.account_data = [acc for acc in self.account_data if acc.get("username") != account_data.get("username")]
#             self.save_data_account_to_file()
#             self.refresh_table() # Gọi hàm làm mới bảng sau khi xóa

#             messagebox.showinfo("Thành công", "Đã xóa tài khoản khỏi hệ thống.")

#     def export_json(self):
#         """Xuất dữ liệu tài khoản ra file JSON"""
#         try:
#             from tkinter import filedialog
#             file_path = filedialog.asksaveasfilename(
#                 title="Lưu file JSON tài khoản",
#                 defaultextension=".json",
#                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
#             )

#             if file_path:
#                 with open(file_path, 'w', encoding='utf-8') as f:
#                     json.dump(self.account_data, f, ensure_ascii=False, indent=2)
#                 messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")

#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

#     def refresh_table(self):
#         """Làm mới lại toàn bộ UI của bảng để hiển thị dữ liệu mới"""
#         # Xóa các widget hiện có
#         for widget in self.master.winfo_children():
#             widget.destroy()
#         # Setup lại UI để tải dữ liệu mới
#         self.setup_ui()

#     def set_navigation_callback(self, callback):
#         """Thiết lập callback cho navigation"""
#         self.navigation_callback = callback


# # Chạy test độc lập
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Test Danh sách tài khoản")
#     root.configure(bg="#f8f9fa")
#     root.resizable(False, False) # Có thể đổi thành True nếu muốn thay đổi kích thước

#     window_width = 1100
#     window_height = 600
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     center_x = int((screen_width - window_width) / 2)
#     center_y = int((screen_height - window_height) / 3)
#     root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

#     content_frame = tk.Frame(root, bg="#f8f9fa")
#     content_frame.pack(expand=True, fill=tk.BOTH)

#     account_list_gui = AccountListGui(content_frame)

#     root.mainloop()


import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton, CTkImage, CTkFrame, CTkScrollbar
import json
from GUI_AccountDetail import AccountDetailGui # Giả định GUI_AccountDetail.py tồn tại và được cấu trúc đúng

class AccountListGui():
    def __init__(self, master, navigation_callback=None):
        self.master = master
        self.navigation_callback = navigation_callback
        self.account_data = [] # Khởi tạo danh sách tài khoản
        self.setup_ui()

    def load_data_account_from_file(self):
        try:
            with open("account.json", "r", encoding="utf-8") as f:
                self.account_data = json.load(f)
        except FileNotFoundError:
            self.account_data = []

    def save_data_account_to_file(self):
        try:
            with open("account.json", "w", encoding="utf-8") as f:
                json.dump(self.account_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)

    def setup_ui(self):
        # Clear existing widgets to allow refresh
        for widget in self.master.winfo_children():
            widget.destroy()

        # Header
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        add_button = CTkButton(master=table_header, text="➕ Thêm tài khoản", width=150, height=35,
                               fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5, command=self.add_new_account)
        add_button.pack(side=tk.RIGHT, pady=10)

        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
                                  fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
                                  command=self.export_json)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        title_label = tk.Label(table_header, text="Danh sách tài khoản hệ thống", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Container
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Header row
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["Tên đăng nhập", "Mật khẩu", "Email", "Số điện thoại", "Thao tác"]
        header_widths = [180, 160, 250, 150, 200]

        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, header in enumerate(headers):
            label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"),
                             bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

        # Scrollable area
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
                                 width=12, corner_radius=6,
                                 fg_color="white", bg_color="white",
                                 button_color="#57a1f8", button_hover_color="#2b8ee0")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = CTkFrame(canvas, fg_color="white")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Load and show data
        self.load_data_account_from_file()

        # Xóa các widget hiện có trong scrollable_frame để tránh trùng lặp khi refresh (đã chuyển lên đầu setup_ui)
        # for widget in scrollable_frame.winfo_children():
        #     widget.destroy()

        for i, account in enumerate(self.account_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#d0e6ff"

            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

            def on_enter(e, frame=row_frame):
                frame.configure(bg=hover_color)
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Frame)):
                        widget.configure(bg=hover_color)

            def on_leave(e, frame=row_frame, color=bg_color):
                frame.configure(bg=color)
                for widget in frame.winfo_children():
                    if isinstance(widget, (tk.Label, tk.Frame)):
                        widget.configure(bg=color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            row_frame.pack(fill=tk.X) # Dùng pack thay vì grid cho row_frame trực tiếp trong scrollable_frame

            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            display_data = [
                account.get('username', ''),
                '********' if 'password_hash' in account and account.get('password_hash') else '', # Đã sửa từ 'password_hash' thành 'password'
                account.get('email', ''),
                account.get('phone', '')
            ]

            for j, text in enumerate(display_data):
                label = tk.Label(row_frame, text=text, font=("Arial", 11),
                                 bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

            # Action buttons
            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=4, padx=5, pady=5)

            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                   fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda acc=account: self.view_account_detail(acc))
            detail_btn.pack(side=tk.LEFT, padx=2)

            edit_btn = CTkButton(master=action_frame, text="Sửa", width=50, height=28,
                                 fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                                 corner_radius=3, font=("Arial", 9),
                                 command=lambda acc=account: self.edit_account(acc))
            edit_btn.pack(side=tk.LEFT, padx=2)

            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                   fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda acc=account: self.delete_account(acc))
            delete_btn.pack(side=tk.LEFT, padx=2)

        # Mouse scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def open_account_detail_window(self, account_data):
        """Mở cửa sổ chi tiết account (dành cho test độc lập)"""
        # Xóa nội dung hiện tại
        for widget in self.master.winfo_children():
            widget.destroy()

        # Tạo AccountDetailGui mới
        detail_gui = AccountDetailGui(self.master, account_data, self.navigation_callback)
        detail_gui.pack(fill=tk.BOTH, expand=True)

    def view_account_detail(self, account_data):
        """Xem chi tiết tài khoản"""
        if self.navigation_callback:
            self.navigation_callback('account_detail', account_data)
        else:
            self.open_account_detail_window(account_data)

    def add_new_account(self):
        """Thêm tài khoản mới"""
        if self.navigation_callback:
            self.navigation_callback('account_detail', None)
        else:
            self.open_account_detail_window(None)

    def edit_account(self, account_data):
        """Chỉnh sửa tài khoản hiện có"""
        if self.navigation_callback:
            self.navigation_callback('account_detail', account_data)
        else:
            self.open_account_detail_window(account_data)

    def delete_account(self, account_data):
        """Xóa tài khoản đã chọn khỏi danh sách và file"""
        if not self.account_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu tài khoản để xóa!")
            return

        result = messagebox.askyesno("Xác nhận",
                                 f"Bạn có chắc chắn muốn xóa tài khoản '{account_data.get('username', '')}'?\n"
                                 "Hành động này không thể hoàn tác!")

        if result:
            # Lọc tài khoản cần xóa
            self.account_data = [acc for acc in self.account_data if acc.get("username") != account_data.get("username")]
            self.save_data_account_to_file()
            self.refresh_table() # Gọi hàm làm mới bảng sau khi xóa

            messagebox.showinfo("Thành công", "Đã xóa tài khoản khỏi hệ thống.")

    def export_json(self):
        """Xuất dữ liệu tài khoản ra file JSON"""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Lưu file JSON tài khoản",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.account_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def refresh_table(self):
        """Làm mới lại toàn bộ UI của bảng để hiển thị dữ liệu mới"""
        # Xóa các widget hiện có và thiết lập lại UI
        self.setup_ui()

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback


# Chạy test độc lập
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách tài khoản")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False) # Có thể đổi thành True nếu muốn thay đổi kích thước

    window_width = 1100
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    account_list_gui = AccountListGui(content_frame)

    root.mainloop()