"""Set up Breqwatr Deployment Tool package"""
from setuptools import setup

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

requirements = []
with open('requirements.txt', 'r') as reqs_file:
    requirements = reqs_file.read().splitlines()

setup(
    name='breqwatr-deployment-tool',
    packages=['bwdt'],
    version='1.00',
    license='',
    description='Deploy and manage Breqwatr services',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kyle Pericak',
    author_email='kyle@breqwatr.com',
    url='https://github.com/breqwatr/breqwatr-deployment-tool',
    keywords=['Breqwatr'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        bwdt=bwdt.cli.main:main
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ]
)
