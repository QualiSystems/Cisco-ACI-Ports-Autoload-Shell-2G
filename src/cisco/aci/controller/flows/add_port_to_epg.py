import re

from cloudshell.api.common_cloudshell_api import CloudShellAPIError


ACI_EPG_RESOURCE_MODEL = "Cisco ACI EPG Controller.CiscoACIEndPointGroup"
ACI_TENANT_RESOURCE_MODEL = "Cisco ACI EPG Controller.CiscoACITenant"
ACI_NAME_ATTR = "ACI Name"
CS_API_UNABLE_TO_LOCATE_ERROR_CODE = "102"


class CiscoACIAddPortToEPGFlow(object):
    def __init__(self, resource_config, cs_api, aci_api_client, reservation_id, logger):
        """

        :param aci_api_client:
        :param resource_config:
        :param logger:
        """
        self._resource_config = resource_config
        self._cs_api = cs_api
        self._aci_api_client = aci_api_client
        self._reservation_id = reservation_id
        self._logger = logger

    @staticmethod
    def _get_resource_attribute_value(resource, attribute_name):
        """
        :param resource cloudshell.api.cloudshell_api.ResourceInfo:
        :param str attribute_name:
        """
        for attribute in resource.ResourceAttributes:
            if attribute.Name == attribute_name:
                return attribute.Value

    def _get_epg_data(self, phys_connected_devices):
        """Retrieves EPG and Tenant data from the connectors

        :param list[str] phys_connected_devices: list of CS resource names, physically connected  to Port
        :return:
        """
        reservation_details = self._cs_api.GetReservationDetails(self._reservation_id)

        for connector in reservation_details.ReservationDescription.Connectors:
            if connector.Target in phys_connected_devices:
                epg_full_name = connector.Source
            elif connector.Source in phys_connected_devices:
                epg_full_name = connector.Target
            else:
                continue

            try:
                epg_resource = self._cs_api.GetResourceDetails(epg_full_name)
            except CloudShellAPIError as e:
                if e.code == CS_API_UNABLE_TO_LOCATE_ERROR_CODE:
                    continue
                raise

            if epg_resource.ResourceModelName == ACI_EPG_RESOURCE_MODEL:
                epg_aci_name = self._get_resource_attribute_value(
                    resource=epg_resource,
                    attribute_name="{}.{}".format(ACI_EPG_RESOURCE_MODEL, ACI_NAME_ATTR))

                tenant_full_name = epg_resource.Name.rsplit("/", 1)[0]
                tenant_resource = self._cs_api.GetResourceDetails(tenant_full_name)

                tenant_aci_name = self._get_resource_attribute_value(
                    resource=tenant_resource,
                    attribute_name="{}.{}".format(ACI_TENANT_RESOURCE_MODEL, ACI_NAME_ATTR))

                return tenant_aci_name, epg_aci_name

        raise Exception("Unable to find connector to the EPG for port in the reservation")

    def _parse_port_address(self, port_address):
        """

        :param port_address:
        :return:
        """
        return re.search("^.*/PD(?P<pod>\d)/N(?P<node>.*)/S(?P<slot>.*)/P(?P<port>.*)$", port_address).groupdict()

    def execute_flow(self, vlan_range, port_mode, port_name, qnq, c_tag):
        """

        :return:
        """
        port = self._cs_api.GetResourceDetails(port_name)

        phys_connected_devices = [device.FullPath for device in port.Connections]

        tenant_name, epg_name = self._get_epg_data(phys_connected_devices=phys_connected_devices)

        port_data = self._parse_port_address(port.FullAddress)

        self._aci_api_client.add_port_to_epg(pod=port_data["pod"],
                                             node=port_data["node"],
                                             module=port_data["slot"],
                                             port=port_data["port"],
                                             vlan_id=vlan_range,
                                             port_mode=port_mode,
                                             tenant_name=tenant_name,
                                             epg_name=epg_name)
