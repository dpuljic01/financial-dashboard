from server.common.cache import Cache


class BlacklistTokensImpl:
    def __init__(self):
        self._revoked_store = None

    @property
    def revoked_store(self):
        if not self._revoked_store:
            self._revoked_store = Cache()
        return self._revoked_store

    def check_revoked(self, decrypted_token):
        """
        Check if a token has been blacklisted. In this simple
        case, we will just store the tokens jti (unique identifier) in redis
        whenever we create a new token (with the revoked status being 'false'). This
        function will return the revoked status of a token. If a token doesn't
        exist in this store, we don't know where it came from (as we are adding newly
        created tokens to our store with a revoked status of 'false'). In this case
        we will consider the token to be revoked, for safety purposes.
        """
        jti = decrypted_token["jti"]
        entry = ("false", False)
        try:
            entry = self.revoked_store.get(jti)
        except:
            pass

        if entry is None:
            return True
        return "true" in entry


BlacklistTokens = BlacklistTokensImpl()
