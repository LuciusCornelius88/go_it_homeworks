import functools


def input_error_decorator(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            value = func(*args, **kwargs)
            return value
        except AttributeError:
            print(
                'Please, enter correct arguments: name or name and phone, separated by 1 space!')
            return None
        except KeyError:
            print('Please, enter the correct command among: hello, add, change, phone, show all, good bye, close, exit')
            return None
        except IndexError:
            print('Please, enter the correct command among: hello, add, change, phone, show all, good bye, close, exit')
            return None
        except ValueError:
            print('''If you''are trying to add a new_contact, so the contact with this name already exists! 
                     If you''are trying to change or get the existing contact, so the contact with this name does not exist!''')
            return None

    return inner
