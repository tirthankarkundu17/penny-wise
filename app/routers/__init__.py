from app.routers.auth import router as auth_router
from app.routers.bills import router as bills_router
from app.routers.analytics import router as analytics_router

__all__ = ["auth_router", "bills_router", "analytics_router"]
