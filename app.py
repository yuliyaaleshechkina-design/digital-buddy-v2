import streamlit as st
from utils.database import get_dashboard_summary
import os

st.set_page_config(
    page_title="Цифровой Бадди",
    page_icon="🤖",
    layout="wide"
)

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

if 'role' not in st.session_state:
    st.session_state['role'] = None

def show_home():
    st.title("🤖 Цифровой Бадди")
    st.markdown("---")
    
    st.header("Выберите вашу роль:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤 Я Новичок", use_container_width=True, type="primary"):
            st.session_state['role'] = 'newcomer'
            st.session_state['page'] = 'newcomer'
            st.rerun()
    
    with col2:
        if st.button("👔 Я HR", use_container_width=True, type="primary"):
            st.session_state['role'] = 'hr'
            st.session_state['page'] = 'hr'
            st.rerun()
    
    st.markdown("---")
    
    st.header("📖 О системе")
    
    st.subheader("💬 Что это?")
    st.write("""
    **Цифровой Бадди** — AI-помощник, который помогает новичкам адаптироваться 
    в первые 90 дней работы.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Для новичков")
        st.write("""
        - Чат с AI-бадди
        - Ответы на вопросы
        - Поддержка и советы
        """)
    
    with col2:
        st.markdown("### 📊 Для HR")
        st.write("""
        - Дашборд со статусами
        - Отслеживание настроения
        - Ранние алерты о проблемах
        """)
    
    with col3:
        st.markdown("### 🚀 Преимущества")
        st.write("""
        - Всегда доступен
        - Дружелюбный тон
        - Конфиденциально
        """)
    
    st.markdown("---")
    
    summary = get_dashboard_summary()
    st.subheader("📈 Общая статистика")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Активных новичков", summary['total_newcomers'])
    
    with col2:
        st.metric("Активных алертов", summary['active_alerts'])
    
    with col3:
        st.metric("Среднее настроение", f"{summary['avg_mood']}/5")

def show_newcomer():
    import random
    from utils.database import (
        get_newcomer, add_mood_checkin, get_mood_history,
        create_session, get_messages, add_message,
        get_tasks, add_task_comment, get_task_comments, update_task_status
    )
    from models.ai import analyze_sentiment, check_alert_triggers, generate_bot_response
    from datetime import datetime
    
    st.title("💬 Чат с Бадди")
    
    col1, col2 = st.columns([5, 1])
    with col2:
        if st.button("🚪 Выйти", use_container_width=True):
            st.session_state['page'] = 'home'
            st.session_state['newcomer_id'] = None
            st.session_state['newcomer_name'] = None
            st.session_state['messages'] = []
            st.rerun()
    
    st.markdown("---")
    
    if 'newcomer_id' not in st.session_state:
        st.info("👋 Привет! Чтобы начать общение с бадди, введите ваш персональный ID, который вам дал HR.")
        
        newcomer_id = st.text_input(
            "Ваш ID новичка:", 
            placeholder="Например: NB-20260428-1234",
            help="ID должен быть в формате NB-ГГГГММДД-XXXX. Получите его у вашего HR после регистрации."
        )
        
        if newcomer_id:
            newcomer = get_newcomer(newcomer_id)
            if newcomer:
                st.session_state['newcomer_id'] = newcomer_id
                st.session_state['newcomer_name'] = newcomer['name']
                create_session(newcomer_id)
                st.success(f"✅ Добро пожаловать, {newcomer['name']}!")
                st.rerun()
            else:
                st.error("❌ Новичок с таким ID не найден. Пожалуйста, проверьте ID или обратитесь к HR.")
        return
    
    newcomer_id = st.session_state['newcomer_id']
    newcomer_name = st.session_state.get('newcomer_name', 'Новичок')
    
    st.subheader(f"Привет, {newcomer_name}! 👋")
    st.write("Я твой AI-бадди. Задавай вопросы, делись впечатлениями!")
    
    tab1, tab2, tab3 = st.tabs(["💬 Чат", "😊 Настроение", "📋 Мои задачи"])
    
    with tab1:
        if 'messages' not in st.session_state:
            st.session_state['messages'] = get_messages(newcomer_id)
        
        for msg in reversed(st.session_state['messages'][-20:]):
            with st.chat_message(msg['sender']):
                st.write(msg['message'])
        
        if prompt := st.chat_input("Напиши сообщение..."):
            add_message(newcomer_id, prompt, 'user')
            st.session_state['messages'].append({
                'message': prompt,
                'sender': 'user',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            sentiment, confidence = analyze_sentiment(prompt)
            triggers = check_alert_triggers(prompt)
            
            if triggers:
                for trigger in triggers:
                    add_message(newcomer_id, f"[Система: {trigger}]", 'system')
            
            bot_response = generate_bot_response(prompt, newcomer_name)
            add_message(newcomer_id, bot_response, 'buddy')
            st.session_state['messages'].append({
                'message': bot_response,
                'sender': 'buddy',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            st.rerun()
    
    with tab2:
        st.write("Как ты себя чувствуешь сегодня?")
        
        mood = st.slider(
            "Оцени своё настроение:",
            min_value=1,
            max_value=5,
            value=3,
            step=1
        )
        
        mood_labels = {
            1: "😞 Очень плохо",
            2: "😕 Плохо",
            3: "😐 Нормально",
            4: "🙂 Хорошо",
            5: "😀 Отлично"
        }
        
        st.write(mood_labels[mood])
        
        feedback = st.text_area("Если хочешь, расскажи подробнее:")
        
        if st.button("Отправить"):
            add_mood_checkin(newcomer_id, mood, feedback)
            st.success("Спасибо! Твоё настроение записано! 💖")
            
            triggers = check_alert_triggers(feedback, mood)
            if triggers:
                st.warning("Обрати внимание: некоторые фразы могут указывать на трудности.")
        
        st.markdown("---")
        
        st.subheader("📊 Моя история настроения")
        history = get_mood_history(newcomer_id, days=30)
        
        if history:
            for entry in reversed(history[-10:]):
                st.write(f"**{entry['created_at'][:10]}**: {'⭐' * entry['mood_score']}")
                if entry['feedback']:
                    st.write(f"_{entry['feedback']}_")
        else:
            st.info("Пока нет записей о настроении")
    
    with tab3:
        st.subheader("📋 Мои задачи")
        tasks = get_tasks(newcomer_id)
        
        if tasks:
            for task in tasks:
                status_emoji = {"pending": "⏳", "in_progress": "🔄", "done": "✅"}.get(task['status'], "⏳")
                with st.expander(f"{status_emoji} {task['title']}", expanded=(task['status'] != 'done')):
                    st.write(f"**Описание:** {task['description'] or 'Нет описания'}")
                    if task['deadline']:
                        st.write(f"**Срок:** {task['deadline']}")
                    st.write(f"**Статус:** {status_emoji} {task['status']}")
                    
                    st.markdown("**Комментарии:**")
                    comments = get_task_comments(task['id'])
                    if comments:
                        for comment in comments:
                            st.write(f"  - {comment['comment']}")
                    
                    new_comment = st.text_area("Добавить комментарий:", key=f"comment_{task['id']}")
                    if st.button("Отправить комментарий", key=f"send_comment_{task['id']}"):
                        if new_comment:
                            add_task_comment(task['id'], newcomer_id, new_comment)
                            st.success("Комментарий добавлен!")
                            st.rerun()
                    
                    if task['status'] != 'done' and st.button("✅ Выполнено", key=f"done_{task['id']}"):
                        update_task_status(task['id'], 'done')
                        st.rerun()
        else:
            st.info("У тебя пока нет задач. Ожидай назначений от HR!")

def show_hr():
    from utils import database
    import plotly.express as px
    import pandas as pd
    from datetime import datetime
    
    st.title("📊 HR Дашборд")
    
    back_button = st.button("← На главную")
    if back_button:
        st.session_state['page'] = 'home'
        st.rerun()
    
    try:
        summary = database.get_dashboard_summary()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Новичков", summary['total_newcomers'])
        with col2:
            st.metric("🚨 Активных алертов", summary['active_alerts'])
        with col3:
            st.metric("😊 Среднее настроение", summary['avg_mood'], delta_color="normal")
        
        st.markdown("---")
        
        st.subheader("➕ Добавить Новичка")
        
        with st.form("newcomer_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Имя и фамилия *")
                position = st.text_input("Должность *")
            with col2:
                department = st.text_input("Отдел *")
                start_date = st.date_input("Дата выхода *")
            mentor = st.text_input("Имя ментора (опционально)")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                add_initial = st.checkbox("✅ Сразу создать 5 стартовых задач для адаптации")
            
            submitted = st.form_submit_button("Добавить новичка")
            
            if submitted:
                if name and position and department and start_date:
                    newcomer_id = database.add_newcomer(
                        name=name,
                        position=position,
                        department=department,
                        start_date=start_date.strftime('%Y-%m-%d'),
                        mentor_name=mentor
                    )
                    
                    if newcomer_id:
                        st.success(f"✅ Новичок добавлен! ID: `{newcomer_id}`")
                        st.info("Покажи этот ID новичку для доступа к чату")
                        
                        if add_initial:
                            database.create_initial_tasks(newcomer_id)
                            st.success("📋 Созданы 5 стартовых задач для адаптации!")
                        
                        st.rerun()
                    else:
                        st.error("❌ Ошибка: возможно, такой новичок уже добавлен")
                else:
                    st.error("❌ Пожалуйста, заполните все обязательные поля *")
        
        st.markdown("---")
        
        st.subheader("📋 Список новичков")
        newcomers = database.get_all_newcomers()
        
        if newcomers:
            latest = newcomers[0]
            st.info(f"**Последний добавленный:** {latest['name']} | **ID:** `{latest['newcomer_id']}`")
            
            df = pd.DataFrame([
                {
                    "Имя": n['name'],
                    "ID": n['newcomer_id'],
                    "Должность": n['position'],
                    "Отдел": n['department'],
                    "Дата выхода": n['start_date'],
                    "Ментор": n['mentor_name'] or '-'
                }
                for n in newcomers
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Пока нет добавленных новичков. Добавь первого выше!")
        
        st.markdown("---")
        
        st.subheader("📈 Настроение новичков")
        
        mood_data = database.get_all_mood_checkins()
        
        if mood_data:
            newcomer_moods = {}
            for entry in mood_data:
                name = entry['newcomer_name']
                if name not in newcomer_moods:
                    newcomer_moods[name] = []
                newcomer_moods[name].append({
                    'score': entry['mood_score'],
                    'feedback': entry['feedback'],
                    'date': entry['created_at'][:10],
                    'id': entry['newcomer_id']
                })
            
            for name, moods in newcomer_moods.items():
                with st.expander(f"😊 {name} ({moods[-1]['id']})", expanded=False):
                    latest = moods[-1]
                    st.write(f"**Последняя оценка:** {'⭐' * latest['score']} ({latest['score']}/5)")
                    st.write(f"**Дата:** {latest['date']}")
                    if latest['feedback']:
                        st.write(f"_{latest['feedback']}_")
                    
                    if len(moods) > 1:
                        st.write("**История:**")
                        for mood in reversed(moods[-5:-1]):
                            st.write(f"  {mood['date']}: {'⭐' * mood['score']} ({mood['score']}/5)")
        else:
            st.info("Пока нет записей о настроении")
        
        st.markdown("---")
        
        st.subheader("🚨 Активные алерты")
        alerts = database.get_active_alerts()
        
        if alerts:
            for alert in alerts:
                with st.container():
                    st.error(f"**{alert['newcomer_name']}** - {alert['reason']}")
                    if st.button(f"Разрешить #{alert['id']}", key=f"resolve_{alert['id']}"):
                        database.resolve_alert(alert['id'])
                        st.rerun()
        else:
            st.success("Нет активных алертов! 🎉")
        
        st.markdown("---")
        
        st.subheader("📋 Задачи новичков")
        
        selected_newcomer = st.selectbox(
            "Выберите новичка:",
            options=[f"{n['name']} ({n['newcomer_id']})" for n in newcomers],
            key="hr_newcomer_select"
        )
        
        if selected_newcomer and newcomers:
            newcomer_id = selected_newcomer.split(" (")[1].rstrip(")")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Существующие задачи")
                tasks = database.get_tasks(newcomer_id)
                
                if tasks:
                    for task in tasks:
                        status_emoji = {"pending": "⏳", "in_progress": "🔄", "done": "✅"}.get(task['status'], "⏳")
                        with st.expander(f"{status_emoji} {task['title']}", expanded=False):
                            st.write(f"**Описание:** {task['description'] or 'Нет описания'}")
                            if task['deadline']:
                                st.write(f"**Срок:** {task['deadline']}")
                            st.write(f"**Статус:** {status_emoji} {task['status']}")
                            
                            comments = database.get_task_comments(task['id'])
                            if comments:
                                st.write("**Комментарии от новичка:**")
                                for comment in comments:
                                    st.write(f"  - {comment['comment']}")
                            
                            new_status = st.selectbox(
                                "Статус:",
                                options=["pending", "in_progress", "done"],
                                index=["pending", "in_progress", "done"].index(task['status']),
                                key=f"hr_status_{task['id']}"
                            )
                            
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                if st.button("Сохранить", key=f"hr_save_{task['id']}"):
                                    database.update_task_status(task['id'], new_status)
                                    st.rerun()
                            with col2:
                                if st.button("🗑️", key=f"hr_delete_{task['id']}"):
                                    database.delete_task(task['id'])
                                    st.rerun()
                else:
                    st.info("У этого новичка пока нет задач")
            
            with col2:
                st.subheader("➕ Новая задача")
                with st.form(f"new_task_{newcomer_id}"):
                    task_title = st.text_input("Название задачи *")
                    task_desc = st.text_area("Описание")
                    task_deadline = st.date_input("Срок")
                    
                    submitted_task = st.form_submit_button("Создать задачу")
                    
                    if submitted_task:
                        if task_title:
                            deadline_str = task_deadline.strftime('%Y-%m-%d') if task_deadline else ""
                            database.add_task(newcomer_id, task_title, task_desc, deadline_str)
                            st.success("✅ Задача создана!")
                            st.rerun()
                        else:
                            st.error("❌ Введите название задачи")
        
        st.markdown("---")
        
        st.subheader("📋 Все задачи (общий вид)")
        all_tasks = database.get_all_tasks_for_hr()
        
        if all_tasks:
            for task in all_tasks:
                status_emoji = {"pending": "⏳", "in_progress": "🔄", "done": "✅"}.get(task['status'], "⏳")
                with st.expander(f"{status_emoji} {task['title']} ({task['newcomer_name']})", expanded=False):
                    st.write(f"**Описание:** {task['description'] or 'Нет описания'}")
                    if task['deadline']:
                        st.write(f"**Срок:** {task['deadline']}")
                    st.write(f"**Статус:** {status_emoji} {task['status']}")
                    
                    comments = database.get_task_comments(task['id'])
                    if comments:
                        st.write("**Комментарии:**")
                        for comment in comments:
                            st.write(f"  - {comment['newcomer_name']}: {comment['comment']}")
                    
                    new_status = st.selectbox(
                        "Изменить статус:",
                        options=["pending", "in_progress", "done"],
                        index=["pending", "in_progress", "done"].index(task['status']),
                        key=f"all_status_{task['id']}"
                    )
                    if st.button("Сохранить", key=f"all_save_{task['id']}"):
                        database.update_task_status(task['id'], new_status)
                        st.success("Статус обновлен!")
                        st.rerun()
        else:
            st.info("Пока нет задач")
            
    except Exception as e:
        st.error(f"Ошибка: {str(e)}")

if st.session_state['page'] == 'home':
    show_home()
elif st.session_state['page'] == 'newcomer':
    show_newcomer()
elif st.session_state['page'] == 'hr':
    show_hr()
