class Component:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Topic(Component):

    def __init__(self, topic: str):
        super().__init__(topic)

    @Component.value.setter
    def value(self, new_value):
        Component.value.fset(self, new_value)

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()


class Text(Component):
    
    def __init__(self, text: str):
        super().__init__(text)
        
    @Component.value.setter
    def value(self, new_value):
        Component.value.fset(self, new_value)

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()


class Tag(Component):

    def __init__(self, tag: str):
        super().__init__(tag)

    @Component.value.setter
    def value(self, new_value):
        Component.value.fset(self, new_value)

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()
