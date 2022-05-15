# Module for final generation of the translated website

from bootstraparse.modules import config, pathresolver, error_mngr
from collections import namedtuple


"""
Named tuple containing all necessary information to select the appropriate
markup element and pass it over to ExportManager.
"""
ExportRequest = namedtuple("ExportRequest", ["type", "subtype", "optionals", "others"], defaults=[None, None, "", {}])

"""
Class containing all necessary information to proceed with the
final output.
"""
ExportResponse = namedtuple("ExportResponse", ["start", "end"])


class ExportManager:
    """
    Transforms ExportRequest tuples to ExportResponse tuples with the config-provided appropriate markup.
    """
    def __init__(self, cnoifg, templates):
        #  self.config = cnoifg  TODO: actually import config
        #  self.templates = templates  TODO: actually import templates
        self.config = config.ConfigLoader(pathresolver.b_path("configs/"))
        self.templates = config.ConfigLoader(pathresolver.b_path("templates/"))
        self.advanced_export = {
            "header": self.header_transform,
            "display": self.display_transform,
            "link": self.link_transform,
            "t_head": self.t_transform,
            "t_row": self.t_transform,
            "t_cell": self.t_transform,
        }

    def __call__(self, export_request):
        return self.transform(export_request)

    def transform(self, export_request):
        """
        Transformation function to magically poof ExportRequest tuples into
        ExportResponse tuples using the loaded config.
        :param export_request: ExportRequest tuples
        :type export_request: ExportRequest
        :return: ExportResponse tuples
        :rtype: ExportResponse
        """
        if export_request.subtype in self.advanced_export:
            return self.advanced_export[export_request.subtype](export_request)
            # return self.__getattribute__(export_request.subtype + "_transform")()   # alternative method
        else:
            return self.basic_transform(export_request)

    def _get_template(self, export_request):
        """
        Function for initializing other transform functions.
        :return: start, end, optionals
        """
        try:
            start, end = self.templates["bootstrap"][export_request.type][export_request.subtype]
        except KeyError:
            log_entries = ["bootstrap", export_request.type, export_request.subtype]
            log_ = error_mngr.dict_check(self.templates, *log_entries)
            print()
            error_mngr.log_exception(
                KeyError(
                    f'Template "bootstrap"/{export_request.type}/{export_request.subtype} could not be found.'
                    '\n'.join([f'{i}: {"Found" if j else "Not found"}' for i, j in zip(log_entries, log_)])
                ),
                level='CRITICAL'
            )
        # future: allow for template selection
        if export_request.optionals != '':
            optionals = " " + export_request.optionals
        else:
            optionals = ''
        return start, end, optionals

    def basic_transform(self, export_request):
        """
        Basic template for ExportResponse objects.
        :param export_request: ExportRequest tuples
        :type export_request: ExportRequest
        :return: ExportResponse tuples
        :rtype: ExportResponse
        """
        start, end, optionals = self._get_template(export_request)
        start = start.format(optionals=optionals)
        return ExportResponse(start, end)

    def header_transform(self, export_request):
        """
        Specific template for headers.
        """
        start, end, optionals = self._get_template(export_request)
        start = start.format(optionals=optionals, header_level=export_request.others["header_level"])
        # TODO: add helpful message if KeyError
        end = end.format(header_level=export_request.others["header_level"])
        return ExportResponse(start, end)

    def display_transform(self, export_request):
        """
        Specific template for display.
        """
        start, end, optionals = self._get_template(export_request)
        start = start.format(optionals=optionals, display_level=export_request.others["display_level"])
        return ExportResponse(start, end)

    def link_transform(self, export_request):
        """
        Specific template for link.
        """
        start, end, _ = self._get_template(export_request)
        start = start.format(url=export_request.others["url"])
        return ExportResponse(start, end)

    def t_transform(self, export_request):
        """
        Specific template for table content.
        """
        start, end, _ = self._get_template(export_request)
        start = start.format(col_span=export_request.others["col_span"])
        return ExportResponse(start, end)


if __name__ == '__main__':
    herbert = ExportManager(cnoifg=None, templates=None)
    herbert._get_template(ExportRequest('b', 'c', 'class="hugues"'))
