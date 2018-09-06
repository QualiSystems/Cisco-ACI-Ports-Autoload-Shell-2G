from cloudshell.devices.standards.base import AbstractResource


AVAILABLE_SHELL_TYPES = ["CS_CiscoACIController", "CS_CiscoACIPod", "CS_CiscoACINode", "CS_CiscoACISlot",
                         "CS_CiscoACIPort", "CS_CiscoACISlot", "CS_CiscoACIFex", "CS_CiscoACIFexSlot",
                         "CS_CiscoACIFexPort"]


class CiscoACIController(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Ports Controller"
    RELATIVE_PATH_TEMPLATE = ""

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACIController"):
        super(CiscoACIController, self).__init__(shell_name, name, unique_id)

        if shell_name:
            self.shell_name = "{}.".format(shell_name)
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""


class CiscoACIPod(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Pod"
    RELATIVE_PATH_TEMPLATE = "PD"

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACIPod"):
        super(CiscoACIPod, self).__init__(shell_name, name, unique_id)

        if shell_name:
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""


class CiscoACINode(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Node"
    RELATIVE_PATH_TEMPLATE = "N"

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACINode"):
        super(CiscoACINode, self).__init__(shell_name, name, unique_id)

        if shell_name:
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""


class CiscoACISlot(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Slot"
    RELATIVE_PATH_TEMPLATE = "S"

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACISlot"):
        super(CiscoACISlot, self).__init__(shell_name, name, unique_id)

        if shell_name:
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""


class CiscoACIPort(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Port"
    RELATIVE_PATH_TEMPLATE = "P"

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACIPort"):
        super(CiscoACIPort, self).__init__(shell_name, name, unique_id)

        if shell_name:
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""


class CiscoACIFex(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Fex"
    RELATIVE_PATH_TEMPLATE = "F"

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACIFex"):
        super(CiscoACIFex, self).__init__(shell_name, name, unique_id)

        if shell_name:
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""


class CiscoACIFexSlot(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Fex Slot"
    RELATIVE_PATH_TEMPLATE = "FS"

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACIFexSlot"):
        super(CiscoACIFexSlot, self).__init__(shell_name, name, unique_id)

        if shell_name:
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""


class CiscoACIFexPort(AbstractResource):
    RESOURCE_MODEL = "Cisco ACI Fex Port"
    RELATIVE_PATH_TEMPLATE = "FP"

    def __init__(self, shell_name, name, unique_id, shell_type="CS_CiscoACIFexPort"):
        super(CiscoACIFexPort, self).__init__(shell_name, name, unique_id)

        if shell_name:
            if shell_type in AVAILABLE_SHELL_TYPES:
                self.shell_type = "{}.".format(shell_type)
            else:
                raise Exception(self.__class__.__name__, "Unavailable shell type {shell_type}."
                                                         "Shell type should be one of: {avail}"
                                .format(shell_type=shell_type, avail=", ".join(AVAILABLE_SHELL_TYPES)))
        else:
            self.shell_name = ""
            self.shell_type = ""
