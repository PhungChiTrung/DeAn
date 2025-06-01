import tkinter as tk
from tkinter import ttk, messagebox
import re

class UserManagement(tk.Toplevel):
    def __init__(self, parent, libraryManager):
        super().__init__(parent)
        self.libraryManager = libraryManager

        self.title("Quản lý người dùng")
        self.geometry("500x400")
        self.giaoDien()
        self.lamMoiListU()

    def giaoDien(self):
        frame = tk.LabelFrame(self, text="Thêm người dùng mới")
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Tên người dùng:").grid(row=0, column=0, padx=5, pady=5)
        self.tenDN = tk.StringVar()
        tk.Entry(frame, textvariable=self.tenDN).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        self.matKhau = tk.StringVar()
        tk.Entry(frame, textvariable=self.matKhau, show="*").grid(row=1, column=1, padx=5, pady=5)

        self.quyenV = tk.BooleanVar()
        tk.Checkbutton(frame, text="Là người quản trị", variable=self.quyenV).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        tk.Button(frame, text="Thêm người dùng", command=self.addUser).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        listUser = tk.LabelFrame(self, text="Danh sách người dùng")
        listUser.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("tenDN", "role")
        self.tree = ttk.Treeview(listUser, columns=columns, show="headings")
        self.tree.heading("tenDN", text="Tên người dùng")
        self.tree.heading("role", text="Vai trò")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def lamMoiListU(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for user in self.libraryManager.users:
            role = "Quản trị viên" if user.quyen else "Người dùng thường"
            self.tree.insert("", "end", values=(user.tenDN, role))

    def addUser(self):
        tenDN = self.tenDN.get()
        matKhau = self.matKhau.get()
        quyen = self.quyenV.get()

        if not tenDN or not matKhau:
            messagebox.showerror("Error", "Vui lòng nhập tên đăng nhập và mật khẩu")
            return
        
        if not re.match(r"^[a-zA-Z0-9_]+$", tenDN):
            messagebox.showerror("Error", "Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới")
            return
        
        if len(matKhau) < 4:
            messagebox.showerror("Error", "Mật khẩu phải có ít nhất 4 ký tự")
            return
        
        success = self.libraryManager.addUser(tenDN, matKhau, quyen)
        if success:
            messagebox.showinfo("Success", "Thêm người dùng thành công")
            self.tenDN.set("")
            self.matKhau.set("")
            self.quyenV.set(False)
            self.lamMoiListU()
        else:
            messagebox.showerror("Error", "Tên đăng nhập đã tồn tại")