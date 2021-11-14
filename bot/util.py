def user_is_chat_admin(chat, user_id):
    settings = chat["chat_settings"]

    if user_id == settings["owner_id"] or user_id in settings["admin_ids"]:
        return True

    else:
        return False
