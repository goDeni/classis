from setuptools import setup, find_packages


setup(
    name='classis',
    version='1.0',
    description='classis',
    packages=find_packages('.'),
    install_requires=['flask'],
    entry_points={
        'console_scripts': [
            'list = classis.cmd.main:main',
        ]
    },
)
