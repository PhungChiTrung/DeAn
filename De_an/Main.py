
from tkinter import messagebox
from Xu_ly import LibraryManager
from Giao_dien_dang_nhap import LoginFrame
from Giao_dien_chinh import MainApp

class LibraryApp:
    def __init__(self, root):
      self.root = root
      self.root.title("Hệ thống Quản lý Thư viện")
      self.root.geometry("800x600+600+200")
      self.root.protocol("WM_DELETE_WINDOW", self.onClose)
      
      self.libraryManager = LibraryManager()
      self.currentFrame = None
      
      self.showLogin()
    
    def showLogin(self):
        if self.currentFrame:
            self.currentFrame.destroy()
        
        self.root.geometry("450x350+600+200")
        self.root.title("Hệ thống Quản lý Thư viện")
        self.root.resizable(False, False)
        
        self.currentFrame = LoginFrame(self.root, self.libraryManager, self.onLoginSuccess)
    
    def onLoginSuccess(self, user):
        if self.currentFrame:
            self.currentFrame.destroy()
        
        self.root.geometry("800x600+600+200")
        self.root.title("Hệ thống Quản lý Thư viện")
        self.root.resizable(True, True)
        
        self.currentFrame = MainApp(self.root, user, self.libraryManager, self.showLogin)

    def onClose(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát khỏi ứng dụng?"):
            self.root.destroy()