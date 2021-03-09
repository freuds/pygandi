from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='pygandi',
    version='0.1.1',
    description='Commandline DNS management utility for Gandi',
    long_description=readme,
    author='Fred',
    author_email='fred@freuds.me',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pygandi=pygandi.cli:main',
        ],
    }
)