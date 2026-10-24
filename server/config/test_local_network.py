import os
from unittest import TestCase
from unittest.mock import patch
from local_network import lan_ipv4_addresses


class LocalNetworkTests(TestCase):
    @patch.dict(os.environ, {'FLUIDMES_LAN_IP': ''})
    @patch('local_network.socket.getaddrinfo')
    def test_discovery_filters_non_lan_addresses_and_duplicates(self, lookup):
        lookup.return_value = [(None, None, None, None, (ip, 0)) for ip in [
            '192.168.10.2', '127.0.0.1', '0.0.0.0', '224.0.0.1', '255.255.255.255', '192.168.10.2',
        ]]
        self.assertEqual(lan_ipv4_addresses(), ['192.168.10.2'])

    @patch.dict(os.environ, {'FLUIDMES_LAN_IP': '192.168.30.4,10.0.0.8'})
    @patch('local_network.socket.getaddrinfo')
    def test_explicit_addresses_work_without_discovery(self, lookup):
        self.assertEqual(lan_ipv4_addresses(), ['10.0.0.8', '192.168.30.4'])
        lookup.assert_not_called()

    @patch.dict(os.environ, {'FLUIDMES_LAN_IP': ''})
    @patch('local_network.socket.getaddrinfo', side_effect=OSError)
    def test_failed_discovery_keeps_local_access_available(self, lookup):
        self.assertEqual(lan_ipv4_addresses(), [])

    @patch.dict(os.environ, {'FLUIDMES_LAN_IP': 'http://192.168.10.2:5173'})
    def test_invalid_explicit_address_is_rejected(self):
        with self.assertRaises(ValueError):
            lan_ipv4_addresses()
