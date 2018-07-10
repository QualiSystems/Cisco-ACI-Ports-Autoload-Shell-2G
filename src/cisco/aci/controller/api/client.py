import acitoolkit.acitoolkit as aci

INTERFACE_TYPE = "eth"
L2_INTERFACE_ENCAP_TYPE = "vlan"

PORT_TRUNK_MODE = "regular"
PORT_ACCESS_UNTAGGED_MODE = "untagged"
PORT_ACCESS_MODE = "native"
PORT_MODE_MAP = {
    "access": PORT_ACCESS_MODE,  # todo: clarify which option use for the access mode (802.1P|Untagged)
    "trunk": PORT_TRUNK_MODE
}


class CiscoACIControllerHTTPClient(object):
    def __init__(self, logger, address, user=None, password=None, scheme="https", port=443):
        """

        :param logging.Logger logger:
        :param str address: controller IP address
        :param str user: controller username
        :param str password: controller password
        :param str scheme: protocol (http|https)
        :param int port: controller port
        """
        full_url = "{}://{}:{}".format(scheme.lower(), address, port)
        self._logger = logger
        self._session = aci.Session(url=full_url, uid=user, pwd=password)
        self._login()

    def _login(self):
        """

        :return:
        """
        resp = self._session.login()

        if not resp.ok:
            self._logger.error("Unable to login to the ACI Controller. HTTP Status code: {} Response: {}"
                               .format(resp.status_code, resp.content))
            raise Exception("Unable to login to the ACI Controller")

    def get_tenant(self, tenant_name):
        """

        :return:
        """
        for tenant in aci.Tenant.get(session=self._session):
            if tenant_name == tenant.name:
                return tenant

        raise Exception("Unable to find Tenant with name '{}'".format(tenant_name))

    def get_epg(self, epg_name, tenant=None):
        """

        :return:
        """
        for epg in aci.EPG.get(session=self._session, tenant=tenant):
            if epg_name == epg.name:
                return epg

        raise Exception("Unable to find EPG with name '{}'".format(epg_name))

    def get_leaf_ports(self):
        """Get leaf ports in the next format: pod->node->slot->port

        :return:
        """
        ports_data = {}
        interfaces = aci.Interface.get(session=self._session)

        for interface in interfaces:
            if interface.attributes['porttype'].lower() == "leaf":
                nodes = ports_data.setdefault(interface.pod, {})
                slots = nodes.setdefault(interface.node, {})
                ports = slots.setdefault(interface.module, [])
                ports.append({
                    "id": interface.port,
                    "name": interface.name
                })

        return ports_data

    def add_port_to_epg(self, pod, node, module, port, vlan_id, port_mode, tenant_name, app_profile_name, epg_name):
        """

        :param pod:
        :param node:
        :param module:
        :param port:
        :param vlan_id:
        :param port_mode:
        :param tenant_name:
        :param app_profile_name:
        :param epg_name:
        :return:
        """
        tenant = self.get_tenant(tenant_name)

        app = aci.AppProfile(app_profile_name, tenant)
        epg = aci.EPG(epg_name=epg_name, parent=app)

        # create the physical interface object
        intf = aci.Interface(interface_type=INTERFACE_TYPE,
                             pod=pod,
                             node=node,
                             module=module,
                             port=port)

        # create a VLAN interface and attach to the physical interface
        vlan_intf = aci.L2Interface(name=vlan_id,
                                    encap_type=L2_INTERFACE_ENCAP_TYPE,
                                    encap_id=vlan_id,
                                    encap_mode=PORT_MODE_MAP[port_mode])

        vlan_intf.attach(intf)

        # attach EPG to the VLAN interface
        epg.attach(vlan_intf)

        # push the tenant config to the APIC
        resp = tenant.push_to_apic(self._session)
        self._logger.info("Pushed Tenant data {}".format(tenant.get_json()))

        if not resp.ok:
            raise Exception('Could not push tenant configuration to APIC. Error response: {}'.format(resp.content))

        # push the interface attachment to the APIC
        self._logger.info("Pushed Interface data {}".format(intf.get_json()))
        resp = intf.push_to_apic(self._session)

        if not resp.ok:
            raise Exception('Could not push interface configuration to APIC. Error response: {}'.format(resp.content))

    def remove_port_from_epg(self, pod, node, module, port, vlan_id, port_mode, tenant_name,
                             app_profile_name, epg_name):
        """

        :param pod:
        :param node:
        :param module:
        :param port:
        :param vlan_id:
        :param port_mode:
        :param tenant_name:
        :param app_profile_name:
        :param epg_name:
        :return:
        """
        tenant = self.get_tenant(tenant_name)

        app = aci.AppProfile(app_profile_name, tenant)
        epg = aci.EPG(epg_name=epg_name, parent=app)

        # create the physical interface object
        intf = aci.Interface(interface_type=INTERFACE_TYPE,
                             pod=pod,
                             node=node,
                             module=module,
                             port=port)

        # create a VLAN interface and attach to the physical interface
        vlan_intf = aci.L2Interface(name=vlan_id,
                                    encap_type=L2_INTERFACE_ENCAP_TYPE,
                                    encap_id=vlan_id,
                                    encap_mode=PORT_MODE_MAP[port_mode])

        vlan_intf.attach(intf)

        # attach EPG to the VLAN interface
        epg.detach(vlan_intf)

        # push the tenant config to the APIC
        resp = tenant.push_to_apic(self._session)
        self._logger.info("Pushed Tenant data {}".format(tenant.get_json()))

        if not resp.ok:
            raise Exception('Could not push tenant configuration to APIC. Error response: {}'.format(resp.content))