# # import os
# # import tkinter as tk
# # from tkinter import ttk
# # from PIL import Image, ImageTk
# # from tkinter import messagebox
# # from customtkinter import CTkButton
# # from customtkinter import CTkImage
# # from customtkinter import CTkFrame
# # from customtkinter import CTkScrollbar
# # from GUI_PatientDetail import PatientDetailGui
# # from GUI_StaffDetail import StaffDetailGui
# # import json

# # class StaffListGui():
# #     def __init__(self, master, navigation_callback=None):
# #         self.master = master  # Đây sẽ là content_frame từ GUI_Main
# #         self.navigation_callback = navigation_callback  # Callback để chuyển màn hình
# #         self.setup_ui()
        
# #     # hàm load và save data
# #     def load_data_staff_from_file(self):
# #         try:
# #             with open("staffs.json", "r", encoding="utf-8") as f:
# #                 self.staff_data = json.load(f)
# #         except FileNotFoundError:
# #             self.staff_data = []
        
# #     def save_data_staff_to_file(self):
# #         try:
# #             with open("staffs.json", "w", encoding="utf-8") as f:
# #                 json.dump(self.staff_data, f, ensure_ascii=False, indent=2)
# #         except Exception as e:
# #             print("Lỗi khi ghi file:", e)
            
# #     def setup_ui(self):
# #         # Chỉ tạo phần content, không tạo header và menu
        
# #         # Header của bảng với nút thêm
# #         table_header = tk.Frame(self.master, bg="white", height=60)
# #         table_header.pack(fill=tk.X, padx=20, pady=(10, 20))

# #         # Nút thêm nhân viên
# #         add_button = CTkButton(master=table_header, text="➕ Thêm nhân viên", width=150, height=35, 
# #                             fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5,
# #                             command=self.add_new_staff)
# #         add_button.pack(side=tk.RIGHT, pady=10)

# #         # Nút xuất file Json
# #         export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35, 
# #                             fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
# #                             command=self.export_json)
# #         export_button.pack(side=tk.RIGHT, padx=10, pady=10)

# #         # Tiêu đề căn giữa
# #         title_label = tk.Label(table_header, text="Danh sách nhân viên", font=("Arial", 16, "bold"), bg="white")
# #         title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# #         # Frame chứa bảng với scrollbar
# #         table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
# #         table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

# #         # Header của bảng
# #         header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
# #         header_frame.pack(fill=tk.X)

# #         headers = ["ID", "Họ tên", "Ngày sinh", "Số điện thoại", "Thao tác"]
# #         header_widths = [60, 120, 250, 180, 180, 200]

# #         # Cấu hình trọng số cho các cột
# #         for i, width in enumerate(header_widths):
# #             header_frame.grid_columnconfigure(i, weight=0, minsize=width)

# #         for i, (header, width) in enumerate(zip(headers, header_widths)):
# #             label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"), 
# #                             bg="#57a1f8", fg="white", anchor="center")
# #             label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

# #         # Frame chứa Canvas và Scrollbar cho nội dung bảng
# #         scroll_container = tk.Frame(table_container, bg="white")
# #         scroll_container.pack(fill=tk.BOTH, expand=True)

# #         # Tạo Canvas và Scrollbar
# #         canvas = tk.Canvas(scroll_container, bg="white")
# #         scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
# #                          width=12, corner_radius=6,
# #                          fg_color="white", bg_color="white",
# #                          button_color="#57a1f8", button_hover_color="#2b8ee0")
# #         scrollbar.pack(side="right", fill="y")
# #         canvas.pack(side="left", fill="both", expand=True)
# #         scrollable_frame = CTkFrame(canvas, fg_color="white")

# #         scrollable_frame.bind(
# #             "<Configure>",
# #             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
# #         )

# #         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
# #         canvas.configure(yscrollcommand=scrollbar.set)
        
                

# #         # load data:
# #         self.load_data_staff_from_file()


# #         # Tạo các dòng dữ liệu
# #         for i, patient in enumerate(self.staff_data):
# #             bg_color = "#f8f9fa" if i % 2 == 1 else "white"
# #             hover_color = "#d0e6ff"  # Màu xanh nhạt khi hover

# #             row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

# #             # Gán sự kiện hover
# #             def on_enter(e, frame=row_frame):
# #                 frame.configure(bg=hover_color)
# #                 for widget in frame.winfo_children():
# #                     if isinstance(widget, tk.Label):
# #                         widget.configure(bg=hover_color)
# #                     elif isinstance(widget, tk.Frame):
# #                         widget.configure(bg=hover_color)

# #             def on_leave(e, frame=row_frame, color=bg_color):
# #                 frame.configure(bg=color)
# #                 for widget in frame.winfo_children():
# #                     if isinstance(widget, tk.Label):
# #                         widget.configure(bg=color)
# #                     elif isinstance(widget, tk.Frame):
# #                         widget.configure(bg=color)

# #             row_frame.bind("<Enter>", on_enter)
# #             row_frame.bind("<Leave>", on_leave)
# #             row_frame.pack(fill=tk.X)
            
# #             # Cấu hình trọng số cho các cột của mỗi dòng để khớp với header
# #             for j, width in enumerate(header_widths):
# #                 row_frame.grid_columnconfigure(j, weight=0, minsize=width)

# #             # Hiển thị thông tin bệnh nhân (chỉ hiển thị các trường cơ bản trong bảng)
# #             display_data = [patient['id'], patient['name'], patient['birth_date'], patient['phone']]
# #             for j, (data, width) in enumerate(zip(display_data, header_widths[:-1])):
# #                 label = tk.Label(row_frame, text=str(data), font=("Arial", 11), 
# #                                 bg=bg_color, anchor="center")
# #                 label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")
            
# #             # Frame chứa các nút thao tác
# #             action_frame = tk.Frame(row_frame, bg=bg_color)
# #             action_frame.grid(row=0, column=len(display_data), padx=5, pady=5)
            
# #             # Nút xem chi tiết
# #             detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
# #                                 fg_color="#17a2b8", text_color="white", hover_color="#138496",
# #                                 corner_radius=3, font=("Arial", 9),
# #                                 command=lambda p=patient: self.view_staff_detail(p))
# #             detail_btn.pack(side=tk.LEFT, padx=2)
            
# #             # Nút xóa
# #             delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
# #                                 fg_color="#dc3545", text_color="white", hover_color="#c82333",
# #                                 corner_radius=3, font=("Arial", 9),
# #                                 command=lambda p=patient: self.delete_patient(p))
# #             delete_btn.pack(side=tk.LEFT, padx=2)

# #         # Bind mousewheel to canvas
# #         def _on_mousewheel(event):
# #             canvas.yview_scroll(int(-1*(event.delta/120)), "units")
# #         canvas.bind_all("<MouseWheel>", _on_mousewheel)

# #     def view_staff_detail(self, staff_data):
# #         """Xem chi tiết bệnh nhân"""
# #         if self.navigation_callback:
# #             # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
# #             self.navigation_callback('staffs_detail', staff_data)
# #         else:
# #             # Mở trực tiếp (dành cho test độc lập)
# #             self.open_staff_detail_window(staff_data)

# #     def add_new_staff(self):
# #         """Thêm bệnh nhân mới"""
# #         if self.navigation_callback:
# #             # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
# #             self.navigation_callback('staffs_detail', None)
# #         else:
# #             # Mở trực tiếp (dành cho test độc lập)
# #             self.open_staff_detail_window(None)

# #     def open_staff_detail_window(self, staff_data):
# #         """Mở cửa sổ chi tiết bệnh nhân (dành cho test độc lập)"""
# #         # Xóa nội dung hiện tại
# #         for widget in self.master.winfo_children():
# #             widget.destroy()
        
# #         # Tạo PatientDetailGui mới
# #         detail_gui = StaffDetailGui(self.master, staff_data)
    
# #     def delete_patient(self, patient_data):
# #         """Xóa bệnh nhân đã chọn khỏi danh sách và file"""
# #         if not self.staff_data:
# #             messagebox.showwarning("Cảnh báo", "Không thể xóa bệnh nhân mới chưa được lưu!")
# #             return

# #         result = messagebox.askyesno("Xác nhận", 
# #                                  "Bạn có chắc chắn muốn xóa thông tin bệnh nhân này?\n"
# #                                  "Hành động này không thể hoàn tác!")

# #         if result:
# #             # Xóa trực tiếp theo object
# #             self.staff_data = [p for p in self.staff_data if p != patient_data]

# #             # Ghi lại vào file JSON
# #             self.save_data_to_file()

# #             # Cập nhật giao diện
# #             self.refresh_patient_list()  # hoặc self.refresh_ui(), tùy tên hàm bạn dùng để cập nhật lại bảng

# #             messagebox.showinfo("Thành công", "Đã xóa bệnh nhân khỏi hệ thống.")

# #     # hàm refresh
# #     def refresh_patient_list(self):
# #         self.display_data.delete("1.0", "end")  # Nếu là Text widget
# #         for patient in self.staff_data:
# #             line = f"{patient.get('id','')} - {patient.get('name','')} - {patient.get('phone','')}\n"
# #             self.display_data.insert("end", line)


            
            
# #     def export_json(self):
# #         """Xuất dữ liệu ra file JSON"""
# #         try:
# #             import json
# #             from tkinter import filedialog
            
# #             # Chọn nơi lưu file
# #             file_path = filedialog.asksaveasfilename(
# #                 title="Lưu file JSON",
# #                 defaultextension=".json",
# #                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
# #             )
            
# #             if file_path:
# #                 # Xuất dữ liệu
# #                 with open(file_path, 'w', encoding='utf-8') as f:
# #                     json.dump(self.staff_data, f, ensure_ascii=False, indent=2)
                
# #                 messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")
                
# #         except Exception as e:
# #             messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

# #     def refresh_table(self):
# #         """Làm mới bảng dữ liệu"""
# #         # Xóa nội dung hiện tại và tạo lại
# #         for widget in self.master.winfo_children():
# #             widget.destroy()
# #         self.setup_ui()

# #     def set_navigation_callback(self, callback):
# #         """Thiết lập callback cho navigation"""
# #         self.navigation_callback = callback


# # # Test riêng biệt (chỉ dành cho development)
# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     root.title("Test Danh sách bệnh nhân")
# #     root.configure(bg="#f8f9fa")
# #     root.resizable(True, True)

# #     window_width = 1200
# #     window_height = 700
# #     screen_width = root.winfo_screenwidth()
# #     screen_height = root.winfo_screenheight()
# #     center_x = int((screen_width - window_width) / 2)
# #     center_y = int((screen_height - window_height) / 3)
# #     root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# #     # Test với frame content
# #     content_frame = tk.Frame(root, bg="#f8f9fa")
# #     content_frame.pack(expand=True, fill=tk.BOTH)

# #     # Khởi tạo giao diện
# #     patient_list_gui = StaffListGui(content_frame)

# #     root.mainloop()


# import os
# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import messagebox
# from customtkinter import CTkButton
# from customtkinter import CTkImage
# from customtkinter import CTkFrame
# from customtkinter import CTkScrollbar
# from GUI_PatientDetail import PatientDetailGui # Có vẻ bạn không dùng PatientDetailGui ở đây, nên có thể bỏ qua nếu không cần
# from GUI_StaffDetail import StaffDetailGui
# import json

# class StaffListGui():
#     def __init__(self, master, navigation_callback=None):
#         self.master = master  # Đây sẽ là content_frame từ GUI_Main
#         self.navigation_callback = navigation_callback  # Callback để chuyển màn hình
#         self.setup_ui()
        
#     # hàm load và save data
#     def load_data_staff_from_file(self):
#         try:
#             with open("staffs.json", "r", encoding="utf-8") as f:
#                 self.staff_data = json.load(f)
#         except FileNotFoundError:
#             self.staff_data = []
        
#     def save_data_staff_to_file(self):
#         try:
#             with open("staffs.json", "w", encoding="utf-8") as f:
#                 json.dump(self.staff_data, f, ensure_ascii=False, indent=2)
#         except Exception as e:
#             print("Lỗi khi ghi file:", e)
            
#     def setup_ui(self):
#         # Chỉ tạo phần content, không tạo header và menu
        
#         # Header của bảng với nút thêm
#         table_header = tk.Frame(self.master, bg="white", height=60)
#         table_header.pack(fill=tk.X, padx=20, pady=(10, 20))

#         # Nút thêm nhân viên
#         add_button = CTkButton(master=table_header, text="➕ Thêm nhân viên", width=150, height=35, 
#                                 fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5,
#                                 command=self.add_new_staff)
#         add_button.pack(side=tk.RIGHT, pady=10)

#         # Nút xuất file Json
#         export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35, 
#                                 fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
#                                 command=self.export_json)
#         export_button.pack(side=tk.RIGHT, padx=10, pady=10)

#         # Tiêu đề căn giữa
#         title_label = tk.Label(table_header, text="Danh sách nhân viên", font=("Arial", 16, "bold"), bg="white")
#         title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#         # Frame chứa bảng với scrollbar
#         table_container = CTkFrame(self.master, border_width=1, corner_radius=10)
#         table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

#         # Header của bảng
#         header_frame = CTkFrame(table_container, fg_color="#57a1f8", height=40)
#         header_frame.pack(fill=tk.X)

#         headers = ["ID", "Họ tên", "Ngày sinh", "Số điện thoại", "Thao tác"]
#         header_widths = [60, 120, 250, 180, 180, 200]

#         # Cấu hình trọng số cho các cột
#         for i, width in enumerate(header_widths):
#             header_frame.grid_columnconfigure(i, weight=0, minsize=width)

#         for i, (header, width) in enumerate(zip(headers, header_widths)):
#             label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"), 
#                                 bg="#57a1f8", fg="white", anchor="center")
#             label.grid(row=0, column=i, padx=1, pady=8, sticky="ew")

#         # Frame chứa Canvas và Scrollbar cho nội dung bảng
#         scroll_container = tk.Frame(table_container, bg="white")
#         scroll_container.pack(fill=tk.BOTH, expand=True)

#         # Tạo Canvas và Scrollbar
#         canvas = tk.Canvas(scroll_container, bg="white")
#         scrollbar = CTkScrollbar(master=scroll_container, orientation="vertical", command=canvas.yview,
#                             width=12, corner_radius=6,
#                             fg_color="white", bg_color="white",
#                             button_color="#57a1f8", button_hover_color="#2b8ee0")
#         scrollbar.pack(side="right", fill="y")
#         canvas.pack(side="left", fill="both", expand=True)
#         scrollable_frame = CTkFrame(canvas, fg_color="white")

#         scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )

#         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)
        
#         # load data:
#         self.load_data_staff_from_file()


#         # Tạo các dòng dữ liệu
#         for i, patient in enumerate(self.staff_data):
#             bg_color = "#f8f9fa" if i % 2 == 1 else "white"
#             hover_color = "#d0e6ff"  # Màu xanh nhạt khi hover

#             row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=45)

#             # Gán sự kiện hover
#             def on_enter(e, frame=row_frame):
#                 frame.configure(bg=hover_color)
#                 for widget in frame.winfo_children():
#                     if isinstance(widget, tk.Label):
#                         widget.configure(bg=hover_color)
#                     elif isinstance(widget, tk.Frame):
#                         widget.configure(bg=hover_color)

#             def on_leave(e, frame=row_frame, color=bg_color):
#                 frame.configure(bg=color)
#                 for widget in frame.winfo_children():
#                     if isinstance(widget, tk.Label):
#                         widget.configure(bg=color)
#                     elif isinstance(widget, tk.Frame):
#                         widget.configure(bg=color)

#             row_frame.bind("<Enter>", on_enter)
#             row_frame.bind("<Leave>", on_leave)
#             row_frame.pack(fill=tk.X)
            
#             # Cấu hình trọng số cho các cột của mỗi dòng để khớp với header
#             for j, width in enumerate(header_widths):
#                 row_frame.grid_columnconfigure(j, weight=0, minsize=width)

#             # Hiển thị thông tin bệnh nhân (chỉ hiển thị các trường cơ bản trong bảng)
#             display_data = [patient['id'], patient['name'], patient['birth_date'], patient['phone']]
#             for j, (data, width) in enumerate(zip(display_data, header_widths[:-1])):
#                 label = tk.Label(row_frame, text=str(data), font=("Arial", 11), 
#                                  bg=bg_color, anchor="center")
#                 label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")
            
#             # Frame chứa các nút thao tác
#             action_frame = tk.Frame(row_frame, bg=bg_color)
#             action_frame.grid(row=0, column=len(display_data), padx=5, pady=5)
            
#             # Nút xem chi tiết
#             detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
#                                     fg_color="#17a2b8", text_color="white", hover_color="#138496",
#                                     corner_radius=3, font=("Arial", 9),
#                                     command=lambda p=patient: self.view_staff_detail(p))
#             detail_btn.pack(side=tk.LEFT, padx=2)
            
#             # Nút xóa
#             delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
#                                     fg_color="#dc3545", text_color="white", hover_color="#c82333",
#                                     corner_radius=3, font=("Arial", 9),
#                                     command=lambda p=patient: self.delete_staff(p)) # Đổi tên hàm delete_patient thành delete_staff cho rõ ràng
#             delete_btn.pack(side=tk.LEFT, padx=2)

#         # Bind mousewheel to canvas
#         def _on_mousewheel(event):
#             canvas.yview_scroll(int(-1*(event.delta/120)), "units")
#         canvas.bind_all("<MouseWheel>", _on_mousewheel)

#     def view_staff_detail(self, staff_data):
#         """Xem chi tiết nhân viên""" # Đổi chú thích từ bệnh nhân sang nhân viên
#         if self.navigation_callback:
#             # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
#             self.navigation_callback('staffs_detail', staff_data)
#         else:
#             # Mở trực tiếp (dành cho test độc lập)
#             self.open_staff_detail_window(staff_data)

#     def add_new_staff(self):
#         """Thêm nhân viên mới""" # Đổi chú thích từ bệnh nhân sang nhân viên
#         if self.navigation_callback:
#             # Sử dụng callback để chuyển màn hình (dành cho tích hợp với GUI_Main)
#             self.navigation_callback('staffs_detail', None)
#         else:
#             # Mở trực tiếp (dành cho test độc lập)
#             self.open_staff_detail_window(None)

#     def open_staff_detail_window(self, staff_data):
#         """Mở cửa sổ chi tiết nhân viên (dành cho test độc lập)""" # Đổi chú thích từ bệnh nhân sang nhân viên
#         # Xóa nội dung hiện tại của master frame
#         for widget in self.master.winfo_children():
#             widget.destroy()
        
#         # Tạo StaffDetailGui mới và hiển thị nó
#         detail_gui = StaffDetailGui(self.master, staff_data)
#         detail_gui.pack(fill=tk.BOTH, expand=True) # *** THÊM DÒNG NÀY ***
    
#     def delete_staff(self, staff_data): # Đổi tên hàm từ delete_patient thành delete_staff
#         """Xóa nhân viên đã chọn khỏi danh sách và file""" # Đổi chú thích từ bệnh nhân sang nhân viên
#         if not self.staff_data:
#             messagebox.showwarning("Cảnh báo", "Không thể xóa nhân viên mới chưa được lưu!") # Đổi từ bệnh nhân sang nhân viên
#             return

#         result = messagebox.askyesno("Xác nhận", 
#                                   "Bạn có chắc chắn muốn xóa thông tin nhân viên này?\n" # Đổi từ bệnh nhân sang nhân viên
#                                   "Hành động này không thể hoàn tác!")

#         if result:
#             # Xóa trực tiếp theo object
#             self.staff_data = [s for s in self.staff_data if s != staff_data] # Đổi p thành s và patient_data thành staff_data

#             # Ghi lại vào file JSON
#             self.save_data_staff_to_file() # Đổi save_data_to_file thành save_data_staff_to_file

#             # Cập nhật giao diện
#             self.refresh_table() # Thay vì refresh_patient_list không tồn tại, dùng refresh_table

#             messagebox.showinfo("Thành công", "Đã xóa nhân viên khỏi hệ thống.") # Đổi từ bệnh nhân sang nhân viên

#     # hàm refresh
#     # Hàm refresh_patient_list không tồn tại trong class này, bạn có refresh_table.
#     # Nếu bạn muốn refresh_patient_list hiển thị dữ liệu dạng text, bạn cần tạo widget display_data.
#     # Hiện tại, refresh_table là hàm hợp lý để dùng.
#     # def refresh_patient_list(self): 
#     #     self.display_data.delete("1.0", "end")  # Nếu là Text widget
#     #     for patient in self.staff_data:
#     #         line = f"{patient.get('id','')} - {patient.get('name','')} - {patient.get('phone','')}\n"
#     #         self.display_data.insert("end", line)
            
#     def export_json(self):
#         """Xuất dữ liệu ra file JSON"""
#         try:
#             import json
#             from tkinter import filedialog
            
#             # Chọn nơi lưu file
#             file_path = filedialog.asksaveasfilename(
#                 title="Lưu file JSON",
#                 defaultextension=".json",
#                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
#             )
            
#             if file_path:
#                 # Xuất dữ liệu
#                 with open(file_path, 'w', encoding='utf-8') as f:
#                     json.dump(self.staff_data, f, ensure_ascii=False, indent=2)
                
#                 messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")
                
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

#     def refresh_table(self):
#         """Làm mới bảng dữ liệu"""
#         # Xóa nội dung hiện tại và tạo lại
#         for widget in self.master.winfo_children():
#             widget.destroy()
#         self.setup_ui()

#     def set_navigation_callback(self, callback):
#         """Thiết lập callback cho navigation"""
#         self.navigation_callback = callback


# # Test riêng biệt (chỉ dành cho development)
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Test Danh sách nhân viên") # Đổi tên cửa sổ
#     root.configure(bg="#f8f9fa")
#     root.resizable(True, True)

#     window_width = 1200
#     window_height = 700
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     center_x = int((screen_width - window_width) / 2)
#     center_y = int((screen_height - window_height) / 3)
#     root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

#     # Test với frame content
#     content_frame = tk.Frame(root, bg="#f8f9fa")
#     content_frame.pack(expand=True, fill=tk.BOTH)

#     # Khởi tạo giao diện
#     staff_list_gui = StaffListGui(content_frame) # Đổi tên biến cho rõ ràng

#     root.mainloop()


# GUI_StaffList.py
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from customtkinter import CTkButton
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkScrollbar
from GUI_StaffDetail import StaffDetailGui # Chỉ giữ import này vì nó được sử dụng
import json

class StaffListGui():
    def __init__(self, master, navigation_callback=None):
        self.master = master
        self.navigation_callback = navigation_callback
        self.setup_ui()

    # hàm load và save data
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
        # Header của bảng với nút thêm
        table_header = tk.Frame(self.master, bg="white", height=60)
        table_header.pack(fill=tk.X, padx=20, pady=(10, 20))

        # Nút thêm nhân viên
        add_button = CTkButton(master=table_header, text="➕ Thêm nhân viên", width=150, height=35,
                                fg_color="#28a745", text_color="white", hover_color="#218838", corner_radius=5,
                                command=self.add_new_staff)
        add_button.pack(side=tk.RIGHT, pady=10)

        # Nút xuất file Json
        export_button = CTkButton(master=table_header, text="📄 Xuất file Json", width=150, height=35,
                                fg_color="#ffc107", text_color="white", hover_color="#e0a800", corner_radius=5,
                                command=self.export_json)
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

        headers = ["ID", "Họ tên", "Ngày sinh", "Số điện thoại", "Thao tác"]
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

        # load data:
        self.load_data_staff_from_file()

        # Tạo các dòng dữ liệu
        for i, staff in enumerate(self.staff_data): # Đổi patient thành staff
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
            display_data = [staff['id'], staff['name'], staff['birth_date'], staff['phone']]
            for j, (data, width) in enumerate(zip(display_data, header_widths[:-1])):
                label = tk.Label(row_frame, text=str(data), font=("Arial", 11),
                                 bg=bg_color, anchor="center")
                label.grid(row=0, column=j, padx=1, pady=8, sticky="ew")

            # Frame chứa các nút thao tác
            action_frame = tk.Frame(row_frame, bg=bg_color)
            action_frame.grid(row=0, column=len(display_data), padx=5, pady=5)

            # Nút xem chi tiết
            detail_btn = CTkButton(master=action_frame, text="Chi tiết", width=60, height=28,
                                    fg_color="#17a2b8", text_color="white", hover_color="#138496",
                                    corner_radius=3, font=("Arial", 9),
                                    command=lambda s=staff: self.view_staff_detail(s)) # Đổi p thành s
            detail_btn.pack(side=tk.LEFT, padx=2)

            # Nút xóa
            delete_btn = CTkButton(master=action_frame, text="Xóa", width=50, height=28,
                                    fg_color="#dc3545", text_color="white", hover_color="#c82333",
                                    corner_radius=3, font=("Arial", 9),
                                    command=lambda s=staff: self.delete_staff(s)) # Đổi p thành s và delete_patient thành delete_staff
            delete_btn.pack(side=tk.LEFT, padx=2)

        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def view_staff_detail(self, staff_data):
        """Xem chi tiết nhân viên"""
        if self.navigation_callback:
            self.navigation_callback('staffs_detail', staff_data)
        else:
            self.open_staff_detail_window(staff_data)

    def add_new_staff(self):
        """Thêm nhân viên mới"""
        if self.navigation_callback:
            self.navigation_callback('staffs_detail', None)
        else:
            self.open_staff_detail_window(None)

    def open_staff_detail_window(self, staff_data):
        """Mở cửa sổ chi tiết nhân viên (dành cho test độc lập)"""
        for widget in self.master.winfo_children():
            widget.destroy()

        detail_gui = StaffDetailGui(self.master, staff_data, self.navigation_callback)
        detail_gui.pack(fill=tk.BOTH, expand=True) # Thêm dòng này để hiển thị GUI_StaffDetail

    def delete_staff(self, staff_data):
        """Xóa nhân viên đã chọn khỏi danh sách và file"""
        if not self.staff_data:
            messagebox.showwarning("Cảnh báo", "Không thể xóa nhân viên mới chưa được lưu!")
            return

        result = messagebox.askyesno("Xác nhận",
                                 "Bạn có chắc chắn muốn xóa thông tin nhân viên này?\n"
                                 "Hành động này không thể hoàn tác!")

        if result:
            self.staff_data = [s for s in self.staff_data if s != staff_data] # Đổi p thành s và patient_data thành staff_data

            self.save_data_staff_to_file() # Gọi đúng hàm lưu

            self.refresh_table() # Gọi refresh_table thay vì refresh_patient_list không tồn tại

            messagebox.showinfo("Thành công", "Đã xóa nhân viên khỏi hệ thống.")

    def export_json(self):
        """Xuất dữ liệu ra file JSON"""
        try:
            import json
            from tkinter import filedialog

            file_path = filedialog.asksaveasfilename(
                title="Lưu file JSON",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.staff_data, f, ensure_ascii=False, indent=2)

                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

    def refresh_table(self):
        """Làm mới bảng dữ liệu"""
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_ui()

    def set_navigation_callback(self, callback):
        """Thiết lập callback cho navigation"""
        self.navigation_callback = callback


# Test riêng biệt (chỉ dành cho development)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Danh sách nhân viên") # Đổi tiêu đề
    root.configure(bg="#f8f9fa")
    root.resizable(True, True)

    window_width = 1200
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 3)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    content_frame = tk.Frame(root, bg="#f8f9fa")
    content_frame.pack(expand=True, fill=tk.BOTH)

    staff_list_gui = StaffListGui(content_frame) # Đổi tên biến

    root.mainloop()