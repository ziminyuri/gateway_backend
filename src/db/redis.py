import pickle

import redis

from core.config import REDIS_HOST, REDIS_PORT


class Redis:
    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def setex_value(self, key, value, time):
        self.redis.setex(key, time, pickle.dumps(value))

    def get_value(self, key):
        value = self.redis.get(key)
        return pickle.loads(value) if value else value

    def delete(self, key):
        self.redis.delete(key)

    @staticmethod
    def make_key(user_id, user_agent, refresh_token=False):
        if refresh_token:
            return f"{user_id}_{user_agent}_"
        else:
            return f"{user_id}_{user_agent}_refresh_token_"


cache = Redis()
