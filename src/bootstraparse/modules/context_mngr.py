# Interprets where the parser is located and resolves errors
# You're probably here for the ContextManager class.
# Containers have class_name, debug_map and validate methods for debug,
#   self.content: accessible via __getitem__, __setitem__, add, __len__, __iter__ and __getslice__.
#   self.optionals: accessible via __rshift__ (remapped to return self.map[other]())
#   and self.map: accessible via __invert__ (remapped to return self.optionals)
# Usage:
#   from bootstraparse.modules.context_mngr import ContextManager
#   ctx = ContextManager()
#   container = BaseContainer()
#   container[number] -> The number element in the content
#   "class_insert" >> container[number] -> Get an element from one of the mapped methods

from bootstraparse.modules import syntax, error_mngr, export
from bootstraparse.modules.error_mngr import MismatchedContainerError, log_exception, log_message, LonelyOptionalError # noqa


class BaseContainer:
    """
    Creates container holding all the elements from the start of a parsed element to its end.
    """
    type = None
    subtype = None

    def __init__(self, content=None, optionals=None, others=None):
        """
        :param content: List of tokens to be added to the container
        :param optionals: List of optional tokens to be added to the container (from the parser)
        :param others: List of values to add to the .format() method
        :type content: (list[(syntax.SemanticType | BaseContainer)])
        :type optionals: (syntax.SemanticType)
        :type others: (dict[str, str])
        """
        if content is None:
            content = []
        if others is None:
            self.others = {}
        self.content = content
        self.map = {}
        self.optionals = optionals
        self.indentation_level = 0  # future: add an indentation level to every token for human readability of the final output

    def get_content(self, exm, arbitrary_list=None):
        """
        Get the content of any BaseContainer object (default self.content).
        :param exm: ExportManager to use for exporting
        :param arbitrary_list: List to get the content from
        :type exm: export.ExportManager
        :type arbitrary_list: list[BaseContainer]
        :rtype : str
        """
        output = ""
        if not arbitrary_list:
            arbitrary_list = self.content
        for element in arbitrary_list:
            if isinstance(element, BaseContainer):
                output += element.export(exm) + " "
        return output[:-1]

    def get_optionals(self):
        """
        Get the optionals of the container.
        :rtype : (syntax.SemanticType | BaseContainer)
        :return: The optionals of the container
        """
        return self.optionals

    def get_others(self):
        """
        Get the other values of the container.
        :rtype : dict[str, str]
        :return: The other values of the container
        """
        return self.others

    def export(self, exm):
        """
        Export the container to a string.
        :type exm: export.ExportManager
        :rtype : str
        """
        start, end = exm(export.ExportRequest(self.type, self.subtype, self.get_optionals(), self.get_others()))

        output = start + self.get_content(exm) + end

        return output

    def add(self, other):
        """
        Adds a list of elements to the container.
        :param other: List of elements to add
        :type other: syntax.SemanticType
        :return: None
        """
        self.content.append(other)

    def class_name(self):
        """
        A string representation of the class name.
        :rtype : str
        """
        return self.__class__.__name__

    def validate(self, other):
        """
        Takes a list as input and checks if every element is in map.
        :param other: List of elements to check
        :type other: list[(syntax.SemanticType | BaseContainer)]
        :return: True if every element is in map, False otherwise
        """
        for o in other:
            if o not in self.map:
                return False
        return True

    def debug_map(self):
        """
        Prints the map of the container.
        :return: None
        """
        print(f'Debug for {self.class_name()} <{id(self)}>')
        for k, v in self.map.items():
            print(f'{k} = {v}')

    def __len__(self):
        """
        :rtype : int
        """
        return len(self.content)

    def __iter__(self):
        """
        :ytype : iter[syntax.SemanticType]
        """
        for content in self.content:
            yield content

    def __getitem__(self, item):
        """
        :param item: Index of the element to get
        :type item: int
        :rtype : (syntax.SemanticType | BaseContainer)
        """
        return self.content[item]

    def __setitem__(self, key, value):
        """
        :param key: Index of the element to set
        :param value: Value to set
        :type key: int
        :type value: (syntax.SemanticType | BaseContainer)
        """
        self.content[key] = value

    def __getslice__(self, start, end):
        """
        :param start: Start index of the slice
        :param end: End index of the slice
        :type start: int
        :type end: int
        :rtype : list[(syntax.SemanticType | BaseContainer)]
        """
        return self.content[start:end]

    def __rshift__(self, other):
        """
        :param other: The name of the map element to get
        :type other: str
        :rtype : (syntax.SemanticType | BaseContainer)
        """
        return self.map[other]()

    def __eq__(self, other):
        """
        :param other: The other object to compare to
        :type other: BaseContainer | list[(syntax.SemanticType | BaseContainer)] | syntax.SemanticType
        :rtype : bool
        """
        if not hasattr(other, "__len__"):
            return False
        if len(self) != len(other):
            return False
        for e, f in zip(self, other):
            if e != f:
                return False

        if self.get_optionals() != other.get_optionals():
            return False

        if len(self.get_others()) != len(other.get_others()):
            return False

        for k, v in self.get_others().items():
            if v != other.get_others()[k]:
                return False

        return True

    def __invert__(self):
        """
        Returns the inverted optionals of the container.
        :rtype : BaseContainer
        """
        return self.get_optionals()

    def __str__(self):
        """
        :rtype : str
        """
        return '{} ({})'.format(", ".join(map(str, self.content)),
                                ", ".join(map(str, self.get_optionals())) if self.get_optionals() else "")

    def __repr__(self):
        """
        :rtype : str
        """
        representation = {}
        for content in self.content:
            if type(content) in representation:
                representation[type(content)] += 1
            else:
                representation[type(content)] = 1
        return "{}({}){}{}".format(
            self.class_name(),
            ", ".join(
                [f'{index.__name__}: {value}' for index, value in representation.items()]
            ),
            f" Opts[{len(self.get_optionals().content)}]" if self.get_optionals() else "",
            f" Otrs[{len(self.get_others())}]" if self.get_others() else ""
        )

    def print_all(self, ident=''):
        """
        Prints the container and all its content.
        """
        print(ident + self.class_name())
        for e in self:
            if isinstance(e, BaseContainer):
                e.print_all(ident + '  ')
            else:
                print(ident + "> " + str(e))
        print("")

    def to_container(self, filter_func=None):  # noqa : C901
        """
        Returns a container with the same content as the current container.
        Used for compatibility with the syntax for encapsulation.
        """
        return self  # idea: additional parameters for encapsulation


# Define containers all the Enhanced text elements, divs, headers, list and any element that can be a container
class TextContainer(BaseContainer):
    def export(self, _):
        output = ""
        for element in self.content:
            if isinstance(element, syntax.TextToken):
                output += element.content[0]
            else:
                log_exception(TypeError(f"{type(element)} found in TextContainer."), level="CRITICAL")
        return output


class EtEmContainer(BaseContainer):
    type = "inline_elements"
    subtype = "em"


class EtStrongContainer(BaseContainer):
    type = "inline_elements"
    subtype = "strong"


class EtUnderlineContainer(BaseContainer):
    type = "inline_elements"
    subtype = "underline"


class EtStrikethroughContainer(BaseContainer):
    type = "inline_elements"
    subtype = "strikethrough"


class EtCustomSpanContainer(BaseContainer):
    type = "inline_elements"

    def export(self, exm):
        self.subtype = "custom_" + self.content[0].content[0] # noqa F821 (self.content[0] is a token, by definition
        return super().export(exm)


class ReContextContainer(BaseContainer):
    children = ""

    def get_content(self, exm, arbitrary_list=None):
        child_start, child_end = exm(export.ExportRequest(self.type, self.children))  # noqa F821
        output = "\n"
        for element in self.content:
            if isinstance(element, syntax.Linebreak):
                output += "\n"
            else:
                output += child_start + super().get_content(exm, element.content) + child_end
        return output


class EtUlistContainer(ReContextContainer):
    type = "oneline_elements"
    subtype = "ulist"
    children = "list_line"


class EtOlistContainer(ReContextContainer):
    type = "oneline_elements"
    subtype = "olist"
    children = "list_line"


class HyperLinkContainer(BaseContainer):
    type = "inline_elements"
    subtype = "link"

    def export(self, exm):
        self.others["url"] = self.content[0].content.url
        return super().export(exm)

    def get_content(self, exm, arbitrary_list=None):
        return self.content[0].content.text


# class IlImageContainer(BaseContainer):
#     pass


class SeContainer(BaseContainer):
    type = "structural_elements"

    def export(self, exm):
        self.subtype = self[0].content[0]
        return super().export(exm)


class HeaderContainer(BaseContainer):
    type = "structural_elements"
    subtype = "header"

    def export(self, exm):
        self.others = {} # noqa F821
        self.others["header_level"] = len(self.content[0].content[0])
        return super().export(exm)

    def get_content(self, exm, arbitrary_list=None):
        return self.content[0].content[1]


class DisplayContainer(BaseContainer):
    type = "structural_elements"
    subtype = "display"

    def export(self, exm):
        # self.others = {}
        self.others["display_level"] = len(self.content[0].content[0])
        return super().export(exm)

    def get_content(self, exm, arbitrary_list=None):
        return self.content[0].content[1]


class TableSeparatorContainer(BaseContainer):
    pass


# class TableHeadContainer(BaseContainer):
#     type = "table"
#     subtype = "t_head"
#
#     def __init__(self, content=None, optionals=None, others=None):
#         super().__init__(content, optionals, others)
#         self.map['colspan'] = ""
#     pass


class TableRowContainer(BaseContainer):
    type = "table"
    subtype = "t_row"

    def __init__(self, content=None, optionals=None, others=None):
        super().__init__(content, optionals, others)
        self.map['colspan'] = ""
    pass


class TableCellContainer(BaseContainer):
    type = "table"
    subtype = "t_cell"

    def __init__(self, content=None, optionals=None, others=None):
        super().__init__(content, optionals, others)
        self.map['colspan'] = ""
    pass


class LinebreakContainer(BaseContainer):
    def export(self, _):
        if len(self.content) == 1:
            return "\n"
        return "<br />\n"*(len(self.content)-1)


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
    "se:start": SeContainer,
    "hyperlink": HyperLinkContainer,
    "linebreak": LinebreakContainer,
    "table:row": TableRowContainer,
    "table:cell": TableCellContainer,
    "table:separator": TableSeparatorContainer,
}


class ContextManager:
    """
    Class in charge of piling all the parsed elements and then encapsulating them inside one another.
    """
    def __init__(self, parsed_list, name=None, ident=0):
        """
        Takes a list of parsed tokens.
        :type parsed_list : list[syntax.SemanticType]
        :param parsed_list: List of parsed tokens output by our parser.
        :type name: str
        :param name: Name of the file being parsed.
        :type ident: int
        :param ident: Number of spaces to indent the output.
        """
        self.output = []
        self.parsed_list = parsed_list
        self.pile = []
        self.name = name
        self.ident = ident
        self.matched_elements = {}
        self.dict_lookahead = {
            "list:ulist": ["list:ulist"],
            "list:olist": ["list:olist"],
            "table:row": ["table:separator", "table:row"],  # future: Implement tables
            "blockquotes": [],  # future: Implement blockquotes
            "linebreak": ["linebreak"],
        }
        self.contextualised = False

    def encapsulate(self, start, end):
        """
        Method to encapsulate a number of tokens together as a final container object
        and replace all elements in the pile with None, except the first one which becomes the container.
        :type start : int
        :param start: Index of the pile where the encapsulation must begin.
        :type end: int
        :param end: Index of the pile where the encapsulation must end.
        :rtype: list[(BaseContainer|None)]
        :return: List of containers and None objects.
        """
        # Enabling this will allow us to debug the pile
        # print(f"Step : [{end}] - encapsulation:")
        # print(" Base:", self.parsed_list)
        # print(" >>> Pile:", self.pile)

        try:
            pile_start = self.pile[start]
            _ = self.pile[end]
            if start > end:
                raise IndexError("Start index must be lower than end index")
        except IndexError:
            log_exception(
                IndexError(f"Indexes ({start}:{end}) must be in the pile range ({len(self.pile)})."),
                level="CRITICAL"
            )
        try:
            container = _to_container[pile_start.label_container]()  # noqa : F821
        except KeyError:
            log_exception(
                KeyError(f"Element {pile_start.label} not in dictionary of tokens-containers correspondences."),
                level="CRITICAL"
            )
        except AttributeError as error:
            if pile_start is None:
                for e, r in zip(self.pile, self.parsed_list):
                    log_message(f'{e} - {r}')
                log_exception(
                    AttributeError("Expected token, found None in pile."),
                    level="CRITICAL"
                )
            else:
                raise error
        for i in range(start, end):
            if self.pile[i]:
                # This line transform the self modifiying containers # MONITOR
                container.add(self.pile[i].to_container(lambda x: x.label == pile_start.label)) # noqa : F821
                self.pile[i] = None
        container.add(self.pile[end])
        self.pile[end] = None
        self.pile[start] = container
        return self.pile  # ? I think this is the right way to return the pile
        # print(" <<< Pile:", self.pile)

    def _add_matched(self, label, index):
        """
        Method to add a matched element to the dictionary of matched elements.
        :type label : str
        :param label: Label of the matched element.
        :type index: int
        :param index: Index of the matched element in the pile.
        """
        if label not in self.matched_elements:
            self.matched_elements[label] = []
        self.matched_elements[label] += [index]

    def _get_matched(self, label):
        """
        Method to get the index of the last matched element of a given label.
        :type label: str
        :param label: Label of the matched element.
        :rtype: int
        :return: Index of the last matched element
        """
        return self.matched_elements[label].pop()

    def __call__(self):
        """
        Interprets the list of tokens provided and deduces context, encapsulating them to their closest neighbour and
        containing all tokens inbetween.
        :rtype: list[BaseContainer]
        :return: Returns the pile entirely processed as a list of containers.
        :raises: MismatchedContainerError if a container is not matched to its corresponding token.
        """
        # self.pile = self.parsed_list.copy()
        if self.contextualised:
            return self.pile

        index, line_number = 0,  1

        while index < len(self.parsed_list):
            token = self.parsed_list[index]
            token.line_number = line_number
            token.file_name = self.name
            token.ident = self.ident
            self.pile.append(token)
            try:
                # Linebreaks
                if isinstance(token, syntax.Linebreak):
                    # self.encapsulate(index, index)
                    line_number += 1

                # Pack the optionnal with the previous container if it exists (else raise error)
                if isinstance(token, syntax.OptionalToken):
                    self.get_last_container_in_pile(index).optionals = token
                    self.pile[index] = None

                # Group together multiple one-lines
                elif token.label in self.dict_lookahead:
                    lookahead_return = self.lookahead(token, index)
                    index += lookahead_return[0]
                    line_number += lookahead_return[1]

                # future: advanced lookahead for * logic
                # elif token.label in self.dict_advanced_lookahead:

                elif isinstance(token, syntax.FinalSemanticType):  # one-liners
                    self.encapsulate(index, index)

                # Found a matching token in encountered tokens
                elif token.counterpart() in self.matched_elements and len(self.matched_elements[token.counterpart()]) != 0:
                    self.encapsulate(self._get_matched(token.counterpart()), index)

                # Error if closing token does not have a start
                elif isinstance(token, syntax.ClosedSemanticType):
                    raise MismatchedContainerError(token)

                # Starting token by default (can cause unintended behaviours on bad implementations)
                elif isinstance(token, syntax.TokensToMatch):
                    self._add_matched(token.label, index)

                else:
                    raise MismatchedContainerError(token)

            except MismatchedContainerError as e:
                error_mngr.log_exception(e, level="CRITICAL")  # FUTURE: Try to guess some hints.
            index += 1

        self.contextualised = True
        return self.finalize_pile()

    def __iter__(self):
        """
        Iterator over the pile.
        :ytype: BaseContainer
        """
        for e in self.pile:
            if e:
                yield e

    def finalize_pile(self):
        """
        Function for cleaning up of the pile after full contextualisation.
        Removes Nones and checks for any errors or illogical containers.
        :return: list[BaseContainer]
        """
        final_pile = []
        for p in self.pile:
            if p is not None:
                if isinstance(p, BaseContainer):
                    final_pile.append(p)
                else:  # Cleanup of non-matched elements
                    if isinstance(p, syntax.SemanticType):
                        line = p.line_number
                        name = p.file_name
                    else:
                        line = "Undefined"
                        name = "Undefined"
                    log_exception(
                        TypeError(
                            f"Encountered a non-container element in the pile during "
                            f"the final pass: {p}, at line {line} in file {name}."
                        ),
                        level="CRITICAL"
                    )
        self.pile = final_pile

        return self.pile

    def lookahead(self, token, index):
        """
        Iterates the pile beginning from index and looks for all tokens matching labels with token.
        :type token : syntax.BaseContainer
        :param token: Token to look for.
        :type index : int
        :param index: Index of the token in the pile.
        :return: (number of tokens matched, number of linebreaks)
        :rtype: (int, int)
        """
        range_to_encapsulate = 0
        line_skipped = 0
        self.recontext(self.parsed_list[index])
        i = index + 1

        while i < len(self.parsed_list):
            if self.parsed_list[i].label in self.dict_lookahead[token.label]:
                self.recontext(self.parsed_list[i])
                self.pile.append(self.parsed_list[i])
                range_to_encapsulate += 1
            elif self.parsed_list[i].label == "linebreak":
                if self.parsed_list[i-1].label == "linebreak":
                    break
                else:
                    self.pile.append(self.parsed_list[i])
                    range_to_encapsulate += 1
                    line_skipped += 1
            else:  # pragma: no cover Python<3.10 doesn't see this as covered, but it actually is.
                break
            i += 1
        self.encapsulate(index, index + range_to_encapsulate)
        return range_to_encapsulate, line_skipped

    def recontext(self, token):
        """
        Function to recontextualise the content of a token.
        :param token: Token to recontextualise.
        :type token: syntax.SemanticType
        :return: Token to recontextualise.
        :rtype: syntax.SemanticType
        """
        token.content = ContextManager(token.content, name=self.name)()

    def get_last_container_in_pile(self, index):
        """
        Returns the last element in the pile if it is a Container, raises an error otherwise.
        :type index : int
        :param index: Index of the element to check.
        :return: Last element in the pile if it is a Container, raises an error otherwise.
        :rtype: BaseContainer
        :raise: error_mngr.LonelyOptionalError when an element is found in the pile that is not encapsulated in a container.
        """
        i = index-1  # skip last token as it is self
        while i >= 0:
            if self.pile[i]:
                if isinstance(self.pile[i], BaseContainer):
                    return self.pile[i]
                else:
                    log_exception(LonelyOptionalError(self.pile[index], self.pile[i]), level="CRITICAL")
            i -= 1
        log_exception(LonelyOptionalError(self.pile[index], None), level="CRITICAL")

    def print_all(self):
        """
        Prints the pile.
        """
        for e in self:
            if isinstance(e, BaseContainer):
                e.print_all()
            else:
                print("> " + str(e))
        print("Matched elements:" + str(self.matched_elements))


# Defines all methods to manage the context of the parser as a file is being parsed
# Builds all containers as the parser is parsing the file


if __name__ == "__main__":  # pragma: no cover
    from bootstraparse.modules import parser
    from io import StringIO
    # io_string = StringIO(
    #     """<<div
    #     Hello world
    #     *how do you do fellow **kids***
    #     div>>
    #     # header 1 #
    #     ! display 1 !"""
    # )
    io_string = StringIO(
        """- item 0
        #. item 1
        #. item 2
        #. item 3
        - item 4
        - item 5

         * pog *"""
    )

    test = parser.parse_line(io_string)
    ctx = ContextManager(test)
    ctx()
    print('----------------------------------')
    # for e in ctx.pile:
    #     rich.inspect(e)
    # rich.print(ctx.pile)
