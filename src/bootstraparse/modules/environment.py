# Module for containing super important variables


class environment():
    """
    Object containing all the important variables,
    with appropriate getters and setters.
    Also contains self integrity checks.
    """

    def __init__(self):
        # mandatoryParameters
        self.mParams = {
            'config': None,
            'context_mngr': None,
            'export_mngr': None,
            'global_path': None,
            'user_path': None,
            'logging': None,
            }

        # secondaryParameters
        self.sParams = {

        }

        # Set all parameters to uninitialised
        self.wasInitialised = {p: False for p in self.mParams}

    def integritycheck(self):
        for value in self.wasInitialised.values():
            if value is False:
                return False
        return True
