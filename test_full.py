"""
Полный набор автотестов для Digital Buddy
Запуск: python test_full.py
"""
import unittest
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.ai import analyze_sentiment, generate_bot_response, check_alert_triggers
from utils.database import (
    init_db, add_newcomer, get_newcomer, get_all_newcomers,
    add_message, get_messages, add_mood_checkin, get_mood_history,
    add_alert, get_active_alerts, resolve_alert, get_dashboard_summary,
    get_all_mood_checkins, create_session
)
from datetime import datetime

class TestAISentiment(unittest.TestCase):
    """Тесты для AI анализа сентимента"""
    
    def test_positive_sentiment(self):
        """Тест позитивного сентимента"""
        text = "Сегодня отличный день, всё прошло хорошо!"
        sentiment, confidence = analyze_sentiment(text)
        self.assertEqual(sentiment, 'positive')
        self.assertGreater(confidence, 0)
    
    def test_negative_sentiment(self):
        """Тест негативного сентимента"""
        text = "Мне очень плохо, я устал и ничего не понимаю"
        sentiment, confidence = analyze_sentiment(text)
        self.assertEqual(sentiment, 'negative')
        self.assertGreater(confidence, 0)
    
    def test_neutral_sentiment(self):
        """Тест нейтрального сентимента"""
        text = "Сегодня обычный рабочий день"
        sentiment, confidence = analyze_sentiment(text)
        self.assertEqual(sentiment, 'neutral')
        self.assertGreater(confidence, 0)
    
    def test_empty_text(self):
        """Тест пустого текста"""
        text = ""
        sentiment, confidence = analyze_sentiment(text)
        self.assertEqual(sentiment, 'neutral')

class TestAIBotResponse(unittest.TestCase):
    """Тесты для генерации ответов бота"""
    
    def test_greeting_response(self):
        """Тест ответа на приветствие"""
        response = generate_bot_response("Привет!", "Алексей")
        self.assertIn("Привет", response)
        self.assertIn("Алексей", response)
    
    def test_how_are_you_response(self):
        """Тест ответа на как дела"""
        response = generate_bot_response("Как дела?", "Мария")
        self.assertIn("отлично", response.lower())
    
    def test_difficulty_response(self):
        """Тест ответа на трудности"""
        response = generate_bot_response("Мне трудно", "Иван")
        self.assertIn("помогу", response.lower())
    
    def test_thanks_response(self):
        """Тест ответа на спасибо"""
        response = generate_bot_response("Спасибо", "Ольга")
        self.assertIn("помочь", response.lower())
    
    def test_default_response(self):
        """Тест ответа по умолчанию"""
        response = generate_bot_response("Какой-то странный вопрос", "Петр")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

class TestAlertTriggers(unittest.TestCase):
    """Тесты для триггеров алертов"""
    
    def test_trigger_on_difficulty(self):
        """Тест триггера на слово 'трудно'"""
        triggers = check_alert_triggers("Мне очень трудно")
        self.assertTrue(len(triggers) > 0)
    
    def test_trigger_on_loneliness(self):
        """Тест триггера на слово 'одиноко'"""
        triggers = check_alert_triggers("Мне одиноко")
        self.assertTrue(len(triggers) > 0)
    
    def test_trigger_on_low_mood(self):
        """Тест триггера на низкое настроение"""
        triggers = check_alert_triggers("", mood_score=1)
        self.assertTrue(len(triggers) > 0)
        self.assertTrue(any("Низкое настроение" in t for t in triggers))
    
    def test_no_alert_on_positive(self):
        """Тест отсутствия алерта на позитиве"""
        triggers = check_alert_triggers("Всё отлично!", mood_score=5)
        self.assertEqual(len(triggers), 0)

class TestDatabaseNewcomers(unittest.TestCase):
    """Тесты для работы с новичками"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_name = f"Test User {datetime.now().timestamp()}"
    
    def test_add_newcomer(self):
        """Тест добавления новичка"""
        newcomer_id = add_newcomer(
            name=self.test_name,
            position="Junior Developer",
            department="IT",
            start_date="2026-04-28",
            mentor_name="John Doe"
        )
        self.assertIsNotNone(newcomer_id)
        self.assertTrue(newcomer_id.startswith("NB-"))
    
    def test_get_newcomer(self):
        """Тест получения новичка"""
        newcomer_id = add_newcomer(
            name=f"Get Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        newcomer = get_newcomer(newcomer_id)
        self.assertIsNotNone(newcomer)
        self.assertEqual(newcomer['newcomer_id'], newcomer_id)
    
    def test_get_all_newcomers(self):
        """Тест получения всех новичков"""
        newcomers = get_all_newcomers()
        self.assertIsInstance(newcomers, list)
    
    def test_duplicate_newcomer(self):
        """Тест дубликата новичка"""
        name = f"Duplicate Test {datetime.now().timestamp()}"
        id1 = add_newcomer(name, "Test", "Test", "2026-04-28")
        id2 = add_newcomer(name, "Test", "Test", "2026-04-28")
        self.assertIsNotNone(id1)
        self.assertIsNone(id2)  # Должен вернуть None для дубликата

class TestDatabaseMessages(unittest.TestCase):
    """Тесты для сообщений"""
    
    def test_add_message(self):
        """Тест добавления сообщения"""
        newcomer_id = add_newcomer(
            name=f"Msg Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        add_message(newcomer_id, "Привет!", "user")
        messages = get_messages(newcomer_id)
        self.assertGreater(len(messages), 0)
        self.assertEqual(messages[0]['message'], "Привет!")
    
    def test_message_senders(self):
        """Тест разных отправителей"""
        newcomer_id = add_newcomer(
            name=f"Sender Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        add_message(newcomer_id, "User message", "user")
        add_message(newcomer_id, "Bot message", "buddy")
        messages = get_messages(newcomer_id)
        senders = [m['sender'] for m in messages]
        self.assertIn("user", senders)
        self.assertIn("buddy", senders)

class TestDatabaseMood(unittest.TestCase):
    """Тесты для настроений"""
    
    def test_add_mood_checkin(self):
        """Тест добавления записи о настроении"""
        newcomer_id = add_newcomer(
            name=f"Mood Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        add_mood_checkin(newcomer_id, 4, "Хороший день")
        history = get_mood_history(newcomer_id)
        self.assertGreater(len(history), 0)
        self.assertEqual(history[0]['mood_score'], 4)
    
    def test_mood_score_range(self):
        """Тест диапазона оценок настроения"""
        newcomer_id = add_newcomer(
            name=f"Range Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        for score in [1, 2, 3, 4, 5]:
            add_mood_checkin(newcomer_id, score, f"Score {score}")
        history = get_mood_history(newcomer_id)
        scores = [h['mood_score'] for h in history]
        self.assertEqual(set(scores), {1, 2, 3, 4, 5})
    
    def test_get_all_mood_checkins(self):
        """Тест получения всех записей о настроении"""
        mood_data = get_all_mood_checkins()
        self.assertIsInstance(mood_data, list)

class TestDatabaseAlerts(unittest.TestCase):
    """Тесты для алертов"""
    
    def test_add_alert(self):
        """Тест добавления алерта"""
        newcomer_id = add_newcomer(
            name=f"Alert Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        add_alert(newcomer_id, "high", "Тестовый алерт")
        alerts = get_active_alerts()
        self.assertGreater(len(alerts), 0)
    
    def test_resolve_alert(self):
        """Тест разрешения алерта"""
        newcomer_id = add_newcomer(
            name=f"Resolve Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        add_alert(newcomer_id, "high", "Resolve test")
        alerts_before = get_active_alerts()
        alert_id = alerts_before[-1]['id']
        resolve_alert(alert_id)
        alerts_after = get_active_alerts()
        self.assertEqual(len(alerts_before), len(alerts_after) + 1)

class TestDatabaseSession(unittest.TestCase):
    """Тесты для сессий"""
    
    def test_create_session(self):
        """Тест создания сессии"""
        newcomer_id = add_newcomer(
            name=f"Session Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        token = create_session(newcomer_id)
        self.assertIsNotNone(token)
        self.assertIn(newcomer_id, token)

class TestDashboardSummary(unittest.TestCase):
    """Тесты для сводки дашборда"""
    
    def test_get_dashboard_summary(self):
        """Тест получения сводки"""
        summary = get_dashboard_summary()
        self.assertIn('total_newcomers', summary)
        self.assertIn('active_alerts', summary)
        self.assertIn('avg_mood', summary)
        self.assertIsInstance(summary['total_newcomers'], int)
        self.assertIsInstance(summary['active_alerts'], int)
        self.assertIsInstance(summary['avg_mood'], float)

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты полного потока"""
    
    def test_full_newcomer_journey(self):
        """Тест полного пути новичка"""
        # 1. Добавляем новичка
        name = f"Journey Test {datetime.now().timestamp()}"
        newcomer_id = add_newcomer(name, "Developer", "IT", "2026-04-28")
        self.assertIsNotNone(newcomer_id)
        
        # 2. Проверяем что добавился
        newcomer = get_newcomer(newcomer_id)
        self.assertEqual(newcomer['name'], name)
        
        # 3. Создаем сессию
        token = create_session(newcomer_id)
        self.assertIsNotNone(token)
        
        # 4. Добавляем сообщения
        add_message(newcomer_id, "Привет!", "user")
        add_message(newcomer_id, "Привет! Как твой день?", "buddy")
        messages = get_messages(newcomer_id)
        self.assertEqual(len(messages), 2)
        
        # 5. Добавляем настроение
        add_mood_checkin(newcomer_id, 4, "Хороший день")
        history = get_mood_history(newcomer_id)
        self.assertEqual(len(history), 1)
        
        # 6. Проверяем сводку
        summary = get_dashboard_summary()
        self.assertGreater(summary['total_newcomers'], 0)

def run_tests():
    """Запуск всех тестов"""
    # Инициализируем БД
    init_db()
    
    # Создаем тестовый suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем все тестовые классы
    suite.addTests(loader.loadTestsFromTestCase(TestAISentiment))
    suite.addTests(loader.loadTestsFromTestCase(TestAIBotResponse))
    suite.addTests(loader.loadTestsFromTestCase(TestAlertTriggers))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseNewcomers))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseMessages))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseMood))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseAlerts))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseSession))
    suite.addTests(loader.loadTestsFromTestCase(TestDashboardSummary))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Запускаем
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Возвращаем код выхода
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit(run_tests())
