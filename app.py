import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


# 連接 SQLite 資料庫
def get_db_connection():
    conn = sqlite3.connect("database.db")

    # 讓查詢結果可以用欄位名稱讀取
    conn.row_factory = sqlite3.Row

    return conn


# 首頁
@app.route("/")
def index():
    conn = get_db_connection()

    # 只取得精選專案
    projects = conn.execute(
        "SELECT * FROM projects WHERE featured = 1"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        projects=projects
    )


# 所有專案
@app.route("/projects")
def project_list():
    conn = get_db_connection()

    projects = conn.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "projects.html",
        projects=projects
    )


# 單一專案詳細介紹
@app.route("/project/<int:project_id>")
def project_detail(project_id):
    conn = get_db_connection()

    project = conn.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    ).fetchone()

    conn.close()

    if project is None:
        return "找不到這個專案", 404

    return render_template(
        "project_detail.html",
        project=project
    )


# 關於我們
@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)