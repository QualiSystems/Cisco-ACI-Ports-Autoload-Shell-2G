from cloudshell.devices.runners.connectivity_runner import ConnectivityRunner

from cisco.aci.physical.flows.connectivity.add_port_to_epg import (
    CiscoACIAddPortToEPGFlow,
)
from cisco.aci.physical.flows.connectivity.remove_port_from_epg import (
    CiscoACIRemovePortFromEPGFlow,
)


class CiscoACIConnectivityRunner(ConnectivityRunner):
    def __init__(self, resource_config, cs_api, aci_api_client, reservation_id, logger):
        super(CiscoACIConnectivityRunner, self).__init__(
            logger=logger, cli_handler=None
        )
        self._resource_config = resource_config
        self._cs_api = cs_api
        self._aci_api_client = aci_api_client
        self._reservation_id = reservation_id
        self._logger = logger

    def _get_vlan_list(self, vlan_str):
        """Get VLAN list from input string.

        :param str vlan_str:
        :return list of VLANs or Exception
        """
        if "," in vlan_str or "-" in vlan_str:
            raise Exception(
                "Wrong VLAN parameter detected: {}. "
                "Cisco ACI supports only one VLAN per Port in EPG".format(vlan_str)
            )

        return super(CiscoACIConnectivityRunner, self)._get_vlan_list(vlan_str)

    @property
    def add_vlan_flow(self):
        return CiscoACIAddPortToEPGFlow(
            resource_config=self._resource_config,
            cs_api=self._cs_api,
            aci_api_client=self._aci_api_client,
            reservation_id=self._reservation_id,
            logger=self._logger,
        )

    @property
    def remove_vlan_flow(self):
        return CiscoACIRemovePortFromEPGFlow(
            resource_config=self._resource_config,
            aci_api_client=self._aci_api_client,
            cs_api=self._cs_api,
            reservation_id=self._reservation_id,
            logger=self._logger,
        )
