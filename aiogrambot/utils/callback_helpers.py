
async def callback_message_editor(callback, text, reply_markup):
    """Обрабатывает callback для корректного использования edit_text или answer."""

    if callback.message.text:
        await callback.message.edit_text(
            text=text,
            reply_markup=reply_markup)
    else:
        # Если в сообщении только фото — удаляем его и отправляем новое
        await callback.message.delete()
        await callback.message.answer(
            text=text,
            reply_markup=reply_markup)