# GUI_StaffList.py
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
        self.staff_data = [] # Changed from self.staff_data to self.staffs_data to avoid confusion with single staff_data
        self.load_data_staff_from_file() # Load data before setting up UI
        self.setup_ui()

    def load_data_staff_from_file(self):
        try:
            with open("staffs.json", "r", encoding="utf-8") as f:
                self.staff_data = json.load(f) # Now self.staff_data refers to the list of all staffs
        except FileNotFoundError:
            self.staff_data = []
        except json.JSONDecodeError:
            self.staff_data = [] # Handle empty or malformed JSON

    def save_data_staff_to_file(self):
        try:
            with open("staffs.json", "w", encoding="utf-8") as f:
                json.dump(self.staff_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Lỗi khi ghi file:", e)

    def setup_ui(self):
        # Clear existing widgets before setting up UI
        for widget in self.master.winfo_children():
            widget.destroy()

        # Header
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

        # Table container
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Header row
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["ID", "Họ tên", "Chức vụ", "Phòng ban", "Số điện thoại", "Thao tác"]
        header_widths = [80, 180, 150, 150, 150, 180] # Adjusted widths

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

        self.populate_table(scrollable_frame, header_widths)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def populate_table(self, scrollable_frame, header_widths):
        """Populates the table with staff data."""
        self.load_data_staff_from_file() # Ensure the data is fresh when populating

        for i, staff in enumerate(self.staff_data): # Use self.staff_data (the list of staffs)
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
                staff.get("position", ""),
                staff.get("department", ""),
                staff.get("phone", "")
            ]

            for j, text in enumerate(display_data):
                label = tk.Label(row_frame, text=text, font=("Arial", 11),
                                 bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=5, padx=5, pady=5) # Column 5 for actions

            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                   fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda s=staff: self.view_staff_detail(s))
            detail_btn.pack(side=tk.LEFT, padx=2)

            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                   fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                   corner_radius=3, font=("Arial", 9),
                                   command=lambda s_id=staff.get('id'): self.delete_staff_by_id(s_id))
            delete_btn.pack(side=tk.LEFT, padx=2)

    def view_staff_detail(self, staff_data):
        if self.navigation_callback:
            # Pass all_staff_data and a refresh callback
            self.navigation_callback('staff_detail', staff_data, self.staff_data, self.refresh_table)
        else:
            self.open_staff_detail_window(staff_data)

    def add_new_staff(self):
        if self.navigation_callback:
            # Pass None for staff_data and all_staffs_data for ID generation, plus refresh callback
            self.navigation_callback('staff_detail', None, self.staff_data, self.refresh_table)
        else:
            self.open_staff_detail_window(None)

    def open_staff_detail_window(self, staff_data):
        for widget in self.master.winfo_children():
            widget.destroy()
        # For standalone testing, pass a dummy all_staffs_data or load it here
        detail_gui = StaffDetailGui(self.master, staff_data, all_staffs_data=self.staff_data, save_callback=self.refresh_table)
        # In a real integrated app, you'd navigate without packing it directly
        # detail_gui.pack(fill=tk.BOTH, expand=True) # This line would be in the main app's navigation


    def delete_staff_by_id(self, staff_id):
        self.load_data_staff_from_file() # Ensure data is fresh before deletion attempt

        if not self.staff_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xóa.")
            return

        staff_name = "N/A"
        for s in self.staff_data:
            if s.get("id") == staff_id:
                staff_name = s.get("name", "Nhân viên không tên")
                break

        result = messagebox.askyesno("Xác nhận",
                                     f"Bạn có chắc chắn muốn xóa nhân viên '{staff_name}' (ID: {staff_id})?\nHành động này không thể hoàn tác!")
        if result:
            self.staff_data = [s for s in self.staff_data if s.get("id") != staff_id]
            self.save_data_staff_to_file()
            self.refresh_table()
            messagebox.showinfo("Thành công", f"Đã xóa nhân viên '{staff_name}' khỏi hệ thống.")

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
        # Reload data and re-setup UI to reflect changes
        self.load_data_staff_from_file()
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

    # # Create a dummy staffs.json for testing - REMOVED/COMMENTED OUT
    # initial_staffs_for_list = [
    #     {'id': 'NV001', 'name': 'Lê Văn Luyện', 'birth_date': '10/05/1980', 'phone': '0901111222',
    #      'gender': 'Nam', 'email': 'luyenlv@example.com', 'address': '123 Đường ABC, Q1, TP.HCM',
    #      'position': 'Bác sĩ', 'department': 'Nội khoa', 'start_date': '01/01/2010', 'salary': '20000000', 'image_path': ''},
    #     {'id': 'NV002', 'name': 'Trần Thị Thu', 'birth_date': '25/11/1992', 'phone': '0983333444',
    #      'gender': 'Nữ', 'email': 'thuttt@example.com', 'address': '456 Đường XYZ, Q2, TP.HCM',
    #      'position': 'Y tá', 'department': 'Phòng khám', 'start_date': '15/07/2015', 'salary': '12000000', 'image_path': ''},
    # ]
    # with open("staffs.json", "w", encoding="utf-8") as f:
    #     json.dump(initial_staffs_for_list, f, ensure_ascii=False, indent=2)

    app = StaffListGui(content_frame)
    root.mainloop()

    # # Clean up the dummy staffs.json after testing - REMOVED/COMMENTED OUT
    # if os.path.exists("staffs.json"):
    #     os.remove("staffs.json")