from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.devices.driver_helper import get_api
from cloudshell.devices.driver_helper import get_logger_with_thread_id
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.cisco.aci.controller.api.client import CiscoACIControllerHTTPClient

from cisco.aci.physical.configuration_attributes_structure import CiscoACIControllerResourse
from cisco.aci.physical.runners.autoload import CiscoACIAutoloadRunner
from cisco.aci.physical.runners.connectivity import CiscoACIConnectivityRunner


class CiscoAciPortsAutoloadDriver(ResourceDriverInterface):

    SHELL_TYPE = "CS_CiscoACIController"
    SHELL_NAME = "Cisco ACI Ports Controller"

    def __init__(self):
        """Constructor must be without arguments.

        It is created with reflection at run time
        """
        pass

    def initialize(self, context):
        """Initialize the driver session.

        This function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration,
        initiate sessions etc.
        """
        pass

    def cleanup(self):
        """Destroy the driver session.

        This function is called everytime a driver instance is destroyed.
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    @GlobalLock.lock
    def get_inventory(self, context):
        """Discovers the resource structure and attributes.

        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource
        :rtype: AutoLoadDetails
        """
        logger = get_logger_with_thread_id(context)
        logger.info("Autoload command started")

        with ErrorHandlingContext(logger):
            resource_config = CiscoACIControllerResourse.from_context(
                context=context,
                shell_type=self.SHELL_TYPE,
                shell_name=self.SHELL_NAME
            )

            cs_api = get_api(context)
            password = cs_api.DecryptPassword(resource_config.password).Value

            aci_api_client = CiscoACIControllerHTTPClient(
                logger=logger,
                address=resource_config.address,
                user=resource_config.user,
                password=password,
                scheme=resource_config.scheme,
                port=resource_config.port
            )

            autoload_runner = CiscoACIAutoloadRunner(
                aci_api_client=aci_api_client,
                logger=logger,
                resource_config=resource_config
            )

            autoload_details = autoload_runner.discover()
            logger.info("Autoload command completed")

            return autoload_details

    def ApplyConnectivityChanges(self, context, request):
        """Create vlan and add or remove it to/from network interface.
        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param str request: request json
        :return:
        """
        logger = get_logger_with_thread_id(context)
        logger.info("ApplyConnectivityChanges started")

        reservation_id = context.reservation.reservation_id

        with ErrorHandlingContext(logger):
            resource_config = CiscoACIControllerResourse.from_context(
                context=context,
                shell_type=self.SHELL_TYPE,
                shell_name=self.SHELL_NAME
            )

            cs_api = get_api(context)
            password = cs_api.DecryptPassword(resource_config.password).Value

            aci_api_client = CiscoACIControllerHTTPClient(
                logger=logger,
                address=resource_config.address,
                user=resource_config.user,
                password=password,
                scheme=resource_config.scheme,
                port=resource_config.port
            )

            connectivity_runner = CiscoACIConnectivityRunner(
                resource_config=resource_config,
                aci_api_client=aci_api_client,
                cs_api=cs_api,
                reservation_id=reservation_id,
                logger=logger
            )

            logger.info("Start applying connectivity changes, request is: {0}".format(str(request)))
            result = connectivity_runner.apply_connectivity_changes(request=request)
            logger.info("Finished applying connectivity changes, response is: {0}".format(str(result)))

            return result
