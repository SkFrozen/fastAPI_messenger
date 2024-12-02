class AuthError(Exception):
    pass


class InvalidTokenError(AuthError):
    pass


class UserAlreadyExist(AuthError):
    pass


class UserDoesNotExist(AuthError):
    pass


class InvalidCredentialsError(AuthError):
    pass
