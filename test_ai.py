import unittest
from models.ai import analyze_sentiment, check_alert_triggers

class TestSentimentAnalysis(unittest.TestCase):
    
    def test_positive_sentiment(self):
        text = "Сегодня отличный день, всё прошло хорошо!"
        sentiment, confidence = analyze_sentiment(text)
        self.assertEqual(sentiment, 'positive')
        self.assertGreater(confidence, 0)
    
    def test_negative_sentiment(self):
        text = "Мне очень плохо, я устал и ничего не понимаю"
        sentiment, confidence = analyze_sentiment(text)
        self.assertEqual(sentiment, 'negative')
        self.assertGreater(confidence, 0)
    
    def test_neutral_sentiment(self):
        text = "Сегодня обычный рабочий день"
        sentiment, confidence = analyze_sentiment(text)
        self.assertEqual(sentiment, 'neutral')
        self.assertGreater(confidence, 0)

class TestAlertTriggers(unittest.TestCase):
    
    def test_alert_on_negative_phrase(self):
        text = "Мне очень трудно, я не понимаю что делать"
        triggers = check_alert_triggers(text)
        self.assertTrue(len(triggers) > 0)
        self.assertTrue(any("трудно" in t for t in triggers))
    
    def test_alert_on_low_mood(self):
        triggers = check_alert_triggers("", mood_score=1)
        self.assertTrue(len(triggers) > 0)
        self.assertTrue(any("Низкое настроение" in t for t in triggers))
    
    def test_no_alert_on_positive(self):
        text = "Сегодня всё отлично, спасибо!"
        triggers = check_alert_triggers(text, mood_score=5)
        self.assertEqual(len(triggers), 0)

if __name__ == '__main__':
    unittest.main()
