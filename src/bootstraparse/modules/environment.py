"""Module for containing super important variables
Environment has self._mParams for mandatory parameters, self._sParams for secondary parameters and
 - self.wasInitialised and integrity_check for debug.
 - __getattr__ and __setattr__ check for existing super, s or m parameters, returns error if not found.
Usage:
 - from bootstraparse.modules.environment import Environment
 - env = Environment()
 - env.integrity_check() -> Checks if all mandatory parameters are set.
 - env["config"] -> returns config object
 - env["template"] -> returns template object
 - env["export_mngr"] -> returns export manager object
 - env["global_path"] -> returns global path ???
 - env["user_path"] -> returns user path ???
 - env["site_path"] -> returns site path
 - env["export"] -> returns export object ???
 - env["site_crawler"] -> returns site crawler object
 """

from bootstraparse.modules import error_mngr


class Environment:
    """
    Object containing all the important variables,
    with appropriate getters and setters.
    Also contains self integrity checks.
    """

    def __init__(self):
        """
        Initialises the environment, all parameters are set to None.
        Set _wasInitialised to False for all parameters.
        """
        # mandatoryParameters
        self._mParams = {
            'config': None,
            'template': None,
            'export_mngr': None,
            'origin': None,
            'destination': None,
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
        Getter for all parameters, looks for super if the parameter is prefaced with an underscore.
        Looks for mandatory parameters first, then secondary parameters.
        :param attribute: The name of the parameter to get.
        :type attribute: str
        :return: The value of the parameter.
        """
        if attribute[0] == "_":
            super().__getattribute__(attribute)
        elif attribute in self._mParams:
            return self._mParams[attribute]
        elif attribute in self._sParams:
            return self._sParams[attribute]
        else:
            error_mngr.log_exception(AttributeError(
                f'Attribute {attribute} not in mandatory, secondary or reserved parameters.'
                f'\nMandatory parameters:\n{self._mParams}'
                f'\nSecondary parameters:\n{self._sParams}'
                f'\nReserved parameters are preceded with an underscore.'
            ), level='CRITICAL')

    def __setattr__(self, attribute, value):
        """
        Setter for all parameters, looks for super if the parameter is prefaced with an underscore.
        :param attribute: The name of the parameter to set.
        :type attribute: str
        """
        if attribute[0] == "_":
            super().__setattr__(attribute, value)
        elif attribute in self._mParams:
            self._mParams[attribute] = value
        elif attribute in self._sParams:
            self._sParams[attribute] = value
        else:
            error_mngr.log_exception(AttributeError(
                f'Attribute {attribute} not in mandatory, secondary or reserved parameters.'
                f'\nMandatory parameters:\n{self._mParams}'
                f'\nSecondary parameters:\n{self._sParams}'
                f'\nReserved parameters are preceded with an underscore.'
            ), level='CRITICAL')  # Could also add attribute as a new entry
