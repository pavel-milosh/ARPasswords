from ..exceptions import ARPasswordsException


class DatabaseException(ARPasswordsException):
    pass


class LabelNotUnique(DatabaseException):
    pass
