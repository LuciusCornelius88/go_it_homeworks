import uuid
from datetime import datetime
from notes_manager.code.decorators import errors_handler, loop_interruption_decorator
from notes_manager.code.abstract_methods import AddComponents, ChangeComponents, DeleteComponents, \
    RepresentObjects
from notes_manager.code.components_creators import TopicCreator, TextCreator, TagCreator
from notes_manager.code.exceptions import TagAlreadyExistsError, TagDoesNotExistError, \
    TextDoesNotMatchError, IncorrectChangeTypeError


class Note:

    def __init__(self):
        self.tags = []
        self.updates = {}
        self.topic = None
        self.text = None
        self.id = str(uuid.uuid4())
        self.creation_time = self.set_time()

    @errors_handler
    def change_topic(self):
        changer = TopicChanger(self)
        return changer.change()

    @errors_handler
    def change_text(self):
        changer = TextChanger(self)
        return changer.change()

    def delete_text(self):
        deleter = TextDeleter(self)
        return deleter.delete()

    @errors_handler
    def add_tag(self):
        adder = TagAdder(self)
        return adder.add()

    @errors_handler
    def change_tag(self):
        changer = TagChanger(self)
        return changer.change()

    @errors_handler
    def delete_tag(self):
        deleter = TagDeleter(self)
        return deleter.delete()

    def set_time(self):
        return datetime.now().isoformat(sep=' ', timespec='seconds')

    def update(self, component, action: str):
        update_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        self.updates[update_time] = ' >>> '.join(
            [action, type(component).__name__, component.value])

    def get_updates(self) -> str:
        return_str = ''
        for key, val in self.updates.items():
            return_str += f'{key} : {val}\n'
        return return_str

    def __repr__(self):
        representer = NoteRepresenter(self)
        return representer.represent()

    def __str__(self):
        return self.__repr__()


# Adders

class TagAdder(AddComponents):

    def __init__(self, note: Note):
        self.note = note
        self.tag_creator = TagCreator()
        self.tag = None

    # TagAlreadyExistsError
    def add(self):
        self.tag = self.tag_creator.create()
        if self.tag.value in list(map(lambda tag: tag.value, self.note.tags)):
            raise TagAlreadyExistsError
        self.note.tags.append(self.tag)
        self.note.update(self.tag, self.add.__name__)

        return f'Tag {self.tag.value} was added to note {self.note.topic.value}, id: {self.note.id}.'


# Changers

class TagChanger(ChangeComponents):

    def __init__(self, note: Note):
        self.note = note
        self.tag_creator = TagCreator()
        self.old_tag = None
        self.new_tag = None
        self.return_string = None

    def redefine_attrs(self):
        self.old_tag = self.old_tag_setter()
        print(f'Old tag: {self.old_tag.value}')
        self.new_tag = self.tag_creator.create()
        print(f'New tag: {self.new_tag.value}')
        self.return_string = (f'Tag {self.old_tag.value} was replaced with tag {self.new_tag.value} ' +
                              f'for note {self.note.topic.value}, id: {self.note.id}.')

    # TagDoesNotExistError
    def old_tag_setter(self):
        old_tag = self.tag_creator.create()
        tag_matched = list(
            filter(lambda tag: tag.value == old_tag.value, self.note.tags))
        if not tag_matched:
            raise TagDoesNotExistError
        return tag_matched[0]

    def change(self):
        self.redefine_attrs()
        index = self.note.tags.index(self.old_tag)
        self.note.tags[index] = self.new_tag
        self.note.update(self.new_tag, self.change.__name__)
        return self.return_string


class TopicChanger(ChangeComponents):

    def __init__(self, note: Note):
        self.note = note
        self.topic_creator = TopicCreator()
        self.old_topic = self.note.topic
        self.new_topic = None

    def change(self):
        self.new_topic = self.topic_creator.create()
        self.note.topic = self.new_topic
        self.note.update(self.new_topic, self.change.__name__)
        return f'''Topic {self.old_topic.value} was replaced with topic {self.new_topic.value},
                   for note {self.note.id}.'''


class TextChanger(ChangeComponents):

    def __init__(self, note: Note):
        self.note = note
        self.text_creator = TextCreator()
        self.old_text = None
        self.new_text = None
        self.return_string = None

    def redefine_attrs(self):
        self.old_text = self.old_text_setter()
        print(f'Old text: {self.old_text.value}')
        self.new_text = self.text_creator.create(ignore_case=True)
        print(f'New text: {self.new_text.value}')
        self.return_string = (f'Text "{self.old_text.value}" was replaced with text ' +
                              f'"{self.new_text.value}" for note {self.note.topic.value}, id: {self.note.id}.')

    # TextDoesNotExistError
    def old_text_setter(self):
        old_text = self.text_creator.create(ignore_case=True)
        if old_text.value not in self.note.text.value:
            raise TextDoesNotMatchError
        return old_text

    # ValueError
    # LoopInterruption
    def replaces(self):
        n_replaces = input('''How many times given string have to be replaced with a new one? Enter "0" if all. 
                              Enter "###" to interrupt the loop: ''')
        try:
            return int(n_replaces)
        except:
            if n_replaces == '###':
                return n_replaces
            else:
                raise ValueError

    @errors_handler
    def check_replaces(self):
        return self.replaces()

    @errors_handler
    def partial_change(self):
        self.redefine_attrs()
        n_replaces = self.check_replaces()

        if n_replaces == 0:
            self.note.text.value = self.note.text.value.replace(
                self.old_text.value, self.new_text.value)
        elif n_replaces == '###':
            return None
        else:
            self.note.text.value = self.note.text.value.replace(
                self.old_text.value, self.new_text.value, n_replaces)

        self.note.update(self.new_text, self.partial_change.__name__)
        return self.return_string

    def total_change(self):
        self.new_text = self.text_creator.create()
        self.note.text = self.new_text
        self.note.update(self.new_text, self.total_change.__name__)
        return f'Text was replaced with new text for note {self.note.topic.value}, id: {self.note.id}.'

    # IncorrectChangeTypeError
    # LoopInterruption

    def get_change_type(self):
        change_type = input('''Please, specify the type of change: "p" for "partial change" or "t" for "total change". 
                               Or insert "###" to exit the loop: ''').lower()
        if change_type == '###':
            return None
        elif change_type == 'p':
            return self.partial_change()
        elif change_type == 't':
            return self.total_change()
        else:
            raise IncorrectChangeTypeError

    @errors_handler
    def handle_incorrect_change(self):
        return self.get_change_type()

    @loop_interruption_decorator
    def change(self):
        return self.handle_incorrect_change()


# Deleters

class TextDeleter(DeleteComponents):

    def __init__(self, note: Note):
        self.note = note

    def delete(self):
        self.note.text.value = ''
        self.note.update(self.note.text, self.delete.__name__)
        return f'Text for note {self.note.topic}, id: {self.note.id} was deleted!'


class TagDeleter(DeleteComponents):

    def __init__(self, note: Note):
        self.note = note
        self.tag_creator = TagCreator()
        self.tag = None

    def delete(self):
        self.tag = self.tag_creator.create()
        tag_matched = list(filter(lambda tag: tag.value ==
                           self.tag.value, self.note.tags))
        if not tag_matched:
            raise TagDoesNotExistError
        self.note.tags.remove(tag_matched[0])
        self.note.update(self.tag, self.delete.__name__)
        return f'Tag {self.tag.value} in note {self.note.topic.value}, id: {self.note.id} was succesfully deleted.'


# Representers

class NoteRepresenter(RepresentObjects):

    def __init__(self, note: Note):
        self.note = note
        self.tags = self.represent_tags()

    def represent_tags(self) -> str:
        tags = 'Tags: '
        length = len(tags)
        for tag in self.note.tags:
            if self.note.tags.index(tag) == 0 and len(self.note.tags) > 1:
                tags += '{:<5}\n'.format(str(tag))
            elif self.note.tags.index(tag) == 0 and len(self.note.tags) <= 1:
                tags += '{:<5}'.format(str(tag))
            elif self.note.tags.index(tag) == len(self.note.tags)-1:
                tags += (' ')*length + '{:<5}'.format(str(tag))
            else:
                tags += (' ')*length + '{:<5}\n'.format(str(tag))
        return tags

    def create_title(self):
        string = ''
        title = f'|Note with id {self.note.id}:|\n'
        spaces = '|' + ' ' * (len(title)-3) + '|\n'
        upper_dash = ' ' + '_' * (len(title)-3) + '\n'
        lower_dash = '|' + '_' * (len(title)-3) + '|\n\n'
        string += upper_dash + spaces + title + lower_dash

        return string

    def represent(self) -> str:
        title = self.create_title()

        note_represantation = (f'Topic: {self.note.topic}\n\n' +
                               f'Text:\n{self.note.text}\n\n' +
                               f'{self.tags}\n\n' +
                               f'Creation time: {self.note.creation_time}\n')
        return title + note_represantation


# Note_Creator

class NoteCreator:

    def __init__(self):
        self.__note = Note()
        self.topic_creator = TopicCreator()
        self.text_creator = TextCreator()
        self.tag_creator = TagCreator()

    def create_topic(self):
        self.__note.topic = self.topic_creator.create()

    def create_text(self):
        self.__note.text = self.text_creator.create()

    def create_tag(self):
        tag = self.tag_creator.create()
        self.__note.tags.append(tag)

    def get_note(self) -> Note:
        return self.__note
