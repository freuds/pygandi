from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

def get_version():
    with open('VERSION', encoding='UTF-8') as f:
        version_content = f.read()

    if (version_content):
        return version_content
    raise ValueError('Unable to find version string')

setup(
    name='pygandi',
    version=get_version(),
    description='Commandline DNS management utility for Gandi',
    long_description=readme,
    author='Fred',
    author_email='fred@freuds.me',
    project_urls={
        'Bug Tracker': 'https://github.com/freuds/pygandi/issues',
        'Source Code': 'https://github.com/freuds/pygandi',
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.7,<3.12',
    keywords='cli gandi dns utility',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pygandi=pygandi.cli:main',
        ],
    }
)