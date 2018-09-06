from cloudshell.devices.flows.action_flows import AddVlanFlow

from cisco.aci.physical.flows.connectivity.base_port_to_epg import BasePortToEPGActionFlow

from cisco.aci.physical.autoload.models import FEX_PORT_FAMILY


class CiscoACIAddPortToEPGFlow(BasePortToEPGActionFlow, AddVlanFlow):
    def __init__(self, resource_config, cs_api, aci_api_client, reservation_id, logger):
        """

        :param resource_config:
        :param cs_api:
        :param aci_api_client:
        :param reservation_id:
        :param logger:
        """
        BasePortToEPGActionFlow.__init__(self,
                                         resource_config=resource_config,
                                         cs_api=cs_api,
                                         aci_api_client=aci_api_client,
                                         reservation_id=reservation_id,
                                         logger=logger)

        AddVlanFlow.__init__(self, cli_handler=None, logger=logger)

    def execute_flow(self, vlan_range, port_mode, port_name, qnq, c_tag):
        """

        :return:
        """
        port = self._cs_api.GetResourceDetails(port_name)

        phys_connected_devices = self._get_phys_connected_device(port_resource=port)

        if port.ResourceFamilyName == FEX_PORT_FAMILY:
            port_data = self._parse_fex_port_address(port.FullAddress)
        else:
            port_data = self._parse_port_address(port.FullAddress)

        tenant_name, app_profile_name, epg_name = self._get_epg_data(phys_connected_devices=phys_connected_devices)

        self._aci_api_client.add_port_to_epg(pod=port_data["pod"],
                                             node=port_data["node"],
                                             fex=port_data.get("fex"),
                                             module=port_data["slot"],
                                             port=port_data["port"],
                                             vlan_id=vlan_range,
                                             port_mode=port_mode,
                                             tenant_name=tenant_name,
                                             app_profile_name=app_profile_name,
                                             epg_name=epg_name)
