from setuptools import setup, find_packages

setup(
    name='bouncer',
    version='0.6.1',
    author = 'mfedoseev',
    url = 'https://sprinthost.ru',
    description='Bounce log parser and sender',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'Click',
    ],

    entry_points='''
        [console_scripts]
        bouncer=bouncer.app:cli
    ''',
)
