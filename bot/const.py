from enum import Enum


class Flag(Enum):
    MENTION = "mention"
    COMMAND = "command"
    UNKNOWN = "unknown"


class AvailableMessageArgs:
    SPEAK = [
        "sm",
        "small",
        "short",
        "маленькое",
        "короткое",
        "md",
        "medium",
        "среднее",
        "lg",
        "large",
        "большое",
        "длинное",
        "any",
        "любое",
    ]


class Links:
    COMMANDS = "https://vk.cc/9ZdHLN"
    INSTRUCTION = "https://vk.cc/9ZPoHM"
