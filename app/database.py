import sqlite3

def init_db():
    conn = sqlite3.connect("interview_data.db")
    cursor = conn.cursor()

    # Create candidates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            key_skills TEXT NOT NULL
        )
    ''')

    # Create interviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    ''')

    conn.commit()
    conn.close()

def save_candidate_to_database(name, key_skills):
    conn = sqlite3.connect("interview_data.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO candidates (name, key_skills) VALUES (?, ?)', (name, key_skills))
    candidate_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return candidate_id

def save_interview_to_database(candidate_id, questions, responses):
    conn = sqlite3.connect("interview_data.db")
    cursor = conn.cursor()
    for q, r in zip(questions, responses):
        cursor.execute('INSERT INTO interviews (candidate_id, question, response) VALUES (?, ?, ?)', (candidate_id, q, r))
    conn.commit()
    conn.close()
