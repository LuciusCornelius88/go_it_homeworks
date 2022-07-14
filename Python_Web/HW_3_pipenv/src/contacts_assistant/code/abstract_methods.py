# abstract classes (interfaces) for classes, that handle with fields and methods of Records and AddressBook

from abc import ABC, abstractmethod


class AddFields(ABC):

    @abstractmethod
    def add(self):
        pass


class ChangeFields(ABC):

    @abstractmethod
    def change(self):
        pass


class DeleteFields(ABC):

    @abstractmethod
    def delete(self):
        pass


class SearchInFields(ABC):

    @abstractmethod
    def search(self):
        pass


class GetFields(ABC):

    @abstractmethod
    def get(self):
        pass


class RepresentObjects(ABC):

    @abstractmethod
    def represent(self):
        pass
