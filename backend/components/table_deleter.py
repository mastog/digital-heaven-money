import os
import sqlite3

# get path
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_file_path = os.path.join(basedir, 'webdb.db')  

def drop_table():
    # connect to database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # delete table which called DailyQuestion
    cursor.execute('''
    DROP TABLE IF EXISTS DailyQuestion;
    ''')
    conn.commit()
    conn.close()

    print('✅ DailyQuestion deleted correctlly！')

if __name__ == '__main__':
    drop_table()
