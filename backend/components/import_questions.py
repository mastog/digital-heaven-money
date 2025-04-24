import os
import sqlite3
import re

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the file paths
db_file_path = os.path.join(basedir, 'webdb.db')  # Replace with the path to your .db file
txt_file_path = os.path.join(basedir, 'DailyQuestion.txt')  # Replace with the path to your .txt file

# Define the question pattern
question_pattern = re.compile(  
    r'Question \d+\s*'
    r'Stem:\s*(?P<question>.*?)\s*'
    r'A\.\s*(?P<A>.*?)\s*'
    r'B\.\s*(?P<B>.*?)\s*'
    r'C\.\s*(?P<C>.*?)\s*'
    r'D\.\s*(?P<D>.*?)\s*'
    r'Answer:\s*(?P<answer>[ABCD])\s*'
    r'Explanation:\s*(?P<explanation>.*?)(?=Question \d+|$)',
    re.DOTALL
)

def parse_questions(file_text):
    questions = []
    for match in question_pattern.finditer(file_text):
        question_data = (
            match.group('question').strip(),
            match.group('A').strip(),
            match.group('B').strip(),
            match.group('C').strip(),
            match.group('D').strip(),
            match.group('answer').strip(),
            match.group('explanation').strip()
        )
        questions.append(question_data)
    return questions

def import_questions_to_db():
    # Connect to the database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answerA TEXT,
        answerB TEXT,
        answerC TEXT,
        answerD TEXT,
        correctAnswer TEXT,
        explanation TEXT
    )
    ''')

    # Read the text file and parse questions
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    question_list = parse_questions(file_content)

    # Insert data into the database
    for q in question_list:
        cursor.execute('''
        INSERT INTO daily_question (question, answerA, answerB, answerC, answerD, correctAnswer, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', q)

    conn.commit()
    conn.close()
    print(f'✅ Successfully imported {len(question_list)} questions into the database!')

if __name__ == '__main__':
    import_questions_to_db()
