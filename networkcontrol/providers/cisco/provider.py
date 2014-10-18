from networkcontrol.providers.base import BaseSwitchBackend
from networkcontrol.providers import registry

class CiscoSwitchBackend(BaseSwitchBackend):

    id = 'CiscoSwitch'
    name = 'Cisco Switch'

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def login(self):
        raise NotImplementedError()

    def find_mac_address(self, ip):
        raise NotImplementedError()

    def change_vlan(self, mac_address, vlan_id):
        raise NotImplementedError()

    def show_port(self, mac_address):
        raise NotImplementedError()


registry.register(CiscoSwitchBackend)