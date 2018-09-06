from cloudshell.devices.autoload.autoload_builder import AutoloadDetailsBuilder

from cisco.aci.physical.autoload import models


class CiscoACIAutoloadFlow(object):
    def __init__(self, aci_api_client, resource_config, logger):
        """

        :param aci_api_client:
        :param resource_config:
        :param logger:
        """
        self._aci_api_client = aci_api_client
        self._resource_config = resource_config
        self._logger = logger

    def execute_flow(self):
        """

        :return:
        """
        root_resource = models.CiscoACIController(shell_name=self._resource_config.shell_name,
                                                  name="Cisco ACI Ports Controller",
                                                  unique_id=self._resource_config.fullname)

        ports_data = self._aci_api_client.get_leaf_ports()

        for pod_id, pod_data in ports_data["pods"].iteritems():
            pod_resource = models.CiscoACIPod(shell_name=self._resource_config.shell_name,
                                              name="Pod {}".format(pod_id),
                                              unique_id="{}.{}".format(self._resource_config.fullname, pod_id))

            root_resource.add_sub_resource(pod_id, pod_resource)

            for node_id, node_data in pod_data["nodes"].iteritems():
                node_resource = models.CiscoACINode(shell_name=self._resource_config.shell_name,
                                                    name="Node {}".format(node_id),
                                                    unique_id="{}.{}.{}".format(self._resource_config.fullname,
                                                                                pod_id, node_id))

                pod_resource.add_sub_resource(node_id, node_resource)

                for slot_id, slot_data in node_data["slots"].iteritems():
                    slot_resource = models.CiscoACISlot(shell_name=self._resource_config.shell_name,
                                                        name="Slot {}".format(slot_id),
                                                        unique_id="{}.{}.{}.{}".format(
                                                            self._resource_config.fullname, pod_id, node_id, slot_id))

                    node_resource.add_sub_resource(slot_id, slot_resource)

                    for port_data in slot_data["ports"]:
                        port_id = port_data["id"]
                        port_resource = models.CiscoACIPort(shell_name=self._resource_config.shell_name,
                                                            name="Port {}".format(port_id),
                                                            unique_id="{}.{}.{}.{}.{}".format(
                                                                self._resource_config.fullname, pod_id, node_id,
                                                                slot_id, port_id))

                        slot_resource.add_sub_resource(port_id, port_resource)

                for fex_id, fex_data in node_data["fexs"].iteritems():
                    fex_resource = models.CiscoACIFex(shell_name=self._resource_config.shell_name,
                                                      name="FEX {}".format(fex_id),
                                                      unique_id="{}.{}.{}.{}".format(
                                                          self._resource_config.fullname, pod_id, node_id, fex_id))

                    node_resource.add_sub_resource(fex_id, fex_resource)

                    for slot_id, slot_data in fex_data["slots"].iteritems():
                        slot_resource = models.CiscoACIFexSlot(shell_name=self._resource_config.shell_name,
                                                               name="Slot {}".format(slot_id),
                                                               unique_id="{}.{}.{}.{}.{}".format(
                                                                   self._resource_config.fullname, pod_id, node_id,
                                                                   fex_id, slot_id))

                        fex_resource.add_sub_resource(slot_id, slot_resource)

                        for port_data in slot_data["ports"]:
                            port_id = port_data["id"]
                            port_resource = models.CiscoACIFexPort(shell_name=self._resource_config.shell_name,
                                                                   name="Port {}".format(port_id),
                                                                   unique_id="{}.{}.{}.{}.{}.{}".format(
                                                                       self._resource_config.fullname, pod_id, node_id,
                                                                       fex_id, slot_id, port_id))

                            slot_resource.add_sub_resource(port_id, port_resource)

        return AutoloadDetailsBuilder(root_resource).autoload_details()
