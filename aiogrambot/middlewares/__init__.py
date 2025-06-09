from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Callable, Dict, Any

class CancelFSMOnGlobalCommand(BaseMiddleware):

    def __init__(self, global_commands: list[str]):
        self.global_commands = global_commands

    async def __call__(self,
                       handler: Callable,
                       event: Message,
                       data: Dict[str, Any],
                       ) -> Any:

        state: FSMContext = data["state"]

        if event.text in self.global_commands and state:
            current_state = await state.get_state()
            if current_state:
                await state.clear()

        return await handler(event, data)
