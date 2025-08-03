import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  Eye,
  Calendar,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

interface Candidate {
  id: number;
  full_name: string;
  name?: string;
  telegram_username?: string;
  email?: string;
  status: string;
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
  const [showFilters, setShowFilters] = useState(false);

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
      
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (statusFilter) params.append('status', statusFilter);
      params.append('skip', String((page - 1) * PAGE_SIZE));
      params.append('limit', String(PAGE_SIZE));
      
      const url = `/api/candidates/?${params}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setCandidates(data);
      
      // Получаем общее количество кандидатов
      const countParams = new URLSearchParams();
      if (searchTerm && searchTerm.trim()) countParams.append('search', searchTerm);
      if (statusFilter && statusFilter.trim()) countParams.append('status', statusFilter);
      const countUrl = `/api/candidates/count${countParams.toString() ? '?' + countParams.toString() : ''}`;
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

  const getStatusEmoji = (status: string) => {
    switch (status) {
      case 'берем': return '✅';
      case 'не берем': return '❌';
      default: return '⏳';
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

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div className="space-y-4 mobile-padding">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-bold text-gray-900">Кандидаты</h1>
        <div className="text-sm text-gray-500">
          {total} кандидатов
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
        <input
          type="text"
          placeholder="Поиск по ФИО..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      {/* Filters Toggle */}
      <div className="mb-4">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="w-full flex items-center justify-between p-3 bg-gray-50 rounded-lg border"
        >
          <span className="font-medium">Фильтры</span>
          <Filter className="w-5 h-5" />
        </button>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Статус
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Все кандидаты</option>
              <option value="берем">Берем</option>
              <option value="не берем">Не берем</option>
            </select>
          </div>
          <button
            onClick={() => setShowFilters(false)}
            className="w-full btn btn-primary"
          >
            Применить фильтры
          </button>
        </div>
      )}

      {/* Candidates List - Mobile Cards */}
      <div className="space-y-3">
        {candidates.map((candidate) => (
          <div key={candidate.id} className="mobile-card">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white font-bold text-lg">
                    {candidate.full_name.charAt(0)}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900 truncate">
                    {candidate.full_name}
                  </h3>
                  <p className="text-sm text-gray-500">
                    ID: {candidate.id}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`status-badge ${getStatusColor(candidate.status)} text-sm px-2 py-1 rounded-full`}>
                  {getStatusEmoji(candidate.status)} {candidate.status}
                </span>
              </div>
            </div>

            <div className="space-y-2 mb-3">
              {candidate.telegram_username && (
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium mr-2">Telegram:</span>
                  <span className="truncate">{candidate.telegram_username}</span>
                </div>
              )}
              {candidate.email && (
                <div className="flex items-center text-sm text-gray-600">
                  <span className="font-medium mr-2">Email:</span>
                  <span className="truncate">{candidate.email}</span>
                </div>
              )}
              <div className="flex items-center text-sm text-gray-600">
                <Calendar className="w-4 h-4 mr-2" />
                <span>{new Date(candidate.last_action_date).toLocaleDateString()}</span>
              </div>
            </div>

            <div className="flex justify-end">
              <Link
                to={`/candidate/${candidate.id}`}
                className="btn btn-primary btn-sm flex items-center space-x-2"
              >
                <Eye className="w-4 h-4" />
                <span>Открыть</span>
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {candidates.length === 0 && !loading && (
        <div className="text-center py-12">
          <div className="text-gray-400 text-6xl mb-4">👥</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Кандидаты не найдены</h3>
          <p className="text-gray-500">
            {searchTerm || statusFilter ? 'Попробуйте изменить фильтры' : 'Добавьте первого кандидата'}
          </p>
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mobile-pagination">
          <button
            className="btn btn-outline touch-target"
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600 px-3">
              {page} из {totalPages}
            </span>
          </div>
          
          <button
            className="btn btn-outline touch-target"
            onClick={() => setPage(page + 1)}
            disabled={page === totalPages}
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
};

export default CandidatesList; 