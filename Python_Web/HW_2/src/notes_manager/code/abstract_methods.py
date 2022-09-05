from abc import ABC, abstractmethod


class GetComponents(ABC):

    @abstractmethod
    def get(self):
        pass

    
class AddComponents(ABC):

    @abstractmethod
    def add(self):
        pass


class ChangeComponents(ABC):

    @abstractmethod
    def change(self):
        pass


class DeleteComponents(ABC):

    @abstractmethod
    def delete(self):
        pass 


class RepresentObjects(ABC):

    @abstractmethod
    def represent(self):
        pass