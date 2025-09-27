### HTTP слой

- Включение роутов: `backend/app/api/router.py` → `include_router(admin_login.router, prefix="/admin")`
- Доступные эндпоинты:
  - POST `/admin/login` — получение `access_token`
  - [отключён] POST `/admin/refresh` — реализован, но не подключён

Замечания по качеству:
- Отсутствует единый `APIRouter` для админ-модулей (частичное подключение).
- Нет описания схем запросов/ответов в OpenAPI (FastAPI автогенерация покрывает только HTTP, WS — отдельно).

