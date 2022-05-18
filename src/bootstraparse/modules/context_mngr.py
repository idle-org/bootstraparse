# Interprets where the parser is located and resolves errors
class BaseContainer:
    """
    Creates container holding all the elements from the start of a parsed element to its end.
    """
    def __init__(self):
        self.content = []
        self.optionals = []
        self.map = {}

    def add(self, other):
        self.content.append(other)

    def class_name(self):
        return self.__class__.__name__

    def validate(self, other):
        """
        Takes a list as input and checks if every element is in map.
        :return: Bool
        """
        for o in other:
            if o not in self.map:
                return False
        return True

    def debug_map(self):
        print(f'Debug for {self.class_name()} <{id(self)}>')
        for k, v in self.map.items():
            print(f'{k} = {v}')

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

    def __rshift__(self, other):
        return self.map[other]()

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


class BaseContainerWithOptionals(BaseContainer):
    def __init__(self):
        super().__init__()
        self.map['html_insert'] = self.fetch_html_insert
        self.map['class_insert'] = self.fetch_class_insert

    def fetch_html_insert(self):
        """
        Returns a list of all html_inserts, and an empty list if none exist.
        :rtype: list
        """
        rlist = []
        for o in self.optionals:
            if o.label == 'optional:insert':
                rlist += [o]
        return rlist

    def fetch_class_insert(self):
        """
        Returns a list of all class_inserts, and an empty list if none exist.
        :rtype: list
        """
        rlist = []
        for o in self.optionals:
            if o.label == 'optional:class':
                rlist += [o]
        return rlist

    # def all_html_insert(self):
    #     """
    #     Returns a list of all html_inserts, and an empty list if none exist.
    #     :rtype: list
    #     """
    #     return [o.content for o in self.fetch_html_insert()]
    #
    # def all_class_insert(self):
    #     """
    #     Returns a list of all class_inserts, and an empty list if none exist.
    #     :rtype: list
    #     """
    #     return [o.content for o in self.fetch_class_insert()]


# Define containers all the Enhanced text elements, divs, headers, list and any element that can be a container
class TextContainer(BaseContainer):
    pass


class EtEmContainer(BaseContainer):
    pass


class ContextManager:
    pass
# Defines all methods to manage the context of the parser as a file is being parsed
# Builds all containers as the parser is parsing the file
