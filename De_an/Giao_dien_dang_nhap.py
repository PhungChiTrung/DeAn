import tkinter as tk
from tkinter import messagebox

class LoginFrame(tk.Frame):
    def __init__(self, master, libraryManager, onLoginSuccess):
        super().__init__(master)
        self.libraryManager = libraryManager
        self.onLoginSuccess = onLoginSuccess
        
        self.place(x=0, y=0, relwidth=1, relheight=1)

        self.giaoDien()
    
    def giaoDien(self):
        # Chiều rộng và chiều cao của form
        formWidth = 300
        formHeight = 250
        
        # Vị trí bắt đầu của form (căn giữa)
        startX = (450 - formWidth) // 2  # giả sử cửa sổ rộng 450px
        startY = 40

        # Tiêu đề
        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 16, "bold")).place(x=startX + formWidth//2 - 60, y=startY)
        
        # Tên đăng nhập - label
        tk.Label(self, text="Tên đăng nhập:", anchor="w").place(x=startX, y=startY + 60, width=formWidth, height=20)
        
        # Tên đăng nhập - entry
        self.tenDN = tk.StringVar()
        nhapTenDN = tk.Entry(self, textvariable=self.tenDN, width=30)
        nhapTenDN.place(x=startX, y=startY + 85, width=formWidth, height=25)
        
        # Mật khẩu - label
        tk.Label(self, text="Mật khẩu:", anchor="w").place(x=startX, y=startY + 120, width=formWidth, height=20)
        
        # Mật khẩu - entry
        self.matKhau = tk.StringVar()
        nhapMK = tk.Entry(self, textvariable=self.matKhau, width=30, show="*")
        nhapMK.place(x=startX, y=startY + 145, width=formWidth, height=25)
        
        # Nút đăng nhập
        login_button = tk.Button(self, text="Đăng nhập", command=self.login, width=12)
        login_button.place(x=startX + formWidth//2 - 50, y=startY + 190, width=100, height=30)
        
        # Focus vào ô tên đăng nhập khi khởi động
        nhapTenDN.focus_set()
        
        # Binding Enter key cho cả hai ô nhập
        nhapTenDN.bind("<Return>", lambda event: self.login())
        nhapMK.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.tenDN.get()
        password = self.matKhau.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Vui lòng nhập tên đăng nhập và mật khẩu")
            return
        
        user = self.libraryManager.athenticateUser(username, password)
        if user:
            self.onLoginSuccess(user)
        else:
            messagebox.showerror("Error", "Tên đăng nhập hoặc mật khẩu không đúng")