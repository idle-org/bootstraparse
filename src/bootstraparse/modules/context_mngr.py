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
import rich

from bootstraparse.modules import syntax, error_mngr, export
from bootstraparse.modules.error_mngr import MismatchedContainerError, log_exception, log_message, LonelyOptionalError # noqa


class BaseContainer:
    """
    Creates container holding all the elements from the start of a parsed element to its end.
    """
    type = None
    subtype = None

    def __init__(self, content=None, optionals=None, others=None):
        if content is None:
            content = []
        if others is None:
            self.others = {}
        self.content = content
        self.map = {}
        self.optionals = optionals

    def get_content(self, exm):
        output = ""
        for element in self.content:
            if isinstance(element, BaseContainer):
                output += element.export(exm)
        return output

    def get_optionals(self):
        return self.optionals

    def get_others(self):
        return self.others

    def export(self, exm):
        """
        :type exm: export.ExportManager
        :rtype : str
        """
        start, end = exm(export.ExportRequest(self.type, self.subtype, self.get_optionals(), self.get_others()))

        output = start + self.get_content(exm) + end

        return output

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

        if self.get_optionals() != other.get_optionals():
            return False

        if len(self.get_others()) != len(other.get_others()):
            return False

        for k, v in self.get_others().items():
            if v != other.get_others()[k]:
                return False

        return True

    def __invert__(self):
        return self.get_optionals()

    def __str__(self):
        return '{} ({})'.format(", ".join(map(str, self.content)),
                                ", ".join(map(str, self.get_optionals())) if self.get_optionals() else "")

    def __repr__(self):
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
        print(ident + self.class_name())
        for e in self:
            if isinstance(e, BaseContainer):
                e.print_all(ident + '  ')
            else:
                print(ident + "> " + str(e))
        print("")

    def to_container(self, filter_func=None):  # idea: additional parameters for encapsulation
        return self


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
        self.subtype = "custom_" + self.content[0].content[0]
        return super().export(exm)


class EtUlistContainer(BaseContainer):
    type = "oneline_elements"
    subtype = "ulist"
    children = "list_line"


class EtOlistContainer(BaseContainer):
    type = "oneline_elements"
    subtype = "olist"
    children = "list_line"


class HyperLinkContainer(BaseContainer):
    type = "inline_elements"
    subtype = "link"

    def export(self, exm):
        self.others["url"] = self.content[0].content.url
        return super().export(exm)


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
        self.others = {}
        self.others["header_level"] = len(self.content[0].content[0])
        return super().export(exm)


class DisplayContainer(BaseContainer):
    type = "structural_elements"
    subtype = "display"

    def export(self, exm):
        self.others = {}
        self.others["display_level"] = len(self.content[0].content[0])
        super().export(exm)


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
    def export(self, _):  # MONITOR: Observe behaviour when we'll be done, might cause unintended side effects
        return "<br/>\n"


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
        self.dict_lookahead = {
            "list:ulist": ["list:ulist"],
            "list:olist": ["list:olist"],
            "table:row": ["table:separator", "table:row"]  # TODO: Implement tables
        }

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
        Returns
        -------
            list[(BaseContainer|None)]
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
            rich.inspect(error)
            rich.inspect(self.pile)
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
                container.add(self.pile[i].to_container(lambda x: x.label==pile_start.label)) # This line transform the self modifiying containers # MONITOR # noqa
                #container.add(self.pile[i])  # TODO: ignore the first and last element, or ignore the self modifying tokens # noqa : F821
                self.pile[i] = None
        container.add(self.pile[end])
        self.pile[end] = None
        self.pile[start] = container

        # print(" <<< Pile:", self.pile)

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
        index = 0
        line_number = 1
        while index < len(self.parsed_list):
            token = self.parsed_list[index]
            token.line_number = line_number
            self.pile.append(token)
            try:
                if isinstance(token, syntax.Linebreak):  # linebreaks
                    self.encapsulate(index, index)
                    line_number += 1

                elif isinstance(token, syntax.OptionalToken):
                    self.get_last_container_in_pile(index).optionals = token
                    self.pile[index] = None

                elif token.label in self.dict_lookahead:  # group together multiple one-lines
                    lookahead_return = self.lookahead(token, index)
                    index += lookahead_return[0]
                    line_number += lookahead_return[1]

                # elif token.label in self.dict_advanced_lookahead:  # TODO: advanced lookahead for * logic

                elif isinstance(token, syntax.FinalSemanticType):  # one-liners
                    self.encapsulate(index, index)

                elif token.counterpart() in self.matched_elements and len(self.matched_elements[token.counterpart()]) != 0:  # found a matching token in encountered tokens
                    self.encapsulate(self._get_matched(token.counterpart()), index)

                elif isinstance(token, syntax.ClosedSemanticType):  # error if closing token does not have a start
                    raise MismatchedContainerError(token)

                else:  # starting token by default (can cause unintended behaviours on bad implementations) # TODO: remove this default behaviour, error instead
                    self._add_matched(token.label, index)
            except MismatchedContainerError as e:
                error_mngr.log_exception(e, level="CRITICAL")  # FUTURE: Be more specific.
            index += 1

        return self.finalize_pile()

    def __iter__(self):
        for e in self.pile:
            if e:
                yield e

    def finalize_pile(self):
        """
        Function for cleaning up of the pile after full contextualisation.
        Removes Nones and checks for any errors or illogical containers.
        """
        final_pile = []
        for p in self.pile:
            if p is not None:
                final_pile.append(p)

        self.pile = final_pile

        # TODO: add cleanup of non-matched elements
        return self.pile

    def lookahead(self, token, index):
        """
        Iterates the pile beginning from index and looks for all tokens matching labels with token.
        """
        range_to_encapsulate = 0
        line_skipped = 0
        i = index + 1
        # print(self.parsed_list)
        while i < len(self.parsed_list):
            if self.parsed_list[i].label in self.dict_lookahead[token.label]:
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

    def get_last_container_in_pile(self, index):
        """
        Returns the last element in the pile if it is a Container, raises an error otherwise.
        Return
        ------
            BaseContainer

        Raises
        ------
            error_mngr.LonelyOptionalError
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
    ctx.print_all()
    # rich.print(ctx.pile)
