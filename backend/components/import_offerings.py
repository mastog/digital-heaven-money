import os
import sqlite3

# 获取数据库文件路径
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_file_path = os.path.join(basedir, 'webdb.db')

# 要插入的数据
offering_data = [
    {"pic_url": "/images/oblation1.png", "name": "Wreath"},
    {"pic_url": "/images/oblation2.png", "name": "Heaven Money"},
    {"pic_url": "/images/oblation3.png", "name": "Incense"},
    {"pic_url": "/images/oblation4.png", "name": "Dessert"},
    {"pic_url": "/images/oblation5.png", "name": "Tribute Meat"},
    {"pic_url": "/images/oblation6.png", "name": "Liquor"},
]

def import_offerings_to_db():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # 创建表（如果还不存在）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS offerings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        pic_url TEXT
    )
    ''')

    for item in offering_data:
        cursor.execute('''
            INSERT INTO offerings (name, pic_url)
            VALUES (?, ?)
        ''', (item["name"], item["pic_url"]))

    conn.commit()
    conn.close()
    print(f"✅ 成功插入 {len(offering_data)} 条 Offering 数据！")

if __name__ == "__main__":
    import_offerings_to_db()
