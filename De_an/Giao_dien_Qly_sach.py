import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class BookForm(tk.Toplevel):
    def __init__(self, parent, libraryManager, book = None, onSave = None):
        super().__init__(parent)
        self.libraryManager = libraryManager
        self.book = book
        self.onSave = onSave

        self.title("Thêm sách mới" if not book else "Cập nhật sách")
        self.geometry("400x300")
        self.giaoDien()

    def giaoDien(self): 
        tk.Label(self, text="Tiêu đề:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.tieuDe = tk.StringVar(value=self.book.tieuDe if self.book else "")
        tk.Entry(self, textvariable=self.tieuDe, width=30).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Tác giả:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.tacGia = tk.StringVar(value=self.book.tacGia if self.book else "")
        tk.Entry(self, textvariable=self.tacGia, width=30).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self, text="Năm xuất bản:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.namXuatBan = tk.StringVar(value=str(self.book.namXuatBan) if self.book else "")
        tk.Entry(self, textvariable=self.namXuatBan, width=30).grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self, text="Thể loại:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.theloai = tk.StringVar(value=self.book.theLoai if self.book else "")
        tk.Entry(self, textvariable=self.theloai, width=30).grid(row=3, column=1, padx=10, pady=10)

        # Save button
        tk.Button(self, text="Lưu", command=self.save).grid(row=5, column=0, columnspan=2, pady=20)

        # Trạng thái (chỉ dùng cho phần cập nhât sách)
        self.trangThai = tk.BooleanVar(value=self.book.tinhTrang if self.book else True)
        if self.book:
            tk.Checkbutton(self, text="Có sẵn", variable=self.trangThai).grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
       
    def save(self):
        tieuDe = self.tieuDe.get()
        tacGia = self.tacGia.get()
        namXuatBanStr = self.namXuatBan.get()
        theLoai = self.theloai.get()
        tinhTrang = self.trangThai.get()

        if not tieuDe or not tacGia or not namXuatBanStr or not theLoai:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return
        
        try:
            namXuatBan = int(namXuatBanStr)
            if namXuatBan < 0 or namXuatBan > datetime.now().year:
                raise ValueError("Năm không hợp lệ")
        except ValueError:
            messagebox.showerror("Lỗi", "Năm xuất bản không hợp lệ")
            return
        
        if self.book:
            updatedBook = self.libraryManager.updateBook(self.book.id, tieuDe, tacGia, namXuatBan, theLoai, tinhTrang)
            if updatedBook:
                messagebox.showinfo("Thành công", "Cập nhật sách thành công")
                if self.onSave:
                    self.onSave()
                self.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật sách")
        else:
            newBook = self.libraryManager.addBook(tieuDe, tacGia, namXuatBan, theLoai)
            if newBook:
                messagebox.showinfo("Thành công", "Thêm sách thành công")
                if self.onSave:
                    self.onSave()
                self.destroy()
            else:
                messagebox.showerror("Lỗi", "Không thể thêm sách")
