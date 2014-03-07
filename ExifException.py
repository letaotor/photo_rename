class ExifException(Exception):
    pass


class UnknownAlign(ExifException):
    def __str__(self):
        return "UnknownAlign"
