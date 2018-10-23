aiohttp-doh
===========

DNS over HTTPS reslover for aiohttp


Installation
------------

.. code-block:: bash

   $ pip install aiohttp-doh


Manual Usage
------------

If you want use manualy, you must import ``ClientSession`` in ``aiohttp.client``
module and ``TCPConnector`` in ``aiohttp.connector`` module and ``DNSOverHTTPSResolver``
in ``aiohttp_doh`` package.

.. code-block:: python3

   from aiohttp.client import ClientSession
   from aiohttp.connector import TCPConnector

   from aiohttp_doh import DNSOverHTTPSResolver

   def my_client_session(*args, **kwargs):
       resolver = DNSOverHTTPSResolver(endpoints=[
           'https://cloudflare-dns.com/dns-query',
       ])
       connector = TCPConnector(resolver=resolver)
       return ClientSession(*args, **kwargs, connector=connector)

    async def main():
       async with my_client_session() as session:
           async with session.get('http://example.com') as resp:
               data = await resp.text()

       print(data)


Shortcut
--------

Manual usage is too board. So I make shortcut to use easily.
You just replace ``aiohttp.ClientSession`` to ``aiohttp_doh.ClientSession``.

.. code-block:: python3

   from aiohttp_doh import ClientSession

   async def main():
       async with ClientSession() as session:
           async with session.get('http://example.com') as resp:
               data = await resp.text()

       print(data)


Options
-------

You can pass below parameter for configuration.

endpoints
  List of str. DNS over HTTPS endpoints.
  Shortcut use `'https://dns.google.com/resolve'`
  and `'https://cloudflare-dns.com/dns-query'` both in default.
  You can also use others instead.

json_loads
  Function for loads json. default is Python builtin json module's one.
  You can use third-party json library like simplejson or ujson.

resolver_class
  Internal DNS resolver class. Using for connect to endpoint.
  default is aiohttp default.


License
-------

MIT
