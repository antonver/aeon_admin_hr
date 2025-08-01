#!/usr/bin/env python3
"""
Полный тест системы уведомлений HR Admin System
Проверяет все типы уведомлений и их интеграцию
"""

import requests
import json
import time
import sys
from datetime import datetime

BASE_URL = "http://localhost:8001"

class NotificationTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.candidate_id = None
        
    def print_step(self, step_num, title):
        print(f"\n{'='*60}")
        print(f"ШАГ {step_num}: {title}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def print_info(self, message):
        print(f"ℹ️  {message}")
    
    def test_connection(self):
        """Тест подключения к серверу"""
        self.print_step(1, "Проверка подключения к серверу")
        try:
            response = self.session.get(f"{BASE_URL}/api/health")
            if response.status_code == 200:
                self.print_success("Сервер доступен")
                return True
            else:
                self.print_error(f"Сервер недоступен: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.print_error("Не удается подключиться к серверу")
            return False
    
    def create_admin(self):
        """Создание тестового администратора"""
        self.print_step(2, "Создание тестового администратора")
        
        # Симулируем данные Telegram
        init_data = "user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22Admin%22%2C%22username%22%3A%22testadmin%22%7D&auth_date=1234567890&hash=test_hash"
        
        try:
            response = self.session.post(f"{BASE_URL}/api/telegram/telegram-auth", json={
                "init_data": init_data
            })
            
            if response.status_code == 200:
                auth_data = response.json()
                self.token = auth_data["access_token"]
                self.print_success(f"Администратор создан: {auth_data['user']['name']}")
                self.print_info(f"Token: {self.token[:20]}...")
                return True
            else:
                self.print_error(f"Ошибка создания администратора: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при создании администратора: {e}")
            return False
    
    def create_test_candidate(self):
        """Создание тестового кандидата"""
        self.print_step(3, "Создание тестового кандидата")
        
        candidate_data = {
            "full_name": "Анна Сидорова",
            "telegram_id": "987654321",
            "telegram_username": "anna_sidorova",
            "results": "Тестовые результаты интервью"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/api/candidates", json=candidate_data)
            
            if response.status_code == 200:
                candidate = response.json()
                self.candidate_id = candidate["id"]
                self.print_success(f"Кандидат создан: {candidate['full_name']} (ID: {self.candidate_id})")
                return True
            else:
                self.print_error(f"Ошибка создания кандидата: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при создании кандидата: {e}")
            return False
    
    def test_interview_start_notification(self):
        """Тест уведомления о начале интервью"""
        self.print_step(4, "Тест уведомления о начале интервью")
        
        try:
            response = self.session.post(f"{BASE_URL}/api/notifications/send-interview-notification/{self.candidate_id}")
            
            if response.status_code == 200:
                self.print_success("Уведомление о начале интервью отправлено")
                return True
            else:
                self.print_error(f"Ошибка отправки уведомления: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при отправке уведомления: {e}")
            return False
    
    def test_interview_questions(self):
        """Тест уведомлений о вопросах интервью"""
        self.print_step(5, "Тест уведомлений о вопросах интервью")
        
        interview_questions = [
            {
                "question": "Расскажите о своем опыте работы в команде",
                "answer": "У меня есть опыт работы в командах до 10 человек. Я умею эффективно коммуницировать и распределять задачи.",
                "score": 9,
                "category": "командная_работа"
            },
            {
                "question": "Как вы решаете конфликтные ситуации?",
                "answer": "Сначала выслушиваю все стороны, затем ищу компромиссное решение, которое устроит всех участников.",
                "score": 8,
                "category": "soft_skills"
            },
            {
                "question": "Какие у вас планы на профессиональное развитие?",
                "answer": "Хочу углубить знания в области машинного обучения и стать тимлидом в течение 2-3 лет.",
                "score": 9,
                "category": "мотивация"
            },
            {
                "question": "Почему вы хотите работать именно в нашей компании?",
                "answer": "Мне нравится миссия компании и возможности для роста. Также привлекает технологический стек.",
                "score": 8,
                "category": "мотивация"
            },
            {
                "question": "Как вы относитесь к дедлайнам и стрессовым ситуациям?",
                "answer": "Я умею эффективно планировать время и работать под давлением. Всегда стараюсь выполнять задачи качественно и вовремя.",
                "score": 9,
                "category": "ответственность"
            }
        ]
        
        success_count = 0
        for i, question_data in enumerate(interview_questions, 1):
            self.print_info(f"Отправка вопроса {i}/5...")
            
            try:
                response = self.session.post(
                    f"{BASE_URL}/api/candidates/{self.candidate_id}/interview-logs",
                    json=question_data
                )
                
                if response.status_code == 200:
                    self.print_success(f"Вопрос {i} отправлен")
                    success_count += 1
                else:
                    self.print_error(f"Ошибка отправки вопроса {i}: {response.status_code}")
                    self.print_error(f"Response: {response.text}")
                
                # Небольшая задержка между вопросами
                time.sleep(1)
                
            except Exception as e:
                self.print_error(f"Исключение при отправке вопроса {i}: {e}")
        
        self.print_info(f"Успешно отправлено: {success_count}/5 вопросов")
        return success_count == 5
    
    def test_status_change_notification(self):
        """Тест уведомления об изменении статуса"""
        self.print_step(6, "Тест уведомления об изменении статуса")
        
        try:
            response = self.session.post(
                f"{BASE_URL}/api/notifications/send-status-change-notification/{self.candidate_id}",
                params={"new_status": "прошёл"}
            )
            
            if response.status_code == 200:
                self.print_success("Уведомление об изменении статуса отправлено")
                return True
            else:
                self.print_error(f"Ошибка отправки уведомления: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при отправке уведомления: {e}")
            return False
    
    def test_notification_stats(self):
        """Тест получения статистики уведомлений"""
        self.print_step(7, "Тест получения статистики уведомлений")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/notifications/stats")
            
            if response.status_code == 200:
                stats = response.json()
                self.print_success("Статистика уведомлений получена")
                self.print_info(f"Всего уведомлений: {stats.get('total', 0)}")
                self.print_info(f"Отправлено в Telegram: {stats.get('telegram_sent', 0)}")
                self.print_info(f"Отправлено в Notion: {stats.get('notion_sent', 0)}")
                self.print_info(f"Процент успеха: {stats.get('success_rate', 0):.1f}%")
                
                if stats.get('type_stats'):
                    self.print_info("Статистика по типам:")
                    for type_stat in stats['type_stats']:
                        self.print_info(f"  - {type_stat['type']}: {type_stat['count']}")
                
                return True
            else:
                self.print_error(f"Ошибка получения статистики: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при получении статистики: {e}")
            return False
    
    def test_notifications_list(self):
        """Тест получения списка уведомлений"""
        self.print_step(8, "Тест получения списка уведомлений")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/notifications/")
            
            if response.status_code == 200:
                notifications = response.json()
                self.print_success(f"Получен список уведомлений: {len(notifications)} записей")
                
                if notifications:
                    self.print_info("Последние уведомления:")
                    for i, notification in enumerate(notifications[:3], 1):
                        self.print_info(f"  {i}. {notification.get('type', 'N/A')} - {notification.get('message', 'N/A')[:50]}...")
                
                return True
            else:
                self.print_error(f"Ошибка получения списка: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при получении списка: {e}")
            return False
    
    def test_test_notification(self):
        """Тест отправки тестового уведомления"""
        self.print_step(9, "Тест отправки тестового уведомления")
        
        try:
            response = self.session.post(f"{BASE_URL}/api/notifications/send-test")
            
            if response.status_code == 200:
                self.print_success("Тестовое уведомление отправлено")
                return True
            else:
                self.print_error(f"Ошибка отправки тестового уведомления: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при отправке тестового уведомления: {e}")
            return False
    
    def check_candidate_status(self):
        """Проверка финального статуса кандидата"""
        self.print_step(10, "Проверка финального статуса кандидата")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/candidates/{self.candidate_id}")
            
            if response.status_code == 200:
                candidate = response.json()
                self.print_success(f"Статус кандидата: {candidate['status']}")
                self.print_info(f"Последнее действие: {candidate.get('last_action_type', 'N/A')}")
                self.print_info(f"Время обновления: {candidate['updated_at']}")
                return True
            else:
                self.print_error(f"Ошибка получения статуса: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"Исключение при получении статуса: {e}")
            return False
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("🚀 ЗАПУСК ПОЛНОГО ТЕСТА СИСТЕМЫ УВЕДОМЛЕНИЙ")
        print(f"📅 Время начала: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        
        tests = [
            self.test_connection,
            self.create_admin,
            self.create_test_candidate,
            self.test_interview_start_notification,
            self.test_interview_questions,
            self.test_status_change_notification,
            self.test_notification_stats,
            self.test_notifications_list,
            self.test_test_notification,
            self.check_candidate_status
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
                if not result:
                    self.print_error("Тест не прошел, но продолжаем...")
            except Exception as e:
                self.print_error(f"Критическая ошибка в тесте: {e}")
                results.append(False)
        
        # Итоговый отчет
        print(f"\n{'='*60}")
        print("ИТОГОВЫЙ ОТЧЕТ")
        print(f"{'='*60}")
        
        passed = sum(results)
        total = len(results)
        
        print(f"✅ Пройдено тестов: {passed}/{total}")
        print(f"📊 Процент успеха: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        else:
            print("⚠️  НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        
        print(f"\n📱 Проверьте Telegram бота - должны прийти уведомления:")
        print("   - О начале интервью")
        print("   - О каждом вопросе интервью (5 штук)")
        print("   - О завершении интервью")
        print("   - Об изменении статуса")
        print("   - Тестовое уведомление")
        
        print(f"\n📅 Время завершения: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        
        return passed == total

def main():
    tester = NotificationTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 Система уведомлений работает корректно!")
        sys.exit(0)
    else:
        print("\n❌ Обнаружены проблемы в системе уведомлений")
        sys.exit(1)

if __name__ == "__main__":
    main() 