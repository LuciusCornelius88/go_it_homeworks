import pickle
from collections import UserDict
from copy import deepcopy
from notes_manager.code.decorators import errors_handler
from notes_manager.code.abstract_methods import GetComponents, AddComponents, DeleteComponents, \
    RepresentObjects
from notes_manager.code.exceptions import LoopInterruptionError, NoteDoesNotExistError
from notes_manager.code.notes_classes import Note, NoteCreator
from notes_manager.code.components_creators import TagCreator, TopicCreator


class NoteBook(UserDict):

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.iterator = NoteBookIterator(self)
        self.serializer = NoteBookSerializer(self, filepath)
        self.sorter = NotesSorter(self)

    @errors_handler
    def add_note(self) -> str:
        adder = NoteAdder(self)
        adder.add()
        return 'Note was successfully added!'

    @errors_handler
    def delete_note(self) -> str:
        deleter = NoteDeleter(self)
        deleter.delete()
        return 'Note was successfully deleted!'

    @errors_handler
    def get_note(self) -> Note:
        getter = NoteGetter(self)
        return getter.get()

    @errors_handler
    def sort_notes_by_topic(self) -> str:
        return self.sorter.sort_by_topic()

    @errors_handler
    def sort_notes_by_tag(self) -> str:
        return self.sorter.sort_by_tag()

    def show_all(self) -> str:
        return str(self) if self.data else 'There is no notes yet in note book!'

    def save_to_file(self) -> str:
        self.serializer.update(self)
        self.serializer.serialize()
        return 'Note book was successfully saved to file!'

    def restore_from_file(self):
        return self.serializer.deserialize()

    @errors_handler
    def iterate(self) -> list:
        self.iterator.update(self)
        return self.iterator.iterate()

    def __deepcopy__(self, memo):
        copy_obj = self.__class__(self.filepath)
        memo[id(copy_obj)] = copy_obj
        copy_obj.data = deepcopy(self.data)
        return copy_obj

    def __repr__(self) -> str:
        representer = NoteBookRepresenter(self)
        return representer.represent()

    def __str__(self) -> str:
        return self.__repr__()


# Getters

# NoteDoesNotExistError(KeyError)
class NoteGetter(GetComponents):

    def __init__(self, note_book: NoteBook):
        self.note_book = note_book

    def get(self):
        note_id = input(
            'Please, give me note_id or enter "###" to exit the loop: ')
        if note_id == '###':
            raise LoopInterruptionError
        elif note_id not in self.note_book.data:
            raise NoteDoesNotExistError
        else:
            return self.note_book.data[note_id]


# Adders

# LoopInterruptionError
class NoteAdder(AddComponents):

    def __init__(self, note_book: NoteBook):
        self.note_book = note_book
        self.note_creator = NoteCreator()
        self.note = None

    def create_note(self) -> Note:
        self.note_creator.create_topic()
        self.note_creator.create_text()
        self.note_creator.create_tag()
        return self.note_creator.get_note()

    def add(self):
        self.note = self.create_note()
        key = self.note.id
        self.note_book.data[key] = self.note


# Deleters

# NoteDoesNotExistError(KeyError)
class NoteDeleter(DeleteComponents):

    def __init__(self, note_book: NoteBook):
        self.note_book = note_book

    def delete(self):
        note_id = input(
            'Please, give me note_id or enter "###" to exit the loop: ')
        if note_id == '###':
            raise LoopInterruptionError
        elif note_id not in self.note_book.data:
            raise NoteDoesNotExistError
        else:
            del self.note_book.data[note_id]


# Sorters

class NotesSorter:

    def __init__(self, note_book: NoteBook):
        self.note_book = note_book

    def sort_by_topic(self):
        topic = TopicCreator().create()

        notes = list(self.note_book.values())
        matched_notes = list(
            filter(lambda note: note.topic.value == topic.value, notes))

        return '\n'.join([str(note) for note in matched_notes]) if matched_notes else f'There is no note with topic {topic}!'

    def sort_by_tag(self):
        tag = TagCreator().create()

        notes = list(self.note_book.values())
        matched_notes = list(filter(lambda note: tag.value in [
                             tag.value for tag in note.tags], notes))

        return '\n'.join([str(note) for note in matched_notes]) if matched_notes else f'There is no note with tag {tag}!'


# Serializer

class NoteBookSerializer:

    def __init__(self, note_book: NoteBook, filepath):
        self.note_book = note_book
        self.filepath = filepath

    def update(self, note_book: NoteBook):
        self.note_book = note_book

    def serialize(self):
        with open(self.filepath, 'w+b') as file:
            pickle.dump(self.note_book, file)

    def deserialize(self):
        with open(self.filepath, 'r+b') as file:
            return deepcopy(pickle.load(file))


# Iterator

# ValueError
class NoteBookIterator:

    def __init__(self, note_book: NoteBook):
        self.note_book = note_book
        self.iter_index = 0

    def update(self, note_book: NoteBook):
        self.note_book = note_book

    def __next__(self):
        keys = list(self.note_book.data.keys())
        if self.iter_index <= len(self.note_book.data)-1:
            self.iter_index += 1
            index = keys[self.iter_index-1]
            return self.note_book.data[index]
        else:
            self.iter_index = 0
        raise StopIteration

    def __iter__(self):
        return self

    def iterate(self) -> list:
        list_of_notes = []
        n_iterations = int(
            input('Please, enter number of notes, that are to be shown: '))

        for _ in range(n_iterations):
            try:
                list_of_notes.append(next(self))
            except StopIteration:
                if not list_of_notes and len(self.list_of_notes.data) > 0:
                    list_of_notes.append(next(self))
                    continue
                else:
                    break

        notes_to_str = ''.join(
            map(lambda note: str(note), list_of_notes))
        return notes_to_str if notes_to_str else 'There is no note yet in address book!'


# Representers

class NoteBookRepresenter(RepresentObjects):

    def __init__(self, note_book: NoteBook):
        self.note_book = note_book

    def represent(self) -> str:
        string = ''
        notes = list(self.note_book.data.values())

        for note in notes:
            string += f'{note}\n'

        return string if string else 'There is no note in note book yet!'
