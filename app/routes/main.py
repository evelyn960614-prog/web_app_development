from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示書籍清單與評分排行榜。
    邏輯：獲取所有書籍與高分排名，渲染 index.html。
    """
    pass

@main_bp.route('/search')
def search():
    """
    搜尋頁面：根據關鍵字搜尋書籍。
    參數：q (str) - 搜尋關鍵字。
    邏輯：呼叫搜尋方法，渲染 search.html。
    """
    pass
