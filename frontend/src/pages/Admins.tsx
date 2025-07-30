import React, { useState, useEffect } from 'react';
import { useTelegramAuth } from '../hooks/useTelegramAuth';

interface Admin {
  id: number;
  name: string;
  email?: string;
  telegram_id?: string;
  telegram_username?: string;
  is_admin: boolean;
}

const Admins: React.FC = () => {
  const { user, token } = useTelegramAuth();
  const [admins, setAdmins] = useState<Admin[]>([]);
  const [loading, setLoading] = useState(false);
  const [newAdminUsername, setNewAdminUsername] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Проверяем права доступа
  if (!user?.is_admin) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger">
          <h4 className="alert-heading">Доступ запрещен</h4>
          <p>У вас нет прав для просмотра этой страницы.</p>
        </div>
      </div>
    );
  }

  const fetchAdmins = async () => {
    if (!token) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/telegram/admins', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setAdmins(data.admins);
      } else {
        setError('Ошибка загрузки списка администраторов');
      }
    } catch (err) {
      setError('Ошибка загрузки списка администраторов');
    } finally {
      setLoading(false);
    }
  };

  const createAdmin = async () => {
    if (!token || !newAdminUsername.trim()) return;

    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      const response = await fetch('/api/telegram/create-admin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          telegram_username: newAdminUsername.trim(),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(`Администратор ${data.user.name} (@${data.user.telegram_username}) успешно создан`);
        setNewAdminUsername('');
        fetchAdmins(); // Обновляем список
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Ошибка создания администратора');
      }
    } catch (err) {
      setError('Ошибка создания администратора');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdmins();
  }, [token]);

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Управление администраторами</h3>
            </div>
            <div className="card-body">
              {/* Форма создания администратора */}
              <div className="row mb-4">
                <div className="col-md-6">
                  <div className="card">
                    <div className="card-header">
                      <h5 className="card-title mb-0">Добавить администратора</h5>
                    </div>
                    <div className="card-body">
                      <div className="mb-3">
                        <label htmlFor="username" className="form-label">
                          Telegram Username
                        </label>
                        <div className="input-group">
                          <span className="input-group-text">@</span>
                          <input
                            type="text"
                            className="form-control"
                            id="username"
                            placeholder="username"
                            value={newAdminUsername}
                            onChange={(e) => setNewAdminUsername(e.target.value)}
                            onKeyPress={(e) => {
                              if (e.key === 'Enter') {
                                createAdmin();
                              }
                            }}
                          />
                          <button
                            className="btn btn-primary"
                            onClick={createAdmin}
                            disabled={loading || !newAdminUsername.trim()}
                          >
                            {loading ? 'Добавление...' : 'Добавить'}
                          </button>
                        </div>
                        <div className="form-text">
                          Введите username пользователя без символа @
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Сообщения */}
              {message && (
                <div className="alert alert-success alert-dismissible fade show" role="alert">
                  {message}
                  <button
                    type="button"
                    className="btn-close"
                    onClick={() => setMessage(null)}
                  ></button>
                </div>
              )}

              {error && (
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                  {error}
                  <button
                    type="button"
                    className="btn-close"
                    onClick={() => setError(null)}
                  ></button>
                </div>
              )}

              {/* Список администраторов */}
              <div className="row">
                <div className="col-12">
                  <h5>Список администраторов</h5>
                  {loading ? (
                    <div className="text-center">
                      <div className="spinner-border" role="status">
                        <span className="visually-hidden">Загрузка...</span>
                      </div>
                    </div>
                  ) : (
                    <div className="table-responsive">
                      <table className="table table-striped">
                        <thead>
                          <tr>
                            <th>ID</th>
                            <th>Имя</th>
                            <th>Username</th>
                            <th>Telegram ID</th>
                            <th>Email</th>
                            <th>Статус</th>
                          </tr>
                        </thead>
                        <tbody>
                          {admins.map((admin) => (
                            <tr key={admin.id}>
                              <td>{admin.id}</td>
                              <td>{admin.name}</td>
                              <td>
                                {admin.telegram_username ? (
                                  <span className="badge bg-primary">
                                    @{admin.telegram_username}
                                  </span>
                                ) : (
                                  <span className="text-muted">-</span>
                                )}
                              </td>
                              <td>
                                {admin.telegram_id ? (
                                  <code>{admin.telegram_id}</code>
                                ) : (
                                  <span className="text-muted">-</span>
                                )}
                              </td>
                              <td>
                                {admin.email ? (
                                  <a href={`mailto:${admin.email}`}>{admin.email}</a>
                                ) : (
                                  <span className="text-muted">-</span>
                                )}
                              </td>
                              <td>
                                <span className="badge bg-success">Администратор</span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Admins; 