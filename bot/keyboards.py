from vk.keyboards import ButtonColor
from vk.keyboards import Keyboard


class InlineKeyboard:
    # todo: сделатб чтобы это нормально выглядело....
    ON_MENTION = Keyboard(one_time=False, inline=True)
    ON_MENTION.add_text_button(
        text="Список команд",
        color=ButtonColor.SECONDARY,
        payload={"witless_btn": "help"},
    )
    ON_MENTION.add_row()
    ON_MENTION.add_vkapps_button(
        app_id=6471849, owner_id=-185313238, label="Пожертвовать"
    )
    ON_MENTION.add_row()
    ON_MENTION.add_vkapps_button(
        app_id=6441755, owner_id=-185313238, label="Добавить в беседу"
    )
    ON_MENTION = ON_MENTION.get_keyboard()

    ON_INVITE_ME = Keyboard(one_time=False, inline=True)
    ON_INVITE_ME.add_text_button(
        text="Инструкция", color=ButtonColor.SECONDARY, payload={"witless_btn": "howto"}
    )
    ON_INVITE_ME.add_row()
    ON_INVITE_ME.add_text_button(
        text="Команды", color=ButtonColor.SECONDARY, payload={"witless_btn": "help"}
    )
    ON_INVITE_ME.add_row()
    ON_INVITE_ME.add_vkapps_button(
        app_id=6441755, owner_id=-185313238, label="Добавить в беседу"
    )
    ON_INVITE_ME = ON_INVITE_ME.get_keyboard()

    ON_UNKNOWN_SPEAK_ARG = Keyboard(one_time=False, inline=True)
    ON_UNKNOWN_SPEAK_ARG.add_text_button(
        text="Короткое",
        color=ButtonColor.SECONDARY,
        payload={"witless_btn": "speak_sm"},
    )
    ON_UNKNOWN_SPEAK_ARG.add_row()
    ON_UNKNOWN_SPEAK_ARG.add_text_button(
        text="Среднее", color=ButtonColor.SECONDARY, payload={"witless_btn": "speak_md"}
    )
    ON_UNKNOWN_SPEAK_ARG.add_row()
    ON_UNKNOWN_SPEAK_ARG.add_text_button(
        text="Длинное", color=ButtonColor.SECONDARY, payload={"witless_btn": "speak_lg"}
    )
    ON_UNKNOWN_SPEAK_ARG = ON_UNKNOWN_SPEAK_ARG.get_keyboard()

    ON_GENERATING_FAIL = Keyboard(one_time=False, inline=True)
    ON_GENERATING_FAIL.add_text_button(
        text="Сколько сохранено",
        color=ButtonColor.SECONDARY,
        payload={"witless_btn": "info"},
    )
    ON_GENERATING_FAIL.add_row()
    ON_GENERATING_FAIL.add_text_button(
        text="Инструкция", color=ButtonColor.SECONDARY, payload={"witless_btn": "howto"}
    )
    ON_GENERATING_FAIL = ON_GENERATING_FAIL.get_keyboard()

    ON_INFO = Keyboard(one_time=False, inline=True)
    ON_INFO.add_text_button(
        text="Инструкция", color=ButtonColor.SECONDARY, payload={"witless_btn": "howto"}
    )
    ON_INFO = ON_INFO.get_keyboard()

    ON_UNKNOWN_COMMAND = Keyboard(one_time=False, inline=True)
    ON_UNKNOWN_COMMAND.add_text_button(
        text="Список команд",
        color=ButtonColor.SECONDARY,
        payload={"witless_btn": "help"},
    )
    ON_UNKNOWN_COMMAND = ON_UNKNOWN_COMMAND.get_keyboard()
