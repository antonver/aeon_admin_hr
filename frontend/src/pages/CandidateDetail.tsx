import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft,
  Edit,
  Save,
  X,
  MessageSquare,
  Copy
} from 'lucide-react';

interface Candidate {
  id: number;
  full_name: string;
  name?: string;
  telegram_username?: string;
  status: string;
  results?: string;
  last_action_date: string;
  last_action_type?: string;
  created_at: string;
  updated_at: string;
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
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'info' | 'results' | 'comments'>('info');

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

  // Функция для анализа результатов интервью и определения статуса
  const analyzeInterviewResults = (results: string): string => {
    if (!results) return 'ожидает';
    
    const lowerResults = results.toLowerCase();
    if (lowerResults.includes('не берем')) {
      return 'не берем';
    } else {
      return 'берем';
    }
  };

  const fetchCandidateData = async () => {
    try {
      const [candidateRes, commentsRes] = await Promise.all([
        fetch(`/api/candidates/${id}`),
        fetch(`/api/candidates/${id}/comments`)
      ]);

      const candidateData = await candidateRes.json();
      const commentsData = await commentsRes.json();

      // Автоматически определяем статус на основе результатов
      if (candidateData.results) {
        const autoStatus = analyzeInterviewResults(candidateData.results);
        if (autoStatus !== candidateData.status) {
          // Обновляем статус в базе данных
          await updateCandidateStatus(candidateData.id, autoStatus);
          candidateData.status = autoStatus;
        }
      }

      setCandidate(candidateData);
      setComments(commentsData);
    } catch (error) {
      console.error('Ошибка загрузки данных кандидата:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateCandidateStatus = async (candidateId: number, newStatus: string) => {
    try {
      const response = await fetch(`/api/candidates/${candidateId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });
      if (!response.ok) {
        console.error('Ошибка обновления статуса');
      }
    } catch (error) {
      console.error('Ошибка обновления статуса:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ожидает': return 'status-waiting';
      case 'берем': return 'status-passed';
      case 'не берем': return 'status-rejected';
      default: return 'status-waiting';
    }
  };

  const getStatusEmoji = (status: string) => {
    switch (status) {
      case 'берем': return '✅';
      case 'не берем': return '❌';
      default: return '⏳';
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
    const data = `Имя: ${candidate.full_name}\nTelegram: ${candidate.telegram_username || 'Нет'}\nСтатус: ${candidate.status}`;
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
        <Link to="/candidates" className="text-blue-600 hover:text-blue-800">
          Вернуться к списку
        </Link>
      </div>
    );
  }

  return (
    <div className="mobile-padding">
      {/* Action Message */}
      {actionMessage && (
        <div className="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
          {actionMessage}
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Link
            to="/candidates"
            className="p-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100"
          >
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-xl font-bold text-gray-900">{candidate.full_name}</h1>
            <p className="text-sm text-gray-500">Карточка кандидата</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={copyCandidateData}
            className="p-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100"
            title="Копировать данные"
          >
            <Copy className="h-5 w-5" />
          </button>
          <button
            onClick={() => setEditing(!editing)}
            className="p-2 text-gray-600 hover:text-gray-800 rounded-lg hover:bg-gray-100"
            title={editing ? 'Отмена' : 'Редактировать'}
          >
            {editing ? <X className="h-5 w-5" /> : <Edit className="h-5 w-5" />}
          </button>
          {editing && (
            <button 
              onClick={handleSave} 
              className="btn btn-primary btn-sm"
            >
              <Save className="h-4 w-4 mr-1" />
              Сохранить
            </button>
          )}
        </div>
      </div>

      {/* Status Badge */}
      <div className="mb-6">
        <span className={`status-badge ${getStatusColor(candidate.status)} text-sm px-3 py-2 rounded-full inline-flex items-center`}>
          {getStatusEmoji(candidate.status)} {candidate.status}
        </span>
      </div>

      {/* Mobile Tabs */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          onClick={() => setActiveTab('info')}
          className={`flex-1 py-3 px-4 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'info'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Информация
        </button>
        <button
          onClick={() => setActiveTab('results')}
          className={`flex-1 py-3 px-4 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'results'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Результаты
        </button>
        <button
          onClick={() => setActiveTab('comments')}
          className={`flex-1 py-3 px-4 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'comments'
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Комментарии ({comments.length})
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'info' && (
        <div className="space-y-4">
          <div className="mobile-card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Основная информация</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  ФИО
                </label>
                <input
                  type="text"
                  value={editing ? editData.full_name || '' : candidate.full_name}
                  disabled={!editing}
                  onChange={e => handleEditChange('full_name', e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Статус
                </label>
                <select
                  value={editing ? editData.status || '' : candidate.status}
                  disabled={!editing}
                  onChange={e => handleEditChange('status', e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                >
                  <option value="ожидает">Ожидает</option>
                  <option value="берем">Берем</option>
                  <option value="не берем">Не берем</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Telegram
                </label>
                <input
                  type="text"
                  value={editing ? editData.telegram_username || '' : candidate.telegram_username || ''}
                  disabled={!editing}
                  onChange={e => handleEditChange('telegram_username', e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-50"
                  placeholder="@username"
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'results' && (
        <div className="mobile-card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Отчёт ÆON-интервью</h3>
          {candidate.results ? (
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                {candidate.results}
              </p>
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="text-gray-400 text-4xl mb-2">📝</div>
              <p className="text-gray-500">Результаты тестирования отсутствуют</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'comments' && (
        <div className="space-y-4">
          {/* Add Comment */}
          <div className="mobile-card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Добавить комментарий</h3>
            <div className="space-y-3">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Введите комментарий..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={4}
              />
              <button
                onClick={handleAddComment}
                disabled={!newComment.trim()}
                className="btn btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <MessageSquare className="h-4 w-4 mr-2" />
                Добавить комментарий
              </button>
            </div>
          </div>

          {/* Comments List */}
          <div className="space-y-3">
            {comments.map((comment) => (
              <div key={comment.id} className="mobile-card">
                <p className="text-gray-700 mb-2">{comment.hr_comment}</p>
                <p className="text-xs text-gray-500">
                  {new Date(comment.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
            
            {comments.length === 0 && (
              <div className="text-center py-8">
                <div className="text-gray-400 text-4xl mb-2">💬</div>
                <p className="text-gray-500">Комментарии отсутствуют</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CandidateDetail; 