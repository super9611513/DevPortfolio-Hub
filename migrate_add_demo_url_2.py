"""安全遷移：為 projects 新增 demo_url_2 欄位。

用法：
  python migrate_add_demo_url_2.py                      # 備份並補欄位（已存在則跳過）
  python migrate_add_demo_url_2.py --db path/to.db      # 指定資料庫
  python migrate_add_demo_url_2.py --merge 主ID 重複ID   # 預覽合併（不寫入）
  python migrate_add_demo_url_2.py --merge 主ID 重複ID --apply
合併只會把重複那筆的 demo_url 複製到主作品的 demo_url_2，且不會刪除任何資料列。
"""
import argparse
import os
import sqlite3
from datetime import datetime


def backup(db_path):
    os.makedirs("backups", exist_ok=True)
    name = datetime.now().strftime("database_%Y%m%d_%H%M%S.db")
    dest = os.path.join("backups", name)
    src = sqlite3.connect(db_path)
    dst = sqlite3.connect(dest)
    src.backup(dst)
    dst.close()
    src.close()
    print(f"已備份到 {dest}")


def ensure_column(conn):
    cols = [r[1] for r in conn.execute("PRAGMA table_info(projects)")]
    if "demo_url_2" in cols:
        print("demo_url_2 已存在，略過。")
    else:
        conn.execute("ALTER TABLE projects ADD COLUMN demo_url_2 TEXT")
        print("已新增 demo_url_2 欄位。")


def merge(conn, main_id, dup_id, apply):
    main = conn.execute(
        "SELECT id, title, demo_url, demo_url_2 FROM projects WHERE id = ?", (main_id,)
    ).fetchone()
    dup = conn.execute(
        "SELECT id, title, demo_url FROM projects WHERE id = ?", (dup_id,)
    ).fetchone()
    if main is None or dup is None:
        raise SystemExit("找不到指定的 ID。")
    print(f"主作品：{main}\n重複作品：{dup}")
    if main[3]:
        raise SystemExit("主作品的 demo_url_2 已有值，為避免覆蓋而中止。")
    if not dup[2]:
        raise SystemExit("重複作品沒有 demo_url 可複製。")
    print(f"將設定 作品 {main_id} 的 demo_url_2 = {dup[2]}（不刪除作品 {dup_id}）")
    if apply:
        conn.execute("UPDATE projects SET demo_url_2 = ? WHERE id = ?", (dup[2], main_id))
        print("已套用。")
    else:
        print("僅預覽，加上 --apply 才會寫入。")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--db", default="database.db")
    p.add_argument("--merge", nargs=2, type=int, metavar=("主ID", "重複ID"))
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()

    backup(a.db)
    conn = sqlite3.connect(a.db)
    ensure_column(conn)
    if a.merge:
        merge(conn, a.merge[0], a.merge[1], a.apply)
    conn.commit()
    conn.close()
