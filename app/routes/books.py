from flask import Blueprint, render_template, request, redirect, url_for, abort

books_bp = Blueprint('books', __name__)

@books_bp.route('/books/add', methods=['GET', 'POST'])
def add():
    """
    新增書籍。
    GET: 渲染 add.html 表單。
    POST: 接收表單資料，儲存至資料庫後重導向至首頁。
    """
    pass

@books_bp.route('/books/<int:id>')
def detail(id):
    """
    查看書籍詳情與心得。
    參數：id (int) - 書籍 ID。
    邏輯：獲取書籍資料，渲染 detail.html。若不存在則回傳 404。
    """
    pass

@books_bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯書籍或心得。
    參數：id (int) - 書籍 ID。
    GET: 渲染 edit.html 並帶入原始資料。
    POST: 接收修改後的資料，更新資料庫後重導向至詳情頁。
    """
    pass

@books_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除書籍。
    參數：id (int) - 書籍 ID。
    邏輯：從資料庫移除紀錄，成功後重導向至首頁。
    """
    pass
