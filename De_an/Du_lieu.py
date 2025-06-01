class User:
    def __init__(self, tenDN, matKhau, quyen=False):
        self.tenDN = tenDN
        self.matKhau = matKhau
        self.quyen = quyen

class Book:
    def __init__(self, id, tieuDe, tacGia, namXuatBan, theLoai, tinhTrang=True):
        self.id = id
        self.tieuDe = tieuDe
        self.tacGia = tacGia
        self.namXuatBan = namXuatBan
        self.theLoai = theLoai
        self.tinhTrang = tinhTrang

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.tieuDe,
            "author": self.tacGia,
            "year": self.namXuatBan,
            "genre": self.theLoai,
            "available": self.tinhTrang
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data["author"],
            data["year"],
            data["genre"],
            data.get("available", True)
        )