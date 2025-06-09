from aiogrambot.handlers.baskets import basket_router
from aiogrambot.handlers.categories import categories_router
from aiogrambot.handlers.goods import goods_router
from aiogrambot.handlers.registration import reg_router
from aiogrambot.handlers.start import start_router


routers = [start_router, goods_router,
           categories_router, basket_router,
           reg_router]








