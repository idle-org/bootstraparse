import pytest

from bootstraparse.modules import syntax, error_mngr, tools, context_mngr

__XF = pytest.mark.xfail

# The SemanticTypes with the .counterpart() and .to_container() expected results
_type_counterpart_container = [
    (syntax.SemanticType, None,  "error", tools.__GLk(1)),
    (syntax.ExplicitSemanticType, None,  "token", tools.__GLk(1)),
    (syntax.FinalSemanticType, None, "self", tools.__GLk(1)),
    (syntax.OpenedSemanticType, None, "error", tools.__GLk(1)),
    (syntax.ClosedSemanticType, None, "error", tools.__GLk(1)),
    (syntax.EmptySemanticType, None, "self", tools.__GLk(1)),
    (syntax.UnimplementedToken, None, "error", tools.__GLk(1)),
    (syntax.TextToken, None, "self", tools.__GLk(1)),
    (syntax.EtEmToken, "text:em", "token", tools.__GLk(1)),
    (syntax.EtStrongToken, 'text:strong', "token", tools.__GLk(1)),
    (syntax.EtUnderlineToken, 'text:underline', "token", tools.__GLk(1)),
    (syntax.EtStrikethroughToken, 'text:strikethrough', "token", tools.__GLk(1)),
    (syntax.EtCustomSpanToken, "text:custom_span:test", "token", tools.__GLk(1)),
    (syntax.EtUlistToken, None, "self", tools.__GLk(1)),
    (syntax.EtOlistToken, None, "self", tools.__GLk(1)),
    (syntax.HeaderToken, None, "self", tools.__GLk(1)),
    (syntax.DisplayToken, None, "self", tools.__GLk(1)),
    (syntax.StructuralElementStartToken, None, "error", tools.__GLk(1)),  # A start can't be in a container (MismatchedContainerError) # noqa
    (syntax.StructuralElementEndToken, 'se:start:test', "error", tools.__GLk(1)),  # An end can't be in a container (MismatchedContainerError) # noqa
    (syntax.HyperlinkToken, None, "self", tools.__GLk(1)),  # Shouldn't be an error
    (syntax.TableToken, None, "error", tools.__GLk(1)),
    (syntax.TableRowToken, None, "error", tools.__GLk(1)),
    (syntax.TableCellToken, None, "error", tools.__GLk(1)),
    (syntax.TableSeparatorToken, None, "error", tools.__GLk(1)),
    (syntax.BlockQuoteToken, None, "error", tools.__GLk(1)),
    (syntax.BlockQuoteAuthorToken, None, "error", tools.__GLk(1)),
    (syntax.Linebreak, "linebreak", "self", tools.__GLk(1)),
]

_zipped_type_counterpart_container = [
    pytest.param(*c[0:4], marks=c[4:]) for c in _type_counterpart_container
]


@pytest.mark.parametrize("type_n, expected_counterpart, expected_container, file_n", _zipped_type_counterpart_container)
def test_counterpart_container(type_n, expected_counterpart, expected_container, file_n):
    """Test the .counterpart() and .to_container() method of SemanticTypes."""
    try:
        token = type_n(["test"])  # noqa
        token.line_number = 1
        assert token.counterpart() == expected_counterpart
        if expected_container == "error":
            with pytest.raises(error_mngr.MismatchedContainerError):
                token.to_container()
        elif expected_container == "self":
            assert token.to_container() == token
        elif expected_container == "token":
            assert isinstance(token.to_container(), context_mngr.TextContainer)
        else:
            raise ValueError("Invalid expected_container value: {}".format(expected_container))
    except Exception as e:
        assert False, "Unexpected exception: {} in \n{}".format(e, file_n)
