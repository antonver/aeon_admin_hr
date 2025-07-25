import os
from notion_client import Client
from notion_client.errors import APIResponseError
from dotenv import load_dotenv
from app.database import Candidate, Notification
from datetime import datetime

load_dotenv()

class NotionService:
    def __init__(self):
        self.notion_token = os.getenv("NOTION_TOKEN")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.client = Client(auth=self.notion_token) if self.notion_token else None
    
    async def create_candidate(self, candidate: Candidate) -> str:
        """Создать кандидата в Notion"""
        if not self.client or not self.database_id:
            return None
        
        try:
            # Определяем статус для Notion
            status_map = {
                "ожидает": "Ожидает",
                "прошёл": "Прошёл",
                "приглашён": "Приглашён",
                "отклонён": "Отклонён"
            }
            
            properties = {
                "Имя": {
                    "title": [
                        {
                            "text": {
                                "content": candidate.full_name
                            }
                        }
                    ]
                },
                "Telegram": {
                    "url": f"https://t.me/{candidate.telegram_username}" if candidate.telegram_username else None
                },
                # "Email": {
                #     "email": candidate.email
                # },
                # "Телефон": {
                #     "phone_number": candidate.phone
                # },
                "Статус": {
                    "select": {
                        "name": status_map.get(candidate.status, "Ожидает")
                    }
                },
                "Дата добавления": {
                    "date": {
                        "start": candidate.created_at.isoformat()
                    }
                },
                "Последнее действие": {
                    "rich_text": [
                        {
                            "text": {
                                "content": candidate.last_action_type or "Нет"
                            }
                        }
                    ]
                }
            }
            
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            return response["id"]
            
        except APIResponseError as e:
            print(f"Ошибка создания кандидата в Notion: {e}")
            return None
    
    async def update_candidate(self, candidate: Candidate):
        """Обновить кандидата в Notion"""
        if not self.client or not candidate.notion_id:
            return False
        
        try:
            status_map = {
                "ожидает": "Ожидает",
                "прошёл": "Прошёл",
                "приглашён": "Приглашён",
                "отклонён": "Отклонён"
            }
            
            properties = {
                "Статус": {
                    "select": {
                        "name": status_map.get(candidate.status, "Ожидает")
                    }
                },
                "Последнее действие": {
                    "rich_text": [
                        {
                            "text": {
                                "content": candidate.last_action_type or "Нет"
                            }
                        }
                    ]
                },
                "Дата обновления": {
                    "date": {
                        "start": candidate.updated_at.isoformat()
                    }
                }
            }
            
            self.client.pages.update(
                page_id=candidate.notion_id,
                properties=properties
            )
            
            return True
            
        except APIResponseError as e:
            print(f"Ошибка обновления кандидата в Notion: {e}")
            return False
    
    async def create_task(self, candidate: Candidate, task_type: str):
        """Создать задачу в Notion"""
        if not self.client or not self.database_id:
            return False
        
        try:
            task_database_id = os.getenv("NOTION_TASKS_DATABASE_ID")
            if not task_database_id:
                return False
            
            properties = {
                "Название": {
                    "title": [
                        {
                            "text": {
                                "content": f"{task_type} - {candidate.full_name}"
                            }
                        }
                    ]
                },
                "Тип": {
                    "select": {
                        "name": task_type
                    }
                },
                "Кандидат": {
                    "rich_text": [
                        {
                            "text": {
                                "content": candidate.full_name
                            }
                        }
                    ]
                },
                "Статус": {
                    "select": {
                        "name": "К выполнению"
                    }
                },
                "Дата создания": {
                    "date": {
                        "start": datetime.utcnow().isoformat()
                    }
                },
                "Ссылка на кандидата": {
                    "url": f"http://localhost:3000/candidate/{candidate.id}"
                }
            }
            
            self.client.pages.create(
                parent={"database_id": task_database_id},
                properties=properties
            )
            
            return True
            
        except APIResponseError as e:
            print(f"Ошибка создания задачи в Notion: {e}")
            return False
    
    async def create_notification_task(self, notification: Notification):
        """Создать задачу на основе уведомления"""
        if not self.client:
            return False
        
        try:
            task_database_id = os.getenv("NOTION_TASKS_DATABASE_ID")
            if not task_database_id:
                return False
            
            properties = {
                "Название": {
                    "title": [
                        {
                            "text": {
                                "content": f"Уведомление: {notification.type}"
                            }
                        }
                    ]
                },
                "Тип": {
                    "select": {
                        "name": "Уведомление"
                    }
                },
                "Сообщение": {
                    "rich_text": [
                        {
                            "text": {
                                "content": notification.message
                            }
                        }
                    ]
                },
                "Статус": {
                    "select": {
                        "name": "К выполнению"
                    }
                },
                "Дата создания": {
                    "date": {
                        "start": notification.created_at.isoformat()
                    }
                }
            }
            
            self.client.pages.create(
                parent={"database_id": task_database_id},
                properties=properties
            )
            
            return True
            
        except APIResponseError as e:
            print(f"Ошибка создания задачи уведомления в Notion: {e}")
            return False
    
    async def create_test_task(self):
        """Создать тестовую задачу"""
        if not self.client:
            return False
        
        try:
            task_database_id = os.getenv("NOTION_TASKS_DATABASE_ID")
            if not task_database_id:
                return False
            
            properties = {
                "Название": {
                    "title": [
                        {
                            "text": {
                                "content": "Тестовая задача - HR Admin Panel"
                            }
                        }
                    ]
                },
                "Тип": {
                    "select": {
                        "name": "Тест"
                    }
                },
                "Сообщение": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Тестовое уведомление от HR-админ панели"
                            }
                        }
                    ]
                },
                "Статус": {
                    "select": {
                        "name": "К выполнению"
                    }
                },
                "Дата создания": {
                    "date": {
                        "start": datetime.utcnow().isoformat()
                    }
                }
            }
            
            self.client.pages.create(
                parent={"database_id": task_database_id},
                properties=properties
            )
            
            return True
            
        except APIResponseError as e:
            print(f"Ошибка создания тестовой задачи в Notion: {e}")
            return False 