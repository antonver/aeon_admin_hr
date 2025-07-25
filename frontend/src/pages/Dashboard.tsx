import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Users, 
  UserCheck, 
  UserX, 
  TrendingUp,
  Plus,
  Search
} from 'lucide-react';

interface Metrics {
  total_candidates: number;
  active_candidates: number;
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
    fetch('/api/candidates?limit=5')
      .then(res => res.json())
      .then(data => setRecentCandidates(data))
      .catch(err => console.error('Ошибка загрузки кандидатов:', err))
      .finally(() => setLoading(false));
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ожидает': return 'status-waiting';
      case 'прошёл': return 'status-passed';
      case 'приглашён': return 'status-invited';
      case 'отклонён': return 'status-rejected';
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-headers text-background mb-2">Дашборд</h1>
          <p className="text-main text-background-2">Обзор HR-процессов и кандидатов</p>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Users className="h-8 w-8 text-main" />
            </div>
            <div className="ml-4">
              <p className="text-add text-background-2">Всего кандидатов</p>
              <p className="text-subheaders text-background font-bold">
                {metrics?.total_candidates || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <UserCheck className="h-8 w-8 text-accept" />
            </div>
            <div className="ml-4">
              <p className="text-add text-background-2">Активные кандидаты</p>
              <p className="text-subheaders text-background font-bold">
                {metrics?.active_candidates || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-accent" />
            </div>
            <div className="ml-4">
              <p className="text-add text-background-2">Процент прохождения</p>
              <p className="text-subheaders text-background font-bold">
                {metrics?.test_pass_rate || 0}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <UserX className="h-8 w-8 text-error" />
            </div>
            <div className="ml-4">
              <p className="text-add text-background-2">Отклонённые</p>
              <p className="text-subheaders text-background font-bold">
                {recentCandidates.filter(c => c.status === 'отклонён').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Candidates */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-subheaders text-background font-bold">Последние кандидаты</h2>
          <Link
            to="/candidates"
            className="text-main hover:text-secondary text-main font-medium"
          >
            Посмотреть всех
          </Link>
        </div>

        <div className="space-y-4">
          {recentCandidates.map((candidate) => (
            <div
              key={candidate.id}
              className="flex items-center justify-between p-4 bg-background-2 rounded-lg"
            >
              <div className="flex items-center space-x-4">
                <div className="h-10 w-10 bg-main rounded-full flex items-center justify-center">
                  <span className="text-white font-medium">
                    {candidate.full_name.charAt(0)}
                  </span>
                </div>
                <div>
                  <p className="text-main text-background font-medium">{candidate.full_name}</p>
                  <p className="text-add text-background-2">
                    {candidate.last_action_type} • {new Date(candidate.last_action_date).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <span className={`status-badge ${getStatusColor(candidate.status)}`}>
                  {candidate.status}
                </span>
                <Link
                  to={`/candidate/${candidate.id}`}
                  className="text-main hover:text-secondary text-main font-medium"
                >
                  Открыть
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 