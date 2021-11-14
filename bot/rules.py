from vk.bot_framework.dispatcher.rule import NamedRule
import bot.const
import vk.types
from bot import config


class BotCommands(NamedRule):
    key = "bot_commands"

    def __init__(self, data: dict):  # actions, commands
        self.flag = data["flag"]
        if self.flag == bot.const.Flag.COMMAND:
            self.commands = data["commands"]

        else:
            self.commands = None

        self.prefixes = ["[club185313238|@witless]", "witless", "w", "витлес", "уитлес"]

    async def check(self, message: vk.types.Message, _):
        text = message.text.lower()
        text_words = text.split(" ")

        if self.flag == bot.const.Flag.MENTION:
            return text in self.prefixes

        elif self.flag == bot.const.Flag.COMMAND:
            if len(text_words) > 1:
                for command in self.commands:
                    for prefix in self.prefixes:
                        if text_words[0] == prefix or text_words[0] == prefix + ",":
                            if text_words[1] == command:
                                return True

                return False

            else:
                return False

        elif self.flag == bot.const.Flag.UNKNOWN:
            if not message.payload:
                if text_words[0] in self.prefixes:
                    return True

            else:
                return False


class InvitedMe(NamedRule):
    key = "invited_me"

    def __init__(self, value: bool):
        self.value = value

    async def check(self, message: vk.types.Message, _):
        if message.action.member_id == -config.GROUP_ID:
            return self.value


class InvitedUser(NamedRule):
    key = "invited_user"

    def __init__(self, value: bool):
        self.value = value

    async def check(self, message: vk.types.Message, _):
        if message.action.member_id > 0:
            return self.value
