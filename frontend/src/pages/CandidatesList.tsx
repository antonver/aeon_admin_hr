import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  Plus,
  MessageSquare,
  Send,
  Copy,
  Eye,
  Calendar,
  User,
  X
} from 'lucide-react';

interface Candidate {
  id: number;
  full_name: string;
  telegram_username?: string;
  email?: string;
  status: string;
  last_action_date: string;
  last_action_type?: string;
}

interface NewCandidate {
  full_name: string;
  telegram_username: string;
  email: string;
  phone?: string;
}

const PAGE_SIZE = 10;

const CandidatesList: React.FC = () => {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [newCandidate, setNewCandidate] = useState<NewCandidate>({
    full_name: '',
    telegram_username: '',
    email: '',
    phone: ''
  });
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [showTelegramModal, setShowTelegramModal] = useState(false);
  const [telegramMessage, setTelegramMessage] = useState('');
  const [telegramCandidateId, setTelegramCandidateId] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchCandidates();
    // eslint-disable-next-line
  }, [page, searchTerm, statusFilter]);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Загружаем кандидатов...');
      
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (statusFilter) params.append('status', statusFilter);
      params.append('skip', String((page - 1) * PAGE_SIZE));
      params.append('limit', String(PAGE_SIZE));
      
      const url = `/api/candidates?${params}`;
      console.log('URL запроса:', url);
      
      const response = await fetch(url);
      console.log('Статус ответа:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Полученные данные:', data);
      setCandidates(data);
      // Получаем общее количество кандидатов (отдельным запросом)
      const countParams = new URLSearchParams();
      if (searchTerm && searchTerm.trim()) countParams.append('search', searchTerm);
      if (statusFilter && statusFilter.trim()) countParams.append('status', statusFilter);
      const countUrl = `/api/candidates/count${countParams.toString() ? '?' + countParams.toString() : ''}`;
      console.log('Count URL:', countUrl);
      const countRes = await fetch(countUrl);
      if (countRes.ok) {
        const countData = await countRes.json();
        setTotal(countData.total);
      }
    } catch (error) {
      console.error('Ошибка загрузки кандидатов:', error);
      setError(error instanceof Error ? error.message : 'Неизвестная ошибка');
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

  const handleQuickAction = async (candidateId: number, action: string, data?: any) => {
    try {
      let message = '';
      
      if (action === 'copy_data') {
        const candidate = candidates.find(c => c.id === candidateId);
        if (candidate) {
          const dataToCopy = `Имя: ${candidate.full_name}\nTelegram: ${candidate.telegram_username || 'Не указан'}\nEmail: ${candidate.email || 'Не указан'}`;
          await navigator.clipboard.writeText(dataToCopy);
          message = 'Данные скопированы в буфер обмена';
        }
      } else {
        let body: any = {
          action_type: action,
          candidate_id: candidateId,
        };
        if (action === 'telegram_message' && data?.message) {
          body.data = { message: data.message };
        }
        const response = await fetch(`/api/candidates/${candidateId}/quick-action`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        });
        
        if (response.ok) {
          const result = await response.json();
          message = result.message || `Действие ${action} выполнено`;
          // Обновить список кандидатов
          fetchCandidates();
        } else {
          throw new Error('Ошибка выполнения действия');
        }
      }
      
      setActionMessage(message);
      setTimeout(() => setActionMessage(null), 3000);
    } catch (error) {
      console.error('Ошибка выполнения действия:', error);
      setActionMessage('Ошибка выполнения действия');
      setTimeout(() => setActionMessage(null), 3000);
    }
  };

  const handleAddCandidate = async () => {
    try {
      const response = await fetch('/api/candidates', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newCandidate),
      });
      
      if (response.ok) {
        setShowAddModal(false);
        setNewCandidate({ full_name: '', telegram_username: '', email: '', phone: '' });
        fetchCandidates();
        setActionMessage('Кандидат успешно добавлен');
        setTimeout(() => setActionMessage(null), 3000);
      } else {
        throw new Error('Ошибка добавления кандидата');
      }
    } catch (error) {
      console.error('Ошибка добавления кандидата:', error);
      setActionMessage('Ошибка добавления кандидата');
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

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="text-error text-headers font-bold mb-4">Ошибка загрузки данных</div>
          <div className="text-main text-background-2 mb-6">{error}</div>
          <button 
            onClick={fetchCandidates}
            className="btn btn-primary"
          >
            Попробовать снова
          </button>
        </div>
      </div>
    );
  }

  // Пагинация
  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div className="space-y-6">
      {/* Action Message */}
      {actionMessage && (
        <div className="fixed top-4 right-4 bg-main text-white px-6 py-3 rounded-lg shadow-lg z-50">
          {actionMessage}
        </div>
      )}
      {/* Модальное окно Telegram */}
      {showTelegramModal && telegramCandidateId && (
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
                  await handleQuickAction(telegramCandidateId, 'telegram_message', { message: telegramMessage });
                  setShowTelegramModal(false);
                  setTelegramMessage('');
                  setTelegramCandidateId(null);
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
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-headers text-background mb-2">Кандидаты</h1>
          <p className="text-main text-background-2">
            Управление кандидатами и их статусами
          </p>
        </div>
        <button 
          onClick={() => setShowAddModal(true)}
          className="btn btn-primary"
        >
          <Plus className="w-5 h-5" />
          <span>Добавить кандидата</span>
        </button>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-background-2" />
              <input
                type="text"
                placeholder="Поиск по ФИО..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-12"
              />
            </div>
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input-field w-48"
          >
            <option value="">Все статусы</option>
            <option value="ожидает">Ожидает</option>
            <option value="прошёл">Прошёл</option>
            <option value="приглашён">Приглашён</option>
            <option value="отклонён">Отклонён</option>
          </select>
          <button
            onClick={fetchCandidates}
            className="btn btn-secondary"
          >
            <Filter className="w-5 h-5" />
            <span>Применить</span>
          </button>
        </div>
      </div>

      {/* Candidates List */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr>
                <th>Кандидат</th>
                <th>Контакты</th>
                <th>Статус</th>
                <th>Последнее действие</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {candidates.map((candidate) => (
                <tr key={candidate.id}>
                  <td>
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-main rounded-full flex items-center justify-center">
                        <span className="text-white font-bold text-main">
                          {candidate.full_name.charAt(0)}
                        </span>
                      </div>
                      <div>
                        <div className="text-main text-background font-medium">
                          {candidate.full_name}
                        </div>
                        <div className="text-add text-background-2">
                          ID: {candidate.id}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div className="space-y-1">
                      {candidate.telegram_username && (
                        <div className="text-main text-background">
                          {candidate.telegram_username}
                        </div>
                      )}
                      {candidate.email && (
                        <div className="text-add text-background-2">
                          {candidate.email}
                        </div>
                      )}
                    </div>
                  </td>
                  <td>
                    <span className={`status-badge ${getStatusColor(candidate.status)}`}>
                      {candidate.status}
                    </span>
                  </td>
                  <td>
                    <div className="space-y-1">
                      <div className="text-add text-background-2">
                        {candidate.last_action_type || 'Нет действий'}
                      </div>
                      <div className="flex items-center gap-2 text-time text-background-2">
                        <Calendar className="w-4 h-4" />
                        {new Date(candidate.last_action_date).toLocaleDateString()}
                      </div>
                    </div>
                  </td>
                  <td>
                    <div className="flex items-center gap-2">
                      <Link
                        to={`/candidate/${candidate.id}`}
                        className="p-2 text-background-2 hover:text-background transition-colors"
                        title="Открыть карточку"
                      >
                        <Eye className="w-5 h-5" />
                      </Link>
                      {candidate.telegram_username && (
                        <button
                          onClick={() => {
                            setTelegramCandidateId(candidate.id);
                            setShowTelegramModal(true);
                          }}
                          className="p-2 text-background-2 hover:text-accent transition-colors"
                          title="Написать в Telegram"
                        >
                          <MessageSquare className="w-5 h-5" />
                        </button>
                      )}
                      <button
                        onClick={() => handleQuickAction(candidate.id, 'invite_test')}
                        className="p-2 text-background-2 hover:text-accept transition-colors"
                        title="Пригласить на тест"
                      >
                        <Send className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => handleQuickAction(candidate.id, 'copy_data')}
                        className="p-2 text-background-2 hover:text-secondary transition-colors"
                        title="Скопировать данные"
                      >
                        <Copy className="w-5 h-5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {/* Пагинация */}
        {totalPages > 1 && (
          <div className="flex justify-center items-center gap-2 mt-4">
            <button
              className="btn btn-outline"
              onClick={() => setPage(page - 1)}
              disabled={page === 1}
            >
              Назад
            </button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
              <button
                key={p}
                className={`btn ${p === page ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setPage(p)}
              >
                {p}
              </button>
            ))}
            <button
              className="btn btn-outline"
              onClick={() => setPage(page + 1)}
              disabled={page === totalPages}
            >
              Вперёд
            </button>
          </div>
        )}
      </div>

      {/* Add Candidate Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-subheaders text-background font-bold">Добавить кандидата</h2>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-background-2 hover:text-background"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-main text-background mb-2">ФИО *</label>
                <input
                  type="text"
                  value={newCandidate.full_name}
                  onChange={(e) => setNewCandidate({...newCandidate, full_name: e.target.value})}
                  className="input-field"
                  placeholder="Введите ФИО"
                />
              </div>
              
              <div>
                <label className="block text-main text-background mb-2">Telegram</label>
                <input
                  type="text"
                  value={newCandidate.telegram_username}
                  onChange={(e) => setNewCandidate({...newCandidate, telegram_username: e.target.value})}
                  className="input-field"
                  placeholder="@username"
                />
              </div>
              
              <div>
                <label className="block text-main text-background mb-2">Email</label>
                <input
                  type="email"
                  value={newCandidate.email}
                  onChange={(e) => setNewCandidate({...newCandidate, email: e.target.value})}
                  className="input-field"
                  placeholder="email@example.com"
                />
              </div>
              
              <div>
                <label className="block text-main text-background mb-2">Телефон</label>
                <input
                  type="tel"
                  value={newCandidate.phone}
                  onChange={(e) => setNewCandidate({...newCandidate, phone: e.target.value})}
                  className="input-field"
                  placeholder="+7 (999) 123-45-67"
                />
              </div>
            </div>
            
            <div className="flex gap-3 mt-6">
              <button
                onClick={handleAddCandidate}
                disabled={!newCandidate.full_name}
                className="btn btn-primary flex-1"
              >
                Добавить
              </button>
              <button
                onClick={() => setShowAddModal(false)}
                className="btn btn-outline flex-1"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CandidatesList; 