"""
AI Ассистент для Цифрового Бадди
Использует HuggingFace Inference API
"""

import requests
import os

class AIBuddy:
    """AI помощник для адаптации новичков"""
    
    def __init__(self):
        # HuggingFace Inference API (бесплатно до 30к запросов/месяц)
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
        # Если есть свой токен, можно добавить:
        # self.headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
        self.headers = {}
        
        # Контекст разговора для каждого новичка
        self.conversation_history = {}
    
    def generate_response(self, message, newcomer_id="default"):
        """
        Генерация ответа от AI-бадди
        
        Args:
            message: Сообщение от пользователя
            newcomer_id: ID новичка для контекста
            
        Returns:
            Строка с ответом
        """
        # Получаем историю разговора
        history = self.conversation_history.get(newcomer_id, [])
        
        # Формируем промпт
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-5:]])
        
        prompt = f"""Ты - дружелюбный AI-бадди по имени Бадди, который помогает новичкам адаптироваться в компании.
Твой стиль общения: теплый, поддерживающий, неформальный, как у коллеги-друга.

История разговора:
{context}

Сообщение новичка: {message}

Твой ответ (на русском языке, кратко, 2-3 предложения):"""
        
        try:
            # Запрос к HuggingFace API
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 150,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "return_full_text": False
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated = result[0].get('generated_text', '').strip()
                    # Если модель вернула весь промпт, берем только генерацию
                    if generated.startswith(prompt):
                        generated = generated[len(prompt):].strip()
                    return generated or self._get_fallback_response(message)
                return self._get_fallback_response(message)
            else:
                print(f"API Error: {response.status_code}")
                return self._get_fallback_response(message)
                
        except Exception as e:
            print(f"AI Error: {str(e)}")
            return self._get_fallback_response(message)
    
    def add_message(self, newcomer_id, role, message):
        """Добавить сообщение в историю"""
        if newcomer_id not in self.conversation_history:
            self.conversation_history[newcomer_id] = []
        
        self.conversation_history[newcomer_id].append({
            'role': role,  # 'user' или 'assistant'
            'content': message
        })
        
        # Ограничиваем историю (последние 10 сообщений)
        if len(self.conversation_history[newcomer_id]) > 10:
            self.conversation_history[newcomer_id] = self.conversation_history[newcomer_id][-10:]
    
    def clear_history(self, newcomer_id):
        """Очистить историю разговора"""
        if newcomer_id in self.conversation_history:
            self.conversation_history[newcomer_id] = []
    
    def _get_fallback_response(self, message):
        """Запасной ответ если AI не работает"""
        message_lower = message.lower()
        
        fallback_responses = {
            'привет': 'Привет! Как твой день проходит? 😊',
            'как дела': 'У меня всё отлично! А у тебя как? Есть какие-то вопросы?',
            'спасибо': 'Всегда рад помочь! 😊',
            'трудно': 'Понимаю! Адаптация может быть сложной. Давай разберём, что именно вызывает трудности?',
            'одиноко': 'Понимаю твои чувства 😊 Попробуй познакомиться с коллегами!',
            'вопрос': 'Конечно! Задавай свой вопрос, я постараюсь помочь 🤗',
            'устал': 'Понимаю! Не забывай делать перерывы. Всё получится! 💪'
        }
        
        for keyword, response in fallback_responses.items():
            if keyword in message_lower:
                return response
        
        return "Понимаю! Расскажи подробнее, что тебя беспокоит? 😊"


# Глобальный экземпляр AI бадди
ai_buddy = AIBuddy()
