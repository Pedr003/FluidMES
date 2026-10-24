"""Discover local IPv4 addresses without connecting to an external service."""
import ipaddress
import os
import socket


def lan_ipv4_addresses():
    explicit = os.environ.get('FLUIDMES_LAN_IP', '').strip()
    if explicit:
        candidates = [str(ipaddress.IPv4Address(value.strip())) for value in explicit.split(',')]
    else:
        try:
            candidates = [item[4][0] for item in socket.getaddrinfo(
                socket.gethostname(), None, socket.AF_INET, socket.SOCK_STREAM,
            )]
        except OSError:
            candidates = []
    return sorted({value for value in candidates if not (
        ipaddress.IPv4Address(value).is_loopback
        or ipaddress.IPv4Address(value).is_unspecified
        or ipaddress.IPv4Address(value).is_multicast
        or value == '255.255.255.255'
    )})
