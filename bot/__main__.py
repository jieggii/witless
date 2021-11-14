from vk import VK
from vk.utils import TaskManager
from vk.bot_framework import Dispatcher
from vk.bot_framework.storages import TTLDictStorage
from vk.bot_framework.addons import cooldown
from vk import types

import logging
import random

from bot import config
import bot
import bot.rules
import bot.const
import bot.keyboards
import bot.replies
import bot.util


logging.basicConfig(level="INFO")

vkobj = VK(config.TOKEN)
api = vkobj.get_api()
task_manager = TaskManager(vkobj.loop)
spam_detector = bot.SpamDetector()
ttl_storage = TTLDictStorage()
cd = cooldown.Cooldown(ttl_storage, standart_cooldown_time=3, for_specify_user=True)
cd.cooldown_message = bot.replies.Reply.ON_SPAM

dp = Dispatcher(vkobj, config.GROUP_ID)
dp.setup_rule(bot.rules.BotCommands)
dp.setup_rule(bot.rules.InvitedMe)
dp.setup_rule(bot.rules.InvitedUser)


# Commands
@dp.message_handler(
    from_bot=False,
    in_chat=True,
    bot_commands={
        "flag": bot.const.Flag.COMMAND,
        "commands": ["s", "speak", "g", "generate"],
    },
)
@cd.cooldown_handler()
async def handle_speak(message: types.Message, _):
    tokens = message.text.split(" ")

    if len(tokens) == 2:
        arg = "any"

    elif len(tokens) == 3:
        if tokens[2] in bot.const.AvailableMessageArgs.SPEAK:
            arg = tokens[2]

        else:
            arg = None

    else:
        arg = None

    if arg:
        async with vkobj.client.get(
            "http://127.0.0.1:8000/generate",
            json={"peer_id": message.peer_id, "size": arg},
        ) as response:
            data = await response.json()

        if data["success"]:
            await message.answer(data["result"])

        else:
            await message.answer(*bot.replies.Reply.ON_GENERATING_FAIL)

    else:  # if unknown argument passed
        await message.answer(*bot.replies.Reply.ON_SPEAK_UNKNOWN_ARG)


@dp.message_handler(
    from_bot=False,
    in_chat=True,
    bot_commands={
        "flag": bot.const.Flag.COMMAND,
        "commands": ["b", "bugurt", "бугурт"],
    },
)
@cd.cooldown_handler()
async def handle_bugurt(message: types.Message, _):
    parts = []

    for i in range(random.randint(3, 4)):
        async with vkobj.client.get(
            "http://127.0.0.1:8000/generate",
            json={"peer_id": message.peer_id, "size": "md"},
        ) as response:
            data = await response.json()
            if data["success"]:
                parts.append(data["result"].upper())

            else:
                await message.answer(*bot.replies.Reply.ON_GENERATING_FAIL)
                return

    response = "\n@\n".join(parts)

    await message.answer(response)


@dp.message_handler(
    from_bot=False,
    in_chat=True,
    bot_commands={
        "flag": bot.const.Flag.COMMAND,
        "commands": ["d", "dialogue", "dialog", "диалог"],
    },
)
@cd.cooldown_handler()
async def handle_dialogue(message: types.Message, _):
    parts = []

    for i in range(random.randint(3, 4)):
        async with vkobj.client.get(
            "http://127.0.0.1:8000/generate",
            json={"peer_id": message.peer_id, "size": "md"},
        ) as response:
            data = await response.json()

        if data["success"]:
            parts.append(data["result"])

        else:
            await message.answer(*bot.replies.Reply.ON_GENERATING_FAIL)
            return

    response = "\n> ".join(parts)

    await message.answer(response)


@dp.message_handler(
    from_bot=False, in_chat=True, bot_commands={"flag": bot.const.Flag.MENTION}
)
@cd.cooldown_handler()
async def handle_mention(message: types.Message, _):
    await message.answer(*bot.replies.Reply.ON_MENTION_ME)


@dp.message_handler(
    from_bot=False,
    in_chat=True,
    bot_commands={
        "flag": bot.const.Flag.COMMAND,
        "commands": ["h", "help", "помощь", "команды"],
    },
)
@cd.cooldown_handler()
async def handle_help(message: types.Message, _):
    await message.answer(*bot.replies.Reply.ON_HELP)


@dp.message_handler(
    from_bot=False,
    in_chat=True,
    bot_commands={
        "flag": bot.const.Flag.COMMAND,
        "commands": ["i", "info", "инфо", "информация"],
    },
)
@cd.cooldown_handler()
async def handle_info(message: types.Message, _):
    async with vkobj.client.get(
        "http://127.0.0.1:8000/count", json={"peer_id": message.peer_id}
    ) as response:
        data = await response.json()

    if data["success"]:
        await message.answer(
            f"Сохранено {data['result']} строк для обучения. \n"
            f"Если это число не увеличивается, проверьте, выдали ли вы мне доступ ко всей переписке",
            keyboard=bot.keyboards.InlineKeyboard.ON_INFO,
        )


@dp.message_handler(
    from_bot=False,
    in_chat=True,
    bot_commands={
        "flag": bot.const.Flag.COMMAND,
        "commands": ["w", "wipe", "delete", "сброс", "сбросить"],
    },
)
@cd.cooldown_handler()
async def handle_wipe(message: types.Message, _):
    response = dict(
        await api.messages.get_conversations_by_id(
            peer_ids=message.peer_id, extended=True
        )
    )["response"]
    if response["items"]:
        chat = response["items"][0]
        if bot.util.user_is_chat_admin(chat, message.from_id):
            async with vkobj.client.get(
                f"http://127.0.0.1:8000/wipe", json={"peer_id": message.peer_id}
            ) as response:
                data = await response.json()

            if data["success"]:
                await message.answer("Данные для обучения в этой беседе были сброшены")

            else:
                await message.answer("Нет данных для обучения, мне нечего сбрасывать")

        else:
            await message.answer(
                "Для выполнения этой команды вы должны быть администратором беседы"
            )
    else:
        await message.answer(
            "Для того, чтобы проверить, являетесь ли вы администратором беседы, "
            "мне нужны права администратора беседы"
        )


@dp.message_handler(
    from_bot=False,
    in_chat=True,
    bot_commands={
        "flag": bot.const.Flag.COMMAND,
        "commands": ["st", "stats", "статистика"],
    },
)
@cd.cooldown_handler()
async def handle_stats(message: types.Message, _):
    async with vkobj.client.get(
        "http://127.0.0.1:8000/stats", json={"peer_id": message.peer_id}
    ) as response:
        data = await response.json()

    if data["success"]:
        await message.answer(
            "Статистика @witless(Witless):\n"
            f"Количество бесед: {data['count']}\n"
            f"Вес данных для обучения в этой беседе: {data['local_size']} мб\n"
            f"Суммарный вес данных для обучения: {data['global_size']} мб"
        )


# Payloads
@dp.message_handler(from_bot=False, in_chat=True, payload={"witless_btn": "howto"})
@cd.cooldown_handler()
async def handle_payload_instruction(message: types.Message, _):
    await message.answer(*bot.replies.Reply.HOWTO)


@dp.message_handler(from_bot=False, in_chat=True, payload={"witless_btn": "help"})
@cd.cooldown_handler()
async def handle_payload_help(message: types.Message, _):
    await message.answer(*bot.replies.Reply.ON_HELP)


@dp.message_handler(from_bot=False, in_chat=True, payload={"witless_btn": "info"})
@cd.cooldown_handler()
async def handle_info(message: types.Message, _):
    async with vkobj.client.get(
        "http://127.0.0.1:8000/count", json={"peer_id": message.peer_id}
    ) as response:
        data = await response.json()

    if data["success"]:
        await message.answer(
            f"Сохранено {data['result']} строк для обучения. \n"
            f"Если это число не увеличивается, проверьте, выдали ли вы мне доступ ко всей переписке",
            keyboard=bot.keyboards.InlineKeyboard.ON_INFO,
        )


@dp.message_handler(from_bot=False, in_chat=True, payload={"witless_btn": "speak_sm"})
@cd.cooldown_handler()
async def handle_payload_speak_sm(message: types.Message, _):
    async with vkobj.client.get(
        "http://127.0.0.1:8000/generate",
        json={"peer_id": message.peer_id, "size": "sm"},
    ) as response:
        data = await response.json()

    if data["success"]:
        await message.answer(data["result"])

    else:
        await message.answer(*bot.replies.Reply.ON_GENERATING_FAIL)


@dp.message_handler(from_bot=False, in_chat=True, payload={"witless_btn": "speak_md"})
@cd.cooldown_handler()
async def handle_payload_speak_md(message: types.Message, _):
    async with vkobj.client.get(
        "http://127.0.0.1:8000/generate",
        json={"peer_id": message.peer_id, "size": "md"},
    ) as response:
        data = await response.json()

    if data["success"]:
        await message.answer(data["result"])

    else:
        await message.answer(*bot.replies.Reply.ON_GENERATING_FAIL)


@dp.message_handler(from_bot=False, in_chat=True, payload={"witless_btn": "speak_lg"})
@cd.cooldown_handler()
async def handle_payload_speak_lg(message: types.Message, _):
    async with vkobj.client.get(
        "http://127.0.0.1:8000/generate",
        json={"peer_id": message.peer_id, "size": "lg"},
    ) as response:
        data = await response.json()

    if data["success"]:
        await message.answer(data["result"])

    else:
        await message.answer(*bot.replies.Reply.ON_GENERATING_FAIL)


# Chat actions
@dp.message_handler(chat_action=types.Action.chat_invite_user, invited_me=True)
async def handle_invited_me(message: types.Message, _):
    await message.answer(*bot.replies.Reply.ON_INVITE_ME)


@dp.message_handler(chat_action=types.Action.chat_invite_user, invited_user=True)
async def handle_invite_user(message: types.Message, _):
    async with vkobj.client.get(
        "http://127.0.0.1:8000/generate",
        json={"peer_id": message.peer_id, "size": "sm"},
    ) as response:
        data = await response.json()

    if data["success"]:
        await message.answer(data["result"])


@dp.message_handler(
    from_bot=False, in_chat=True, bot_commands={"flag": bot.const.Flag.UNKNOWN}
)
async def unknown(message: types.Message, _):
    await message.answer(*bot.replies.Reply.ON_UNKNOWN_COMMAND)


@dp.message_handler(from_bot=False, in_chat=True)
async def other(message: types.Message, _):
    if random.randint(0, 10) == 0:  # 9%
        async with vkobj.client.get(
            "http://127.0.0.1:8000/generate",
            json={"peer_id": message.peer_id, "size": "any"},
        ) as response:
            data = await response.json()

        if data["success"]:
            await message.answer(data["result"])

    if not await spam_detector.spam(message.from_id):
        text = message.text

        if len(text.split(" ")) > 1 and len(text) <= 400:
            async with vkobj.client.get(
                "http://127.0.0.1:8000/push",
                json={"peer_id": message.peer_id, "message": text.lower()},
            ):
                pass


@dp.message_handler(in_chat=False)
async def direct(message: types.Message, _):
    await message.reply(
        "Привет! Бот работает только в беседах. Если есть вопросы, можешь посмотреть эту статью: https://vk.cc/9UeRzB"
    )


async def run():
    dp.run_polling()


if __name__ == "__main__":
    try:
        task_manager.add_task(run)
        task_manager.run(auto_reload=False)

    except KeyboardInterrupt:
        logging.info("Govnobot was killed...")
        exit(0)
