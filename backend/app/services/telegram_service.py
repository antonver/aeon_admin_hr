import os
import json
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv
from backend.app.database import Candidate, Notification, User
from sqlalchemy.orm import Session

load_dotenv()

class TelegramService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = Bot(token=self.bot_token) if self.bot_token else None
    
    async def send_message(self, candidate: Candidate, message: str):
        """Отправить сообщение кандидату в Telegram"""
        if not self.bot or not candidate.telegram_id:
            return False
        
        try:
            chat_id = f"{candidate.telegram_id}"
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
        if not self.bot or not candidate.telegram_id:
            return False
        # Формируем данные
        data = {
            'ID': candidate.id,
            'ФИО': candidate.full_name,
            'Telegram': candidate.telegram_username or '',
            # 'Email': candidate.email or '',
            # 'Телефон': candidate.phone or '',
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
            
            text = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            text = 'Неверный формат данных.'
        try:
            chat_id = f"{candidate.telegram_id}"
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=None if format == 'json' or format == 'csv' else 'Markdown'
            )
            return True
        except TelegramError as e:
            print(f"Ошибка отправки данных кандидата: {e}")
            return False

    async def send_interview_notification_to_admins(self, candidate: Candidate, interview_log, db: Session):
        """Отправить уведомление администраторам о прохождении интервью"""
        if not self.bot:
            return False
        
        # Получаем всех администраторов
        admins = db.query(User).filter(User.is_admin == True).all()
        
        if not admins:
            print("Нет администраторов для отправки уведомлений")
            return False
        
        # Формируем сообщение
        message = f"🎯 <b>Новое интервью</b>\n\n"
        message += f"👤 <b>Кандидат:</b> {candidate.full_name}\n"
        message += f"📝 <b>Вопрос:</b> {interview_log.question}\n"
        message += f"💬 <b>Ответ:</b> {interview_log.answer[:200]}{'...' if len(interview_log.answer) > 200 else ''}\n"
        
        if interview_log.score:
            message += f"⭐ <b>Оценка:</b> {interview_log.score}/10\n"
        
        if interview_log.category:
            message += f"🏷️ <b>Категория:</b> {interview_log.category}\n"
        
        message += f"📅 <b>Время:</b> {interview_log.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        # Добавляем ссылку на карточку кандидата
        webview_url = self.create_webview_url(candidate.id)
        message += f"<a href='{webview_url}'>📋 Открыть карточку кандидата</a>"
        
        # Отправляем уведомление каждому администратору
        success_count = 0
        for admin in admins:
            if admin.telegram_id:
                try:
                    await self.bot.send_message(
                        chat_id=admin.telegram_id,
                        text=message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    success_count += 1
                except TelegramError as e:
                    print(f"Ошибка отправки уведомления администратору {admin.name}: {e}")
        
        print(f"Уведомления отправлены {success_count} из {len(admins)} администраторов")
        return success_count > 0

    async def send_interview_completion_notification(self, candidate: Candidate, total_questions: int, avg_score: float, db: Session):
        """Отправить уведомление о завершении интервью"""
        if not self.bot:
            return False
        
        # Получаем всех администраторов
        admins = db.query(User).filter(User.is_admin == True).all()
        
        if not admins:
            print("Нет администраторов для отправки уведомлений")
            return False
        
        # Определяем эмодзи и текст статуса
        status_emoji = "✅" if candidate.status == "берем" else "❌"
        status_text = "БЕРЕМ" if candidate.status == "берем" else "НЕ БЕРЕМ"
        
        # Формируем сообщение
        message = f"{status_emoji} <b>Интервью завершено - {status_text}</b>\n\n"
        message += f"👤 <b>Кандидат:</b> {candidate.full_name}\n"
        message += f"📊 <b>Вопросов:</b> {total_questions}\n"
        message += f"⭐ <b>Средняя оценка:</b> {avg_score:.1f}/10\n"
        message += f"📅 <b>Завершено:</b> {candidate.updated_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        # Добавляем ссылку на карточку кандидата
        webview_url = self.create_webview_url(candidate.id)
        message += f"<a href='{webview_url}'>📋 Открыть карточку кандидата</a>"
        
        # Отправляем уведомление каждому администратору
        success_count = 0
        for admin in admins:
            if admin.telegram_id:
                try:
                    await self.bot.send_message(
                        chat_id=admin.telegram_id,
                        text=message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    success_count += 1
                except TelegramError as e:
                    print(f"Ошибка отправки уведомления администратору {admin.name}: {e}")
        
        print(f"Уведомления о завершении отправлены {success_count} из {len(admins)} администраторов")
        return success_count > 0

    async def send_interview_start_notification(self, candidate: Candidate, db: Session):
        """Отправить уведомление о начале интервью"""
        if not self.bot:
            return False
        
        # Получаем всех администраторов
        admins = db.query(User).filter(User.is_admin == True).all()
        
        if not admins:
            print("Нет администраторов для отправки уведомлений")
            return False
        
        # Формируем сообщение
        message = f"🎬 <b>Интервью началось</b>\n\n"
        message += f"👤 <b>Кандидат:</b> {candidate.full_name}\n"
        message += f"📅 <b>Время начала:</b> {candidate.updated_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        # Добавляем ссылку на карточку кандидата
        webview_url = self.create_webview_url(candidate.id)
        message += f"<a href='{webview_url}'>📋 Открыть карточку кандидата</a>"
        
        # Отправляем уведомление каждому администратору
        success_count = 0
        for admin in admins:
            if admin.telegram_id:
                try:
                    await self.bot.send_message(
                        chat_id=admin.telegram_id,
                        text=message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    success_count += 1
                except TelegramError as e:
                    print(f"Ошибка отправки уведомления администратору {admin.name}: {e}")
        
        print(f"Уведомления о начале интервью отправлены {success_count} из {len(admins)} администраторов")
        return success_count > 0

    async def send_status_change_notification(self, candidate: Candidate, new_status: str, db: Session):
        """Отправить уведомление об изменении статуса кандидата"""
        if not self.bot:
            return False
        
        # Получаем всех администраторов
        admins = db.query(User).filter(User.is_admin == True).all()
        
        if not admins:
            print("Нет администраторов для отправки уведомлений")
            return False
        
        # Определяем эмодзи для статуса
        status_emoji = {
            'ожидает': '⏳',
            'прошёл': '✅',
            'приглашён': '🎉',
            'отклонён': '❌'
        }
        
        emoji = status_emoji.get(new_status, '📊')
        
        # Формируем сообщение
        message = f"{emoji} <b>Статус изменен</b>\n\n"
        message += f"👤 <b>Кандидат:</b> {candidate.full_name}\n"
        message += f"📊 <b>Новый статус:</b> {new_status}\n"
        message += f"📅 <b>Время изменения:</b> {candidate.updated_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        # Добавляем ссылку на карточку кандидата
        webview_url = self.create_webview_url(candidate.id)
        message += f"<a href='{webview_url}'>📋 Открыть карточку кандидата</a>"
        
        # Отправляем уведомление каждому администратору
        success_count = 0
        for admin in admins:
            if admin.telegram_id:
                try:
                    await self.bot.send_message(
                        chat_id=admin.telegram_id,
                        text=message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    success_count += 1
                except TelegramError as e:
                    print(f"Ошибка отправки уведомления администратору {admin.name}: {e}")
        
        print(f"Уведомления об изменении статуса отправлены {success_count} из {len(admins)} администраторов")
        return success_count > 0

    async def send_daily_summary(self, db: Session):
        """Отправить ежедневную сводку администраторам"""
        if not self.bot:
            return False
        
        # Получаем всех администраторов
        admins = db.query(User).filter(User.is_admin == True).all()
        
        if not admins:
            print("Нет администраторов для отправки уведомлений")
            return False
        
        # Получаем статистику за сегодня
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        
        total_candidates = db.query(Candidate).filter(
            Candidate.created_at >= today,
            Candidate.created_at < tomorrow
        ).count()
        
        passed_candidates = db.query(Candidate).filter(
            Candidate.status == 'прошёл',
            Candidate.updated_at >= today,
            Candidate.updated_at < tomorrow
        ).count()
        
        rejected_candidates = db.query(Candidate).filter(
            Candidate.status == 'отклонён',
            Candidate.updated_at >= today,
            Candidate.updated_at < tomorrow
        ).count()
        
        # Формируем сообщение
        message = f"📊 <b>Ежедневная сводка</b>\n\n"
        message += f"📅 <b>Дата:</b> {today.strftime('%d.%m.%Y')}\n"
        message += f"👥 <b>Новых кандидатов:</b> {total_candidates}\n"
        message += f"✅ <b>Прошли интервью:</b> {passed_candidates}\n"
        message += f"❌ <b>Отклонены:</b> {rejected_candidates}\n"
        
        if total_candidates > 0:
            success_rate = (passed_candidates / total_candidates) * 100
            message += f"📈 <b>Процент успеха:</b> {success_rate:.1f}%\n"
        
        message += f"\n🎯 <b>Отличная работа!</b>"
        
        # Отправляем уведомление каждому администратору
        success_count = 0
        for admin in admins:
            if admin.telegram_id:
                try:
                    await self.bot.send_message(
                        chat_id=admin.telegram_id,
                        text=message,
                        parse_mode='HTML'
                    )
                    success_count += 1
                except TelegramError as e:
                    print(f"Ошибка отправки сводки администратору {admin.name}: {e}")
        
        print(f"Ежедневные сводки отправлены {success_count} из {len(admins)} администраторов")
        return success_count > 0 