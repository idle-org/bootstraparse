import pyparsing
import pytest
import bootstraparse.modules.syntax as sy


# Dictionnary of all label and assotiated token used in the language
list_of_token_types = {
    "alias": sy.AliasToken,
    "image": sy.ImageToken,
}


# Dictionnary of all lexical elements and a list of matching strings
expressions_to_match = {
    # Base elements
    "quotes": ["'hi, there'", "'hi, there'"],
    "value": ["0.1", "'hello'"],
    "assignation": ["a=1", "a=1.33", "tr2='hu'"],

    # Composite elements
    "var": ['[a,b,c]', '[a=12,22,"c","d,ERE,r,3"]'],

    # Specific elements
    "image_element": ["image(a,b,c)"],
    "alias_element": ["alias(a,b,c)"],
    "expression": ["a+b+c"],
    "html_insert": ["html(a,b,c)"],

    # Optional elements
    "optional": ["a=1", "a=1.33", "tr2='hu'"],

    # Preparser elements
    "image": ["image(a,b,c)"],
    "alias": ["alias(a,b,c)"],

    # Syntax elements
    "line_to_replace": ["a=1", "a=1.33", "tr2='hu'"],
}


@pytest.mark.parametrize("token_name,token_class", list_of_token_types.items())
def test_token_type_exists(token_name, token_class):
    """
    Test that the token type exists.
    :param token_name: The name of the token type.
    :param token_class: The class of the token type.
    :type token_name: str
    :type token_class: sy.SemanticType
    """
    assert token_class.label == token_name


def test_token_type_exists_fail():
    """
    Test that the token type does not exist.
    """
    with pytest.raises(AttributeError):
        # noinspection PyUnresolvedReferences, PyStatementEffect
        sy.UnexistingTypeToken.label == "non_existing_token"  # pylint: disable=pointless-statement


@pytest.mark.parametrize("token_class", list_of_token_types.values())
def test_of_type_creator(token_class):
    """
    Test that the of_type_creator function returns the correct type.
    :param token_class: The class of the token type.
    :type token_class: sy.SemanticType
    """
    fcr = sy.of_type(token_class)
    tnk = fcr(None, None, None)
    assert isinstance(tnk, token_class)
    assert tnk.label == token_class.label


def strings_in_Token(token, string_list):
    token_str = str(token)
    for string in string_list:
        if string not in token_str:
            return False
    return True


def test_semantic_type():
    """
    Test that the semantic type is correctly created.
    """
    st = sy.SemanticType("test")
    assert st.label is None
    assert strings_in_Token(st, ["test", "None"])
    assert strings_in_Token(repr(st), ["test", "None"])
    st = sy.SemanticType([1, 2, 3])
    assert st.label is None
    st.label = "test"
    assert strings_in_Token(st, ["[1, 2, 3]", "test"])


def find_expression_from_str(expression_str):
    """
    Find the expression from its string representation.
    Just trust on this one.
    :param expression_str: The string representation of the expression.
    :type expression_str: str
    :return: The expression.
    :rtype: pyparsing.ParserElement
    """
    # noinspection PyUnresolvedReferences
    return sy.__getattribute__(expression_str)  # pylint: disable=no-member


@pytest.mark.xfail(reason="Not implemented yet")
@pytest.mark.parametrize("expression,to_parse", expressions_to_match.items())
def test_expression_matching(expression, to_parse):
    """
    Test that the expression is correctly parsed.
    :param expression: The expression to test.
    :param to_parse: A list of string that should be matched by the expression.
    :type expression: str
    :type to_parse: list
    """
    for string in to_parse:
        expr = find_expression_from_str(expression)
        assert isinstance(expr, pyparsing.ParserElement)
        assert expr.parse_string(string) is not None
