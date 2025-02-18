# calculator.py
#
# Copyright 2024 Vladimir Kosolapov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import ipaddress

class IPCalculator:
    def __init__(self):
        self.show_binary = False

    def set_show_binary(self, show_binary):
        self.show_binary = show_binary

    def calculate(self, ip, mask):
        try:
            interface = ipaddress.IPv4Interface(f"{ip}/{mask}")
            network = interface.network
            results = {
                (_('Address')): self.format_ip(interface.ip),
                (_('Netmask')): self.format_ip(network.netmask),
                (_('Wildcard')): self.format_ip(network.hostmask),
                (_('Network')): self.format_ip(network.network_address),
                (_('First Host')): self.format_ip(network.network_address + 1),
                (_('Last Host')): self.format_ip(network.broadcast_address - 1),
                (_('Broadcast')): self.format_ip(network.broadcast_address),
                (_('Total Hosts')): str(network.num_addresses - 2),
                (_('Category')): self.get_ip_class(interface.ip)
            }
            return results
        except ValueError:
            return {(_('Error')): (_('Invalid IP address or mask'))}

    def format_ip(self, ip):
        if self.show_binary:
            return f"{ip} ({self.ip_to_binary(ip)})"
        return str(ip)

    def ip_to_binary(self, ip):
        return '.'.join([bin(int(x)+256)[3:] for x in str(ip).split('.')])

    def get_ip_class(self, ip):
        ip_int = int(ipaddress.IPv4Address(ip))
        if ipaddress.IPv4Address('10.0.0.0') <= ip <= ipaddress.IPv4Address('10.255.255.255'):
            return (_('Private (Class A)'))
        elif ipaddress.IPv4Address('172.16.0.0') <= ip <= ipaddress.IPv4Address('172.31.255.255'):
            return (_('Private (Class B)'))
        elif ipaddress.IPv4Address('192.168.0.0') <= ip <= ipaddress.IPv4Address('192.168.255.255'):
            return (_('Private (Class C)'))
        elif ipaddress.IPv4Address('127.0.0.0') <= ip <= ipaddress.IPv4Address('127.255.255.255'):
            return (_('Loopback'))
        elif ipaddress.IPv4Address('169.254.0.0') <= ip <= ipaddress.IPv4Address('169.254.255.255'):
            return (_('Link-Local (APIPA)'))
        elif ipaddress.IPv4Address('224.0.0.0') <= ip <= ipaddress.IPv4Address('239.255.255.255'):
            return (_('Multicast'))
        elif ipaddress.IPv4Address('240.0.0.0') <= ip <= ipaddress.IPv4Address('255.255.255.255'):
            return (_('Reserved'))
        else:
            return (_('Public'))

    def int_to_dotted_netmask(self, mask_int):
        mask = (0xffffffff >> (32 - mask_int)) << (32 - mask_int)
        return '.'.join([str((mask >> (8 * i)) & 0xff) for i in range(3, -1, -1)])
