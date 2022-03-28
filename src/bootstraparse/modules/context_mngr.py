# Interprets where the parser is located and resolves errors
class BaseContainer:
    """
    Creates container holding all the elements from the start of a parsed element to its end.
    """
    def __init__(self):
        self.content = []
        self.optionals = []

    def add(self, other):
        self.content.append(other)

    def class_name(self):
        return self.__class__.__name__

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        for content in self.content:
            yield content

    def __getitem__(self, item):
        return self.content[item]

    def __setitem__(self, key, value):
        self.content[key] = value

    def __getslice__(self, start, end):
        return self.content[start:end]

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for e, f in zip(self, other):
            if e != f:
                return False
        return True

    def __invert__(self):
        return self.optionals

    def __str__(self):
        return '{} ({})'.format(", ".join(map(str, self.content)),
                                ", ".join(map(str, self.optionals)) if self.optionals != [] else "")

    def __repr__(self):
        representation = {}
        for content in self.content:
            if type(content) in representation:
                representation[type(content)] += 1
            else:
                representation[type(content)] = 1
        return "{}({})".format(
            self.class_name(),
            ", ".join(
                [f'{index.__name__}: {value}' for index, value in representation.items()]
            )
        )


# Define containers all the Enhanced text elements, divs, headers, list and any element that can be a container
class TextContainer(BaseContainer):
    pass


class EtEmContainer(BaseContainer):
    pass


class ContextManager:
    pass
# Defines all methods to manage the context of the parser as a file is being parsed
# Builds all containers as the parser is parsing the file
