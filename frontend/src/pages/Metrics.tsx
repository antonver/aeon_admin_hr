import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Users, 
  UserCheck,
  UserX,
  Calendar,
  ChevronDown
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Pie } from 'react-chartjs-2';

// Регистрируем компоненты Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface MetricsData {
  total_candidates: number;
  passed_candidates: number;
  test_pass_rate: number;
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

type TimeScope = 'month' | 'year';

const Metrics: React.FC = () => {
  const [overview, setOverview] = useState<MetricsData | null>(null);
  const [statusDistribution, setStatusDistribution] = useState<StatusDistribution | null>(null);
  const [activityTimeline, setActivityTimeline] = useState<ActivityTimeline | null>(null);
  const [loading, setLoading] = useState(true);
  
  // Состояние для управления периодом
  const [timeScope, setTimeScope] = useState<TimeScope>('month');
  const [selectedPeriod, setSelectedPeriod] = useState<string>('');
  const [showPeriodSelector, setShowPeriodSelector] = useState(false);

  // Обработчик клика вне селектора периода
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Element;
      if (!target.closest('.period-selector')) {
        setShowPeriodSelector(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Генерируем список периодов для селектора
  const generatePeriodOptions = () => {
    const periods = [];
    const currentDate = new Date();
    
    if (timeScope === 'month') {
      // Генерируем месяцы за последние 12 месяцев
      for (let i = 0; i < 12; i++) {
        const date = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1);
        const value = date.toISOString().slice(0, 7); // YYYY-MM
        const label = date.toLocaleDateString('ru-RU', { 
          year: 'numeric', 
          month: 'long' 
        });
        periods.push({ value, label });
      }
    } else {
      // Генерируем годы за последние 5 лет
      for (let i = 0; i < 5; i++) {
        const year = currentDate.getFullYear() - i;
        const value = year.toString();
        const label = year.toString();
        periods.push({ value, label });
      }
    }
    
    return periods;
  };

  const periodOptions = generatePeriodOptions();

  // Получаем текущий период по умолчанию
  useEffect(() => {
    if (periodOptions.length > 0 && !selectedPeriod) {
      setSelectedPeriod(periodOptions[0].value);
    }
  }, [periodOptions, selectedPeriod]);

  // Функция для загрузки данных с учетом периода
  const fetchMetrics = async (period?: string, scope?: TimeScope) => {
    const currentPeriod = period || selectedPeriod;
    const currentScope = scope || timeScope;
    
    try {
      setLoading(true);
      
      // Формируем параметры для API
      const params = new URLSearchParams();
      if (currentPeriod) {
        params.append('period', currentPeriod);
        params.append('scope', currentScope);
      }



      const [
        overviewRes,
        statusRes,
        activityRes
      ] = await Promise.all([
        fetch(`/api/metrics/overview?${params}`),
        fetch(`/api/metrics/status-distribution?${params}`),
        fetch(`/api/metrics/activity-timeline?${params}`)
      ]);

      const overviewData = await overviewRes.json();
      const statusData = await statusRes.json();
      const activityData = await activityRes.json();

      setOverview(overviewData);
      setStatusDistribution(statusData);
      setActivityTimeline(activityData);
    } catch (error) {
      console.error('Ошибка загрузки метрик:', error);
    } finally {
      setLoading(false);
    }
  };

  // Загружаем данные при изменении периода
  useEffect(() => {
    if (selectedPeriod) {
      fetchMetrics(selectedPeriod, timeScope);
    } else {
      // Если период не выбран, загружаем все данные
      fetchMetrics();
    }
  }, [selectedPeriod, timeScope]);

  // Загружаем данные при монтировании компонента
  useEffect(() => {
    fetchMetrics();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ожидает': return '#fbbf24'; // yellow-400
              case 'берем': return '#10b981'; // green-500
        case 'не берем': return '#ef4444'; // red-500
      default: return '#6b7280'; // gray-500
    }
  };

  // Функция для фильтрации данных по выбранному периоду
  const getFilteredTimelineData = () => {
    if (!activityTimeline?.timeline) return null;

    let startDate: Date;
    let endDate: Date;

    if (timeScope === 'month') {
      const selectedDate = new Date(selectedPeriod + '-01');
      startDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), 1);
      endDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth() + 1, 0);
    } else {
      const selectedYear = parseInt(selectedPeriod);
      startDate = new Date(selectedYear, 0, 1);
      endDate = new Date(selectedYear, 11, 31);
    }

    return activityTimeline.timeline.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= startDate && itemDate <= endDate;
    });
  };

  // Подготовка данных для круговой диаграммы
  const pieChartData = statusDistribution?.distribution ? {
    labels: statusDistribution.distribution.map(item => item.status),
    datasets: [
      {
        data: statusDistribution.distribution.map(item => item.count),
        backgroundColor: statusDistribution.distribution.map(item => getStatusColor(item.status)),
        borderColor: statusDistribution.distribution.map(item => getStatusColor(item.status)),
        borderWidth: 2,
      },
    ],
  } : null;

  // Подготовка данных для линейной диаграммы
  const filteredData = getFilteredTimelineData();
  const lineChartData = filteredData ? {
    labels: filteredData.map(item => {
      const date = new Date(item.date);
      if (timeScope === 'month') {
        return date.toLocaleDateString('ru-RU', { day: 'numeric' });
      } else {
        return date.toLocaleDateString('ru-RU', { month: 'short' });
      }
    }),
    datasets: [
      {
        label: 'Кандидаты',
        data: filteredData.map(item => item.count),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  } : null;

  const pieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          usePointStyle: true,
          padding: 20,
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            const total = context.dataset.data.reduce((a: number, b: number) => a + b, 0);
            const percentage = ((context.parsed / total) * 100).toFixed(1);
            return `${context.label}: ${context.parsed} (${percentage}%)`;
          },
        },
      },
    },
  };

  const lineChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
    interaction: {
      mode: 'nearest' as const,
      axis: 'x' as const,
      intersect: false,
    },
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

      {/* Period Selector */}
      <div className="card">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">Выбор периода</h2>
          
          <div className="flex items-center space-x-3">
            {/* Селектор типа периода */}
            <div className="relative">
              <select
                value={timeScope}
                onChange={(e) => {
                  setTimeScope(e.target.value as TimeScope);
                  setSelectedPeriod(''); // Сбрасываем выбранный период при смене типа
                }}
                className="appearance-none bg-white border border-gray-300 rounded-lg px-3 py-2 pr-8 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="month">Месяц</option>
                <option value="year">Год</option>
              </select>
              <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
            </div>

            {/* Селектор конкретного периода */}
            <div className="relative period-selector">
              <button
                onClick={() => setShowPeriodSelector(!showPeriodSelector)}
                className="flex items-center space-x-2 bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <Calendar className="h-4 w-4 text-gray-500" />
                <span>
                  {periodOptions.find(opt => opt.value === selectedPeriod)?.label || 'Выберите период'}
                </span>
                <ChevronDown className="h-4 w-4 text-gray-400" />
              </button>

              {/* Выпадающий список периодов */}
              {showPeriodSelector && (
                <div className="absolute top-full left-0 mt-1 w-48 bg-white border border-gray-300 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto">
                  {periodOptions.map((option) => (
                    <button
                      key={option.value}
                      onClick={() => {
                        setSelectedPeriod(option.value);
                        setShowPeriodSelector(false);
                      }}
                      className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-100 ${
                        selectedPeriod === option.value ? 'bg-blue-50 text-blue-600' : 'text-gray-700'
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Users className="h-8 w-8 text-main" />
            </div>
            <div className="ml-4">
              <p className="text-add text-background-2">Всего кандидатов</p>
              <p className="text-subheaders text-background font-bold">
                {overview?.total_candidates || 0}
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
              <p className="text-add text-background-2">Прошедшие кандидаты</p>
              <p className="text-subheaders text-background font-bold">
                {overview?.passed_candidates || 0}
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
                {overview?.test_pass_rate || 0}%
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
                              <p className="text-add text-background-2">Не берем</p>
              <p className="text-subheaders text-background font-bold">
                {(overview?.total_candidates || 0) - (overview?.passed_candidates || 0)}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Status Distribution - Pie Chart */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Распределение по статусам</h2>
          {pieChartData ? (
            <div className="h-80">
              <Pie data={pieChartData} options={pieChartOptions} />
            </div>
          ) : (
            <div className="flex items-center justify-center h-80">
              <p className="text-gray-500">Нет данных для отображения</p>
            </div>
          )}
        </div>

        {/* Activity Timeline - Line Chart */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Активность по дням</h2>
          {lineChartData ? (
            <div className="h-80">
              <Line data={lineChartData} options={lineChartOptions} />
            </div>
          ) : (
            <div className="flex items-center justify-center h-80">
              <p className="text-gray-500">Нет данных для отображения</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Metrics; 