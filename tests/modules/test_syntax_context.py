import pytest

from bootstraparse.modules import syntax, error_mngr

# The SemanticTypes with the .counterpart() and .to_container() expected results
_type_counterpart_container = [
    (syntax.SemanticType, None,  "error"),
    (syntax.ExplicitSemanticType, None,  "token"),
    (syntax.FinalSemanticType, None, "self"),
    (syntax.OpenedSemanticType, None, "self"),
    (syntax.ClosedSemanticType, None, "error"),
    (syntax.EmptySemanticType, None, "self"),
    (syntax.UnimplementedToken, None, "error"),
    (syntax.TextToken, None, "self"),
    (syntax.EnhancedToken, 'text:enhanced', "token"),  # Not sure Enhanced text is used
    (syntax.EtEmToken, "text:em", "token"),
    (syntax.EtStrongToken, 'text:strong', "token"),
    (syntax.EtUnderlineToken, 'text:underline', "token"),
    (syntax.EtStrikethroughToken, 'text:strikethrough', "token"),
    (syntax.EtCustomSpanToken, None, "token"),
    (syntax.EtUlistToken, None, "token"),
    (syntax.EtOlistToken, None, "token"),
    (syntax.HeaderToken, None, "self"),
    (syntax.DisplayToken, None, "self"),
    (syntax.StructuralElementStartToken, None, "self"),
    (syntax.StructuralElementEndToken, 'se:start:test', "error"),
    (syntax.HyperlinkToken, None, "token"),
    (syntax.TableToken, None, "error"),
    (syntax.TableRowToken, None, "error"),
    (syntax.TableCellToken, None, "error"),
    (syntax.TableSeparatorToken, None, "error"),
    (syntax.BlockQuoteToken, None, "error"),
    (syntax.BlockQuoteAuthorToken, None, "error"),
    (syntax.Linebreak, "linebreak", "self"),
]


@pytest.mark.parametrize("type_n, expected_counterpart, expected_container", _type_counterpart_container)
def test_counterpart_container(type_n, expected_counterpart, expected_container):
    """Test the .counterpart() and .to_container() method of SemanticTypes."""
    token = type_n(["test"])
    token.line_number = 1
    assert token.counterpart() == expected_counterpart
    if expected_container == "error":
        with pytest.raises(error_mngr.MismatchedContainerError):
            token.to_container()
    elif expected_container == "self":
        assert token.to_container() == token
    elif expected_container == "token":
        assert isinstance(token.to_container(), syntax.TextToken)
    else:
        raise ValueError("Invalid expected_container value: {}".format(expected_container))