import json
import os
import requests
import sys
import shutil
from tkinter import messagebox
from Du_lieu import User, Book

def get_read_path(filename):
    """Đường dẫn tới file đã được PyInstaller đóng gói (chỉ để copy lần đầu)"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, filename)

def get_data_path(filename):
    """Đường dẫn tới file mà chương trình sẽ thực sự đọc/ghi"""
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filename))

def ensure_data_file_exists(filename):
    """Copy file gốc từ bản đóng gói ra thư mục ghi nếu chưa tồn tại"""
    data_path = get_data_path(filename)
    if not os.path.exists(data_path):
        shutil.copy(get_read_path(filename), data_path)
    return data_path
class LibraryManager:
    def __init__(self):
        self.books = []
        self.users = []
        self.usersFile = ensure_data_file_exists("users.json")
        self.booksFile = ensure_data_file_exists("books.json")
        self.loadData()
    
    def loadData(self):
        # Load dữ liệu từ file books.json
        if os.path.exists(self.booksFile):
            try:
                with open(self.booksFile, "r", encoding="utf-8") as f:
                    booksData = json.load(f)
                    self.books = [Book.from_dict(book) for book in booksData]
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu: {e}")
                self.books = []

        # Load dữ liệu từ file users.json
        if os.path.exists(self.usersFile):
            try:
                with open(self.usersFile, "r", encoding="utf-8") as f:
                    usersData = json.load(f)
                    self.users = [User(user["username"], user["password"], user["is_admin"]) for user in usersData]
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu: {e}")
                self.users = []

        # Tạo quản trị viên mặc định(admin)
        if not self.users:
            self.users.append(User("admin", "admin", True))
            self.saveUsers()

    def saveBooks(self):
        # Save dữ liệu vào file books.json
        try:
            with open(self.booksFile, "w", encoding="utf-8") as f:
                booksData = [book.to_dict() for book in self.books]
                json.dump(booksData, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu dữ liệu: {e}")
    
    def saveUsers(self):
        # Save dữ liệu vào file users.json
        try:
            with open(self.usersFile, "w", encoding="utf-8") as f:
                usersData = [{"username": user.tenDN, "password": user.matKhau, "is_admin": user.quyen} for user in self.users]
                json.dump(usersData, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu dữ liệu: {e}")

    def addBook(self, tieuDe, tacGia, namXuatBan, theLoai):
        newID = 1
        if self.books:
            newID = max(book.id for book in self.books) + 1
        
        newBook = Book(newID, tieuDe, tacGia, namXuatBan, theLoai)
        self.books.append(newBook)
        self.saveBooks()
        return newBook
    
    def updateBook(self, id, tieuDe, tacGia, namXuatBan, theLoai, tinhTrang):
        for book in self.books:
            if book.id == id:
                book.tieuDe = tieuDe
                book.tacGia = tacGia
                book.namXuatBan = namXuatBan
                book.theLoai = theLoai
                book.tinhTrang = tinhTrang
                self.saveBooks()
                return book
        return None
    
    def deleteBook(self, id):
        for i, book in enumerate(self.books):
            if book.id == id:
                del self.books[i]
                self.saveBooks()
                return True
        return False
    
    def getBook(self, id):
        for book in self.books:
            if book.id == id:
                return book
        return None
    
    def getAllBooks(self):
        return self.books
    
    def searchBooks(self, tuKhoa):
        tuKhoa = tuKhoa.lower()
        ketQua = []
        for book in self.books:
            if (tuKhoa in book.tieuDe.lower() or
                tuKhoa in book.tacGia.lower() or
                tuKhoa in book.theLoai.lower() or
                tuKhoa in str(book.namXuatBan)):
                ketQua.append(book)
        return ketQua
    
    def athenticateUser(self, username, password):
        # Kiểm tra thông tin người dùng có tồn tại không
        for user in self.users:
            if user.tenDN == username and user.matKhau == password:
                return user
        return None

    def addUser(self, username, password, isAdmin=False):
        for user in self.users:
            if user.tenDN == username:
                return False
        
        self.users.append(User(username, password, isAdmin))
        self.saveUsers()
        return True
    
    def addBooksAPI(self, tuKhoa):
        try:
            # Sử dụng Open Library API để lấy thông tin sách và giới hạn 15 cuốn sách
            url = f"https://openlibrary.org/search.json?q={tuKhoa}&limit=15"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                messagebox.showerror("Lỗi", f"Lỗi khi gọi API: {response.status_code}")
                return []

            data = response.json()

            newBooks = []
            for doc in data.get("docs", []):
                tieuDe = doc.get("title", "Unknown Title")

                # Xử lý tác giả
                tacGia = "Unknown Author"
                if doc.get("author_name"):
                    tacGia = doc.get("author_name")[0]

                # Xử lý năm xuất bản
                namXuatBan = doc.get("first_publish_year", 0)
                if not namXuatBan:
                    namXuatBan = doc.get("publish_year", [0])[0] if doc.get("publish_year") else 0

                # Xử lý thể loại
                theLoai = "General"
                if doc.get("subject"):
                    subjects = doc.get("subject")
                    if len(subjects) > 0:
                        theLoai = subjects[0]

                # Tạo và thêm sách
                newBook = self.addBook(tieuDe, tacGia, namXuatBan, theLoai)
                newBooks.append(newBook)
            
            return newBooks
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Lỗi", f"Lỗi kết nối API: {e}")
            return []
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xử lý API: {e}")
            return []