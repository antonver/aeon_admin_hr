import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Users, 
  BarChart3, 
  Home, 
  Bell,
  Settings,
  User
} from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  // --- СТЕЙТ ДЛЯ ЛОГИНА ---
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [loginError, setLoginError] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  // --- СТЕЙТ ДЛЯ МОДАЛКИ НАСТРОЕК ---
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [profileData, setProfileData] = useState({
    name: '',
    email: '',
    currentPassword: '',
    newPassword: '',
  });
  const [profileMessage, setProfileMessage] = useState<string | null>(null);
  const [profileLoading, setProfileLoading] = useState(false);

  // --- СТЕЙТ ДЛЯ УВЕДОМЛЕНИЙ ---
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState<any[]>([]);
  const [notificationsLoading, setNotificationsLoading] = useState(false);

  // --- Проверка токена при загрузке ---
  useEffect(() => {
    const savedToken = localStorage.getItem('access_token');
    if (savedToken) {
      setToken(savedToken);
      fetchProfile(savedToken);
    } else {
      setShowLoginModal(true);
    }
  }, []);

  // --- Получить профиль пользователя ---
  const fetchProfile = async (jwtToken: string) => {
    try {
      const res = await fetch('/api/user/profile', {
        headers: { Authorization: `Bearer ${jwtToken}` },
      });
      if (res.ok) {
        const data = await res.json();
        setProfileData({
          name: data.name,
          email: data.email,
          currentPassword: '',
          newPassword: '',
        });
      } else {
        setShowLoginModal(true);
      }
    } catch {
      setShowLoginModal(true);
    }
  };

  // --- Логин ---
  const handleLogin = async () => {
    setLoginError(null);
    try {
      const res = await fetch('/api/user/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      });
      if (res.ok) {
        const data = await res.json();
        setToken(data.access_token);
        localStorage.setItem('access_token', data.access_token);
        setShowLoginModal(false);
        fetchProfile(data.access_token);
      } else {
        setLoginError('Неверный email или пароль');
      }
    } catch {
      setLoginError('Ошибка авторизации');
    }
  };

  // --- Выход ---
  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('access_token');
    setShowLoginModal(true);
    setProfileData({ name: '', email: '', currentPassword: '', newPassword: '' });
  };

  // --- Сохранение профиля ---
  const handleProfileChange = (field: string, value: string) => {
    setProfileData(prev => ({ ...prev, [field]: value }));
  };

  const handleProfileSave = async () => {
    setProfileLoading(true);
    try {
      const res = await fetch('/api/user/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: profileData.name,
          email: profileData.email,
          current_password: profileData.currentPassword,
          new_password: profileData.newPassword,
        }),
      });
      if (res.ok) {
        setProfileMessage('Профиль успешно обновлён');
        setTimeout(() => setProfileMessage(null), 3000);
        setShowProfileModal(false);
        fetchProfile(token!);
      } else {
        setProfileMessage('Ошибка обновления профиля');
        setTimeout(() => setProfileMessage(null), 3000);
      }
    } catch {
      setProfileMessage('Ошибка обновления профиля');
      setTimeout(() => setProfileMessage(null), 3000);
    } finally {
      setProfileLoading(false);
    }
  };

  // Загрузка уведомлений
  const fetchNotifications = async () => {
    if (!token) return;
    setNotificationsLoading(true);
    try {
      const res = await fetch('/api/notifications', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setNotifications(data);
      }
    } finally {
      setNotificationsLoading(false);
    }
  };

  // Открытие окна уведомлений
  const handleOpenNotifications = () => {
    setShowNotifications(true);
    fetchNotifications();
  };

  const navigation = [
    { name: 'Дашборд', href: '/', icon: Home },
    { name: 'Кандидаты', href: '/candidates', icon: Users },
    { name: 'Метрики', href: '/metrics', icon: BarChart3 },
  ];

  return (
    <div className="flex h-screen bg-background">
      {/* Модальное окно логина */}
      {showLoginModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-subheaders text-background font-bold mb-4">Вход</h2>
            <div className="space-y-4">
              <input
                type="email"
                className="input-field"
                placeholder="Email"
                value={loginData.email}
                onChange={e => setLoginData({ ...loginData, email: e.target.value })}
              />
              <input
                type="password"
                className="input-field"
                placeholder="Пароль"
                value={loginData.password}
                onChange={e => setLoginData({ ...loginData, password: e.target.value })}
              />
              {loginError && <div className="text-error text-center">{loginError}</div>}
              <button className="btn btn-primary w-full" onClick={handleLogin}>
                Войти
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Модальное окно уведомлений */}
      {showNotifications && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-lg max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-subheaders text-background font-bold">Уведомления</h2>
              <button
                onClick={() => setShowNotifications(false)}
                className="text-background-2 hover:text-background"
              >
                <span style={{fontSize: 24, fontWeight: 700}}>×</span>
              </button>
            </div>
            {notificationsLoading ? (
              <div className="text-center text-main">Загрузка...</div>
            ) : notifications.length === 0 ? (
              <div className="text-center text-main">Нет уведомлений</div>
            ) : (
              <div className="space-y-4">
                {notifications.map((n) => (
                  <div key={n.id} className="p-4 rounded-lg bg-background-2">
                    <div className="text-main font-medium mb-1">{n.type}</div>
                    <div className="text-add mb-2">{n.message}</div>
                    <div className="text-time text-background-2">{new Date(n.created_at).toLocaleString()}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
      {/* Sidebar */}
      <div className="sidebar">
        {/* Logo */}
        <div className="mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-main rounded-lg flex items-center justify-center">
              <User className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-subheaders text-background font-bold">HR Admin</h1>
              <p className="text-add text-background-2">Панель управления</p>
            </div>
          </div>
        </div>
        
        {/* Navigation */}
        <nav className="mb-8">
          <div className="space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`nav-item ${isActive ? 'active' : ''}`}
                >
                  <item.icon className="w-5 h-5" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </nav>
        
        {/* User Profile */}
        <div className="mt-auto">
          <div className="flex items-center gap-3 p-4 bg-background-2 rounded-lg">
            <div className="w-10 h-10 bg-main rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-main">HR</span>
            </div>
            <div className="flex-1">
              <p className="text-nav text-background font-medium">{profileData.name}</p>
              <p className="text-add text-background-2">{profileData.email}</p>
            </div>
            <button className="text-background-2 hover:text-background transition-colors" onClick={() => setShowProfileModal(true)}>
              <Settings className="w-5 h-5" />
            </button>
            <button className="ml-2 text-background-2 hover:text-error transition-colors" onClick={handleLogout}>
              Выйти
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Top Bar */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-headers text-background">
              {navigation.find(item => item.href === location.pathname)?.name || 'HR Admin Panel'}
            </h2>
            <p className="text-main text-background-2 mt-2">
              Управление HR процессами и кандидатами
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <button className="relative p-3 text-background-2 hover:text-background transition-colors" onClick={handleOpenNotifications}>
              <Bell className="w-6 h-6" />
              {notifications.some(n => !n.read) && (
                <span className="absolute top-2 right-2 w-3 h-3 bg-error rounded-full"></span>
              )}
            </button>
            <div className="w-px h-8 bg-background-2"></div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-main rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-add">HR</span>
              </div>
              <div className="hidden md:block">
                <p className="text-nav text-background font-medium">{profileData.name}</p>
                <p className="text-add text-background-2">{profileData.email}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Page Content */}
        <div className="container">
          {children}
        </div>
      </div>

      {/* Модальное окно профиля */}
      {showProfileModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-subheaders text-background font-bold">Настройки профиля</h2>
              <button
                onClick={() => setShowProfileModal(false)}
                className="text-background-2 hover:text-background"
              >
                <span style={{fontSize: 24, fontWeight: 700}}>×</span>
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-main text-background mb-2">Имя</label>
                <input
                  type="text"
                  value={profileData.name}
                  onChange={e => handleProfileChange('name', e.target.value)}
                  className="input-field"
                  placeholder="Ваше имя"
                />
              </div>
              <div>
                <label className="block text-main text-background mb-2">Email</label>
                <input
                  type="email"
                  value={profileData.email}
                  onChange={e => handleProfileChange('email', e.target.value)}
                  className="input-field"
                  placeholder="email@example.com"
                />
              </div>
              <div>
                <label className="block text-main text-background mb-2">Текущий пароль</label>
                <input
                  type="password"
                  value={profileData.currentPassword}
                  onChange={e => handleProfileChange('currentPassword', e.target.value)}
                  className="input-field"
                  placeholder="Введите текущий пароль"
                />
              </div>
              <div>
                <label className="block text-main text-background mb-2">Новый пароль</label>
                <input
                  type="password"
                  value={profileData.newPassword}
                  onChange={e => handleProfileChange('newPassword', e.target.value)}
                  className="input-field"
                  placeholder="Введите новый пароль"
                />
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <button
                onClick={handleProfileSave}
                className="btn btn-primary flex-1"
                disabled={profileLoading}
              >
                Сохранить
              </button>
              <button
                onClick={() => setShowProfileModal(false)}
                className="btn btn-outline flex-1"
                disabled={profileLoading}
              >
                Отмена
              </button>
            </div>
            {profileMessage && (
              <div className="mt-4 text-center text-main">{profileMessage}</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Layout; 