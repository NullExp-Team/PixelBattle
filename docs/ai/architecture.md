### Архитектура (набросок)

#### Обзор
- Приложение на FastAPI/Starlette с HTTP и WebSocket интерфейсами.
- Слой схем/моделей данных.
- Подсистема БД (пул соединений, init).
- Интеграция с Prometheus для метрик.

#### Диаграмма (логическая)
```
Client (HTTP/WS)
   |               
   v               
API Routers ---- WebSocket Handlers
   |                    |
   v                    v
Schemas/Validation   Connection Manager/Auth
   |                    |
   v                    v
DB Access Layer ---- Metrics (Prometheus)
```

> Конкретика по классам/функциям будет добавлена из AST-анализа и поиска по коду.


