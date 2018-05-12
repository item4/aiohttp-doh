aiohttp-doh
===========

DNS over HTTPS reslover for aiohttp


Installation
------------

.. code-block:: bash

   $ pip install aiohttp-doh


Usage
-----

.. code-block:: python3

   # You just replace aiohttp.ClientSession to aiohttp_doh.ClientSession
   from aiohttp_doh import ClientSession

   async def main():
       async with ClientSession() as session:
           async with session.get('http://example.com') as resp:
               data = await resp.text()

       print(data)


Configuration
-------------

You can pass some options by parameters of ``ClientSession``.

endpoint
  DNS over HTTPS endpoint. default is `'https://dns.google.com/resolve'`.
  You can also use others instead.

json_loads
  Function for loads json. default is Python builtin json module's one.

resolver_class
  Internal DNS resolver class. Using for connect to endpoint.
  default is aiohttp default.


License
-------

MIT
