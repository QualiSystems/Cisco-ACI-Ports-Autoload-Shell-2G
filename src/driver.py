from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.devices.driver_helper import get_api
from cloudshell.devices.driver_helper import get_logger_with_thread_id

from cisco.aci.controller.api.client import CiscoACIControllerHTTPClient
from cisco.aci.controller.configuration_attributes_structure import CiscoACIControllerResourse
from cisco.aci.controller.runners.autoload import CiscoACIAutoloadRunner
from cisco.aci.controller.runners.connectivity import CiscoACIConnectivityRunner


class CiscoAciPortsAutoloadDriver(ResourceDriverInterface):

    SHELL_TYPE = "CS_CiscoACIController"
    SHELL_NAME = "Cisco ACI Ports Controller"

    def __init__(self):
        """
        ctor must be without arguments, it is created with reflection at run time
        """
        pass

    def initialize(self, context):
        """
        Initialize the driver session, this function is called everytime a new instance of the driver is created
        This is a good place to load and cache the driver configuration, initiate sessions etc.
        :param InitCommandContext context: the context the command runs on
        """
        pass

    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass

    @GlobalLock.lock
    def get_inventory(self, context):
        """Discovers the resource structure and attributes.

        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource you can return an AutoLoadDetails object
        :rtype: AutoLoadDetails
        """
        logger = get_logger_with_thread_id(context)
        logger.info("Autoload command started")

        with ErrorHandlingContext(logger):
            resource_config = CiscoACIControllerResourse.from_context(context=context,
                                                                      shell_type=self.SHELL_TYPE,
                                                                      shell_name=self.SHELL_NAME)

            cs_api = get_api(context)
            password = cs_api.DecryptPassword(resource_config.password).Value

            aci_api_client = CiscoACIControllerHTTPClient(logger=logger,
                                                          address=resource_config.address,
                                                          user=resource_config.user,
                                                          password=password,
                                                          scheme=resource_config.scheme,
                                                          port=resource_config.port)

            autoload_runner = CiscoACIAutoloadRunner(aci_api_client=aci_api_client,
                                                     logger=logger,
                                                     resource_config=resource_config)

            autoload_details = autoload_runner.discover()
            logger.info("Autoload command completed")

            return autoload_details

    def ApplyConnectivityChanges(self, context, request):
        """Create vlan and add or remove it to/from network interface
        :param ResourceCommandContext context: ResourceCommandContext object with all Resource Attributes inside
        :param str request: request json
        :return:
        """
        logger = get_logger_with_thread_id(context)
        logger.info('ApplyConnectivityChanges started')

        # todo: 1 request - will got all data for PORT and VLAN from There
        # todo: 2 get all connectors from the reservation
        # todo: 3 get current port full path - FullName
        "sandbox.api.com/PD1/N2/S1/P1"
        # reservation_id = context.remote_reservation.reservation_id
        reservation_id = context.reservation.reservation_id

        # ipdb > xxx.ReservationDescription.Connectors[0].__dict__
        # {'Direction': 'bi', 'Target': 'DUT 1/Chassis 1/Module 1/Port 1', 'Alias': 'Connection Failed',
        #  'Source': 'VLAN 255', 'State': 'ConnectionFailed', 'Attributes': [], 'Type': 'Default'}
        # ipdb > xxx.ReservationDescription.Connectors[1].__dict__
        # {'Direction': 'bi', 'Target': 'Cisco ACI EPG Structure/database/database', 'Alias': None,
        #  'Source': 'DUT 1/Chassis 1/Module 1/Port 1', 'State': 'None', 'Attributes': [], 'Type': 'Default'}

        # ipdb > cs_api.GetResourceDetails("DUT 1/Chassis 1/Module 1/Port 1").FullAddress
        # '10.10.10.10/CH1/M1/P1'

        # ipdb > cs_api.GetResourceDetails("Cisco ACI EPG Structure/database/database").FullAddress
        # 'sandboxapicdc.cisco.com/T3/EPG1

        # logger.info("=" * 100)

        with ErrorHandlingContext(logger):
            resource_config = CiscoACIControllerResourse.from_context(context=context,
                                                                      shell_type=self.SHELL_TYPE,
                                                                      shell_name=self.SHELL_NAME)

            cs_api = get_api(context)
            # password = cs_api.DecryptPassword(resource_config.password).Value
            password = "ciscopsdt"

            aci_api_client = CiscoACIControllerHTTPClient(logger=logger,
                                                          address=resource_config.address,
                                                          user=resource_config.user,
                                                          password=password,
                                                          scheme=resource_config.scheme,
                                                          port=resource_config.port)

            connectivity_runner = CiscoACIConnectivityRunner(resource_config=resource_config,
                                                             aci_api_client=aci_api_client,
                                                             cs_api=cs_api,
                                                             reservation_id=reservation_id,
                                                             logger=logger)

            logger.info('Start applying connectivity changes, request is: {0}'.format(str(request)))
            result = connectivity_runner.apply_connectivity_changes(request=request)
            logger.info('Finished applying connectivity changes, response is: {0}'.format(str(result)))

            return result

    def remote_add_port_to_endpoint_group(self, context):
        """

        :param context:
        :return:
        """
        logger = get_logger_with_thread_id(context)
        logger.info("Add Port to the Endpoint Group command started")

        cs_api = get_api(context)
        reservation_id = "7787550b-8c04-48a1-9940-401b670586ec"
        import ipdb;ipdb.set_trace()

        # VLAN_ID = 335
        # EPG = "fancyapp"
        # PORT = "pod-1/node-101/slot-1/35"

        ################# CALLED ON THE DUT #################
        # # reservation_id = context.remote_reservation.reservation_id
        # reservation_id = "26c98cd8-0336-4b7f-8249-730ce2f53881"
        # resource = Cisco API Ports Controller
        # remote_endpoints = [CS_Port 1, CS_Port 2] <---- DUTS PORT
        # remote_endpoint fullanme - the same as in connector DUT 1/Chassis 1/Module 1/Port 2

        # cs_api = get_api(context)
        # # todo: get reservation ID
        #
        #
        # connectors = cs_api.ReservationDescription.Connectors
        #
        # # {'Direction': 'bi', 'Target': 'DUT 2/Chassis 1/Module 1/Port 2', 'Alias': None,
        # #  'Source': 'DUT 1/Chassis 1/Module 1/Port 2', 'State': 'None', 'Attributes': [], 'Type': 'Default'}
        #
        # cs_api.GetReservationDetails(reservationId=reservation_id)
        # cs_api.GetResourceDetails("DUT 1")
        #
        # # y = ii.ChildResources[0].ChildResources[0].ChildResources
        # # ipdb > yy[0].Connections[0].__dict__
        # # {'FullPath': 'DUT 2/Chassis 1/Module 1/Port 2', 'Weight': 10}

        with ErrorHandlingContext(logger):
            resource_config = CiscoACIControllerResourse.from_context(context=context,
                                                                      shell_type=self.SHELL_TYPE,
                                                                      shell_name=self.SHELL_NAME)

            cs_api = get_api(context)
            password = cs_api.DecryptPassword(resource_config.password).Value

            aci_api_client = CiscoACIControllerHTTPClient(logger=logger,
                                                          address=resource_config.address,
                                                          user=resource_config.user,
                                                          password=password,
                                                          scheme=resource_config.scheme,
                                                          port=resource_config.port)

            connectivity_runner = CiscoACIConnectivityRunner(aci_api_client=aci_api_client,
                                                             logger=logger,
                                                             resource_config=resource_config)

            connectivity_runner.add_port_to_epg(port=PORT, vlan_id=VLAN_ID, epg=EPG)
            logger.info("Add Port to the Endpoint Group command completed")


if __name__ == "__main__":
    import json
    import mock
    from cloudshell.shell.core.driver_context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

    address = "sandboxapicdc.cisco.com"

    user = "admin"
    password = "ciscopsdt"
    port = 443
    scheme = "https"
    auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
    api_port = 8029

    context = ResourceCommandContext(*(None, ) * 4)
    context.resource = ResourceContextDetails(*(None, ) * 13)
    context.resource.name = 'tvm_m_2_fec7-7c42'
    context.resource.fullname = 'tvm_m_2_fec7-7c42'
    context.reservation = ReservationContextDetails(*(None, ) * 7)
    context.reservation.reservation_id = '79350efb-51ba-4f3e-b54c-cd834706d188'
    context.resource.attributes = {}
    context.resource.attributes['{}.Scheme'.format(CiscoAciPortsAutoloadDriver.SHELL_NAME)] = "HTTPS"
    context.resource.attributes['{}.Controller TCP Port'.format(CiscoAciPortsAutoloadDriver.SHELL_NAME)] = 443
    context.resource.attributes['{}.User'.format(CiscoAciPortsAutoloadDriver.SHELL_NAME)] = user
    context.resource.attributes['{}.Password'.format(CiscoAciPortsAutoloadDriver.SHELL_NAME)] = password
    context.resource.address = address
    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = "192.168.85.28"

    # add VLAN
    action = "setVlan"
    # action = "removeVlan"
    request = {"driverRequest": {"actions": [{"connectionId": "22ec7879-e996-4f9a-83ab-bf24f1107281",
                                    "connectionParams": {"vlanId": "1016", "mode": "Access", "vlanServiceAttributes": [
                                        {"attributeName": "QnQ", "attributeValue": "False",
                                         "type": "vlanServiceAttribute"},
                                        {"attributeName": "CTag", "attributeValue": "", "type": "vlanServiceAttribute"},
                                        {"attributeName": "Isolation Level", "attributeValue": "Shared",
                                         "type": "vlanServiceAttribute"},
                                        {"attributeName": "Access Mode", "attributeValue": "Access",
                                         "type": "vlanServiceAttribute"},
                                        {"attributeName": "VLAN ID", "attributeValue": "4011",
                                         "type": "vlanServiceAttribute"},
                                        {"attributeName": "Pool Name", "attributeValue": "",
                                         "type": "vlanServiceAttribute"},
                                        {"attributeName": "Virtual Network", "attributeValue": "255",
                                         "type": "vlanServiceAttribute"}], "type": "setVlanParameter"},
                                    "connectorAttributes": [],
                                    "actionId": "22ec7879-e996-4f9a-83ab-bf24f1107281_085a8f57-d09d-4f92-9201-0da098d14c06",
                                    "actionTarget": {
                                        "fullName": "Cisco ACI Phys Ports/Pod 1/Node 101/Slot 1/Port 1",
                                        "fullAddress": "sandboxapicdc.cisco.com/PD1/N2/S1/P1", "type": "actionTarget"},
                                    "customActionAttributes": [], "type": action}]}}

    request = json.dumps(request)
    dr = CiscoAciPortsAutoloadDriver()
    dr.initialize(context)

    # result = dr.get_inventory(context)
    # result = dr.remote_add_port_to_endpoint_group(context)
    # with mock.patch('__main__.get_api') as get_api:
    #     get_api.return_value = type('api', (object,), {
    #         'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

        # result = dr.get_inventory(context)
        #
        # for res in result.resources:
        #     print res.__dict__
        #
    result = dr.ApplyConnectivityChanges(context, request)
