from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from app.models.book import Book

books_bp = Blueprint('books', __name__)

@books_bp.route('/books/add', methods=['GET', 'POST'])
def add():
    """
    新增書籍。
    GET: 渲染 add.html 表單。
    POST: 接收表單資料，儲存至資料庫後重導向至首頁。
    """
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        reading_date = request.form.get('reading_date')
        note = request.form.get('note')
        rating = request.form.get('rating')

        # 基本驗證
        if not title or not author or not rating:
            flash('書名、作者與評分為必填項目！', 'error')
            return render_template('add.html')

        try:
            rating = int(rating)
        except ValueError:
            flash('評分必須是數字！', 'error')
            return render_template('add.html')

        data = {
            'title': title,
            'author': author,
            'reading_date': reading_date,
            'note': note,
            'rating': rating
        }

        if Book.create(data):
            flash('書籍記錄新增成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('新增失敗，請檢查資料或稍後再試。', 'error')
            return render_template('add.html')

    return render_template('add.html')

@books_bp.route('/books/<int:id>')
def detail(id):
    """
    查看書籍詳情與心得。
    參數：id (int) - 書籍 ID。
    邏輯：獲取書籍資料，渲染 detail.html。若不存在則回傳 404。
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
    return render_template('detail.html', book=book)

@books_bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯書籍或心得。
    參數：id (int) - 書籍 ID。
    GET: 渲染 edit.html 並帶入原始資料。
    POST: 接收修改後的資料，更新資料庫後重導向至詳情頁。
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        reading_date = request.form.get('reading_date')
        note = request.form.get('note')
        rating = request.form.get('rating')

        # 基本驗證
        if not title or not author or not rating:
            flash('書名、作者與評分為必填項目！', 'error')
            return render_template('edit.html', book=book)

        data = {
            'title': title,
            'author': author,
            'reading_date': reading_date,
            'note': note,
            'rating': int(rating)
        }

        if Book.update(id, data):
            flash('更新成功！', 'success')
            return redirect(url_for('books.detail', id=id))
        else:
            flash('更新失敗。', 'error')
            return render_template('edit.html', book=book)

    return render_template('edit.html', book=book)

@books_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除書籍。
    參數：id (int) - 書籍 ID。
    邏輯：從資料庫移除紀錄，成功後重導向至首頁。
    """
    if Book.delete(id):
        flash('書籍已刪除。', 'success')
    else:
        flash('刪除失敗。', 'error')
    return redirect(url_for('main.index'))
