from setuptools import setup, find_packages

setup(
    name='oura_cdm',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['pandas', 'pandera', 'requests']
)
