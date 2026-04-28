# 讀書筆記本 (Reading Notebook) 路由設計文件

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `index.html` | 顯示書籍清單與高分排行榜 |
| **搜尋書籍** | GET | `/search` | `search.html` | 根據關鍵字搜尋書籍與心得 |
| **顯示新增頁面** | GET | `/books/add` | `add.html` | 顯示新增書籍的表單 |
| **執行新增動作** | POST | `/books/add` | — | 接收表單、存入資料庫、重導向至首頁 |
| **書籍詳情** | GET | `/books/<id>` | `detail.html` | 顯示特定書籍的詳細心得 |
| **顯示編輯頁面** | GET | `/books/<id>/edit` | `edit.html` | 顯示編輯書籍/心得的表單 |
| **執行編輯動作** | POST | `/books/<id>/edit` | — | 更新資料庫、重導向至詳情頁 |
| **執行刪除動作** | POST | `/books/<id>/delete`| — | 從資料庫移除紀錄、重導向至首頁 |

---

## 2. 每個路由的詳細說明

### 首頁 (Index)
- **處理邏輯**：呼叫 `Book.get_all(sort_by_rating=True)` 獲取排行，呼叫 `Book.get_all()` 獲取清單。
- **輸出**：渲染 `index.html`。

### 搜尋書籍 (Search)
- **輸入**：URL 參數 `q` (關鍵字)。
- **處理邏輯**：呼叫 `Book.search(keyword)`。
- **輸出**：渲染 `search.html` 並傳遞搜尋結果。

### 書籍詳情 (Detail)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Book.get_by_id(id)`。若不存在則回傳 404。
- **輸出**：渲染 `detail.html`。

### 新增/編輯/刪除 (CRUD)
- **輸入**：表單欄位 `title`, `author`, `reading_date`, `note`, `rating`。
- **處理邏輯**：呼叫 `Book.create`, `Book.update`, 或 `Book.delete`。
- **錯誤處理**：驗證必填欄位。若 `id` 不存在則回傳 404。

---

## 3. Jinja2 模板清單

所有模板皆位於 `app/templates/` 目錄。

- `base.html`：基礎模板，包含導覽列 (Navbar) 與頁尾 (Footer)。
- `index.html`：繼承 `base.html`。首頁，展示書架與排行。
- `search.html`：繼承 `base.html`。搜尋結果頁。
- `add.html`：繼承 `base.html`。新增書籍表單。
- `detail.html`：繼承 `base.html`。書籍詳細心得。
- `edit.html`：繼承 `base.html`。編輯心得與評分表單。

---

## 4. 路由模組化 (Blueprints) 規劃

依據架構文件，我們將路由拆分為兩個 Blueprint：

1. **main**: 處理通用頁面。
   - 檔案：`app/routes/main.py`
2. **books**: 處理書籍資源的 CRUD。
   - 檔案：`app/routes/books.py`
