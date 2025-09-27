### База данных

Инициализация и пул:
- `common/app/db/db_pool.py` — `AsyncConnectionPool`, декоратор `get_pool_cur`
- `common/app/db/create_db.py` — создание схемы (users, pixels, admins)

Основные таблицы:
- `users(id, nickname, is_banned, last_pixel_update)`
- `pixels(x, y, color, user_id, action_time)`
- `admins(id, username, password_hash)`

Доступ к данным (выборка/запись): `common/app/db/api_db.py`

