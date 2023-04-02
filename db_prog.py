import sqlite3

db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    open()
    query = 'DROP TABLE IF EXISTS quiz'
    do(query)
    query = 'DROP TABLE IF EXISTS question'
    do(query)
    query = 'DROP TABLE IF EXISTS connect'
    do(query)

def create():
    open()
    cursor.execute('PRAGMA foreign_key=on')
    do("""CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR
        )""")
    do("""CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR
        )""")
    do("""CREATE TABLE IF NOT EXISTS connect (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz(id),
        FOREIGN KEY (question_id) REFERENCES question(id)
        )""")
    close()

def add_questions():
    questions = [
        ('Сколько мне лет?', '15', '14', '16', '13'),
        ('За каким ноутбуком я сижу?', '2', '3', '5', '7'),
        ('Мой рост?', '176', '166', '170', '184'),
        ('Что у меня не растёт дома?', 'манго', 'авокадо', 'маракуйя', 'толстянка'),
        ('Мой любимый цвет?', '#2F60BD', '#123456', '#D78B24', '#ABCDEF')
    ]
    open()
    cursor.executemany('INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)', questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Моё описание', ),
        ('Алгоритмика', ),
        ('Я', )
    ]
    open()
    cursor.executemany('INSERT INTO quiz (name) VALUES (?)', quizes)
    conn.commit()
    close()

def add_link():
    open()
    # cursor.execute('PRAGMA foreing_keys=on')
    # query = 'INSERT INTO connect (quiz_id, question_id) VALUES (?,?)'
    # answer = input('y/n: ')
    # while answer != 'n':
    #     qzi = int(input('викторина: '))
    #     qti = int(input('вопрос: '))
    #     cursor.execute(query, [qzi, qti])
    #     conn.commit()
    #     answer = input('y/n')
    query = [
        (1, 1),
        (1, 3),
        (1, 5),
        (2, 2),
        (3, 3),
        (3, 4),
        (3, 5),
    ]
    cursor.executemany('INSERT INTO connect (quiz_id, question_id) VALUES (?,?)', query)
    conn.commit()
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print('[')
    for fa in cursor.fetchall():
        print(fa)
    print(']')
    close()

def show_table():
    show('question')
    show('quiz')
    show('connect')

def get_question_after(question_id=0, quiz_id=1):
    open()
    query = """
    SELECT connect.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, connect
    WHERE connect.question_id == question.id
    AND connect.id > ? AND connect.quiz_id == ?
    ORDER BY connect.id
    """
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result

def get_quises():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def check_answer(q_id, ans_text):
    query = """
    SELECT question.answer
    FROM connect, question
    WHERE connect.id = ?
    AND connect.question_id = question.id"""
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()

    if result is None:
        return False
    else:
        if result[0] == ans_text:
            return True
        else:
            return False
    
# def main():
#     clear_db()
#     create()
#     add_questions()
#     add_quiz()
#     add_link()
#     show_table()

# if __name__ == "__main__":
#     main()