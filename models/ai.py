import os
import requests

AI_GATEWAY_URL = os.getenv('AI_GATEWAY_URL')
AI_GATEWAY_API_KEY = os.getenv('AI_GATEWAY_API_KEY')

def fallback_sentiment(text):
    """Простая эвристика для сентимента"""
    text_lower = text.lower()
    
    negative_words = [
        'плохо', 'грустно', 'трудно', 'страшно', 'не понимаю',
        'одиноко', 'хочу уйти', 'бросаю', 'не хочу', 'ужасно',
        'проблема', 'злой', 'разочарован', 'устал', 'не нравится'
    ]
    
    positive_words = [
        'хорошо', 'отлично', 'круто', 'классно', 'рад', 'радостно',
        'понравилось', 'легко', 'увлекательно', 'интересно', 'супер'
    ]
    
    negative_count = sum(1 for word in negative_words if word in text_lower)
    positive_count = sum(1 for word in positive_words if word in text_lower)
    
    if negative_count > positive_count:
        return 'negative', 0.7
    elif positive_count > positive_count:
        return 'positive', 0.7
    else:
        return 'neutral', 0.5

def analyze_sentiment(text):
    """Анализировать сентимент текста"""
    return fallback_sentiment(text)

def generate_bot_response(user_message, newcomer_name):
    """Генерация ответа от бадди через AI Gateway"""
    message_lower = user_message.lower()
    
    # Простые шаблоны для быстрых ответов
    quick_responses = {
        'привет': f"Привет, {newcomer_name}! 👋 Как твой день проходит?",
        'как дела': "У меня всё отлично! А у тебя как? Есть какие-то вопросы или трудности?",
        'что делаешь': "Я здесь, чтобы помочь тебе с адаптацией! Могу ответить на вопросы, поддержать или просто поболтать 😊",
        'трудно': "Понимаю, адаптация может быть сложной! 😊 Давай разберём, что именно вызывает трудности? Я помогу!",
        'вопрос': "Конечно! Задавай свой вопрос, я постараюсь помочь 🤗",
        'спасибо': "Всегда рад помочь! 😊 Если ещё что-то нужно - обращайся!",
        'устал': "Понимаю, первые дни могут быть утомительными! Не забывай делать перерывы. Всё получится! 💪",
        'одиноко': "Понимаю твои чувства 😊 Попробуй познакомиться с коллегами, пригласить на кофе! Команда всегда готова помочь!",
    }
    
    for keyword, response in quick_responses.items():
        if keyword in message_lower:
            return response
    
    # Если нет быстрого совпадения, используем AI Gateway
    if AI_GATEWAY_URL and AI_GATEWAY_API_KEY:
        try:
            response = requests.post(
                AI_GATEWAY_URL,
                json={
                    "model": os.getenv('AI_MODEL', 'gpt-4'),
                    "messages": [
                        {"role": "system", "content": "Ты дружелюбный AI-бадди, который помогает новичкам адаптироваться на новой работе. Отвечай тепло, поддерживающе и с эмодзи."},
                        {"role": "user", "content": f"{newcomer_name} пишет: {user_message}"}
                    ],
                    "temperature": float(os.getenv('AI_TEMPERATURE', '0.7'))
                },
                headers={
                    "Authorization": f"Bearer {AI_GATEWAY_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_reply = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                if bot_reply:
                    return bot_reply
        except Exception as e:
            print(f"AI Gateway error: {e}")
    
    # Fallback на случай ошибки или если AI Gateway не настроен
    default_responses = [
        f"{newcomer_name}, понимаю! Расскажи подробнее, что тебя беспокоит? 😊",
        "Интересный вопрос! Давай обсудим это подробнее 🤗",
        "Спасибо, что поделился! Я здесь, чтобы поддержать тебя! 💪",
        "Понимаю! Если есть вопросы - спрашивай, помогу чем могу! 😊",
    ]
    import random
    return random.choice(default_responses)

def fallback_sentiment(text):
    """Простая эвристика для сентимента"""
    text_lower = text.lower()
    
    negative_words = [
        'плохо', 'грустно', 'трудно', 'страшно', 'не понимаю',
        'одиноко', 'хочу уйти', 'бросаю', 'не хочу', 'ужасно',
        'проблема', 'злой', 'разочарован', 'устал', 'не нравится'
    ]
    
    positive_words = [
        'хорошо', 'отлично', 'круто', 'классно', 'рад', 'радостно',
        'понравилось', 'легко', 'увлекательно', 'интересно', 'супер'
    ]
    
    negative_count = sum(1 for word in negative_words if word in text_lower)
    positive_count = sum(1 for word in positive_words if word in text_lower)
    
    if negative_count > positive_count:
        return 'negative', 0.7
    elif positive_count > negative_count:
        return 'positive', 0.7
    else:
        return 'neutral', 0.5

def check_alert_triggers(text, mood_score=None):
    """Проверить триггеры для алертов"""
    triggers = []
    text_lower = text.lower()
    
    # Триггерные слова
    trigger_words = [
        'не понимаю', 'трудно', 'страшно', 'одиноко', 
        'бросаю', 'не хочу', 'хочу уйти', 'плохо'
    ]
    
    for word in trigger_words:
        if word in text_lower:
            triggers.append(f"Триггерное слово: '{word}'")
            break
    
    # Низкое настроение
    if mood_score is not None and mood_score <= 2:
        triggers.append(f"Низкое настроение: {mood_score}/5")
    
    return triggers
