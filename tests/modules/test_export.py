from itertools import zip_longest

import bootstraparse.modules.export as export
import pytest

from bootstraparse.modules import context_mngr, syntax, config, pathresolver
from bootstraparse.modules.tools import __GLk

__config = config.ConfigLoader(pathresolver.b_path("configs/"))
__templates = config.ConfigLoader(pathresolver.b_path("templates/"))

__XF = pytest.mark.xfail
_all_templates = {
    "structural_elements": [
        ["div", __GLk(1)],
        ["article", __GLk(1)],
        ["aside", __GLk(1)],
        ["section", __GLk(1)],
        ["header", __GLk(1)],
        ["display", __GLk(1)],
    ],
    "inline_elements": [
        ["link", __GLk(1)],
        ["em", __GLk(1)],
        ["strong", __GLk(1)],
        ["underline", __GLk(1)],
        ["strikethrough", __GLk(1)],
        ["image", __GLk(1)],
        ["custom_0", __GLk(1)],
    ],
    "table": [
        ["table", __GLk(1)],
        ["t_head", __GLk(1)],
        ["t_row", __GLk(1)],
        ["t_cell", __GLk(1)],
    ],
}

zipped_templates = [
    pytest.param(item[0], item[1][0], item[1][1], marks=item[1][2:], id=f"{item[0][0]} : {item[1][0]}")
    for sublist in [zip_longest([key], value, fillvalue=key) for key, value in _all_templates.items()]
    for item in sublist
]

_opts = syntax.OptionalToken([
    syntax.OptionalVarToken([
        syntax.BeAssignToken([["class", "blue"]]),
        syntax.BeValueToken([123]),
    ]),
    syntax.OptionalInsertToken(["var='test', number=11"]),
])


def test_export():
    """
    Test the export module
    """
    em = export.ExportManager(__config, __templates)
    assert type(em) is export.ExportManager


def test_export_request():
    """
    Test the export_request named_tuple
    """
    export_test = export.ExportRequest("type", "subtype", "optionals", "others")
    assert export_test.type == "type"
    assert export_test.subtype == "subtype"
    assert export_test.optionals == "optionals"
    assert export_test.others == "others"


def test_export_response():
    """
    Test the export_response named_tuple
    """
    export_test = export.ExportResponse("start", "end")
    assert export_test.start == "start"
    assert export_test.end == "end"


@pytest.mark.parametrize("export_type, export_subtype", [
    ("structural_elements", "header"),
    ("structural_elements", "display"),
    ("inline_elements", "link"),
    ("table", "t_head"),
    ("table", "t_row"),
    ("table", "t_cell"),
    ("structural_elements", "div"),
])
def test_transform(export_type, export_subtype):
    """
    Test the transform method
    """
    em = export.ExportManager(__config, __templates)
    re = em.transform(export.ExportRequest(export_type, export_subtype, "", { # noqa E741
        "header_level": "1",
        "display_level": "1",
        "col_span": "1",
        "row_span": "1",
        "url": "1"
    }))
    re = em(export.ExportRequest(export_type, export_subtype, "", {
        "header_level": "1",
        "display_level": "1",
        "col_span": "1",
        "row_span": "1",
        "url": "1"
    }))
    assert type(re) is export.ExportResponse


def test_get_template_error():
    with pytest.raises(KeyError):
        em = export.ExportManager(__config, __templates)
        em(export.ExportRequest("nope", "header", "", {}))


def test_with_optionnals():
    em = export.ExportManager(__config, __templates)
    em(export.ExportRequest("structural_elements", "div", _opts)) # noqa E741


def test_format_optionnals():
    from bootstraparse.modules import syntax # noqa E402
    op = export.format_optionals(_opts)
    expected = syntax.OptionalToken([
        syntax.OptionalVarToken([
            syntax.BeAssignToken([["class", "blue"]]),
            syntax.BeValueToken([123]),
        ]),
        syntax.OptionalInsertToken(["var='test', number=11"]),
    ])
    assert expected == _opts
    assert op == " var='test', number=11"


def test_return_values():
    pass


def test_bad_header():
    em = export.ExportManager(__config, __templates)
    with pytest.raises(KeyError):
        em(export.ExportRequest("structural_elements", "header", "", {}))


@pytest.mark.parametrize("export_type, export_subtype, line", zipped_templates)
def test_get_templates(export_type, export_subtype, line):
    em = export.ExportManager(__config, __templates)
    # assert type(em.get_templates()) is dict
    print(export_type, export_subtype)
    r = em(export.ExportRequest(export_type, export_subtype, "", {
        "header_level": "1",
        "url": "1",
        "col_span": "1",
        "row_span": "1",
        "display_level": "1"
    }))
    assert isinstance(r, export.ExportResponse)
    r2 = em(export.ExportRequest(export_type, export_subtype, _opts, {
        "header_level": "2",
        "url": "2",
        "col_span": "2",
        "row_span": "2",
        "display_level": "2"
    }))
    assert isinstance(r2, export.ExportResponse)


def test_context_cov():
    em = export.ExportManager(__config, __templates)
    lst = [context_mngr.TextContainer([syntax.TextToken("test")])]

    # base = context_mngr.ContextManager(lst)
    # base.pile = lst
    # return base
    convr = export.ContextConverter(lst, em, "Undefined")
    convr.process_pile()
    convr.__repr__()
    convr.readlines()
    convr.__str__()
    convr.print_all()

    class A:
        pass

    assert convr == convr
    assert convr != A()
