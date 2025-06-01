import tkinter as tk
from tkinter import messagebox, ttk
from Giao_dien_Qly_sach import BookForm
from Giao_dien_Qly_Ngdung import UserManagement
from Giao_dien_Tkiem_API import APISearchFrame

class MainApp(tk.Frame):
    def __init__(self, master, user, libraryManager, onLogout):
        super().__init__(master)
        self.master = master
        self.user = user
        self.libraryManager = libraryManager
        self.onLogout = onLogout

        self.pack(fill="both", expand=True)
        self.giaoDien()
        self.lamMoiListB()

    def giaoDien(self):
        topFrame = tk.Frame(self)
        topFrame.pack(fill="x", padx=10, pady=10)

        # Search
        tk.Label(topFrame, text="Tìm kiếm:").pack(side="left", padx=5)
        self.timKiemV = tk.StringVar()
        timKiem = tk.Entry(topFrame, textvariable=self.timKiemV, width=30)
        timKiem.pack(side="left", padx=5)
        timKiem.bind("<Return>", lambda event: self.searchBook())
        tk.Button(topFrame, text="Tìm kiếm", command=self.searchBook).pack(side="left", padx=5)

        # Thông tin người dùng
        userInfo = tk.Label(topFrame, text=f"Đăng nhập với: {self.user.tenDN} ({'Admin' if self.user.quyen else 'User'})")
        userInfo.pack(side="right", padx=5)

        # Sách
        bookFrame = tk.LabelFrame(self, text="Danh sách sách")
        bookFrame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title", "author", "year", "genre", "available")
        self.tree = ttk.Treeview(bookFrame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Tiêu đề")
        self.tree.heading("author", text="Tác giả")
        self.tree.heading("year", text="Năm")
        self.tree.heading("genre", text="Thể loại")
        self.tree.heading("available", text="Trạng thái")

        self.tree.column("id", width=50)
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("year", width=80)
        self.tree.column("genre", width=150)
        self.tree.column("available", width=100)

        scrollbar = ttk.Scrollbar(bookFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Button frame
        buttonFrame = tk.Frame(self)
        buttonFrame.pack(fill="x", padx=10, pady=10)

        # Button chỉ dành cho người dùng
        tk.Button(buttonFrame, text="Xem chi tiết", command=self.viewBook).pack(side="left", padx=5)

        # Button chính cho admin
        if self.user.quyen:
            tk.Button(buttonFrame, text="Thêm sách", command=self.addBook).pack(side="left", padx=5)
            tk.Button(buttonFrame, text="Xóa sách", command=self.deleteBook).pack(side="left", padx=5)
            tk.Button(buttonFrame, text="Cập nhật lại sách", command=self.editBook).pack(side="left", padx=5)
            tk.Button(buttonFrame, text="Quản lý người dùng", command=self.manageUsers).pack(side="left", padx=5)
            tk.Button(buttonFrame, text="Tìm kiếm API", command=self.searchAPI).pack(side="left", padx=5)

        tk.Button(buttonFrame, text="Đăng xuất", command=self.lougout).pack(side="right", padx=5)

    def lamMoiListB(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for book in self.libraryManager.getAllBooks():
            status = "Có sẵn" if book.tinhTrang else "Đã mượn"
            self.tree.insert("", "end", values=(book.id, book.tieuDe, book.tacGia, book.namXuatBan, book.theLoai, status))

    def searchBook(self):
        tuKhoa = self.timKiemV.get()
        if not tuKhoa:
            self.lamMoiListB()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        ketQua = self.libraryManager.searchBooks(tuKhoa)
        for book in ketQua:
            status = "Có sẵn" if book.tinhTrang else "Đã mượn"
            self.tree.insert("", "end", values=(book.id, book.tieuDe, book.tacGia, book.namXuatBan, book.theLoai, status))

    def viewBook(self):
        chon = self.tree.selection()
        if not chon:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sách để xem")
            return
        
        item = chon[0]
        bookID = int(self.tree.item(item, "values")[0])
        book = self.libraryManager.getBook(bookID)
        
        if book:
            details = f"ID: {book.id}\n"
            details += f"Tiêu đề: {book.tieuDe}\n"
            details += f"Tác giả: {book.tacGia}\n"
            details += f"Năm xuất bản: {book.namXuatBan}\n"
            details += f"Thể loại: {book.theLoai}\n"
            details += f"Trạng thái: {'Có sẵn' if book.tinhTrang else 'Đã mượn'}"
            
            messagebox.showinfo("Chi tiết sách", details)
        
    def addBook(self):
        if not self.user.quyen:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này")
            return

        BookForm(self.master, self.libraryManager, onSave=self.lamMoiListB)

    def editBook(self):
        if not self.user.quyen:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này")
            return
        
        chon = self.tree.selection()
        if not chon:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sách để sửa")
            return
        
        item = chon[0]
        bookID = int(self.tree.item(item, "values")[0])
        book = self.libraryManager.getBook(bookID)
        
        if book:
            BookForm(self.master, self.libraryManager, book=book, onSave=self.lamMoiListB)

    def deleteBook(self):
        if not self.user.quyen:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này")
            return
        
        chon = self.tree.selection()
        if not chon:
            messagebox.showerror("Lỗi", "Vui lòng chọn một sách để xóa")
            return
        
        item = chon[0]
        bookID = int(self.tree.item(item, "values")[0])
        book = self.libraryManager.getBook(bookID)
        
        if book:
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sách '{book.tieuDe}'?")
            if confirm:
                success = self.libraryManager.deleteBook(bookID)
                if success:
                    messagebox.showinfo("Thành công", "Xóa sách thành công")
                    self.lamMoiListB()
                else:
                    messagebox.showerror("Lỗi", "Không thể xóa sách")
    
    def manageUsers(self):
        if not self.user.quyen:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này")
            return

        UserManagement(self.master, self.libraryManager)

    def searchAPI(self):
        if not self.user.quyen:
            messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này")
            return

        APISearchFrame(self.master, self.libraryManager, onBooksAdded=self.lamMoiListB)

    def lougout(self):
        comfirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?")
        if comfirm:
            self.onLogout()
        