from fastapi import APIRouter
import backend.app.api.admin_login as admin_login
import backend.app.api.admin_refresh_token as admin_refresh


def include_api(router: APIRouter):
    router.include_router(admin_login.router, prefix="/admin")
    router.include_router(admin_refresh.router, prefix="/admin")
