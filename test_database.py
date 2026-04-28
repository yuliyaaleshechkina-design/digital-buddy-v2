import unittest
from utils.database import (
    add_newcomer, get_newcomer, get_all_newcomers,
    add_message, get_messages,
    add_mood_checkin, get_mood_history,
    add_alert, get_active_alerts, resolve_alert,
    get_dashboard_summary
)
from datetime import datetime, timedelta

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_id = f"NB-TEST-{datetime.now().timestamp()}"
        self.test_name = f"Test User {datetime.now().timestamp()}"
    
    def test_add_and_get_newcomer(self):
        """Тест добавления и получения новичка"""
        newcomer_id = add_newcomer(
            name=self.test_name,
            position="Junior Developer",
            department="IT",
            start_date="2026-04-28",
            mentor_name="John Doe"
        )
        self.assertIsNotNone(newcomer_id)
        
        newcomer = get_newcomer(newcomer_id)
        self.assertIsNotNone(newcomer)
        self.assertEqual(newcomer['name'], self.test_name)
    
    def test_get_all_newcomers(self):
        """Тест получения всех новичков"""
        newcomers = get_all_newcomers()
        self.assertIsInstance(newcomers, list)
    
    def test_add_and_get_messages(self):
        """Тест добавления и получения сообщений"""
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
    
    def test_add_and_get_mood_checkin(self):
        """Тест добавления и получения записи о настроении"""
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
    
    def test_alert_lifecycle(self):
        """Тест жизненного цикла алерта"""
        newcomer_id = add_newcomer(
            name=f"Alert Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        
        if newcomer_id:
            add_alert(newcomer_id, "high", "Тестовый алерт")
            alerts = get_active_alerts()
            self.assertGreater(len(alerts), 0)
            
            latest_alert = next((a for a in alerts if a['reason'] == "Тестовый алерт"), None)
            if latest_alert:
                resolve_alert(latest_alert['id'])
                alerts = get_active_alerts()
                resolved_alert = next((a for a in alerts if a['id'] == latest_alert['id']), None)
                self.assertIsNone(resolved_alert)
    
    def test_dashboard_summary(self):
        """Тест сводки дашборда"""
        summary = get_dashboard_summary()
        self.assertIn('total_newcomers', summary)
        self.assertIn('active_alerts', summary)
        self.assertIn('avg_mood', summary)
        self.assertIsInstance(summary['total_newcomers'], int)
        self.assertIsInstance(summary['active_alerts'], int)

if __name__ == '__main__':
    unittest.main()
