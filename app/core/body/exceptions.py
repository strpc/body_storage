from app.core.exceptions import AppError


class BodyError(AppError):
    pass


class BodyNotFound(BodyError):
    msg_template = "body with key {key} not finded"
