from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton

from .. import base
from ...locale import _ as locale


@base.router.callback_query(F.data == "cancel")
async def _cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(await locale("common", "operation_interrupted"))


async def button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text=await locale("common", "cancel"), callback_data="cancel")
