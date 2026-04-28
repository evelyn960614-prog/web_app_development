import os
from app import create_app, init_db

app = create_app()

if __name__ == '__main__':
    # 如果資料庫檔案不存在，自動初始化
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run(debug=True)
