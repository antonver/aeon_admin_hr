import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv
from app.database import Candidate, Notification

load_dotenv()

class TelegramService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = Bot(token=self.bot_token) if self.bot_token else None
    
    async def send_message(self, candidate: Candidate, message: str):
        """Отправить сообщение кандидату в Telegram"""
        if not self.bot or not candidate.telegram_username:
            return False
        
        try:
            chat_id = f"@{candidate.telegram_username}"
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
        except TelegramError as e:
            print(f"Ошибка отправки сообщения в Telegram: {e}")
            return False
    
    async def send_notification(self, notification: Notification):
        """Отправить уведомление HR-менеджеру"""
        if not self.bot or not self.chat_id:
            return False
        
        try:
            message = f"🔔 <b>Уведомление</b>\n\n"
            message += f"Тип: {notification.type}\n"
            message += f"Сообщение: {notification.message}\n"
            message += f"Время: {notification.created_at.strftime('%d.%m.%Y %H:%M')}"
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
        except TelegramError as e:
            print(f"Ошибка отправки уведомления в Telegram: {e}")
            return False
    
    async def send_test_invitation(self, candidate: Candidate):
        """Отправить приглашение на тест"""
        message = f"🎯 <b>Приглашение на тест</b>\n\n"
        message += f"Здравствуйте, {candidate.full_name}!\n\n"
        message += "Вам приглашение пройти тест по софт-скиллам.\n"
        message += "Ссылка на тест: https://forms.gle/example\n\n"
        message += "Удачи! 🚀"
        
        return await self.send_message(candidate, message)
    
    async def send_feedback(self, candidate: Candidate, feedback: str):
        """Отправить фидбэк кандидату"""
        message = f"📝 <b>Фидбэк по интервью</b>\n\n"
        message += f"Здравствуйте, {candidate.full_name}!\n\n"
        message += f"{feedback}\n\n"
        message += "Спасибо за участие! 🙏"
        
        return await self.send_message(candidate, message)
    
    async def send_test_message(self):
        """Отправить тестовое сообщение"""
        if not self.bot or not self.chat_id:
            return False
        
        try:
            message = "🧪 <b>Тестовое уведомление</b>\n\n"
            message += "HR-админ панель работает корректно! ✅"
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
        except TelegramError as e:
            print(f"Ошибка отправки тестового сообщения: {e}")
            return False
    
    def create_webview_url(self, candidate_id: int) -> str:
        """Создать URL для WebView с карточкой кандидата"""
        base_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return f"{base_url}/candidate/{candidate_id}"
    
    async def send_candidate_card_link(self, candidate: Candidate):
        """Отправить ссылку на карточку кандидата"""
        if not self.bot or not self.chat_id:
            return False
        
        try:
            webview_url = self.create_webview_url(candidate.id)
            
            message = f"👤 <b>Карточка кандидата</b>\n\n"
            message += f"Имя: {candidate.full_name}\n"
            message += f"Статус: {candidate.status}\n"
            message += f"Последнее действие: {candidate.last_action_type}\n\n"
            message += f"<a href='{webview_url}'>Открыть карточку</a>"
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            return True
        except TelegramError as e:
            print(f"Ошибка отправки ссылки на карточку: {e}")
            return False 
    
    async def send_candidate_data_formatted(self, candidate: Candidate, format: str):
        """Отправить все данные кандидата в Telegram в выбранном формате (csv, md, json)"""
        if not self.bot or not candidate.telegram_username:
            return False
        # Формируем данные
        data = {
            'ID': candidate.id,
            'ФИО': candidate.full_name,
            'Telegram': candidate.telegram_username or '',
            'Email': candidate.email or '',
            'Телефон': candidate.phone or '',
            'Статус': candidate.status,
            'Последнее действие': candidate.last_action_type or '',
            'Дата создания': candidate.created_at.strftime('%Y-%m-%d %H:%M') if candidate.created_at else '',
            'Дата обновления': candidate.updated_at.strftime('%Y-%m-%d %H:%M') if candidate.updated_at else '',
        }
        if format == 'csv':
            text = ','.join(data.keys()) + '\n' + ','.join(str(v) for v in data.values())
        elif format == 'md':
            text = '### Данные кандидата\n' + '\n'.join([f'- **{k}:** {v}' for k, v in data.items()])
        elif format == 'json':
            import json
            text = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            text = 'Неверный формат данных.'
        try:
            chat_id = f"@{candidate.telegram_username}"
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=None if format == 'json' or format == 'csv' else 'Markdown'
            )
            return True
        except TelegramError as e:
            print(f"Ошибка отправки данных кандидата: {e}")
            return False 