from base64 import b64encode, b64decode
from datetime import timedelta
import pickle
import bz2
from flask import current_app
from redis import StrictRedis
from cryptography.fernet import Fernet

cipher = Fernet(Fernet.generate_key())


class Cache:
    DEFAULT_TTL = 60 * 60 * 24  # 24 hours

    def __init__(self, encrypted=False, ttl=None):
        self.redis = StrictRedis.from_url(current_app.config["RESULT_REDIS"])
        self.encrypted = encrypted
        if ttl is None:
            self.ttl = Cache.DEFAULT_TTL
        else:
            self.ttl = ttl

    def get(self, key):
        data = self.redis.get(key)
        if data is None:
            return False, None

        data = pickle.loads(data)
        if self.encrypted:
            data = cipher.decrypt(data.encode("utf-8")).decode("utf-8")
        else:
            data = b64decode(data).decode("utf-8")

        return True, bz2.decompress(data)

    def set(self, key, value, ttl=None):
        if ttl is None:
            ttl = self.ttl

        compressed_value = bz2.compress(value)
        if self.encrypted:
            value = cipher.encrypt(compressed_value.encode("utf-8")).decode("utf-8")
        else:
            value = b64encode(compressed_value.encode("utf-8")).decode("utf-8")

        self.redis.setex(key, timedelta(seconds=ttl), pickle.dumps(value))

    def delete(self, key):
        self.redis.delete(key)
