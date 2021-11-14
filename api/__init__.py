from aiofile import AIOFile
from os import remove
from re import findall
from api import util
from os.path import getsize
from os import listdir
from random import randint


async def improve_result(result: str):
    rnd = randint(0, 4)
    if rnd == 0:  # ну чиста для прекола иногда бот пишет постироничнее....
        return result

    elif rnd == 1:
        return result.upper()  # ну чиста для прекола в иногда бот орет кричит....

    else:
        improved_result = ""

        for i in range(len(result)):
            if i == 0:
                improved_result += result[i].upper()

            elif i > 1:
                if result[i - 1] == " " and result[i - 2] in ["?", ".", "!"]:
                    improved_result += result[i].upper()

                else:
                    improved_result += result[i]

            else:
                improved_result += result[i]

        return improved_result


class Stats:
    @staticmethod
    async def get(peer_id):
        files = [f"messages/{filename}" for filename in listdir("messages")]
        global_size = round(sum([getsize(file) for file in files]) / 1048576, 2)
        try:
            local_size = round(getsize(f"messages/{peer_id}.raw") / 1048576, 2)

        except FileNotFoundError:
            local_size = 0

        return len(files), global_size, local_size


async def censor_result(result: str):
    blacklisted_tokens = [
        "сова никогда не спит",
        "#cинийкит",
        "#рaзбудименяв420",
        "all",
        "everyone",
    ]
    links = util.remove_duplicates(
        findall(r"[^ (){\}\[\]\'\";]+\.[^ (){\}\[\]\'\";]+", result)
    )

    for link in links:
        result = result.replace(link, "[ссылка удалена]")

    for token in blacklisted_tokens:
        result = result.replace(token, "*" * len(token))

    return result


async def escape_string(string: str):
    return string.replace(";", "\;")


async def unescape_string(string: str):
    return string.replace("\;", ";")


async def parse_raw(raw: str):
    result = []
    start = 0

    for i in range(len(raw)):
        if i != 0:
            if raw[i] == ";" and raw[i - 1] != "\\":
                result.append(raw[start:i])

                start = i + 1

    return [await unescape_string(message) for message in result]


class MessagesStorage:
    def __init__(self, peer_id: int):
        self.path = f"messages/{peer_id}.raw"

    async def wipe(self):
        try:
            remove(self.path)
            return True

        except:
            return False

    async def get(self):
        try:
            async with AIOFile(self.path, "r", encoding="utf-8") as file:
                raw = await file.read()

            messages = await parse_raw(raw)
            # messages = messages[::-1][0:150]  # в эфире рубрика ЕХперементы....
            return messages

        except FileNotFoundError:
            return []

    async def push(self, messages: list):
        async with AIOFile(self.path, "a", encoding="utf-8") as file:
            line = ";".join([await escape_string(message) for message in messages])
            await file.write(line + ";")
