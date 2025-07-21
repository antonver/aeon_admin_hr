import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft,
  MessageSquare,
  Send,
  Copy,
  Edit,
  Save,
  X
} from 'lucide-react';

interface Candidate {
  id: number;
  full_name: string;
  telegram_username?: string;
  email?: string;
  phone?: string;
  status: string;
  last_action_date: string;
  last_action_type?: string;
  created_at: string;
  updated_at: string;
}

interface InterviewLog {
  id: number;
  question: string;
  answer: string;
  score?: number;
  category?: string;
  created_at: string;
}

interface Comment {
  id: number;
  hr_comment: string;
  created_at: string;
}

const CandidateDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [editData, setEditData] = useState<Partial<Candidate>>({});
  const [interviewLogs, setInterviewLogs] = useState<InterviewLog[]>([]);
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [showTelegramModal, setShowTelegramModal] = useState(false);
  const [telegramMessage, setTelegramMessage] = useState('');

  useEffect(() => {
    if (id) {
      fetchCandidateData();
    }
  }, [id]);

  useEffect(() => {
    if (editing && candidate) {
      setEditData({ ...candidate });
    }
  }, [editing, candidate]);

  const fetchCandidateData = async () => {
    try {
      const [candidateRes, logsRes, commentsRes] = await Promise.all([
        fetch(`/api/candidates/${id}`),
        fetch(`/api/candidates/${id}/interview-logs`),
        fetch(`/api/candidates/${id}/comments`)
      ]);

      const candidateData = await candidateRes.json();
      const logsData = await logsRes.json();
      const commentsData = await commentsRes.json();

      setCandidate(candidateData);
      setInterviewLogs(logsData);
      setComments(commentsData);
    } catch (error) {
      console.error('Ошибка загрузки данных кандидата:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ожидает': return 'status-waiting';
      case 'прошёл': return 'status-passed';
      case 'приглашён': return 'status-invited';
      case 'отклонён': return 'status-rejected';
      default: return 'status-waiting';
    }
  };

  const handleQuickAction = async (action: string, data?: any) => {
    if (!candidate) return;
    try {
      let body: any = {
        action_type: action,
        candidate_id: candidate.id,
      };
      if (action === 'telegram_message' && data?.message) {
        body.data = { message: data.message };
      }
      const response = await fetch(`/api/candidates/${candidate.id}/quick-action`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      if (response.ok) {
        fetchCandidateData();
        setActionMessage('Действие выполнено');
        setTimeout(() => setActionMessage(null), 3000);
      } else {
        setActionMessage('Ошибка выполнения действия');
        setTimeout(() => setActionMessage(null), 3000);
      }
    } catch (error) {
      setActionMessage('Ошибка выполнения действия');
      setTimeout(() => setActionMessage(null), 3000);
    }
  };

  const handleAddComment = async () => {
    if (!candidate || !newComment.trim()) return;
    try {
      const response = await fetch(`/api/candidates/${candidate.id}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          candidate_id: candidate.id,
          hr_comment: newComment,
        }),
      });
      if (response.ok) {
        setNewComment('');
        fetchCandidateData();
      }
    } catch (error) {
      console.error('Ошибка добавления комментария:', error);
    }
  };

  const copyCandidateData = () => {
    if (!candidate) return;
    const data = `Имя: ${candidate.full_name}\nTelegram: ${candidate.telegram_username || 'Нет'}\nEmail: ${candidate.email || 'Нет'}\nТелефон: ${candidate.phone || 'Нет'}\nСтатус: ${candidate.status}`;
    navigator.clipboard.writeText(data);
    setActionMessage('Данные скопированы в буфер обмена');
    setTimeout(() => setActionMessage(null), 3000);
  };

  const handleEditChange = (field: keyof Candidate, value: string) => {
    setEditData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!candidate) return;
    try {
      const response = await fetch(`/api/candidates/${candidate.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editData),
      });
      if (response.ok) {
        setEditing(false);
        setActionMessage('Изменения сохранены');
        fetchCandidateData();
        setTimeout(() => setActionMessage(null), 3000);
      } else {
        setActionMessage('Ошибка сохранения');
        setTimeout(() => setActionMessage(null), 3000);
      }
    } catch (error) {
      setActionMessage('Ошибка сохранения');
      setTimeout(() => setActionMessage(null), 3000);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!candidate) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold text-gray-900">Кандидат не найден</h2>
        <Link to="/candidates" className="text-main hover:text-secondary">
          Вернуться к списку
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Action Message */}
      {actionMessage && (
        <div className="fixed top-4 right-4 bg-main text-white px-6 py-3 rounded-lg shadow-lg z-50">
          {actionMessage}
        </div>
      )}
      {/* Модальное окно Telegram */}
      {showTelegramModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-subheaders text-background font-bold">Сообщение в Telegram</h2>
              <button
                onClick={() => setShowTelegramModal(false)}
                className="text-background-2 hover:text-background"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <textarea
              className="input-field w-full h-28 mb-4"
              placeholder="Введите сообщение..."
              value={telegramMessage}
              onChange={e => setTelegramMessage(e.target.value)}
            />
            <div className="flex gap-3">
              <button
                className="btn btn-primary flex-1"
                disabled={!telegramMessage.trim()}
                onClick={async () => {
                  await handleQuickAction('telegram_message', { message: telegramMessage });
                  setShowTelegramModal(false);
                  setTelegramMessage('');
                }}
              >
                Отправить
              </button>
              <button
                className="btn btn-outline flex-1"
                onClick={() => setShowTelegramModal(false)}
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/candidates"
            className="text-background-2 hover:text-background"
          >
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-headers text-background">{candidate.full_name}</h1>
            <p className="text-main text-background-2">Карточка кандидата</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setEditing(!editing)}
            className="btn btn-secondary flex items-center space-x-2"
          >
            {editing ? <X className="h-4 w-4" /> : <Edit className="h-4 w-4" />}
            <span>{editing ? 'Отмена' : 'Редактировать'}</span>
          </button>
          {editing && (
            <button onClick={handleSave} className="btn btn-primary flex items-center space-x-2">
              <Save className="h-4 w-4" />
              <span>Сохранить</span>
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Основная информация */}
        <div className="lg:col-span-2 space-y-6">
          {/* Информация о кандидате */}
          <div className="card">
            <h2 className="text-subheaders text-background font-bold mb-4">Основная информация</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-main text-background mb-1">
                  ФИО
                </label>
                <input
                  type="text"
                  value={editing ? editData.full_name || '' : candidate.full_name}
                  disabled={!editing}
                  onChange={e => handleEditChange('full_name', e.target.value)}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-main text-background mb-1">
                  Статус
                </label>
                <select
                  value={editing ? editData.status || '' : candidate.status}
                  disabled={!editing}
                  onChange={e => handleEditChange('status', e.target.value)}
                  className="input-field"
                >
                  <option value="ожидает">Ожидает</option>
                  <option value="прошёл">Прошёл</option>
                  <option value="приглашён">Приглашён</option>
                  <option value="отклонён">Отклонён</option>
                </select>
              </div>
              <div>
                <label className="block text-main text-background mb-1">
                  Telegram
                </label>
                <input
                  type="text"
                  value={editing ? editData.telegram_username || '' : candidate.telegram_username || ''}
                  disabled={!editing}
                  onChange={e => handleEditChange('telegram_username', e.target.value)}
                  className="input-field"
                  placeholder="@username"
                />
              </div>
              <div>
                <label className="block text-main text-background mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={editing ? editData.email || '' : candidate.email || ''}
                  disabled={!editing}
                  onChange={e => handleEditChange('email', e.target.value)}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-main text-background mb-1">
                  Телефон
                </label>
                <input
                  type="tel"
                  value={editing ? editData.phone || '' : candidate.phone || ''}
                  disabled={!editing}
                  onChange={e => handleEditChange('phone', e.target.value)}
                  className="input-field"
                  placeholder="+7 (999) 123-45-67"
                />
              </div>
            </div>
          </div>

          {/* Логи интервью */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Отчёт ÆON-интервью</h2>
            {interviewLogs.length > 0 ? (
              <div className="space-y-4">
                {interviewLogs.map((log) => (
                  <div key={log.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-gray-900">{log.question}</h3>
                      {log.score && (
                        <span className="text-sm text-gray-500">Балл: {log.score}/10</span>
                      )}
                    </div>
                    <p className="text-gray-700">{log.answer}</p>
                    {log.category && (
                      <span className="inline-block mt-2 px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                        {log.category}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">Логи интервью отсутствуют</p>
            )}
          </div>
        </div>

        {/* Боковая панель */}
        <div className="space-y-6">
          {/* Быстрые действия */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Быстрые действия</h2>
            <div className="space-y-3">
              <button
                onClick={() => handleQuickAction('invite_test')}
                className="w-full btn-primary flex items-center justify-center space-x-2"
              >
                <Send className="h-4 w-4" />
                <span>Пригласить на тест</span>
              </button>
              
              {candidate.telegram_username && (
                <button
                  onClick={() => setShowTelegramModal(true)}
                  className="w-full btn-secondary flex items-center justify-center space-x-2"
                >
                  <MessageSquare className="h-4 w-4" />
                  <span>Написать в Telegram</span>
                </button>
              )}
              
              <button
                onClick={copyCandidateData}
                className="w-full btn-secondary flex items-center justify-center space-x-2"
              >
                <Copy className="h-4 w-4" />
                <span>Скопировать данные</span>
              </button>
            </div>
          </div>

          {/* Комментарии HR */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Комментарии HR</h2>
            
            {/* Добавить комментарий */}
            <div className="mb-4">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Добавить комментарий..."
                className="input-field h-20 resize-none"
              />
              <button
                onClick={handleAddComment}
                disabled={!newComment.trim()}
                className="mt-2 btn-primary w-full"
              >
                Добавить
              </button>
            </div>

            {/* Список комментариев */}
            <div className="space-y-3">
              {comments.map((comment) => (
                <div key={comment.id} className="bg-gray-50 rounded-lg p-3">
                  <p className="text-sm text-gray-700">{comment.hr_comment}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(comment.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Статистика */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Статистика</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Вопросов в интервью:</span>
                <span className="text-sm font-medium">{interviewLogs.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Средний балл:</span>
                <span className="text-sm font-medium">
                  {interviewLogs.length > 0
                    ? Math.round(
                        interviewLogs
                          .filter(log => log.score)
                          .reduce((sum, log) => sum + (log.score || 0), 0) /
                        interviewLogs.filter(log => log.score).length
                      )
                    : 'Нет данных'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Комментариев HR:</span>
                <span className="text-sm font-medium">{comments.length}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateDetail; 