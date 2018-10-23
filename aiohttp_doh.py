import asyncio
import enum
import json
import socket
from typing import List

from aiohttp.abc import AbstractResolver
from aiohttp.client import ClientSession as CS
from aiohttp.connector import TCPConnector
from aiohttp.resolver import DefaultResolver

__all__ = 'ClientSession', 'DNSOverHTTPSResolver', 'RecordType'


class RecordType(enum.Enum):
    """Record Type"""

    A = 1
    AAAA = 28


class DNSOverHTTPSResolver(AbstractResolver):
    """DNS over HTTPS Resolver"""

    def __init__(
        self,
        *,
        endpoints: List[str],
        json_loads=json.loads,
        resolver_class=None,
    ) -> None:
        self.endpoints = endpoints
        self.json_loads = json_loads
        if resolver_class is None:
            resolver_class = DefaultResolver
        self.resolveer_class = resolver_class
    
    async def _resolve(self, endpoint: str, host, port, family):
        if family == socket.AF_INET6:
            record_type = RecordType.AAAA
        else:
            record_type = RecordType.A

        params = {
            'ct': 'application/dns-json',
            'name': host,
            'type': record_type.name,
        }

        resolver = self.resolveer_class()
        connector = TCPConnector(resolver=resolver)
    
        async with CS(connector=connector) as session:
            async with session.get(endpoint, params=params) as resp:
                data = self.json_loads(await resp.text())

        connector.close()

        if data['Status'] != 0:
            raise OSError("DNS lookup failed")

        return [
            {
                'hostname': host,
                'host': r['data'],
                'port': port,
                'family': family,
                'proto': 0,
                'flags': socket.AI_NUMERICHOST
            } for r in data['Answer']
            if r['type'] in (
                record_type.name,
                record_type.value,
            ) and r['data']
        ]

    async def resolve(self, host, port=0, family=socket.AF_INET):
        tasks = [
            self._resolve(endpoint, host, port, family)
            for endpoint in self.endpoints
        ]
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED,
        )
        for p in pending:
            p.cancel()
        return list(done)[0].result()

    async def close(self):
        pass


def ClientSession(*args, **kwargs) -> CS:  # noqa
    """Shortcut of aiohttp.ClientSession and DNSOverHTTPSResolver"""

    endpoints = kwargs.pop(
        'endpoints',
        [
            'https://dns.google.com/resolve',
            'https://cloudflare-dns.com/dns-query',
        ],
    )
    json_loads = kwargs.pop('json_loads', json.loads)
    resolver_class = kwargs.pop('resolver_class', None)
    resolver = DNSOverHTTPSResolver(
        endpoints=endpoints,
        json_loads=json_loads,
        resolver_class=resolver_class,
    )
    connector = TCPConnector(resolver=resolver)

    return CS(*args, **kwargs, connector=connector)
