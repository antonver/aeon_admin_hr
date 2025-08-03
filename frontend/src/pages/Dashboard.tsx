import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Users, 
  UserCheck, 
  UserX, 
  TrendingUp,
  Eye
} from 'lucide-react';

interface Metrics {
  total_candidates: number;
  passed_candidates: number;
  test_pass_rate: number;
}

interface Candidate {
  id: number;
  full_name: string;
  status: string;
  last_action_date: string;
  last_action_type: string;
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [recentCandidates, setRecentCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Загрузка метрик
    fetch('/api/metrics/overview')
      .then(res => res.json())
      .then(data => setMetrics(data))
      .catch(err => console.error('Ошибка загрузки метрик:', err));

    // Загрузка последних кандидатов
    fetch('/api/candidates/?limit=5')
      .then(res => res.json())
      .then(data => setRecentCandidates(data))
      .catch(err => console.error('Ошибка загрузки кандидатов:', err))
      .finally(() => setLoading(false));
  }, []);

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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="mobile-padding space-y-6" style={{ paddingBottom: '100px' }}>
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">HR Админ Панель</h1>
        <p className="text-gray-600 text-base">Управление кандидатами и процессами</p>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-2 gap-4 mb-8">
        <div className="mobile-card text-center">
          <div className="flex flex-col items-center">
            <div className="w-14 h-14 bg-blue-500 rounded-full flex items-center justify-center mb-4">
              <Users className="h-7 w-7 text-white" />
            </div>
            <p className="text-sm text-gray-600 mb-2">Всего</p>
            <p className="text-2xl font-bold text-gray-900">
              {metrics?.total_candidates || 0}
            </p>
          </div>
        </div>

        <div className="mobile-card text-center">
          <div className="flex flex-col items-center">
            <div className="w-14 h-14 bg-green-500 rounded-full flex items-center justify-center mb-4">
              <UserCheck className="h-7 w-7 text-white" />
            </div>
            <p className="text-sm text-gray-600 mb-2">Берем</p>
            <p className="text-2xl font-bold text-gray-900">
              {metrics?.passed_candidates || 0}
            </p>
          </div>
        </div>

        <div className="mobile-card text-center">
          <div className="flex flex-col items-center">
            <div className="w-14 h-14 bg-red-500 rounded-full flex items-center justify-center mb-4">
              <UserX className="h-7 w-7 text-white" />
            </div>
            <p className="text-sm text-gray-600 mb-2">Не берем</p>
            <p className="text-2xl font-bold text-gray-900">
              {(metrics?.total_candidates || 0) - (metrics?.passed_candidates || 0)}
            </p>
          </div>
        </div>

        <div className="mobile-card text-center">
          <div className="flex flex-col items-center">
            <div className="w-14 h-14 bg-purple-500 rounded-full flex items-center justify-center mb-4">
              <TrendingUp className="h-7 w-7 text-white" />
            </div>
            <p className="text-sm text-gray-600 mb-2">Процент</p>
            <p className="text-2xl font-bold text-gray-900">
              {metrics?.test_pass_rate || 0}%
            </p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mobile-card mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-6">Быстрые действия</h2>
        <div className="grid grid-cols-2 gap-4">
          <Link
            to="/candidates"
            className="flex flex-col items-center p-5 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors"
            style={{ minHeight: '80px' }}
          >
            <Users className="h-8 w-8 text-blue-600 mb-3" />
            <span className="text-sm font-medium text-blue-900">Кандидаты</span>
          </Link>
          <Link
            to="/metrics"
            className="flex flex-col items-center p-5 bg-purple-50 rounded-xl hover:bg-purple-100 transition-colors"
            style={{ minHeight: '80px' }}
          >
            <TrendingUp className="h-8 w-8 text-purple-600 mb-3" />
            <span className="text-sm font-medium text-purple-900">Метрики</span>
          </Link>
        </div>
      </div>

      {/* Recent Candidates */}
      <div className="mobile-card mb-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-900">Последние кандидаты</h2>
          <Link
            to="/candidates"
            className="text-blue-600 hover:text-blue-800 text-sm font-medium px-3 py-2 rounded-lg hover:bg-blue-50 transition-colors"
          >
            Все
          </Link>
        </div>

        <div className="space-y-4">
          {recentCandidates.map((candidate) => (
            <div
              key={candidate.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-xl"
            >
              <div className="flex items-center space-x-4 flex-1 min-w-0">
                <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white font-medium text-sm">
                    {candidate.full_name.charAt(0)}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-gray-900 truncate text-base">
                    {candidate.full_name}
                  </p>
                  <p className="text-sm text-gray-500 truncate">
                    {new Date(candidate.last_action_date).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <span className={`status-badge ${getStatusColor(candidate.status)} text-xs px-2 py-1 rounded-full`}>
                  {getStatusEmoji(candidate.status)}
                </span>
                <Link
                  to={`/candidate/${candidate.id}`}
                  className="p-3 text-gray-600 hover:text-gray-800 rounded-xl hover:bg-gray-100 transition-colors"
                  style={{ minWidth: '44px', minHeight: '44px' }}
                >
                  <Eye className="w-5 h-5" />
                </Link>
              </div>
            </div>
          ))}
          
          {recentCandidates.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-400 text-5xl mb-4">👥</div>
              <p className="text-gray-500 text-base">Кандидаты отсутствуют</p>
            </div>
          )}
        </div>
      </div>

      {/* Stats Summary */}
      <div className="mobile-card" style={{ marginBottom: '40px' }}>
        <h2 className="text-lg font-semibold text-gray-900 mb-6">Статистика</h2>
        <div className="space-y-4">
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <span className="text-gray-600">Всего кандидатов:</span>
            <span className="font-semibold text-gray-900">{metrics?.total_candidates || 0}</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <span className="text-gray-600">Процент прохождения:</span>
            <span className="font-semibold text-green-600">{metrics?.test_pass_rate || 0}%</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
            <span className="text-gray-600">Последние 7 дней:</span>
            <span className="font-semibold text-blue-600">{recentCandidates.length} новых</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 