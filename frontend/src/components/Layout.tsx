import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Users, 
  BarChart3, 
  Home, 
  User,
  Shield
} from 'lucide-react';
import { useTelegramAuth } from '../hooks/useTelegramAuth';
import 'bootstrap/dist/css/bootstrap.min.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const { user, token, loading, authenticate, logout } = useTelegramAuth();

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

  const [sidebarOpen, setSidebarOpen] = useState(false);

  // --- Получить профиль пользователя ---
  const fetchProfile = async () => {
    if (!user) return;
    
    try {
      const res = await fetch('/api/telegram/profile', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setProfileData({
          name: data.name,
          email: data.email || '',
          currentPassword: '',
          newPassword: '',
        });
      }
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error);
    }
  };

  // Обновляем профиль при изменении пользователя
  useEffect(() => {
    if (user) {
      setProfileData({
        name: user.name,
        email: user.email || '',
        currentPassword: '',
        newPassword: '',
      });
    }
  }, [user]);

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
        fetchProfile();
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



  const navigation = [
    { name: 'Дашборд', href: '/', icon: Home },
    { name: 'Кандидаты', href: '/candidates', icon: Users },
    { name: 'Метрики', href: '/metrics', icon: BarChart3 },
  ];

  // Добавляем пункт управления админами только для админов
  console.log('User data:', user);
  console.log('Is admin:', user?.is_admin);
  
  if (user?.is_admin) {
    navigation.push({ name: 'Администраторы', href: '/admins', icon: Shield });
    console.log('Added admin navigation item');
  } else {
    console.log('User is not admin, skipping admin navigation');
  }

  return (
    <div className="container-fluid p-0 h-100">
      {/* Bootstrap Navbar for mobile */}
      <nav className="navbar navbar-expand-md navbar-light bg-light d-md-none">
        <div className="container-fluid">
          <button className="navbar-toggler" type="button" onClick={() => setSidebarOpen(true)}>
            <span className="navbar-toggler-icon"></span>
          </button>
          <span className="navbar-brand">HR Admin</span>
        </div>
      </nav>
      {/* Sidebar as offcanvas on mobile, static on desktop */}
      <div className="row g-0 h-100 flex-nowrap">
        {/* Offcanvas Sidebar for mobile */}
        <div className={`offcanvas offcanvas-start d-md-none ${sidebarOpen ? 'show' : ''}`} tabIndex={-1} style={{visibility: sidebarOpen ? 'visible' : 'hidden'}}>
          <div className="offcanvas-header">
            <h5 className="offcanvas-title">Меню</h5>
            <button type="button" className="btn-close text-reset" onClick={() => setSidebarOpen(false)}></button>
          </div>
          <div className="offcanvas-body p-0">
            {renderSidebar(true)}
          </div>
        </div>
        {/* Static Sidebar for md+ */}
        <aside className="col-md-3 col-lg-2 d-none d-md-flex flex-column bg-light p-0 border-end" style={{minHeight: '100vh', height: '100vh', position: 'relative'}}>
          <div style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
            <div style={{flex: 1, overflowY: 'auto'}}>
              {renderSidebar(false, false)}
            </div>
          </div>
          <div style={{
            position: 'fixed',
            left: 0,
            bottom: 0,
            width: '16.6667%', // col-md-3 is 25%, col-lg-2 is 16.6667%
            minWidth: '200px', // fallback for sidebar min width
            maxWidth: '320px', // fallback for sidebar max width
            background: '#f8f9fa',
            borderTop: '1px solid #dee2e6',
            padding: '1rem',
            zIndex: 1040
          }}>
            {renderSidebar(false, true)}
          </div>
        </aside>
        {/* Main Content */}
        <main className="col-12 col-md-9 col-lg-10 px-3 py-4" style={{minHeight: '100vh'}}>
          {/* Top Bar */}
          <div className="d-flex flex-column flex-md-row align-items-start align-items-md-center justify-content-between mb-4 gap-3">
            <div>
              <h2 className="h4 mb-1">{navigation.find(item => item.href === location.pathname)?.name || 'HR Admin Panel'}</h2>
              <p className="text-muted mb-0">Управление HR процессами и кандидатами</p>
            </div>
            <div className="d-flex align-items-center gap-3">
              <div className="vr mx-2 d-none d-md-block"></div>
                              <div className="d-flex align-items-center gap-2">
                  <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center" style={{width: 32, height: 32}}>
                    <span className="text-white fw-bold">HR</span>
                  </div>
                  <div className="d-none d-md-block">
                    <div className="fw-medium">{user?.name || profileData.name}</div>
                    <div className="text-muted small">
                      {user?.telegram_username ? `@${user.telegram_username}` : profileData.email}
                      {user?.is_admin && (
                        <span className="badge bg-success ms-2">Админ</span>
                      )}
                    </div>
                  </div>
                </div>
            </div>
          </div>
          {/* Page Content */}
          <div className="flex-grow-1 w-100">
            {loading ? (
              <div className="d-flex justify-content-center align-items-center" style={{minHeight: '400px'}}>
                <div className="spinner-border" role="status">
                  <span className="visually-hidden">Загрузка...</span>
                </div>
              </div>
            ) : !user ? (
              <div className="d-flex justify-content-center align-items-center" style={{minHeight: '400px'}}>
                <div className="text-center">
                  <h3>Требуется авторизация</h3>
                  <p className="text-muted">Для доступа к панели необходимо авторизоваться через Telegram</p>
                  <button className="btn btn-primary" onClick={authenticate}>
                    Авторизоваться
                  </button>
                </div>
              </div>
            ) : (
              children
            )}
          </div>
        </main>
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

// Helper to render sidebar content
function renderSidebar(showProfileSection = true, onlyProfileSection = false) {
  if (onlyProfileSection) {
    // Inline profile section since ProfileSection component is missing
    return (
      <div>
        <div className="fw-bold">{profileData?.name || "Пользователь"}</div>
        <div className="text-muted small mb-2">{profileData?.email || ""}</div>
        <button
          className="btn btn-link p-0 d-block"
          onClick={() => setShowProfileModal(true)}
        >
          Профиль
        </button>
        <button
          className="btn btn-link text-danger p-0 d-block mt-2"
          onClick={logout}
        >
          Выйти
        </button>
      </div>
    );
  }
  return (
    <div className="d-flex flex-column h-100 p-3">
      {/* Logo */}
      <div className="mb-4 d-flex align-items-center gap-3">
        <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center" style={{width: 40, height: 40}}>
          <User className="text-white" />
        </div>
        <div>
          <h1 className="h5 mb-0">HR Admin</h1>
          <small className="text-muted">Панель управления</small>
        </div>
      </div>
      {/* Navigation */}
      <ul className="nav flex-column mb-4">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <li className="nav-item" key={item.name}>
              <Link
                to={item.href}
                className={`nav-link d-flex align-items-center gap-2 ${isActive ? 'active fw-bold text-primary' : ''}`}
                onClick={() => setSidebarOpen(false)}
              >
                <item.icon />
                {item.name}
              </Link>
            </li>
          );
        })}
      </ul>
      {/* User Profile (for mobile/offcanvas sidebar) */}
      {showProfileSection && (
        <div className="border-top pt-3">
          <div>
            <div className="fw-bold">{profileData?.name || "Пользователь"}</div>
            <div className="text-muted small mb-2">{profileData?.email || ""}</div>
            <button
              className="btn btn-link p-0 d-block"
              onClick={() => setShowProfileModal(true)}
            >
              Профиль
            </button>
            <button
              className="btn btn-link text-danger p-0 d-block mt-2"
              onClick={logout}
            >
              Выйти
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
};

export default Layout; 