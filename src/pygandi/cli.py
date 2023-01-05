from argparse import ArgumentParser
import argparse
from pygandi import gandi, helpers

import os
import sys
import pkg_resources
import logging
import math

IPV4_PROVIDER_URL = "https://api.ipify.org"
IPV6_PROVIDER_URL = "https://api6.ipify.org"
GANDI_API_URL = "https://dns.api.gandi.net/api/v5"
LOG_FORMAT = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"

def create_parser():

    parser = ArgumentParser(
        description=f"""
    Utility to keep up-to-date your DNS records with your current IP.
    Works with Gandi.net API services

    To authenticate with Gandi API, pass your token as environment variable :
    => API_KEY=xxxxxxxxxx

    Current version : {pkg_resources.require("pygandi")[0].version}""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('zone', type=str, help="Zone to update")
    parser.add_argument('record', type=str, nargs='+', help="Records to update (can be write with a separator")
    parser.add_argument('--ttl', type=int, default=300, help="Set a custom ttl (in second)")
    parser.add_argument('--noipv4', action='store_true', help="Do not set 'A' records to current ipv4")
    parser.add_argument('--noipv6', action='store_false', help="Do not set 'AAAA' records to current ipv6")
    parser.add_argument('--dry-run', action='store_true', help="do a dry run and don't change anything")
    parser.add_argument('--log', type=str, default='INFO', help='Available levels are CRITICAL (3), ERROR (2), WARNING (1), INFO (0), DEBUG (-1)')
    return parser

def mask_string(s, perc=0.8):
    mask_chars = math.ceil(len(s) * perc)
    return f'{"*" * mask_chars}{s[mask_chars:]}'

def main():

    args = create_parser().parse_args()

    try:
        loglevel = getattr(logging, args.log)
    except AttributeError:
        loglevel = {
            3:logging.CRITICAL,
            2:logging.ERROR,
            1:logging.WARNING,
            0:logging.INFO,
            -1:logging.DEBUG,
        }[int(args.log)]

    logging.basicConfig(level=loglevel, format=LOG_FORMAT)
    log = logging.getLogger(__name__)

    log.info('Gandi DNS record update started.')

    if "API_KEY" in os.environ:
        gandi_api_key = os.environ.get('API_KEY')
        log.debug(f'Found variable environment API_KEY : {mask_string(gandi_api_key)}')
    else:
        log.error("Missing env for API_KEY")
        sys.exit(1)

    try:
        helpers.check_apikey_format(gandi_api_key)
    except ValueError as err:
        log.error(err)
        sys.exit(1)

    try:
        helpers.check_domain_format(args.zone)
        log.debug(f'Domain Name found: {args.zone}')
    except Exception as e:
        log.error(e)
        sys.exit(1)

    log.debug(f'Records found: {args.record}')

    api = gandi.GandiAPI(GANDI_API_URL, gandi_api_key, args.dry_run)

    if not args.noipv4:
        current_ipv4 = gandi.get_current_ip(IPV4_PROVIDER_URL)
        api.update_records(args.zone, args.record, current_ipv4, ttl=args.ttl)
    if not args.noipv6:
        current_ipv6 = gandi.get_current_ip(IPV6_PROVIDER_URL)
        api.update_records(
            args.zone, args.record, current_ipv6, ttl=args.ttl, rtype="AAAA"
        )
    log.info('Gandi DNS record update ended.')

if __name__ == ' __main__':
    main()
