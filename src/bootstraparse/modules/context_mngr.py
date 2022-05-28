# Interprets where the parser is located and resolves errors
# You're probably here for the ContextManager class.
# Containers have class_name, debug_map and validate methods for debug,
#   self.content: accessible via __getitem__, __setitem__, add, __len__, __iter__ and __getslice__.
#   self.optionals: accessible via __rshift__ (remapped to return self.map[other]())
#   and self.map: accessible via __invert__ (remapped to return self.optionals)
# Usage:
#   from bootstraparse.modules.context_mngr import ContextManager
#   ctx = ContextManager()
#   ctx.???
#   container = BaseContainer()
#   container[number] -> The number element in the content
#   "class_insert" >> container[number] -> Get an element from one of the mapped methods


from bootstraparse.modules import syntax
from bootstraparse.modules.error_mngr import MismatchedContainerError, log_exception, log_message  # noqa


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
        if not hasattr(other, "__len__"):
            return False
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

    def print_all(self, ident=''):
        print(ident + self.class_name())
        for e in self:
            if isinstance(e, BaseContainer):
                e.print_all(ident + '  ')
            else:
                print(ident + str(e))

    def to_container(self):
        return self


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


# Define containers all the Enhanced text elements, divs, headers, list and any element that can be a container
class TextContainer(BaseContainer):
    pass


class EtEmContainer(BaseContainer):
    pass


class EtStrongContainer(BaseContainer):
    pass


class EtUnderlineContainer(BaseContainer):
    pass


class EtStrikethroughContainer(BaseContainer):
    pass


class EtCustomSpanContainer(BaseContainer):
    pass


class EtUlistContainer(BaseContainer):
    pass


class EtOlistContainer(BaseContainer):
    pass


class HyperLinkContainer(BaseContainer):
    def __init__(self):
        super().__init__()
        self.map['url']: ""
    pass


# class IlImageContainer(BaseContainer):
#     pass


class SeContainer(BaseContainer):
    pass


class HeaderContainer(BaseContainer):
    def __init__(self):
        super().__init__()
        self.map['header_level'] = ''
    pass


class DisplayContainer(BaseContainer):
    def __init__(self):
        super().__init__()
        self.map['display_level'] = ""
    pass


class TableMainContainer(BaseContainer):
    pass


class TableHeadContainer(BaseContainer):
    def __init__(self):
        super().__init__()
        self.map['colspan'] = ""
    pass


class TableRowContainer(BaseContainer):
    def __init__(self):
        super().__init__()
        self.map['colspan'] = ""
    pass


class TableCellContainer(BaseContainer):
    def __init__(self):
        super().__init__()
        self.map['colspan'] = ""
    pass


class LinebreakContainer(BaseContainer):
    pass


"""
Dictionary of all correspondences between tokens and containers.
"""
_to_container = {
    "text": TextContainer,
    "text:em": EtEmContainer,
    "text:strong": EtStrongContainer,
    "text:underline": EtUnderlineContainer,
    "text:strikethrough": EtStrikethroughContainer,
    "text:custom_span": EtCustomSpanContainer,
    "list:ulist": EtUlistContainer,
    "list:olist": EtOlistContainer,
    "header": HeaderContainer,
    "display": DisplayContainer,
    "se:start:div": SeContainer,
    "se:start:article": SeContainer,
    "se:start:aside": SeContainer,
    "se:start:section": SeContainer,
    "hyperlink": HyperLinkContainer,
    "linebreak": LinebreakContainer,
}


class ContextManager:
    """
    Class in charge of piling all the parsed elements and then encapsulating them inside one another.
    """
    def __init__(self, parsed_list):
        """
        Takes a list of parsed tokens.
        Parameters
        ----------
            parsed_list : list[syntax.SemanticType]
                List of parsed tokens output by our parser.
        """
        self.output = []
        self.parsed_list = parsed_list
        self.pile = []
        self.matched_elements = {}

    def __iter__(self):
        for e in self.pile:
            if e:
                yield e

    def encapsulate(self, start, end):
        """
        Method to encapsulate a number of tokens together as a final container object
        and replace all elements in the pile with None, except the first one which becomes the container.
        Parameters
        ----------
            start : int
                Index of the pile where the encapsulation must begin.
            end : int
                Index of the pile where the encapsulation must end.
        """
        try:
            pile_start = self.pile[start]
            _ = self.pile[end]
            if start > end:
                raise IndexError("Start index must be lower than end index")
        except IndexError:
            log_exception(
                KeyError(f"Indexes ({start}:{end}) must be in the pile range ({len(self.pile)})."),
                level="CRITICAL"
            )
        try:
            container = _to_container[pile_start.label]()
        except KeyError:
            log_exception(
                KeyError(f"Element {self.pile[start].label} not in dictionary of tokens-containers correspondences."),
                level="CRITICAL"
            )
        for i in range(start, end):
            if self.pile[i]:
                container.add(self.pile[i].to_container())
                self.pile[i] = None
        container.add(self.pile[end])
        self.pile[end] = None
        self.pile[start] = container

    def _add_matched(self, label, index):
        if label not in self.matched_elements:
            self.matched_elements[label] = []
        self.matched_elements[label] += [index]

    def _get_matched(self, label):
        return self.matched_elements[label].pop()

    def __call__(self):
        """
        Interprets the list of tokens provided and deduces context, encapsulating them to their closest neighbour and
        containing all tokens inbetween.
        Returns
        -------
            list[BaseContainer]
                Returns the pile entirely processed as a list of containers.
        """
        # self.pile = self.parsed_list.copy()
        line_number = 1
        for index, token in enumerate(self.parsed_list):
            token.line_number = line_number
            self.pile.append(token)
            try:
                if isinstance(token, syntax.Linebreak):
                    self.encapsulate(index, index)
                    line_number += 1
                elif isinstance(token, syntax.FinalSemanticType):
                    self.encapsulate(index, index)
                elif token.counterpart() in self.matched_elements:
                    self.encapsulate(self._get_matched(token.counterpart()), index)
                elif isinstance(token, syntax.ClosedSemanticType):
                    raise MismatchedContainerError(token)
                else:
                    self._add_matched(token.label, index)

            except MismatchedContainerError as e:
                print(e)

    def print_all(self):
        for e in self:
            if isinstance(e, BaseContainer):
                e.print_all()
            else:
                print(str(e))


# Defines all methods to manage the context of the parser as a file is being parsed
# Builds all containers as the parser is parsing the file


if __name__ == "__main__":  # pragma: no cover
    from bootstraparse.modules import parser
    from io import StringIO
    io_string = StringIO(
        """<<div
        Hello world
        *how do you do fellow **kids***
        div>>
        # header 1 #
        ! display 1 !"""
    )

    test = parser.parse_line(io_string)
    ctx = ContextManager(test)
    ctx()
    print('----------------------------------')
    ctx.print_all()
