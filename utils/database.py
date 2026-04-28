import sqlite3
import os
from datetime import datetime, timedelta
import json

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'digital_buddy.db')

def get_db():
    """Получить соединение с базой данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализировать базу данных"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Таблица новичков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newcomers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT UNIQUE,
            name TEXT NOT NULL,
            position TEXT,
            department TEXT,
            start_date TEXT,
            mentor_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица сообщений чата
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT,
            message TEXT NOT NULL,
            sender TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица настроений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT,
            mood_score INTEGER,
            feedback TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица алертов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT,
            level TEXT,
            reason TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица сессий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT UNIQUE,
            token TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица задач
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            newcomer_id TEXT,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    # Таблица комментариев к задачам
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            newcomer_id TEXT,
            comment TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id),
            FOREIGN KEY (newcomer_id) REFERENCES newcomers(newcomer_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_newcomer(name, position, department, start_date, mentor_name=""):
    """Добавить нового новичка"""
    conn = get_db()
    cursor = conn.cursor()
    
    newcomer_id = f"NB-{datetime.now().strftime('%Y%m%d')}-{hash(name) % 10000:04d}"
    
    try:
        cursor.execute('''
            INSERT INTO newcomers (newcomer_id, name, position, department, start_date, mentor_name)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (newcomer_id, name, position, department, start_date, mentor_name))
        conn.commit()
        return newcomer_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_newcomer(newcomer_id):
    """Получить информацию о новичке"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM newcomers WHERE newcomer_id = ?', (newcomer_id,))
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def get_all_newcomers():
    """Получить всех новичков"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM newcomers ORDER BY start_date DESC')
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def add_message(newcomer_id, message, sender):
    """Добавить сообщение в чат"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (newcomer_id, message, sender)
        VALUES (?, ?, ?)
    ''', (newcomer_id, message, sender))
    conn.commit()
    conn.close()

def get_messages(newcomer_id, limit=50):
    """Получить историю сообщений"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM messages 
        WHERE newcomer_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (newcomer_id, limit))
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def add_mood_checkin(newcomer_id, mood_score, feedback=""):
    """Добавить проверку настроения"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mood_checkins (newcomer_id, mood_score, feedback)
        VALUES (?, ?, ?)
    ''', (newcomer_id, mood_score, feedback))
    conn.commit()
    conn.close()

def get_mood_history(newcomer_id, days=30):
    """Получить историю настроения"""
    conn = get_db()
    cursor = conn.cursor()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT * FROM mood_checkins 
        WHERE newcomer_id = ? AND created_at >= ?
        ORDER BY created_at ASC
    ''', (newcomer_id, cutoff_date))
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def add_alert(newcomer_id, level, reason):
    """Добавить алерт"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alerts (newcomer_id, level, reason)
        VALUES (?, ?, ?)
    ''', (newcomer_id, level, reason))
    conn.commit()
    conn.close()

def get_active_alerts():
    """Получить активные алерты"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, n.name as newcomer_name 
        FROM alerts a 
        JOIN newcomers n ON a.newcomer_id = n.newcomer_id 
        WHERE a.status = 'active'
        ORDER BY a.created_at DESC
    ''')
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def resolve_alert(alert_id):
    """Разрешить алерт"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE alerts SET status = 'resolved' WHERE id = ?
    ''', (alert_id,))
    conn.commit()
    conn.close()

def create_session(newcomer_id):
    """Создать сессию для новичка"""
    conn = get_db()
    cursor = conn.cursor()
    token = f"tok_{newcomer_id}_{datetime.now().timestamp()}"
    cursor.execute('''
        INSERT OR REPLACE INTO sessions (newcomer_id, token)
        VALUES (?, ?)
    ''', (newcomer_id, token))
    conn.commit()
    conn.close()
    return token

def verify_session(token):
    """Проверить сессию"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT newcomer_id FROM sessions WHERE token = ?
    ''', (token,))
    result = cursor.fetchone()
    conn.close()
    return result['newcomer_id'] if result else None

def get_dashboard_summary():
    """Получить сводку для дашборда"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Общее количество новичков
    cursor.execute('SELECT COUNT(*) as count FROM newcomers')
    total = cursor.fetchone()['count']
    
    # Активные алерты
    cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE status = 'active'")
    alerts = cursor.fetchone()['count']
    
    # Среднее настроение за неделю
    cutoff_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute(f'''
        SELECT AVG(mood_score) as avg_mood FROM mood_checkins 
        WHERE created_at >= ?
    ''', (cutoff_date,))
    avg_mood = cursor.fetchone()['avg_mood'] or 0
    
    conn.close()
    
    return {
        'total_newcomers': total,
        'active_alerts': alerts,
        'avg_mood': round(avg_mood, 2)
    }

def get_all_mood_checkins():
    """Получить все записи о настроении с именами новичков"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.*, n.name as newcomer_name 
        FROM mood_checkins m 
        JOIN newcomers n ON m.newcomer_id = n.newcomer_id 
        ORDER BY m.created_at DESC
    ''')
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

# --- Функции для задач ---

def add_task(newcomer_id, title, description="", deadline=""):
    """Добавить задачу новичку"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (newcomer_id, title, description, deadline)
        VALUES (?, ?, ?, ?)
    ''', (newcomer_id, title, description, deadline))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_tasks(newcomer_id):
    """Получить все задачи новичка"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tasks 
        WHERE newcomer_id = ? 
        ORDER BY deadline ASC, created_at DESC
    ''', (newcomer_id,))
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def update_task_status(task_id, status):
    """Обновить статус задачи"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks SET status = ? WHERE id = ?
    ''', (status, task_id))
    conn.commit()
    conn.close()

def add_task_comment(task_id, newcomer_id, comment):
    """Добавить комментарий к задаче"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO task_comments (task_id, newcomer_id, comment)
        VALUES (?, ?, ?)
    ''', (task_id, newcomer_id, comment))
    conn.commit()
    conn.close()

def get_task_comments(task_id):
    """Получить комментарии к задаче"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.*, n.name as newcomer_name 
        FROM task_comments c 
        JOIN newcomers n ON c.newcomer_id = n.newcomer_id 
        WHERE c.task_id = ?
        ORDER BY c.created_at ASC
    ''', (task_id,))
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_all_tasks_for_hr():
    """Получить все задачи всех новичков для HR"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.*, n.name as newcomer_name 
        FROM tasks t 
        JOIN newcomers n ON t.newcomer_id = n.newcomer_id 
        ORDER BY t.deadline ASC
    ''')
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def delete_task(task_id):
    """Удалить задачу"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def get_task(task_id):
    """Получить одну задачу"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

def create_initial_tasks(newcomer_id):
    """Создать стартовые задачи для новичка"""
    tasks = [
        {
            "title": "📝 Познакомься с командой",
            "description": "Пройдись по отделу, представишься коллегам. Запиши имена и роли людей, с которыми будешь работать.",
            "deadline": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        },
        {
            "title": "🏢 Ознакомься с документами",
            "description": "Прочитай внутреннюю документацию, устав компании, правила корпоративной культуры.",
            "deadline": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        },
        {
            "title": "☕ Сходи на кофе с ментором",
            "description": "Договорись о встрече с ментором, задай вопросы о работе, процессах, ожиданиях.",
            "deadline": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        },
        {
            "title": "💻 Настрой рабочее место",
            "description": "Установи необходимое ПО, получи доступы к системам, проверь что всё работает.",
            "deadline": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        },
        {
            "title": "📋 Первая небольшая задача",
            "description": "Выполни свою первую рабочую задачу под руководством ментора. Это поможет понять процессы изнутри.",
            "deadline": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        }
    ]
    
    created_tasks = []
    for task in tasks:
        task_id = add_task(
            newcomer_id,
            task['title'],
            task['description'],
            task['deadline']
        )
        created_tasks.append(task_id)
    
    return created_tasks

# Инициализировать БД при импорте
init_db()
