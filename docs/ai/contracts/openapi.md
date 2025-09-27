### Контракты HTTP API

Источники: `backend/app/api/**`, включение роутеров — `backend/app/api/router.py`.

- POST `/admin/login` — выдаёт `access_token` по паре логин/пароль.
  - Имплементация: `backend/app/api/admin_login.py` (`@router.post("/login")`).
  - Примечание: аутентификация админа временно захардкожена; пароль хэшируется, запись создаётся при первом логине.
- POST `/admin/refresh` — обновление access токена. ОПРЕДЕЛЕНО, НО НЕ ПРОВЕДЕНО В РОУТЕР.
  - Имплементация: `backend/app/api/admin_refresh_token.py` (`@router.post("/refresh")`).
  - Проблема: модуль не подключён в `backend/app/api/router.py` → эндпоинт недоступен.

Метрики Prometheus: автоматически экспонируются на `/metrics` (`Instrumentator().expose`).

Список будет дополнен при расширении API.

### Контракты WebSocket (канал `/ws/`)

Источники: `backend/app/api/web_socket.py`, `backend/app/api/websocket_core/**`, спецификация — `backend/app/docs/asyncapi.yaml`.

- Логин пользователя: сообщение `{ "type": "login", data: { nickname, user_id? } }`
- Логин администратора: `{ "type": "login_admin", data: <JWT> }`
- Пользовательские события: `update_pixel`, `update_selection`, `get_field_state`, `get_online_count`, `get_cooldown`
- Админские события: `update_pixel_admin`, `pixel_info_admin`, `toggle_ban_user_admin`, `update_cooldown_admin`, `reset_game_admin`, `get_online_info_admin`

Детализация схем сообщений см. в `backend/app/docs/asyncapi.yaml`.


