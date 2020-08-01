from datetime import timedelta
import bz2
from flask import current_app
from redis import StrictRedis
from cryptography.fernet import Fernet

cipher = Fernet(Fernet.generate_key())


class Cache:
    DEFAULT_TTL = 1800  # 30 min

    def __init__(self, encrypted=False, ttl=None):
        self.redis = StrictRedis.from_url(url=current_app.config["REDIS_URL"])
        self.encrypted = encrypted
        if ttl is None:
            self.ttl = Cache.DEFAULT_TTL
        else:
            self.ttl = ttl

    def get(self, key):
        data = self.redis.get(key)
        if data is None:
            return False, None

        if self.encrypted:
            data = cipher.decrypt(data)

        return True, bz2.decompress(data).decode("utf-8")

    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.ttl

        value = bz2.compress(value.encode("utf-8"))
        if self.encrypted:
            value = cipher.encrypt(value)

        self.redis.setex(key, timedelta(seconds=ttl), value)

    def delete(self, key):
        self.redis.delete(key)
