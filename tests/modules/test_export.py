import bootstraparse.modules.export as export
import pytest


def test_export():
    """
    Test the export module
    """
    em = export.ExportManager("test", "test")
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
    em = export.ExportManager("test", "test")
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
    with pytest.raises(SystemExit):
        em = export.ExportManager("test", "test")
        em(export.ExportRequest("nope", "header", "", {}))


def test_with_optionnals():
    em = export.ExportManager("test", "test")
    em(export.ExportRequest("structural_elements", "div", "boo")) # noqa E741


@pytest.mark.xfail(reason="Not implemented")
def test_format_optionnals():
    from bootstraparse.modules import syntax # noqa E402
    export.format_optionals("")
    assert False


def test_return_values():
    pass


def test_bad_header():
    em = export.ExportManager("test", "test")
    with pytest.raises(KeyError):
        em(export.ExportRequest("structural_elements", "header", "", {}))
