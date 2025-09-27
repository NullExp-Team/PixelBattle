
## О проекте

Многопользовательское pixel‑art приложение на FastAPI + WebSocket. Основное взаимодействие — через WebSocket; присутствуют пользовательские и админ‑операции.

Полезные разделы документации:
- `docs/ai/project_brief.md`
- `docs/ai/architecture.md`

## Требования

- Docker и Docker Compose (для Windows рекомендуется WSL2)
- Сетевые порты:
  - `SERVICE_PORT` — порт бекенда (FastAPI)
  - 9090 — Prometheus (опционально)
  - 3000 — Grafana (опционально)

## Быстрый старт (dev)

1) Создайте файл `.env` по примеру `.env.example` и задайте значения (см. раздел Переменные окружения).
2) Сборка образов:
```bash
docker-compose build
```
3) Запуск:
```bash
docker-compose up -d
```
4) Проверки:
- Документация HTTP (только HTTP‑эндпоинты): `http://localhost:${SERVICE_PORT}/docs`
- WebSocket (dev): `ws://localhost:${SERVICE_PORT}/ws/`
- Метрики (dev, если включено): `http://localhost:${SERVICE_PORT}/metrics`

Ключ `-d` (detach) запускает контейнеры в фоне.

## Прод/демо запуск

- Не использовать `--reload`
- `DEBUG_MODE=false` обязательно; на старте не вызывается init_db
- Метрики не публиковать наружу (ограничить сетью/ingress)
- CORS: указывать конкретный `FRONTEND_URL`
- Рекомендовано реверс‑прокси (nginx/caddy); для приватной демо — Basic Auth и запрет индексирования

## Переменные окружения (.env)

База данных:
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`

Сервис:
- `SERVICE_PORT` (порт FastAPI), `PYTHONPATH`
- `DEBUG_MODE` (`true|false`)
- `FRONTEND_URL` (разрешённый origin для CORS в prod)
- `BACKEND_DOMAIN`, `BACKEND_DOMAIN_PORT` (если требуется)

Безопасность:
- `SECRET_KEY`, `SECURITY_PASSWORD_SALT`

Пример:
```env
POSTGRES_USER=app
POSTGRES_PASSWORD=app_password
POSTGRES_DB=pixel
POSTGRES_HOST=db
POSTGRES_PORT=5432

SERVICE_PORT=8000
DEBUG_MODE=true
FRONTEND_URL=http://localhost:8000
SECRET_KEY=please_change_me
SECURITY_PASSWORD_SALT=please_change_me
```

Примечания по режимам:
- Dev (`DEBUG_MODE=true`): CORS `*`, доступ к `/metrics`, возможна инициализация БД на старте
- Prod (`DEBUG_MODE=false`): CORS ограничен до `FRONTEND_URL`, `/metrics` не экспонируются приложением, init_db не вызывается

## Инициализация БД

- Dev: допустима пересоздающая инициализация при запуске (если включено)
- Prod: строго запрещено дропать/создавать таблицы на старте; используйте миграции (Alembic — в планах)

## Контракты API/WS

- HTTP: `docs/ai/contracts/openapi.md` (эндпоинты `/admin/login`, `/admin/refresh` и др.)
- WS: `docs/ai/contracts/asyncapi.md` (исходник — `backend/app/docs/asyncapi.yaml`)
  - Детальная спецификация WS сообщений: `docs/ai/modules/websocket.md`

Контракты не менялись; фронтенд совместим.

## Smoke‑проверки

HTTP:
```bash
curl -X POST http://localhost:${SERVICE_PORT}/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'
```
Ожидание: `200` и `{"access_token": "...", "token_type": "bearer"}`

WS (dev):
- Подключиться к `ws://localhost:${SERVICE_PORT}/ws/`
- Отправить `{ "type": "login", "data": { "nickname": "user123" } }` → получить `user_id`
- Отправить `update_pixel`, `get_field_state` — увидеть бродкасты/ответы

## Нюансы и безопасность

- CORS: в prod — только `FRONTEND_URL`, в dev — допускается `*`
- Метрики: только в dev или во внутренней сети
- Секреты — через ENV/Vault, не хранить в коде
- Админ‑аутентификация: JWT по `/admin/login` (хэши в БД); в dev может существовать базовая учётка, в prod — отключить

## Тесты

- `pytest` (часть WS‑тестов требует запущенный сервер и БД)
- Не использовать прод‑URI по умолчанию; локальный WS `ws://localhost:${SERVICE_PORT}/ws/`

## Масштабирование (для демо/CDN)

- Для горизонтали потребуются sticky‑sessions и/или Redis pub/sub для бродкастов; текущая версия не HA

## Известные ограничения

- Нет Alembic‑миграций (запланировано)
- Ограниченная защита WS (rate limiting/Origin check — отдельная задача)
- `/metrics` не предназначен для внешней публикации