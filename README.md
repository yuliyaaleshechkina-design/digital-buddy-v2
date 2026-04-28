# Digital Buddy 🤖

AI-помощник для адаптации новичков в компании.

## 🚀 Быстрый старт

### Локально (Flask + HTML)

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
python api/main.py

# Открыть в браузере
# http://localhost:8501
```

### 🌐 Деплой на Vercel

1. **Загрузи код на GitHub**
```bash
git init
git add .
git commit -m "Deploy to Vercel"
git branch -M main
git remote add origin https://github.com/ТВОЙ_НИК/digital-buddy.git
git push -u origin main
```

2. **Зайди на [vercel.com](https://vercel.com)**
3. Нажми **"Add New Project"**
4. Выбери свой репозиторий
5. Нажми **"Deploy"**

Готово! Получишь ссылку типа:
```
https://digital-buddy.vercel.app
```

### 🌱 Демо-данные`n```bash`n# Загрузить демо-данные вручную`npython seed.py`n`n# Или запустить в демо-режиме`n$env:DEMO_MODE="true"`npython api/main.py`n```
```bash
python test_full.py      # Все тесты (33 теста)
python test_tasks.py     # Тесты для задач (6 тестов)
```

## 📁 Структура проекта

```
digital-buddy/
├── api/                     # Flask API
│   ├── main.py             # Основной файл
│   └── routes/             # API роуты
│       ├── auth.py
│       ├── chat.py
│       ├── tasks.py
│       ├── mood.py
│       └── alerts.py
├── frontend/               # HTML/JS фронтенд
│   ├── index.html         # Главная
│   ├── newcomer.html      # Страница новичка
│   └── hr.html           # HR дашборд
├── models/
│   └── ai.py             # AI функции
├── utils/
│   └── database.py       # Работа с БД
├── test_full.py          # Все автотесты
├── test_tasks.py         # Тесты задач
├── requirements.txt      # Зависимости
├── vercel.json          # Vercel конфиг
├── DEVELOPMENT_RULES.md # Правила разработки
└── README.md           # Этот файл
```

## 🎯 Функционал

### Для новичков:
- 💬 Чат с AI-бадди
- 😊 Проверка настроения
- 📋 Доска заданий с комментариями

### Для HR:
- ➕ Добавление новичков со стартовыми задачами
- 📊 Дашборд со всеми новичками
- 📈 Настроение каждого новичка
- 🚨 Алерты о проблемах
- ✏️ Создание/редактирование задач
- 💬 Просмотр комментариев

## ⚠️ Важные правила

**ПЕРЕД изменениями:**
1. Запусти тесты: `python test_full.py`
2. Проверь что все проходят

**НИКОГДА не:**
- Удаляй функции без запроса
- Игнорируй падающие тесты

Подробно в [DEVELOPMENT_RULES.md](DEVELOPMENT_RULES.md)

## 🛠 Технологии

- **Frontend:** HTML + JavaScript
- **Backend:** Python + Flask
- **AI:** AI Gateway (опционально)
- **Database:** SQLite
- **Deployment:** Vercel

## 🐛 Отладка

```bash
# Логи локально
python api/main.py

# Проверка API
curl http://localhost:8501/api/get-dashboard-summary

# Перезапуск
python api/main.py
```

## 📝 Лицензия
Internal use only

