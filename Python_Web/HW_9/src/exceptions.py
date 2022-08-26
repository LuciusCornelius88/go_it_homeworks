class PhoneAlreadyExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class PhoneDoesNotExistError(Exception):
    pass


class EmailDoesNotExistError(Exception):
    pass


class AddressAlreadyExistsError(Exception):
    pass


class AddressDoesNotExistError(Exception):
    pass


class RecordAlreadyExistsError(Exception):
    pass


class RecordDoesNotExistError(KeyError):
    pass


class LoopInterruptionError(Exception):
    pass


class EmailLengthException(Exception):
    pass
