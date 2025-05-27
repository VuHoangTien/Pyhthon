import os
import tkinter as tk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkScrollbar

from GUI_StaffDetail import StaffDetailGui

class StaffListGui():
    def __init__(self, master):
        self.master = master  # Đây sẽ là content_frame từ GUI_Main
        self.setup_ui()
 
    def setup_ui(self):
        # Chỉ tạo phần content, không tạo header và menu
        
        # Header của bảng với nút thêm
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(20, 10))

        # Nút thêm nhân viên
        add_button = CTkButton(master=table_header, text="➕ Thêm nhân viên", width=150, height=35, 
                            fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5)
        add_button.pack(side=tk.RIGHT, pady=10)

        # Nút xuất file Json
        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35, 
                            fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5)
        export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Tiêu đề căn giữa
        title_label = tk.Label(table_header, text="Danh sách nhân viên", font=("Arial", 16, "bold"), bg="white")
        title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Frame chứa bảng với scrollbar
        table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Header của bảng
        header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
        header_frame.pack(fill=tk.X)

        headers = ["STT", "ID", "Họ tên", "Ngày sinh", "Số điện thoại", "Thao tác"]
        header_widths = [60, 120, 250, 180, 180, 200]

        # Cấu hình trọng số cho các cột
        for i, width in enumerate(header_widths):
            header_frame.grid_columnconfigure(i, weight=0, minsize=width)

        for i, (header, width) in enumerate(zip(headers, header_widths)):
            label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"), 
                            bg="#57a1f8", fg="white", anchor="center")
            label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

        # Frame chứa Canvas và Scrollbar cho nội dung bảng
        scroll_container = tk.Frame(table_container, bg="white")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        # Tạo Canvas và Scrollbar
        canvas = tk.Canvas(scroll_container, bg="white")
        scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
                         width=12, corner_radius=6,
                         fg_color="white", bg_color="white",
                         button_color="#57a1f8", button_hover_color="#2b8ee0")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        scrollable_frame = CTkFrame(canvas, fg_color="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Data mẫu nhân viên
        staff_data = [
            (1, "NV001", "Nguyễn Văn A", "15/03/1985", "0901234567"),
            (2, "NV002", "Trần Thị B", "20/05/1990", "0912345678"),
            (3, "NV003", "Lê Văn C", "10/07/1988", "0923456789"),
            (4, "NV004", "Phạm Thị D", "25/12/1992", "0934567890"),
            (5, "NV005", "Nguyễn Văn E", "30/01/1987", "0945678901"),
            (6, "NV006", "Trần Thị F", "05/09/1991", "0956789012"),
            (7, "NV007", "Lê Văn G", "15/11/1989", "0967890123"),
            (8, "NV008", "Phạm Thị H", "20/02/1993", "0978901234"),
            (9, "NV009", "Nguyễn Văn I", "10/04/1986", "0989012345"),
            (10, "NV010", "Trần Thị J", "25/08/1994", "0990123456"),
            (11, "NV011", "Hoàng Văn K", "12/06/1990", "0991234567"),
            (12, "NV012", "Võ Thị L", "18/09/1992", "0992345678")
        ]

        # Tạo các dòng dữ liệu
        for i, staff in enumerate(staff_data):
            bg_color = "#f8f9fa" if i % 2 == 1 else "white"
            hover_color = "#d0e6ff"  # Màu xanh nhạt khi hover

            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

            # Gán sự kiện hover
            def on_enter(e, frame=row_frame):
                frame.configure(bg=hover_color)
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=hover_color)
                    elif isinstance(widget, tk.Frame):
                        widget.configure(bg=hover_color)

            def on_leave(e, frame=row_frame, color=bg_color):
                frame.configure(bg=color)
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.configure(bg=color)
                    elif isinstance(widget, tk.Frame):
                        widget.configure(bg=color)

            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            row_frame.pack(fill=tk.X)
            
            # Cấu hình trọng số cho các cột của mỗi dòng để khớp với header
            for j, width in enumerate(header_widths):
                row_frame.grid_columnconfigure(j, weight=0, minsize=width)

            # Hiển thị thông tin nhân viên
            for j, (data, width) in enumerate(zip(staff, header_widths[:-1])):
                label = tk.Label(row_frame, text=str(data), font=("Arial", 11), 
                                bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")
            
            # Frame chứa các nút thao tác
            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=len(staff), padx=5, pady=5)
            
            # Nút xem chi tiết
            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                corner_radius=3, font=("Arial", 9),
                                 command=lambda p=staff: self.view_staff_detail(p))
            detail_btn.pack(side=tk.LEFT, padx=2)
            
            # Nút sửa
            edit_btn = CTkButton(master=action_frame, text="Sửa", width=50, height=28,
                                fg_color="#ffc107", text_color="white", hover_color="#e0a800",
                                corner_radius=3, font=("Arial", 9))
            edit_btn.pack(side=tk.LEFT, padx=2)
            
            # Nút xóa
            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                corner_radius=3, font=("Arial", 9))
            delete_btn.pack(side=tk.LEFT, padx=2)

    def view_staff_detail(self, staff_data):
        """Xem chi tiết nhân viên"""
        if self.navigation_callback:
            # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
            self.navigation_callback('staff_detail', staff_data)
        else:
            # Mở trực tiếp (dành cho test độc lập)
            self.open_staff_detail_window(staff_data)

    def add_new_staff(self):
        """Thêm nhân viên mới"""
        if self.navigation_callback:
            # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
            self.navigation_callback('staff_detail', None)
        else:
            # Mở trực tiếp (dành cho test độc lập)
            self.open_staff_detail_window(None)

    def open_staff_detail_window(self, staff_data):
        """Mở cửa sổ chi tiết nhân viên (dành cho test độc lập)"""
        # Xóa nội dung hiện tại
        for widget in self.master.winfo_children():
            widget.destroy()

        # Tạo StaffDetailGui mới
        detail_gui = StaffDetailGui(self.master, staff_data)

    def delete_staff(self, staff_data):
        """Xóa nhân viên"""
        result = messagebox.askyesno("Xác nhận xóa",
                                   f"Bạn có chắc chắn muốn xóa nhân viên '{staff_data['name']}'?\n"
                                   "Hành động này không thể hoàn tác!")
        
        if result:
            try:
                # Xóa khỏi danh sách
                self.staff_data.remove(staff_data)

                # Refresh giao diện
                self.refresh_table()

                messagebox.showinfo("Thành công", f"Đã xóa nhân viên '{staff_data['name']}' thành công!")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa nhân viên: {str(e)}")

    def export_json(self):
        """Xuất dữ liệu ra file JSON"""
        try:
            import json
            from tkinter import filedialog
            
            # Chọn nơi lưu file
            file_path = filedialog.asksaveasfilename(
                title="Lưu file JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                # Xuất dữ liệu
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.patients_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def refresh_table(self):
        """Làm mới bảng dữ liệu"""
        # Xóa nội dung hiện tại và tạo lại
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_ui()

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            self.master.yview_scroll(int(-1*(event.delta/120)), "units")


# Test riêng biệt (chỉ dành cho development)
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

    # Test với frame content
    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    # Khởi tạo giao diện
    staff_list_gui = StaffListGui(content_frame)

    root.mainloop()