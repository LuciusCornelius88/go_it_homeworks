from abc import ABC, abstractmethod
from notes_manager.code.decorators import loop_interruption_decorator, errors_handler
from notes_manager.code.parsers import TopicParser, TagParser, TextParser
from notes_manager.code.components import Topic, Text, Tag


class ComponentsCreator(ABC):

    @abstractmethod
    def create(self):
        pass


class TopicCreator(ComponentsCreator):

    def __init__(self):
        self.default_value = 'Topic'
        self.parser = TopicParser()

    @errors_handler
    def topic_creator(self) -> Topic:
        input_topic = input(
            'Please, enter topic or enter "***" to set topic to default value or enter "###" to exit the loop: ')
        if input_topic == '###':
            return None
        elif input_topic == '***':
            self.parser.string = self.default_value
        else:
            self.parser.string = input_topic

        topic_value = self.parser.parse_string()
        return Topic(topic_value)

    @loop_interruption_decorator
    def create(self) -> Topic:
        return self.topic_creator()


class TagCreator(ComponentsCreator):

    def __init__(self):
        self.default_value = 'tag'
        self.parser = TagParser()

    @errors_handler
    def tag_creator(self) -> Tag:
        input_tag = input(
            'Please, enter tag or enter "***" to set tag to default value or enter "###" to exit the loop: ')
        if input_tag == '###':
            return None
        elif input_tag == '***':
            self.parser.string = self.default_value
        else:
            self.parser.string = input_tag

        tag_value = self.parser.parse_string()
        return Tag(tag_value)

    @loop_interruption_decorator
    def create(self) -> Tag:
        return self.tag_creator()


class TextCreator(ComponentsCreator):

    def __init__(self):
        self.default_value = 'Text'
        self.parser = TextParser()
        self.max_length = 200

    @errors_handler
    def text_creator(self, ignore_case) -> Text:
        input_text = input(
            f'''Please, enter text or enter "***" to set text to default value or enter "###" to exit the loop.
                Take note, that the maximal length of the text is {self.max_length} chars: ''')
        if input_text == '###':
            return None
        elif input_text == '***':
            self.parser.string = self.default_value
        else:
            self.parser.string = input_text[:self.max_length]
        text_value = self.parser.parse_string(ignore_case)
        return Text(text_value)

    @loop_interruption_decorator
    def create(self, ignore_case=False) -> Text:
        return self.text_creator(ignore_case)
