from time import time


class SpamDetector:
    def __init__(self):
        self.data = {}

    async def spam(self, user_id: int):
        current_ts = int(time())
        last_time = self.data.get(user_id)

        if last_time:
            if current_ts - last_time >= 3:
                self.data[user_id] = current_ts
                return False

            else:
                return True

        else:
            self.data[user_id] = current_ts
            return False
