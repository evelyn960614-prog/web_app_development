import sqlite3
import os

# 資料庫路徑 (依據 ARCHITECTURE.md 規劃)
DB_PATH = os.path.join('instance', 'database.db')

class Book:
    def __init__(self, id=None, title=None, author=None, reading_date=None, note=None, rating=None, created_at=None):
        self.id = id
        self.title = title
        self.author = author
        self.reading_date = reading_date
        self.note = note
        self.rating = rating
        self.created_at = created_at

    @staticmethod
    def get_db_connection():
        """建立資料庫連線"""
        # 確保 instance 資料夾存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, title, author, reading_date, note, rating):
        """新增一筆書籍記錄"""
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, reading_date, note, rating) VALUES (?, ?, ?, ?, ?)",
            (title, author, reading_date, note, rating)
        )
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return book_id

    @classmethod
    def get_all(cls, sort_by_rating=False):
        """獲取所有書籍，可選擇是否依評分排序"""
        conn = cls.get_db_connection()
        query = "SELECT * FROM books"
        if sort_by_rating:
            query += " ORDER BY rating DESC"
        else:
            query += " ORDER BY created_at DESC"
            
        books_raw = conn.execute(query).fetchall()
        conn.close()
        return [cls(**dict(row)) for row in books_raw]

    @classmethod
    def get_by_id(cls, book_id):
        """透過 ID 獲取特定書籍"""
        conn = cls.get_db_connection()
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        conn.close()
        if row:
            return cls(**dict(row))
        return None

    @classmethod
    def search(cls, keyword):
        """搜尋書名或作者中包含關鍵字的書籍"""
        conn = cls.get_db_connection()
        query = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR note LIKE ?"
        pattern = f"%{keyword}%"
        books_raw = conn.execute(query, (pattern, pattern, pattern)).fetchall()
        conn.close()
        return [cls(**dict(row)) for row in books_raw]

    @classmethod
    def update(cls, book_id, title, author, reading_date, note, rating):
        """更新書籍資訊"""
        conn = cls.get_db_connection()
        conn.execute(
            "UPDATE books SET title = ?, author = ?, reading_date = ?, note = ?, rating = ? WHERE id = ?",
            (title, author, reading_date, note, rating, book_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, book_id):
        """刪除一筆書籍記錄"""
        conn = cls.get_db_connection()
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
