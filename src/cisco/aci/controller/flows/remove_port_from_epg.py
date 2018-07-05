from cloudshell.devices.flows.action_flows import RemoveVlanFlow


class CiscoACIRemovePortFromEPGFlow(object):
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

    def execute_flow(self, vlan_range, port_name, port_mode):
        """

        :return:
        """
        port = "".split()
        pod = "1"
        node = "101"
        module = "1"
        port = "45"
        epg = "tenant/epg_name".split()
        tenant_name = "qs_tenant"
        epg_name = "qs_epg"
        return
        self._aci_api_client.add_port_to_epg(pod=pod,
                                             node=node,
                                             module=module,
                                             port=port,
                                             vlan_id=vlan_id,
                                             tenant_name=tenant_name,
                                             epg_name=epg_name)
