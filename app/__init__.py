import os
import sqlite3
from flask import Flask
from app.routes.main import main_bp
from app.routes.books import books_bp

def create_app():
    app = Flask(__name__)
    
    # 基本配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp)

    return app

def init_db():
    """初始化資料庫並建立資料表"""
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print("資料庫初始化成功！")
