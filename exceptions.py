class GetApiAnswerError(Exception):
    """Нет доступа к эндпоинту."""
    pass


class NoResponseError(Exception):
    """Нет ответа от API."""
    pass


class UndocumentedStatusError(Exception):
    """Не существующий статус домашней работы."""
    pass
