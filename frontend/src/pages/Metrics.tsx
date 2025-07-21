import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  UserCheck,
  AlertTriangle
} from 'lucide-react';

interface Metrics {
  total_candidates: number;
  active_candidates: number;
  test_pass_rate: number;
  weak_questions: string[];
}

interface StatusDistribution {
  distribution: Array<{
    status: string;
    count: number;
  }>;
}

interface ActivityTimeline {
  timeline: Array<{
    date: string;
    count: number;
  }>;
}

interface CategoryStats {
  category_stats: Array<{
    category: string;
    avg_score: number;
    count: number;
  }>;
}

interface TopCandidate {
  full_name: string;
  avg_score: number;
  questions_count: number;
}

const Metrics: React.FC = () => {
  const [overview, setOverview] = useState<Metrics | null>(null);
  const [statusDistribution, setStatusDistribution] = useState<StatusDistribution | null>(null);
  const [activityTimeline, setActivityTimeline] = useState<ActivityTimeline | null>(null);
  const [categoryStats, setCategoryStats] = useState<CategoryStats | null>(null);
  const [topCandidates, setTopCandidates] = useState<TopCandidate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const [
        overviewRes,
        statusRes,
        activityRes,
        categoryRes,
        topRes
      ] = await Promise.all([
        fetch('/api/metrics/overview'),
        fetch('/api/metrics/status-distribution'),
        fetch('/api/metrics/activity-timeline'),
        fetch('/api/metrics/interview-stats'),
        fetch('/api/metrics/top-candidates')
      ]);

      const overviewData = await overviewRes.json();
      const statusData = await statusRes.json();
      const activityData = await activityRes.json();
      const categoryData = await categoryRes.json();
      const topData = await topRes.json();

      setOverview(overviewData);
      setStatusDistribution(statusData);
      setActivityTimeline(activityData);
      setCategoryStats(categoryData);
      setTopCandidates(topData.top_candidates || []);
    } catch (error) {
      console.error('Ошибка загрузки метрик:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ожидает': return 'bg-yellow-500';
      case 'прошёл': return 'bg-green-500';
      case 'приглашён': return 'bg-blue-500';
      case 'отклонён': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Метрики и аналитика</h1>
        <p className="text-gray-600">Анализ HR-процессов и эффективности</p>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Users className="h-8 w-8 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Всего кандидатов</p>
              <p className="text-2xl font-bold text-gray-900">
                {overview?.total_candidates || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <UserCheck className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Активные кандидаты</p>
              <p className="text-2xl font-bold text-gray-900">
                {overview?.active_candidates || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Процент прохождения</p>
              <p className="text-2xl font-bold text-gray-900">
                {overview?.test_pass_rate || 0}%
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-8 w-8 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Слабых вопросов</p>
              <p className="text-2xl font-bold text-gray-900">
                {overview?.weak_questions?.length || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Status Distribution */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Распределение по статусам</h2>
          {statusDistribution?.distribution && (
            <div className="space-y-4">
              {statusDistribution.distribution.map((item) => (
                <div key={item.status} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`h-3 w-3 rounded-full ${getStatusColor(item.status)}`}></div>
                    <span className="text-sm font-medium text-gray-700">
                      {item.status}
                    </span>
                  </div>
                  <span className="text-sm font-bold text-gray-900">
                    {item.count}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Category Statistics */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Статистика по категориям</h2>
          {categoryStats?.category_stats && (
            <div className="space-y-4">
              {categoryStats.category_stats.map((stat) => (
                <div key={stat.category} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">
                    {stat.category}
                  </span>
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-500">
                      {stat.count} вопросов
                    </span>
                    <span className="text-sm font-bold text-gray-900">
                      {stat.avg_score}/10
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Top Candidates */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Топ кандидатов</h2>
        {topCandidates.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Кандидат
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Средний балл
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Количество вопросов
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {topCandidates.map((candidate, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                          <span className="text-primary-700 font-medium">
                            {candidate.full_name.charAt(0)}
                          </span>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {candidate.full_name}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-bold text-gray-900">
                        {candidate.avg_score}/10
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {candidate.questions_count}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500">Нет данных о кандидатах</p>
        )}
      </div>

      {/* Weak Questions */}
      {overview?.weak_questions && overview.weak_questions.length > 0 && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Слабые вопросы</h2>
          <div className="space-y-3">
            {overview.weak_questions.map((question, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg">
                <div className="h-2 w-2 bg-red-500 rounded-full"></div>
                <p className="text-sm text-gray-700">{question}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Activity Timeline */}
      {activityTimeline?.timeline && activityTimeline.timeline.length > 0 && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Активность по дням</h2>
          <div className="space-y-3">
            {activityTimeline.timeline.slice(-7).map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {new Date(item.date).toLocaleDateString()}
                </span>
                <div className="flex items-center space-x-2">
                  <div className="h-2 bg-primary-600 rounded" style={{ width: `${Math.min(item.count * 10, 100)}px` }}></div>
                  <span className="text-sm font-medium text-gray-900">
                    {item.count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Metrics; 