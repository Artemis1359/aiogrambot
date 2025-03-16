from aiogrambot.handlers.admin.users import users_router
from aiogrambot.handlers.admin.goods import goods_router
from aiogrambot.handlers.admin.categories import categories_router
from aiogrambot.handlers.admin.panel import admin_router

admin_routers = [categories_router, goods_router,
                admin_router, users_router]








