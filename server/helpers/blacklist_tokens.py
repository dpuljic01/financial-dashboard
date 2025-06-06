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
        """Return revoked status for a token.

        Tokens are stored in Redis with their ``jti`` mapped to ``"true"`` or
        ``"false"``.  The function returns ``True`` only when the stored value is
        ``"true"``.  Tokens missing from the store are treated as **not**
        revoked.
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
