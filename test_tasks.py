"""
Тесты для системы задач
Запуск: python test_tasks.py
"""
import unittest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.database import (
    init_db, add_newcomer, add_task, get_tasks,
    update_task_status, add_task_comment, get_task_comments,
    get_all_tasks_for_hr
)

class TestTasks(unittest.TestCase):
    """Тесты для задач"""
    
    def test_add_task(self):
        """Тест добавления задачи"""
        newcomer_id = add_newcomer(
            name=f"Task Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        task_id = add_task(newcomer_id, "Test Task", "Description", "2026-05-01")
        self.assertIsNotNone(task_id)
    
    def test_get_tasks(self):
        """Тест получения задач"""
        newcomer_id = add_newcomer(
            name=f"Get Task Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        add_task(newcomer_id, "Task 1")
        tasks = get_tasks(newcomer_id)
        self.assertGreater(len(tasks), 0)
    
    def test_update_task_status(self):
        """Тест обновления статуса задачи"""
        newcomer_id = add_newcomer(
            name=f"Status Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        task_id = add_task(newcomer_id, "Status Task")
        update_task_status(task_id, 'done')
        tasks = get_tasks(newcomer_id)
        self.assertEqual(tasks[0]['status'], 'done')
    
    def test_task_comment(self):
        """Тест комментария к задаче"""
        newcomer_id = add_newcomer(
            name=f"Comment Test {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        task_id = add_task(newcomer_id, "Comment Task")
        add_task_comment(task_id, newcomer_id, "Test comment")
        comments = get_task_comments(task_id)
        self.assertGreater(len(comments), 0)
        self.assertEqual(comments[0]['comment'], "Test comment")
    
    def test_get_all_tasks_for_hr(self):
        """Тест получения всех задач для HR"""
        tasks = get_all_tasks_for_hr()
        self.assertIsInstance(tasks, list)
    
    def test_task_multiple_statuses(self):
        """Тест смены статусов задачи"""
        newcomer_id = add_newcomer(
            name=f"Multi Status {datetime.now().timestamp()}",
            position="Test",
            department="Test",
            start_date="2026-04-28"
        )
        task_id = add_task(newcomer_id, "Multi Status Task")
        
        # Проверка начального статуса
        tasks = get_tasks(newcomer_id)
        self.assertEqual(tasks[0]['status'], 'pending')
        
        # Изменение на in_progress
        update_task_status(task_id, 'in_progress')
        tasks = get_tasks(newcomer_id)
        self.assertEqual(tasks[0]['status'], 'in_progress')
        
        # Изменение на done
        update_task_status(task_id, 'done')
        tasks = get_tasks(newcomer_id)
        self.assertEqual(tasks[0]['status'], 'done')

def run_tests():
    """Запуск тестов"""
    init_db()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTasks)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit(run_tests())
