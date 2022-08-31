import functools
from exceptions import *
from pyparsing import ParseException
from bson.errors import InvalidId
from mongoengine.errors import ValidationError


def loop_interruption_decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result == None:
            raise LoopInterruptionError
        else:
            return result
    return inner


def errors_handler(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except TagAlreadyExistsError:
            print('Such tag already exists in this note!')
            return inner(*args, **kwargs)
        except TagDoesNotExistError:
            print('Such tag does not exist in this note!')
            return inner(*args, **kwargs)
        except TextDoesNotMatchError:
            print('Such subtext does not exist in the text of the note!')
            return inner(*args, **kwargs)
        except IncorrectChangeTypeError:
            print('Change type must be "t" or "p"!')
            return inner(*args, **kwargs)
        except IncorrectInputType:
            print('ValueError: Please, enter number of changes using integers!')
            return inner(*args, **kwargs)
        except (NoteDoesNotExistError, ValidationError, InvalidId):
            print('Such note does not exist in the note book!')
            return inner(*args, **kwargs)
        except LoopInterruptionError:
            return 'Process was interrupted!'
        except ParseException:
            if func.__qualname__ == 'TopicCreator.topic_creator':
                print('ParseException: Topic must contain alphanums and symbols!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'TagCreator.tag_creator':
                print('ParseException: Tag must contain alphanums and symbols "-", "_", " "!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'TextCreator.text_creator':
                print('ParseException: Text must consist of alphanums and delimiters!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'InterfaceClient.handle_command':
                print('ParseException: Please, enter one of commands to handle with notes database!')
                return inner(*args, **kwargs)
        except KeyError:
            if func.__qualname__.split('.')[0] == 'InterfaceClient':
                print('KeyError: There is no such command among those, that handle with notes database!')
                return inner(*args, **kwargs)
        except ValueError:
            if func.__qualname__ == 'InterfaceClient.handle_command':
                print('ValueError: Please, enter number of notes to be shown using integers!')
                return inner(*args, **kwargs)
    return inner
