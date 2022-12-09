========
pygandi
========

CLI for create / Update DNS records on `Gandi.net <https://gandi.net/>`_

Install and Build
-----------------
``$ make help``

Usage: make <command>

Available Commands:
 - make help : Display help for this command (default)
 - make pyenv : Create python environment and install needed python modules
 - make pywheel : Create the python wheel package
 - make pytest : launch pytest on src directory
 - make image : create local docker image
 - make image-test : run docker image
 - make image-push : push local image on docker hub

Install python environment

``$ make pyenv``

Build the package

``$ make pywheel``

Install the wheel package
``$ sudo pip install dist/pygandi-version-py37-none-any.whl``

Use sudo command, if you want install package in the normal site-packages folder

Usage
-----
usage: pygandi [-h] [--ttl TTL] [--noipv4] [--noipv6] [--dry-run] [--log LOG] apikey zone record [record ...]

    Utility to keep up-to-date your DNS records with your current IP.
    Works with Gandi.net API services
    Current version : 0.1.4

positional arguments:
  zone        Zone to update
  record      Records to update

optional arguments:
  -h, --help  show this help message and exit
  --ttl TTL   Set a custom ttl (in second)
  --noipv4    Do not set 'A' records to current ipv4
  --noipv6    Do not set 'AAAA' records to current ipv6
  --dry-run   do a dry run and don't change anything
  --log LOG   Available levels are CRITICAL (3), ERROR (2), WARNING (1), INFO (0), DEBUG (-1)

DEVELOPMENT
-----------

``$ make pyenv``

This command install dependency libraries and activate a virtualenv :
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.

To launch the script, you can use:
``PYTHONPATH=./src API_KEY=xxxxx pygandi --help``

INSTALL AS CLASSIC CRONJOB
--------------------------

Add a file in your /etc/cron.d folder

example: gandi-dns-update

``5 * * * * root test -x pygandi && API_KEY=xxxxxxxxxx ; pygandi example.com www subdomain1 subdomain2``

DOCKER IMAGE
-------------------------

You can use a docker image for launch in kubernetes as cronjob : `DockerHub <https://hub.docker.com/repository/docker/freuds2k/pygandi>`_
