from setuptools import setup

setup(
    name='zabbctl',
    version='0.1',
    py_modules=['zabbctl'],
    install_requires=[
        'Click',
	'pyzabbix',
	'tabulate',
    ],
    entry_points='''
        [console_scripts]
        zabbctl=zabbctl.app:cli
    ''',
)
