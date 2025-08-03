import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  Eye,
  Calendar
} from 'lucide-react';

interface Candidate {
  id: number;
  full_name: string;
  name?: string;  // Добавляем поле name
  telegram_username?: string;
  email?: string;
  status: string;  // Теперь "берем" и "не берем"
  last_action_date: string;
  last_action_type?: string;
}

const PAGE_SIZE = 10;

const CandidatesList: React.FC = () => {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

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
      
      const url = `/api/candidates/?${params}`;
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
      case 'берем': return 'status-passed';
      case 'не берем': return 'status-rejected';
      default: return 'status-waiting';
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
      {/* Filters */}
      <div className="card">
        <div className="flex flex-col md:flex-row items-center gap-4">
          <div className="flex-1 w-full">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-background-2 pointer-events-none" />
              <input
                type="text"
                placeholder="Поиск по ФИО..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10 w-full"
              />
            </div>
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input-field w-full md:w-48"
          >
            <option value="">Все кандидаты</option>
            <option value="берем">Берем</option>
            <option value="не берем">Не берем</option>
          </select>
          <button
            onClick={fetchCandidates}
            className="btn btn-secondary w-full md:w-auto"
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
                <th>Дата прохождения</th>
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
                    <div className="flex items-center gap-2 text-time text-background-2">
                      <Calendar className="w-4 h-4" />
                      {new Date(candidate.last_action_date).toLocaleDateString()}
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
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {/* Пагинация - улучшенная для мобильных устройств */}
        {totalPages > 1 && (
          <div className="flex flex-col sm:flex-row justify-center items-center gap-2 mt-6 pb-4">
            <div className="flex items-center gap-2 mb-2 sm:mb-0">
              <button
                className="btn btn-outline px-3 py-2 text-sm"
                onClick={() => setPage(page - 1)}
                disabled={page === 1}
              >
                Назад
              </button>
              <span className="text-sm text-background-2 px-2">
                {page} из {totalPages}
              </span>
              <button
                className="btn btn-outline px-3 py-2 text-sm"
                onClick={() => setPage(page + 1)}
                disabled={page === totalPages}
              >
                Вперёд
              </button>
            </div>
            
            {/* Номера страниц - только для десктопа */}
            <div className="hidden md:flex items-center gap-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                let pageNum;
                if (totalPages <= 5) {
                  pageNum = i + 1;
                } else if (page <= 3) {
                  pageNum = i + 1;
                } else if (page >= totalPages - 2) {
                  pageNum = totalPages - 4 + i;
                } else {
                  pageNum = page - 2 + i;
                }
                
                return (
                  <button
                    key={pageNum}
                    className={`btn px-3 py-2 text-sm ${pageNum === page ? 'btn-primary' : 'btn-outline'}`}
                    onClick={() => setPage(pageNum)}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CandidatesList; 