import requests
from tkinter import messagebox, ttk
import tkinter as tk
from Du_lieu import Book

class APISearchFrame(tk.Toplevel):
    def __init__(self, parent, libraryManager, onBooksAdded=None):
        super().__init__(parent)
        self.libraryManager = libraryManager
        self.onBooksAdded = onBooksAdded

        self.title("Tìm kiếm và nhập sách từ API")
        self.geometry("600x400")
        self.giaoDien()

    def giaoDien(self):
        timKiemFrame = tk.Frame(self)
        timKiemFrame.pack(fill="x", padx=10, pady=10)

        tk.Label(timKiemFrame, text="Từ khóa tìm kiếm:").pack(side="left", padx=5)
        self.timKiem = tk.StringVar()
        tk.Entry(timKiemFrame, textvariable=self.timKiem, width=30).pack(side="left", padx=5)
        tk.Button(timKiemFrame, text="Tìm kiếm", command=self.searchAPI).pack(side="left", padx=5)

        # Results list
        ketQuaFrame = tk.LabelFrame(self, text="Kết quả tìm kiếm")
        ketQuaFrame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("title", "author", "year", "genre")
        self.tree = ttk.Treeview(ketQuaFrame, columns=columns, show="headings")
        self.tree.heading("title", text="Tiêu đề")
        self.tree.heading("author", text="Tác giả")
        self.tree.heading("year", text="Năm")
        self.tree.heading("genre", text="Thể loại")

        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("year", width=80)
        self.tree.column("genre", width=150)

        scrollbar = ttk.Scrollbar(ketQuaFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        buttonFrame = tk.Frame(self)
        buttonFrame.pack(fill="x", padx=10, pady=10)

        tk.Button(buttonFrame, text="Thêm sách đã chọn", command=self.addBooks).pack(side="left", padx=5)
        tk.Button(buttonFrame, text="Thêm tất cả", command=self.addAllBooks).pack(side="left", padx=5)

    def searchAPI(self):
        tuKhoa = self.timKiem.get()
        if not tuKhoa:
            messagebox.showerror("Lỗi", "Vui lòng nhập từ khóa tìm kiếm")
            return
        
        # Clear existing results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Hiển thị trạng thái tìm kiếm
            statusLabel = tk.Label(self, text="Đang tìm kiếm...", fg="blue")
            statusLabel.pack(pady=5)
            self.update()  # Cập nhật giao diện ngay lập tức
        
            # Gọi API Open Library
            url = f"https://openlibrary.org/search.json?q={tuKhoa}&limit=15"
            response = requests.get(url, timeout=60)
        
            if response.status_code != 200:
                messagebox.showerror("Lỗi", f"Lỗi khi gọi API: {response.status_code}")
                statusLabel.destroy()
                return
            
            data = response.json()
        
            # Xu ly ket qua
            self.searchResults = []
            for doc in data.get("docs", []):
                title = doc.get("title", "Unknown Title")
        
                # Xu ly tac gia
                author = "Unknown Author"
                if doc.get("author_name"):
                    author = doc.get("author_name")[0]
        
                # Xu ly nam xuat ban
                year = doc.get("first_publish_year", 0)
                if not year:
                    year = doc.get("publish_year", [0])[0] if doc.get("publish_year") else 0
        
                # Xu ly the loai
                genre = "General"
                if doc.get("subject"):
                    subjects = doc.get("subject")
                    if len(subjects) > 0:
                        genre = subjects[0]

                book = Book(0, title, author, year, genre)
                self.searchResults.append(book)

            if not self.searchResults:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp")
            else:
                for book in self.searchResults:
                    self.tree.insert("", "end", values=(book.tieuDe, book.tacGia, book.namXuatBan, book.theLoai))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối: {e}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xử lý: {e}")
        finally:
            if 'statusLabel' in locals():
                statusLabel.destroy()

    def addBooks(self):
        chon = self.tree.selection()
        if not chon:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một sách")
            return
        
        windowXLy = tk.Toplevel(self)
        windowXLy.title("Đang xử lý")
        windowXLy.geometry("300x100")
        windowXLy.transient(self)
        windowXLy.grab_set()

        labelXLy = tk.Label(windowXLy, text="Đang thêm sách vào thư viện...")
        labelXLy.pack(pady=20)

        windowXLy.update()

        try:
            addedBooks = []
            for i, item in enumerate(chon):
                values = self.tree.item(item, "values")
                title, author = values[0], values[1]

                try:
                    year = int(values[2])
                except ValueError:
                    year = 0

                genre = values[3]

                newBook = self.libraryManager.addBook(title, author, year, genre)
                addedBooks.append(newBook)

            messagebox.showinfo("Thành công", f"Đã thêm {len(addedBooks)} sách vào thư viện")
            if self.onBooksAdded:
                self.onBooksAdded()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm sách: {e}")
        finally:
            windowXLy.destroy()

    def addAllBooks(self):
        if not hasattr(self, 'searchResults') or not self.searchResults:
            messagebox.showerror("Lỗi", "Không có sách nào để thêm")
            return

        windowXLy = tk.Toplevel(self)
        windowXLy.title("Đang xử lý")
        windowXLy.geometry("300x100")
        windowXLy.transient(self)
        windowXLy.grab_set()

        labelXLy = tk.Label(windowXLy, text="Đang thêm sách vào thư viện...")
        labelXLy.pack(pady=20)

        windowXLy.update()

        try:
            addedBooks = []
            for book in self.searchResults:
                newBook = self.libraryManager.addBook(book.tieuDe, book.tacGia, book.namXuatBan, book.theLoai)
                addedBooks.append(newBook)

            messagebox.showinfo("Thành công", f"Đã thêm {len(addedBooks)} sách vào thư viện")
            if self.onBooksAdded:
                self.onBooksAdded()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm sách: {e}")
        finally:
            windowXLy.destroy()
