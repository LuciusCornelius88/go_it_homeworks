import functools
from exceptions import *
from pyparsing import ParseException


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
        except PhoneAlreadyExistsError:
            print('Such phone number already exists!')
            return inner(*args, **kwargs)
        except EmailAlreadyExistsError:
            print('Such email already exists!')
            return inner(*args, **kwargs)
        except PhoneDoesNotExistError:
            print('Such phone number does not exist!')
            return inner(*args, **kwargs)
        except EmailDoesNotExistError:
            print('Such email does not exist!')
            return inner(*args, **kwargs)
        except RecordAlreadyExistsError:
            print('Such record already exists!')
            return inner(*args, **kwargs)
        except RecordDoesNotExistError:
            print('Such record does not exist!')
            return inner(*args, **kwargs)
        except AddressAlreadyExistsError:
            print('Such address already exists!')
            return inner(*args, **kwargs)
        except AddressDoesNotExistError:
            print('Such address does not exist!')
            return inner(*args, **kwargs)
        except EmailLengthException:
            print('Length of local-part of email must be <= 64 chars!')
            return inner(*args, **kwargs)
        except LoopInterruptionError:
            print('Process was interrupted!')
            # return 'Process was interrupted!'
        except ParseException:
            if func.__qualname__ == 'NameCreator.name_creator':
                print(
                    'ParseException: Name must contain alphas, nums and some separators!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'PhoneCreator.phone_creator':
                print(
                    'ParseException: Phone number must contain chars and some special symbols!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'EmailCreator.email_creator':
                print('ParseException: Please, enter email in correct form!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'BirthdayCreator.birthday_creator':
                print(
                    'ParseException: Date must contain integers and delimiters in form "dd mm yyy"')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'AddressCreator.city_creator':
                print('ParseException: Please, enter name of the city!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'AddressCreator.street_creator':
                print(
                    'ParseException: Please, enter name of the street, that must contain printables!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'AddressCreator.house_number_creator':
                print(
                    'ParseException: Please, enter house number, that must contain integers and some special symbols!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'AddressCreator.appartament_creator':
                print(
                    'ParseException: Please, enter your flat number, that must contain integers and some special symbols!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'AddressCreator.zip_code_creator':
                print(
                    'ParseException: Please, enter your zip code, that must contain only integers!')
                return inner(*args, **kwargs)
            if func.__qualname__ == 'InterfaceClient.handle_command':
                print(
                    'ParseException: Please, enter one of commands to handle with database!')
                return inner(*args, **kwargs)
        except KeyError:
            if func.__qualname__.split('.')[0] == 'InterfaceClient':
                print('KeyError: There is no such command among commands!')
                return inner(*args, **kwargs)
        except ValueError:
            if func.__qualname__ == 'main':
                print('ValueError: Please, enter number of days using integers!')
                return inner(*args, **kwargs)
    return inner
