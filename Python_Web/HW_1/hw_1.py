import pickle
import json
from copy import deepcopy
from abc import abstractmethod, ABC


class SerializationInterface(ABC):
    def __init__(self, data, filepath):
        self.data = data
        self.filepath = filepath

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass


class JsonData(SerializationInterface):
    def __init__(self, data, filepath):
        super().__init__(data, filepath)

    def serialize(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.data, file)

    def deserialize(self):
        with open(self.filepath, 'r') as file:
            return JsonData(json.load(file), self.filepath)


class BinData(SerializationInterface):
    def __init__(self, data, filepath):
        super().__init__(data, filepath)

    def serialize(self):
        with open(self.filepath, 'w+b') as file:
            pickle.dump(self, file)

    def deserialize(self):
        with open(self.filepath, 'r+b') as file:
            return deepcopy(pickle.load(file))

    def __deepcopy__(self, memo):
        copy = BinData(self.data, self.filepath)
        memo[id(copy)] = copy
        copy.data = deepcopy(self.data)
        copy.filepath = deepcopy(self.filepath)
        return copy
