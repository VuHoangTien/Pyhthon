import os
import tkinter as tk
from tkinter import messagebox, filedialog
from customtkinter import CTkButton, CTkFrame, CTkScrollbar
from GUI_StaffDetail import StaffDetailGui
import json

class StaffListGui():
    def __init__(self, master, navigation_callback=None):
        self.master = master
        self.navigation_callback = navigation_callback
        self.staff_data = []
        self.setup_ui()

    def load_data_staff_from_file(self):
        try:
            with open("staffs.json", "r", encoding="utf-8") as f:
                self.staff_data = json.load(f)
        except FileNotFoundError:
            self.staff_data = []

    def save_data_staff_to_file(self):
        try:
            with open("staffs.json", "w", encoding="utf-8") as f:
                json.dump(self.staff_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)

    def setup_ui(self):
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        add_button = CTkButton(master=table_header, text="➕ Thêm nhân viên", width=150, height=35,
                               fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5,
                               command=self.add_new_staff)
        add_button.pack(side=tk.RIGHT, pady=10)

        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
                                  fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
                                  command=self.export_json)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        title_label = tk.Label(table_header, text="Danh sách nhân viên", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["ID", "Họ tên", "Ngày sinh", "Số điện thoại", "Thao tác"]
        header_widths = [80, 200, 150, 180, 200]

        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, header in enumerate(headers):
            label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"),
                             bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

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

        self.load_data_staff_from_file()

        for i, staff in enumerate(self.staff_data):
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
            row_frame.pack(fill=tk.X)

            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            display_data = [
                staff.get("id", ""),
                staff.get("name", ""),
                staff.get("birth_date", ""),
                staff.get("phone", "")
            ]

            for j, text in enumerate(display_data):
                label = tk.Label(row_frame, text=text, font=("Arial", 11),
                                 bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=4, padx=5, pady=5)

            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                   fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda s=staff: self.view_staff_detail(s))
            detail_btn.pack(side=tk.LEFT, padx=2)

            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                   fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda s=staff: self.delete_staff(s))
            delete_btn.pack(side=tk.LEFT, padx=2)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def view_staff_detail(self, staff_data):
        if self.navigation_callback:
            self.navigation_callback('staffs_detail', staff_data)
        else:
            self.open_staff_detail_window(staff_data)

    def add_new_staff(self):
        if self.navigation_callback:
            self.navigation_callback('staffs_detail', None)
        else:
            self.open_staff_detail_window(None)

    def open_staff_detail_window(self, staff_data):
        for widget in self.master.winfo_children():
            widget.destroy()
        detail_gui = StaffDetailGui(self.master, staff_data, self.navigation_callback)
        detail_gui.pack(fill=tk.BOTH, expand=True)

    def delete_staff(self, staff_data):
        if not self.staff_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xóa.")
            return

        result = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên '{staff_data.get('name', '')}'?")
        if result:
            self.staff_data = [s for s in self.staff_data if s != staff_data]
            self.save_data_staff_to_file()
            self.refresh_table()
            messagebox.showinfo("Thành công", "Đã xóa nhân viên khỏi hệ thống.")

    def export_json(self):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Lưu file JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.staff_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Thành công", f"Đã lưu tại:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

    def refresh_table(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_ui()

    def set_navigation_callback(self, callback):
        self.navigation_callback = callback

# Test độc lập
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách nhân viên")
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)

    window_width = 1100
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    app = StaffListGui(content_frame)
    root.mainloop()
