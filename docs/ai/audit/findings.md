### Аудит — ключевые проблемы

Критические:
- Инициализация БД при старте сервера дропает таблицы (потеря данных).
  - См. `backend/app/main.py` (startup вызывает `create_db.init_db()`), `common/app/db/create_db.py` (`DROP TABLE IF EXISTS`).
- Админские креды захардкожены, пароль хэшируется на лету без политики.
  - См. `backend/app/api/admin_login.py` → `authenticate_admin`.
- Эндпоинт `/admin/refresh` реализован, но не подключён в роутер.
  - См. `backend/app/api/admin_refresh_token.py` vs `backend/app/api/router.py`.
- Неверное использование `await` в `/admin/refresh` (возвращается корутина вместо строки).
  - См. `backend/app/api/admin_refresh_token.py` → вызов `refresh_access_token(... )` без `await`.
- Секреты в коде: `SECRET_KEY`, `SECURITY_PASSWORD_SALT` заданы константами.
  - См. `common/app/core/config.py`.
- CORS `allow_origins=["*"]` в проде.
  - См. `backend/app/main.py`.

Высокие:
- Логи при импорте конфигурации: печать `DB_URL_without_password` (шум/риски инфоутечки окружения).
  - См. `common/app/core/config.py` (print при импорте).
- Отсутствие миграций (drop/create вместо Alembic), нет версионирования схемы.
- Тесты завязаны на внешний прод URL, небезопасно и нестабильно.
  - См. `backend/app/tests/websocket_login_actions_admin_test.py`.
- Слабая валидация входящих WS-сообщений и массовые try/except с широкими исключениями.

Средние/Низкие:
- Дублирование функций в `api_db.py` (`get_users_info` определён дважды).
- Комментарии TODO в коде, нет контрактов север/клиент на возврат поля (структура field state).
- Жёстко заданные порты/пароли Grafana в compose.

