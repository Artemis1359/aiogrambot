from aiogrambot.handlers.admin.users import users_router
from aiogrambot.handlers.admin.goods import goods_router
from aiogrambot.handlers.admin.categories import categories_router
from aiogrambot.handlers.admin.panel import panel_router

admin_router = [categories_router, goods_router,
                panel_router, users_router]








