import sqlite3

# 連接資料庫；如果不存在，就建立 database.db
conn = sqlite3.connect("database.db")

# 建立 projects 資料表
conn.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    tech_stack TEXT,
    demo_url TEXT,
    github_url TEXT,
    image_url TEXT,
    status TEXT DEFAULT '開發中',
    featured INTEGER DEFAULT 0
)
""")

# 加入範例專案
projects = [
    (
        "商家網站系統",
        "Web",
        "展示商家資訊與商品，並提供相關網站功能。",
        "HTML, CSS, Flask",
        "",
        "",
        "images/shop.png",
        "開發中",
        1
    ),
    (
        "Database 知識庫",
        "Database",
        "整理與查詢資料庫相關知識。",
        "Python, Database",
        "",
        "",
        "images/database.png",
        "開發中",
        1
    ),
    (
        "AI 應用專案",
        "AI",
        "展示人工智慧或知識檢索相關應用。",
        "Python, AI, RAG",
        "",
        "",
        "images/ai.png",
        "開發中",
        0
    )
]

# 避免每次執行都重複新增範例資料
count = conn.execute(
    "SELECT COUNT(*) FROM projects"
).fetchone()[0]

if count == 0:
    conn.executemany("""
        INSERT INTO projects (
            title, category, description, tech_stack,
            demo_url, github_url, image_url, status, featured
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, projects)

conn.commit()
conn.close()

print("資料庫初始化完成！")