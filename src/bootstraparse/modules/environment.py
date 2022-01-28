# Module for containing super important variables


import rich


class environment():
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
            'logging': None,
            }

        # secondaryParameters
        self._sParams = {

        }

        # Set all parameters to uninitialised
        self._wasInitialised = {p: False for p in self._mParams}

    def integritycheck(self):
        for value in self._wasInitialised.values():
            if value is False:
                return False
        return True

    def __getattr__(self, attribute):
        if attribute[0] == "_":
            super().__getattr__(attribute)
        elif attribute in self._mParams:
            return self._mParams[attribute]
        elif attribute in self._sParams:
            return self._sParams[attribute]
        else: 
            raise KeyError(attribute)

    def __setattr__ (self, attribute, value):
        if attribute[0] == "_":
            super().__setattr__(attribute, value)
        elif attribute in self._mParams:
            self._mParams[attribute] = value
        elif attribute in self._sParams:
            self._sParams[attribute] = value
        else: 
            raise KeyError(attribute) #could also add attribute as a new entry
