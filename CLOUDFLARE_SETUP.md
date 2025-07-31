# Настройка Cloudflare Tunnel

Этот документ описывает, как развернуть приложение через Cloudflare Tunnel вместо Heroku.

## Предварительные требования

1. Установите `cloudflared`:
   - **macOS**: `brew install cloudflare/cloudflare/cloudflared`
   - **Linux**: Скачайте с https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   - **Windows**: Скачайте с официального сайта

2. Создайте аккаунт на Cloudflare (если еще нет)

## Настройка Cloudflare Tunnel

### 1. Создание туннеля

```bash
# Создайте новый туннель
cloudflared tunnel create aeon-hr-admin

# Получите ID туннеля
cloudflared tunnel list
```

### 2. Настройка конфигурации

Отредактируйте файл `cloudflared.yml`:

```yaml
tunnel: YOUR_TUNNEL_ID  # Замените на ваш ID туннеля
credentials-file: /path/to/your/credentials.json

ingress:
  - hostname: your-domain.com  # Замените на ваш домен
    service: http://localhost:8000
  - hostname: www.your-domain.com
    service: http://localhost:8000
  - service: http_status:404
```

### 3. Настройка DNS

```bash
# Создайте DNS запись для вашего домена
cloudflared tunnel route dns aeon-hr-admin your-domain.com
```

### 4. Получение credentials

```bash
# Скачайте credentials файл
cloudflared tunnel token YOUR_TUNNEL_ID
```

## Запуск приложения

### Вариант 1: Использование готового скрипта

```bash
./start-cloudflare.sh
```

### Вариант 2: Ручной запуск

1. Запустите backend:
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

2. В другом терминале запустите frontend:
```bash
cd frontend
npm start
```

3. В третьем терминале запустите Cloudflare Tunnel:
```bash
cloudflared tunnel --config cloudflared.yml run
```

## Преимущества Cloudflare Tunnel

- ✅ Бесплатный SSL сертификат
- ✅ Глобальная CDN сеть
- ✅ Защита от DDoS атак
- ✅ Простая настройка
- ✅ Нет необходимости в публичном IP
- ✅ Работает за NAT/firewall

## Устранение неполадок

### Туннель не подключается
- Проверьте правильность ID туннеля в конфигурации
- Убедитесь, что credentials файл находится в правильном месте
- Проверьте, что backend запущен на порту 8000

### DNS не работает
- Убедитесь, что DNS запись создана правильно
- Проверьте настройки домена в Cloudflare Dashboard

### Ошибки аутентификации
- Пересоздайте credentials файл
- Проверьте права доступа к файлу credentials

## Полезные команды

```bash
# Просмотр статуса туннеля
cloudflared tunnel info YOUR_TUNNEL_ID

# Просмотр логов
cloudflared tunnel logs YOUR_TUNNEL_ID

# Удаление туннеля
cloudflared tunnel delete YOUR_TUNNEL_ID
``` 