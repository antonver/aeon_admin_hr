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

interface PendingAdmin {
  id: number;
  telegram_username: string;
  created_by?: number;
  created_at: string;
}

const Admins: React.FC = () => {
  const { user, token } = useTelegramAuth();
  const [admins, setAdmins] = useState<Admin[]>([]);
  const [pendingAdmins, setPendingAdmins] = useState<PendingAdmin[]>([]);
  const [loading, setLoading] = useState(false);
  const [newAdminUsername, setNewAdminUsername] = useState('');
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

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

  const fetchPendingAdmins = async () => {
    if (!token) return;
    
    try {
      const response = await fetch('/api/telegram/pending-admins', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setPendingAdmins(data.pending_admins);
      } else {
        console.error('Ошибка загрузки списка ожидающих администраторов');
      }
    } catch (err) {
      console.error('Ошибка загрузки списка ожидающих администраторов');
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
        if (data.user) {
          setMessage(`Администратор ${data.user.name} (@${data.user.telegram_username}) успешно создан`);
        } else if (data.pending_admin) {
          setMessage(`Пользователь @${data.pending_admin.telegram_username} добавлен в список ожидающих администраторов. Он станет администратором при первом входе в приложение.`);
        }
        setNewAdminUsername('');
        fetchAdmins(); // Обновляем список
        fetchPendingAdmins(); // Обновляем список ожидающих
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

  const removePendingAdmin = async (username: string) => {
    if (!token) return;

    try {
      const response = await fetch(`/api/telegram/pending-admins/${username}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setMessage(`Пользователь @${username} удален из списка ожидающих администраторов`);
        fetchPendingAdmins(); // Обновляем список
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Ошибка удаления из списка ожидающих');
      }
    } catch (err) {
      setError('Ошибка удаления из списка ожидающих');
    }
  };

  useEffect(() => {
    fetchAdmins();
    fetchPendingAdmins();
  }, [token]);

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

              {/* Список ожидающих администраторов */}
              {pendingAdmins.length > 0 && (
                <div className="row mb-4">
                  <div className="col-12">
                    <div className="card">
                      <div className="card-header">
                        <h5 className="card-title mb-0">Ожидающие администраторы</h5>
                      </div>
                      <div className="card-body">
                        <div className="alert alert-info">
                          <i className="fas fa-info-circle me-2"></i>
                          Эти пользователи будут назначены администраторами при первом входе в приложение
                        </div>
                        <div className="table-responsive">
                          <table className="table table-sm">
                            <thead>
                              <tr>
                                <th>Username</th>
                                <th>Добавлен</th>
                                <th>Действия</th>
                              </tr>
                            </thead>
                            <tbody>
                              {pendingAdmins.map((pending) => (
                                <tr key={pending.id}>
                                  <td>
                                    <span className="badge bg-warning text-dark">
                                      @{pending.telegram_username}
                                    </span>
                                  </td>
                                  <td>
                                    {new Date(pending.created_at).toLocaleDateString('ru-RU')}
                                  </td>
                                  <td>
                                    <button
                                      className="btn btn-sm btn-outline-danger"
                                      onClick={() => removePendingAdmin(pending.telegram_username)}
                                      title="Удалить из списка ожидающих"
                                    >
                                      <i className="fas fa-trash"></i> Удалить
                                    </button>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
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