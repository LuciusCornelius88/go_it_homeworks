from abc import ABC, abstractmethod
from pyparsing import *


class Parser(ABC):

    @abstractmethod
    def create_parser(self):
        pass

    @abstractmethod
    def parse_string(self):
        pass


class TopicParser(Parser):

    def __init__(self):
        self.__string = None
        self.parser = self.create_parser()

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, new_value):
        self.__string = new_value

    def create_parser(self):
        cyril_symbols = ''.join([chr(i) for i in range(
            1040, 1104)] + [chr(1108), chr(1110), chr(1111)])
        raw_symbols = Word(
            printables + ' ', excludeChars=alphanums).leaveWhitespace()
        unified_symbol = raw_symbols.setParseAction(replaceWith('_'))

        topic_parser = Word(alphanums + cyril_symbols) + \
            ZeroOrMore(Suppress(unified_symbol) +
                       Word(alphanums + cyril_symbols))

        return topic_parser

    # ParseException
    def parse_string(self) -> str:
        topic = self.parser.parseString(self.string).asList()
        topic = ' '.join([t.strip() for t in topic])
        topic = topic.replace(topic[0], topic[0].upper(), 1)
        return topic


class TagParser(Parser):

    def __init__(self):
        self.__string = None
        self.parser = self.create_parser()

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, new_value):
        self.__string = new_value

    def create_parser(self):
        raw_symbols = Word('- _').leaveWhitespace()
        tag_parser = Word(alphanums) + \
            ZeroOrMore(raw_symbols + Word(alphanums))
        return tag_parser

    # ParseException
    def parse_string(self) -> str:
        tag = self.parser.parseString(self.string).asList()
        tag = ' '.join(t.strip() for t in tag if t[0] != ' ')
        tag = tag.replace(tag[0], tag[0].upper(), 1)
        return tag


class TextParser(Parser):

    def __init__(self):
        self.__string = None
        self.parser = self.create_parser()

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, new_value):
        self.__string = new_value

    def create_parser(self):
        end_symbols = Word('.!? ').leaveWhitespace()
        non_end_symbols = Word(',;:-() ').leaveWhitespace()
        sentence_parser = OneOrMore(
            Word(alphanums) + Optional(non_end_symbols)) + Optional(end_symbols)
        text_parser = ZeroOrMore(sentence_parser)
        return text_parser

    def create_string(self, text_list: list, ignore_case: bool):
        sentence = []
        sentences = []
        text = []

        # create sublists, that consist of items within one sentence
        for item in text_list:
            sentence.append(item)
            if item[0] in '.!?':
                sentences.append(sentence)
                sentence = []

        # if last sentence has no no stop mark, we also add this sentence to list of sentences
        if sentence:
            sentences.append(sentence)

        # delete spaces in all items in each sentence, remove empty items, join items regarding the rules
        # for different punctuation marks
        for sentence in sentences:
            sentence = [s.strip() for s in sentence]

            for value in sentence:
                if not value:
                    sentence.remove(value)

            sentence_str = sentence[0] if sentence else ''

            for count, value in enumerate(sentence[1:]):
                if value[0] in '-).!?,;:' or sentence_str[-1] in '(-':
                    sentence_str += value
                else:
                    sentence_str += (' ' + value)

            if ignore_case:
                text.append(sentence_str)
            else:
                text.append(sentence_str.replace(
                    sentence_str[0], sentence_str[0].upper(), 1))

        return ' '.join(text)

    # ParseException
    def parse_string(self, ignore_case) -> str:
        text_list = self.parser.parseString(self.string).asList()
        text_str = self.create_string(text_list, ignore_case)
        return text_str


class CommandsParser(Parser):

    def __init__(self, string: str):
        self.string = string
        self.parser = self.create_parser()

    def create_parser(self):
        raw_delimiter = Word(
            printables + ' ', excludeChars=alphas).leaveWhitespace()
        unified_delimiter = raw_delimiter.setParseAction(replaceWith('_'))

        parser = Word(alphas) + \
            ZeroOrMore(Suppress(unified_delimiter) + Word(alphas))
        low_cased_parser = parser.setParseAction(
            lambda t: [i.lower() for i in t.asList()])

        return low_cased_parser

    # ParseException
    def parse_string(self) -> list:
        self.parser.transformString(self.string)
        string_items = self.parser.parseString(self.string, parseAll=True)

        return string_items
