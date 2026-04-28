from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from utils.database import init_db
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# Инициализация БД при старте
init_db()

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/newcomer')
def newcomer_page():
    return send_from_directory('frontend', 'newcomer.html')

@app.route('/hr')
def hr_page():
    return send_from_directory('frontend', 'hr.html')

# API Routes
from api.routes import auth, chat, tasks, mood, alerts

app.register_blueprint(auth.bp, url_prefix='/api')
app.register_blueprint(chat.bp, url_prefix='/api')
app.register_blueprint(tasks.bp, url_prefix='/api')
app.register_blueprint(mood.bp, url_prefix='/api')
app.register_blueprint(alerts.bp, url_prefix='/api')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8501))
    app.run(host='0.0.0.0', port=port, debug=True)
