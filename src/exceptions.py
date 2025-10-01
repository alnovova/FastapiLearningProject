class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __int__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"

class WrongDateOrderException(NabronirovalException):
    detail = "Дата выезда раньше даты заезда"
