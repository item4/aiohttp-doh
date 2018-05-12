import os.path

from setuptools import setup

setup(
    name='aiohttp-doh',
    version='0.0.0',
    description='DNS over HTTPS reslover for aiohttp',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Kim, Jinsu',
    author_email=('item4_hun' '@' 'hotmail.com'),
    url='https://github.com/item4/aiohttp-doh/',
    license='MIT',
    keywords='aiohttp asyncio dns https',
    py_modules=['aiohttp_doh'],
    install_requires=['aiohttp'],
    python_requires='~=3.5',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
    ],
)
