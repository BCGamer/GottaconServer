from network.providers.base import BaseSwitchBackend
from network.providers import registry
from network.exceptions import MacNotFound
from netaddr import *
import re
import time


class CiscoSwitchBackend(BaseSwitchBackend):

    id = 'CiscoSwitch'
    name = 'Cisco Switch'

    def ssh_find_port(self, mac):
        # Format as 00:00:00:00:00:00
        mac = EUI(mac, dialect=mac_unix)

        self.ssh_run_command("show mac-address-table address %s" % mac)
        output = self.ssh_receive_data()
        port = re.findall(r'Fa0/\d+', output)

        if len(port) == 1:
            return port[0]
        else:
            # There is a problem
            raise MacNotFound()

    def ssh_change_port_vlan(self, port, vlan):
        # Confirm port is presented correctly
        # Lookup correct name
        portname = re.findall(r'\D+\d+\/\d+', port)

        if not portname:
            try:
                portname = self.snmp_find_portname(port)
            except Exception, e:
                pass

        # Change the port's VLAN
        self.ssh_run_command("configure terminal")
        self.ssh_run_command("interface %s" % portname)
        self.ssh_run_command("switchport access vlan %s" % vlan)
        self.ssh_run_command("shutdown")
        time.sleep(1)
        self.ssh_run_command("no shutdown")
        self.ssh_receive_data()

#registry.register(CiscoSwitchBackend)