import os
import sqlite3
import re

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 修改为你的数据库文件和 txt 文件路径
db_file_path = os.path.join(basedir, 'webdb.db')
txt_file_path = os.path.join(basedir, 'TodayInHistory.txt')

# 正则表达式：匹配 (id, year, month, day, type, 'name', 'data', insert_time)
row_pattern = re.compile(
    r'\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*\'((?:\\\'|[^\'])*)\',\s*\'((?:\\\'|[^\'])*)\',\s*(\d+)\s*\)',
    re.DOTALL
)

def parse_history_entries(file_text):
    return [
        (
            int(match.group(1)),  # id
            int(match.group(2)),  # year
            int(match.group(3)),  # month
            int(match.group(4)),  # day
            int(match.group(5)),  # type
            match.group(6).replace("\\'", "'"),  # name
            match.group(7).replace("\\'", "'"),  # data
            int(match.group(8))   # insert_time
        )
        for match in row_pattern.finditer(file_text)
    ]

def import_history_to_db():
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS today_in_history (
        id INTEGER PRIMARY KEY,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        type INTEGER,
        name TEXT,
        data TEXT,
        insert_time INTEGER
    )
    ''')

    # 读取文件
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = parse_history_entries(content)
    print(f"发现 {len(entries)} 条历史记录，正在写入数据库...")

    # 写入数据库
    cursor.executemany('''
    INSERT OR REPLACE INTO today_in_history (id, year, month, day, type, name, data, insert_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', entries)

    conn.commit()
    conn.close()
    print(f"✅ 成功导入历史记录！")

if __name__ == '__main__':
    import_history_to_db()