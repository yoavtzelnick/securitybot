from securitybot.auth.auth import Auth, AUTH_STATES


class DummyAuth(Auth):
    def __init__(self, auth_api, username):
        # type: (Any, str) -> None
        '''
        Args:
            auth_api: Just to match API
            username (str): Just to match API
        '''
        pass

    def can_auth(self):
        # type: () -> bool
        return True

    def auth(self, reason=None):
        # type: (str) -> None
        pass

    def auth_status(self):
        # type: () -> int
        return AUTH_STATES.AUTHORIZED

    def reset(self):
        # type: () -> None
        pass
