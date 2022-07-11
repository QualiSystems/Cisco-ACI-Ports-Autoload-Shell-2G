from cloudshell.devices.runners.autoload_runner import AutoloadRunner

from cisco.aci.physical.flows.autoload import CiscoACIAutoloadFlow


class CiscoACIAutoloadRunner(AutoloadRunner):
    def __init__(self, resource_config, aci_api_client, logger):
        super(CiscoACIAutoloadRunner, self).__init__(resource_config)
        self._aci_api_client = aci_api_client
        self._logger = logger

    @property
    def autoload_flow(self):
        return CiscoACIAutoloadFlow(
            aci_api_client=self._aci_api_client,
            resource_config=self.resource_config,
            logger=self._logger,
        )

    def discover(self):
        return self.autoload_flow.execute_flow()
