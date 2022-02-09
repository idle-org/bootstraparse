# Module for containing super important variables


class Environment:
    """
    Object containing all the important variables,
    with appropriate getters and setters.
    Also contains self integrity checks.
    """

    def __init__(self):
        # mandatoryParameters
        self._mParams = {
            'config': None,
            'context_mngr': None,
            'export_mngr': None,
            'global_path': None,
            'user_path': None,
            'site_path': None,
            'export': None,
            'site_crawler': None,
            }

        # secondaryParameters
        self._sParams = {

        }

        # Set all parameters to uninitialised
        self._wasInitialised = {p: False for p in self._mParams}

    def integrity_check(self):
        """
        Checks if all mandatory parameters are set.
        :return: True if all mandatory parameters are set, False otherwise.
        """
        for value in self._wasInitialised.values():
            if value is False:
                return False
        return True

    def __getattr__(self, attribute):
        """
        Getter for all parameters.
        :param attribute: The name of the parameter to get.
        :return: The value of the parameter.
        """
        if attribute[0] == "_":
            super().__getattribute__(attribute)
        elif attribute in self._mParams:
            return self._mParams[attribute]
        elif attribute in self._sParams:
            return self._sParams[attribute]
        else:
            raise AttributeError(attribute)

    def __setattr__(self, attribute, value):
        """
        Setter for all parameters.
        :param attribute: The name of the parameter to set.
        """
        if attribute[0] == "_":
            super().__setattr__(attribute, value)
        elif attribute in self._mParams:
            self._mParams[attribute] = value
        elif attribute in self._sParams:
            self._sParams[attribute] = value
        else:
            raise AttributeError(attribute)  # Could also add attribute as a new entry
