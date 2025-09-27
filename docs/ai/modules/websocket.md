### WebSocket протокол

Входная точка: `ws://<host>/ws/` (см. монтирование подприложения в `backend/app/main.py`).

Ключевые файлы:
- `backend/app/api/web_socket.py` — эндпоинт `/`, диспетчеризация сообщений
- `backend/app/api/websocket_core/authenticate.py` — аутентификация пользователя и админа (JWT)
- `backend/app/api/websocket_core/handlers.py` — обработчики событий
- `backend/app/api/websocket_core/connection_manager.py` — управление соединениями и рассылками
- `backend/app/api/websocket_core/metrics_handler.py` — учёт метрик отправки/приёма

Аутентификация:
- Пользователь: отправляет сообщение `login` c `data = { nickname: str, user_id?: str }`.
  - При первом входе сервер создаёт пользователя и возвращает `user_id` (type: `user_id`, data: `str`).
  - После успешного логина сервер отправляет `success` с текстом подтверждения.
- Админ: отправляет `login_admin` с `data = <JWT access_token>` (получается через HTTP `/admin/login`).
  - При успехе сервер отправляет `success` с текстом подтверждения.

Сообщения клиента → сервера (user):
- `login` — `backend/app/schemas/user/user_requests.py: LoginRequest`
- `update_pixel` — `PixelUpdateRequest`, `data: { x: int, y: int, color: "#RRGGBB" }`
- `update_selection` — `SelectionUpdateRequest`, `data: { position: { x:int, y:int } | null }`
- `get_field_state` — `GetFieldStateRequest`
- `get_online_count` — `GetOnlineCountRequest`
- `get_cooldown` — `GetCooldownRequest`
- `disconnect` — `DisconnectRequest`

Сообщения клиента → сервера (admin):
- `login_admin` — `backend/app/schemas/admin/admin_requests.py: AdminLoginRequest`, `data: str` (access token)
- `update_pixel_admin` — `AdminPixelUpdateRequest`, `data: { x:int, y:int, color:string }`
- `pixel_info_admin` — `AdminPixelInfoRequest`, `data: { x:int, y:int }`
- `toggle_ban_user_admin` — `AdminBanUserRequest`, `data: { user_id: string }`
- `update_cooldown_admin` — `AdminChangeCooldownRequest`, `data: int`
- `reset_game_admin` — `AdminResetGameRequest`, `data: [int, int]` (tuple как массив из двух int)
- `get_online_info_admin` — `AdminGetOnlineUsersRequest`

События сервера → клиента (broadcast/ответы):
- `user_id` — `AuthResponse(data: str)` — отправляется при создании нового пользователя на `login`
- `success` — `SuccessResponse(data: str)` — подтверждения успешных действий (логин, reset и т.д.)
- `error` — `ErrorResponse(message: str)` — ошибки валидации/прав доступа и пр.
- `pixel_update` — `PixelUpdateResponse(data: { x:int, y:int, color:string, nickname:string })`
- `selection_update` — `SelectionUpdateResponse(data: { nickname:string, position?: { x:int, y:int } })`
- `field_state` — `FieldStateResponse(size: [int,int], cooldown:int, data: { pixels: Pixel[], selections: Selection[] })`
- `online_count_update` — `OnlineCountResponse(data: { online:int })`
- `cooldown_update` — `ChangeCooldownResponse(data: int)`
- `users_info_update` — `AdminUserInfoResponse(data: Array<{ nickname:string, id:string }>)`
- `pixel_info_update` — `AdminPixelInfoResponse(data: { x:int, y:int, color:string, user_id?:string, nickname?:string })`

Примеры полезной последовательности:
1) Пользователь: `login` → получает `user_id` (если новый) → `success` → далее: `update_pixel`, `get_field_state`, ...
2) Админ: `login_admin` (с access_token из HTTP `/admin/login`) → `success` → `get_online_info_admin` / `pixel_info_admin` / `update_pixel_admin` / ...

Замечания:
- Все типы сообщений и структуры жёстко заданы в Pydantic-схемах в `backend/app/schemas/**`. Контракты WS неизменны.
- Закрытие по ошибкам: сервер может закрыть соединение кодами 1002/1003/1008/1011 в зависимости от нарушения протокола.
