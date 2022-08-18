class TagAlreadyExistsError(Exception):
    pass


class TagDoesNotExistError(Exception):
    pass


class TextDoesNotMatchError(Exception):
    pass


class IncorrectChangeTypeError(Exception):
    pass


class NoteDoesNotExistError(Exception):
    pass


class LoopInterruptionError(Exception):
    pass