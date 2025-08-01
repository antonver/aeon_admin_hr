import React, { useState, useEffect } from 'react';
import { Bell, Settings, Send, Trash2, Eye, EyeOff } from 'lucide-react';

interface Notification {
  id: number;
  type: string;
  message: string;
  candidate_id: number;
  telegram_sent: boolean;
  notion_sent: boolean;
  created_at: string;
  candidate?: {
    full_name: string;
    telegram_username?: string;
  };
}

interface NotificationSettings {
  telegram_enabled: boolean;
  notion_enabled: boolean;
  interview_notifications: boolean;
  completion_notifications: boolean;
  test_notifications: boolean;
}

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [settings, setSettings] = useState<NotificationSettings>({
    telegram_enabled: true,
    notion_enabled: true,
    interview_notifications: true,
    completion_notifications: true,
    test_notifications: true
  });
  const [loading, setLoading] = useState(true);
  const [showSettings, setShowSettings] = useState(false);
  const [selectedNotification, setSelectedNotification] = useState<Notification | null>(null);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await fetch('/api/notifications');
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (error) {
      console.error('Ошибка загрузки уведомлений:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteNotification = async (id: number) => {
    try {
      const response = await fetch(`/api/notifications/${id}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        setNotifications(prev => prev.filter(n => n.id !== id));
      }
    } catch (error) {
      console.error('Ошибка удаления уведомления:', error);
    }
  };

  const sendTestNotification = async () => {
    try {
      const response = await fetch('/api/notifications/send-test', {
        method: 'POST'
      });
      if (response.ok) {
        alert('Тестовое уведомление отправлено!');
      }
    } catch (error) {
      console.error('Ошибка отправки тестового уведомления:', error);
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'interview_completed':
        return '🎯';
      case 'notion_updated':
        return '📝';
      case 'task_created':
        return '✅';
      default:
        return '🔔';
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'interview_completed':
        return 'bg-green-100 border-green-300';
      case 'notion_updated':
        return 'bg-blue-100 border-blue-300';
      case 'task_created':
        return 'bg-purple-100 border-purple-300';
      default:
        return 'bg-gray-100 border-gray-300';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Bell className="h-8 w-8 text-main" />
          <div>
            <h1 className="text-2xl font-bold text-background">Уведомления</h1>
            <p className="text-main text-background-2">Управление системными уведомлениями</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="btn btn-secondary flex items-center space-x-2"
          >
            <Settings className="h-4 w-4" />
            <span>Настройки</span>
          </button>
          <button
            onClick={sendTestNotification}
            className="btn btn-primary flex items-center space-x-2"
          >
            <Send className="h-4 w-4" />
            <span>Тест</span>
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="card">
          <h2 className="text-lg font-semibold text-background mb-4">Настройки уведомлений</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <h3 className="font-medium text-background">Каналы отправки</h3>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.telegram_enabled}
                  onChange={(e) => setSettings(prev => ({ ...prev, telegram_enabled: e.target.checked }))}
                  className="checkbox"
                />
                <span className="text-main">Telegram</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.notion_enabled}
                  onChange={(e) => setSettings(prev => ({ ...prev, notion_enabled: e.target.checked }))}
                  className="checkbox"
                />
                <span className="text-main">Notion</span>
              </label>
            </div>
            <div className="space-y-3">
              <h3 className="font-medium text-background">Типы уведомлений</h3>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.interview_notifications}
                  onChange={(e) => setSettings(prev => ({ ...prev, interview_notifications: e.target.checked }))}
                  className="checkbox"
                />
                <span className="text-main">Интервью</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.completion_notifications}
                  onChange={(e) => setSettings(prev => ({ ...prev, completion_notifications: e.target.checked }))}
                  className="checkbox"
                />
                <span className="text-main">Завершение</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={settings.test_notifications}
                  onChange={(e) => setSettings(prev => ({ ...prev, test_notifications: e.target.checked }))}
                  className="checkbox"
                />
                <span className="text-main">Тестовые</span>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Notifications List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-background">
            История уведомлений ({notifications.length})
          </h2>
          <button
            onClick={fetchNotifications}
            className="text-main hover:text-secondary"
          >
            Обновить
          </button>
        </div>

        {notifications.length === 0 ? (
          <div className="text-center py-12">
            <Bell className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">Уведомлений пока нет</p>
          </div>
        ) : (
          <div className="space-y-3">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`card border-l-4 ${getNotificationColor(notification.type)} cursor-pointer hover:shadow-md transition-shadow`}
                onClick={() => setSelectedNotification(notification)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3 flex-1">
                    <span className="text-2xl">{getNotificationIcon(notification.type)}</span>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <h3 className="font-medium text-background capitalize">
                          {notification.type.replace('_', ' ')}
                        </h3>
                        <div className="flex items-center space-x-1">
                          {notification.telegram_sent && (
                            <span className="text-green-600 text-xs">📱</span>
                          )}
                          {notification.notion_sent && (
                            <span className="text-blue-600 text-xs">📝</span>
                          )}
                        </div>
                      </div>
                      <p className="text-main text-sm mb-2">{notification.message}</p>
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>{formatDate(notification.created_at)}</span>
                        {notification.candidate && (
                          <span>👤 {notification.candidate.full_name}</span>
                        )}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteNotification(notification.id);
                    }}
                    className="text-red-500 hover:text-red-700 p-1"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Notification Detail Modal */}
      {selectedNotification && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-background">
                Детали уведомления
              </h3>
              <button
                onClick={() => setSelectedNotification(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Тип</label>
                <p className="text-sm text-gray-900 capitalize">
                  {selectedNotification.type.replace('_', ' ')}
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Сообщение</label>
                <p className="text-sm text-gray-900">{selectedNotification.message}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Время создания</label>
                <p className="text-sm text-gray-900">{formatDate(selectedNotification.created_at)}</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Статус отправки</label>
                <div className="flex items-center space-x-4 text-sm">
                  <span className={`flex items-center space-x-1 ${selectedNotification.telegram_sent ? 'text-green-600' : 'text-red-600'}`}>
                    <span>📱</span>
                    <span>{selectedNotification.telegram_sent ? 'Отправлено' : 'Не отправлено'}</span>
                  </span>
                  <span className={`flex items-center space-x-1 ${selectedNotification.notion_sent ? 'text-green-600' : 'text-red-600'}`}>
                    <span>📝</span>
                    <span>{selectedNotification.notion_sent ? 'Отправлено' : 'Не отправлено'}</span>
                  </span>
                </div>
              </div>
            </div>
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setSelectedNotification(null)}
                className="btn btn-secondary"
              >
                Закрыть
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Notifications; 