import sqlite3
import os
from datetime import datetime, timedelta
import json

# На Vercel используем /tmp, локально - data папка
if os.environ.get('VERCEL'):
    DB_PATH = '/tmp/data/digital_buddy.db'
    os.makedirs('/tmp/data', exist_ok=True)
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'digital_buddy.db')

