import re

from cloudshell.api.common_cloudshell_api import CloudShellAPIError
from cloudshell.devices.flows.action_flows import BaseFlow

from cisco.aci.physical.autoload.models import FEX_PORT_FAMILY

ACI_TENANT_RESOURCE_MODEL = "Cisco ACI EPG Controller.CiscoACITenant"
ACI_APP_PROFILE_RESOURCE_MODEL = "Cisco ACI EPG Controller.CiscoACIAppProfile"
ACI_EPG_RESOURCE_MODEL = "Cisco ACI EPG Controller.CiscoACIEndPointGroup"
ACI_NAME_ATTR = "ACI Name"
CS_API_UNABLE_TO_LOCATE_ERROR_CODE = "102"


class BasePortToEPGActionFlow(BaseFlow):
    def __init__(self, resource_config, cs_api, aci_api_client, reservation_id, logger):
        """EPG Port Action Flow base class.

        :param aci_api_client:
        :param resource_config:
        :param logger:
        """
        super(BasePortToEPGActionFlow, self).__init__(cli_handler=None, logger=logger)
        self._resource_config = resource_config
        self._cs_api = cs_api
        self._aci_api_client = aci_api_client
        self._reservation_id = reservation_id

    def _get_resource_attribute_value(self, resource, attribute_name):
        for attribute in resource.ResourceAttributes:
            if attribute.Name == attribute_name:
                return attribute.Value

    def _get_epg_data(self, phys_connected_devices):
        """Retrieves EPG and Tenant data from the connectors.

        :param list[str] phys_connected_devices: list of CS resource names,
        physically connected to Port
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
                    attribute_name="{}.{}".format(
                        ACI_EPG_RESOURCE_MODEL, ACI_NAME_ATTR
                    ),
                )

                app_profile_full_name = epg_resource.Name.rsplit("/", 1)[0]
                app_profile_resource = self._cs_api.GetResourceDetails(
                    app_profile_full_name
                )

                app_profile_aci_name = self._get_resource_attribute_value(
                    resource=app_profile_resource,
                    attribute_name="{}.{}".format(
                        ACI_APP_PROFILE_RESOURCE_MODEL, ACI_NAME_ATTR
                    ),
                )

                tenant_full_name = app_profile_resource.Name.rsplit("/", 1)[0]
                tenant_resource = self._cs_api.GetResourceDetails(tenant_full_name)

                tenant_aci_name = self._get_resource_attribute_value(
                    resource=tenant_resource,
                    attribute_name="{}.{}".format(
                        ACI_TENANT_RESOURCE_MODEL, ACI_NAME_ATTR
                    ),
                )

                return tenant_aci_name, app_profile_aci_name, epg_aci_name

        raise Exception(
            "Unable to find connector to the EPG for port in the reservation"
        )

    def _get_port_data(self, port):
        if port.ResourceFamilyName == FEX_PORT_FAMILY:
            return self._parse_fex_port_address(port.FullAddress)

        return self._parse_port_address(port.FullAddress)

    def _parse_port_address(self, port_address):

        return re.search(
            r"^.*/PD(?P<pod>\d)/N(?P<node>.*)/S(?P<slot>.*)/P(?P<port>.*)$",
            port_address,
        ).groupdict()

    def _parse_fex_port_address(self, fex_port_address):
        return re.search(
            r"^.*/PD(?P<pod>\d)/N(?P<node>.*)/F(?P<fex>.*)/FS(?P<slot>.*)/FP("
            r"?P<port>.*)$",
            fex_port_address,
        ).groupdict()

    def _get_phys_connected_device(self, port_resource):
        return [device.FullPath for device in port_resource.Connections]
