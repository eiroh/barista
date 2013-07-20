from setuptools import setup, find_packages

setup(
    name='barista',
    version='0.1',
    description='call api for system operators',
    author='HiDE',
    url='http://6pongi.wordpress.com',
    packages=find_packages(),
    license='Apache License, Version 2.0',
    install_requires=[
        'pyres == 1.4.1',
        'redis == 2.7.2',
        'tornado == 2.4.1',
        'twilio == 3.4.5',
    ],
)
