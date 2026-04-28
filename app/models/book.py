import sqlite3
import os
from flask import current_app

# 資料庫路徑
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
        """
        建立資料庫連線。
        使用 sqlite3.Row 讓結果可以透過欄位名稱存取。
        """
        try:
            # 確保 instance 資料夾存在
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"資料庫連線失敗: {e}")
            return None

    @classmethod
    def create(cls, data):
        """
        新增一筆書籍記錄。
        :param data: 包含 title, author, reading_date, note, rating 的字典
        :return: 新增紀錄的 ID
        """
        conn = cls.get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, reading_date, note, rating) VALUES (?, ?, ?, ?, ?)",
                (data['title'], data['author'], data.get('reading_date'), data.get('note'), data['rating'])
            )
            conn.commit()
            book_id = cursor.lastrowid
            return book_id
        except (sqlite3.Error, KeyError) as e:
            print(f"新增書籍失敗: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @classmethod
    def get_all(cls, sort_by_rating=False):
        """
        獲取所有書籍。
        :param sort_by_rating: 是否依評分從高到低排序
        :return: Book 物件列表
        """
        conn = cls.get_db_connection()
        if not conn:
            return []
        try:
            query = "SELECT * FROM books"
            if sort_by_rating:
                query += " ORDER BY rating DESC"
            else:
                query += " ORDER BY created_at DESC"
            
            rows = conn.execute(query).fetchall()
            return [cls(**dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"獲取書籍列表失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, book_id):
        """
        透過 ID 獲取特定書籍。
        :param book_id: 書籍 ID
        :return: Book 物件或 None
        """
        conn = cls.get_db_connection()
        if not conn:
            return None
        try:
            row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            if row:
                return cls(**dict(row))
            return None
        except sqlite3.Error as e:
            print(f"獲取書籍詳情失敗: {e}")
            return None
        finally:
            conn.close()

    @classmethod
    def search(cls, keyword):
        """
        搜尋書名、作者或心得中包含關鍵字的書籍。
        :param keyword: 搜尋關鍵字
        :return: Book 物件列表
        """
        conn = cls.get_db_connection()
        if not conn:
            return []
        try:
            query = "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR note LIKE ?"
            pattern = f"%{keyword}%"
            rows = conn.execute(query, (pattern, pattern, pattern)).fetchall()
            return [cls(**dict(row)) for row in rows]
        except sqlite3.Error as e:
            print(f"搜尋書籍失敗: {e}")
            return []
        finally:
            conn.close()

    @classmethod
    def update(cls, book_id, data):
        """
        更新書籍資訊。
        :param book_id: 要更新的書籍 ID
        :param data: 包含更新內容的字典
        :return: True if success, False otherwise
        """
        conn = cls.get_db_connection()
        if not conn:
            return False
        try:
            conn.execute(
                "UPDATE books SET title = ?, author = ?, reading_date = ?, note = ?, rating = ? WHERE id = ?",
                (data['title'], data['author'], data.get('reading_date'), data.get('note'), data['rating'], book_id)
            )
            conn.commit()
            return True
        except (sqlite3.Error, KeyError) as e:
            print(f"更新書籍失敗: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @classmethod
    def delete(cls, book_id):
        """
        刪除一筆書籍記錄。
        :param book_id: 書籍 ID
        :return: True if success, False otherwise
        """
        conn = cls.get_db_connection()
        if not conn:
            return False
        try:
            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"刪除書籍失敗: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
