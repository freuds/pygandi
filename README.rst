========
pygandi
========

CLI for Update DNS on `Gandi <https://gandi.net/>`_


Clone repository
----------------

``git clone https://github.com/freuds/pygandi.git``


Install and Build
-----------------
``$ make help``
Usage: make <command>

Available Commands:
 - make help : Display help for this command (default)
 - make install : Create env with pip
 - make build : Create the wheel package
 - make test : launch pytest on src directory

Install python environment

``$ make install``

Build the package

``$ make build``

Install the wheel package
``$ sudo pip install dist/pygandi-version-py37-none-any.whl``

Use sudo command, if you want install package in the normal site-packages folder

Usage
-----
usage: pygandi [-h] [--ttl TTL] [--noipv4] [--noipv6] [--dry-run] [--log LOG]
               key zone record [record ...]

Keep your gandi DNS records up to date with your current IP (version: 0.1.1)

positional arguments:
  key         Gandi API key or path to a file containing the key.
  zone        Zone to update
  record      Records to update

optional arguments:
  -h, --help  show this help message and exit
  --ttl TTL   Set a custom ttl (in second)
  --noipv4    Do not set 'A' records to current ipv4
  --noipv6    Do not set 'AAAA' records to current ipv6
  --dry-run   do a dry run and don't change anything
  --log LOG   Available levels are CRITICAL (3), ERROR (2), WARNING (1), INFO
              (0), DEBUG (-1)


CRONJOB
-------

Add a file in your /etc/cron.d folder

example: gandi-dns-update

5 * * * * root test -x pygandi && pygandi YOUR_API_KEY example.com www subdomain 

