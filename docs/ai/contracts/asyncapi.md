### AsyncAPI (WebSocket)

Ниже — актуальная спецификация каналов и сообщений на основе кода (`backend/app/schemas/**`, `web_socket.py`, `handlers.py`).

Канал: `/` (адрес `ws://<host>/ws/`)

Клиент → Сервер (messages):
- login
- login_admin
- update_pixel
- update_selection
- get_field_state
- get_online_count
- get_cooldown
- disconnect
- update_pixel_admin
- pixel_info_admin
- toggle_ban_user_admin
- update_cooldown_admin
- reset_game_admin
- get_online_info_admin

Сервер → Клиент (messages):
- user_id
- success
- error
- pixel_update
- selection_update
- field_state
- online_count_update
- cooldown_update
- users_info_update
- pixel_info_update

См. точные структуры и примеры в `docs/ai/modules/websocket.md` (они синхронизированы с Pydantic-моделями).

