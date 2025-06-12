# Standard library imports
import argparse
import logging
import math
import os
import sys
from argparse import ArgumentParser
from importlib.metadata import version

from pygandi import gandi, helpers
from pygandi.gandi import DNSUpdateRequest

IPV4_PROVIDER_URL = "https://api.ipify.org"
IPV6_PROVIDER_URL = "https://api6.ipify.org"
GANDI_API_URL = "https://dns.api.gandi.net/api/v5"
LOG_FORMAT = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"


def create_parser() -> ArgumentParser:
    """Create and return the argument parser.

    Returns:
        ArgumentParser: The configured argument parser
    """
    parser = ArgumentParser(
        description=f"""
    Utility to keep up-to-date your DNS records with your current IP.
    Works with Gandi.net API services

    To authenticate with Gandi API, pass your token as environment variable :
    => API_TOKEN=xxxxxxxxxx

    Current version : {version("pygandi")}""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("zone", type=str, help="Zone to update")
    parser.add_argument(
        "record", type=str, nargs="+", help="Records to update (can be write with a separator"
    )
    parser.add_argument("--ttl", type=int, default=300, help="Set a custom ttl (in second)")
    parser.add_argument(
        "--noipv4", action="store_true", help="Do not set 'A' records to current ipv4"
    )
    parser.add_argument(
        "--noipv6", action="store_false", help="Do not set 'AAAA' records to current ipv6"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="do a dry run and don't change anything"
    )
    parser.add_argument(
        "--log",
        type=str,
        default="INFO",
        help="Available levels are CRITICAL (3), ERROR (2), WARNING (1), INFO (0), DEBUG (-1)",
    )
    return parser


def mask_string(s: str, perc: float = 0.8) -> str:
    """Mask a portion of a string with asterisks.

    Args:
        s: String to mask
        perc: Percentage of string to mask (default: 0.8)

    Returns:
        str: Masked string
    """
    mask_chars = math.ceil(len(s) * perc)
    return f'{"*" * mask_chars}{s[mask_chars:]}'


def main() -> None:
    """Main entry point for the CLI."""

    args = create_parser().parse_args()

    try:
        loglevel = getattr(logging, args.log)
    except AttributeError:
        loglevel = {
            3: logging.CRITICAL,
            2: logging.ERROR,
            1: logging.WARNING,
            0: logging.INFO,
            -1: logging.DEBUG,
        }[int(args.log)]

    logging.basicConfig(level=loglevel, format=LOG_FORMAT)
    log = logging.getLogger(__name__)

    log.info("Gandi DNS record update started.")

    gandi_api_token = os.environ.get("API_TOKEN")

    if not gandi_api_token:
        log.error("API_TOKEN is not set or empty.")
        sys.exit(1)

    # If we've reached here, gandi_api_token is a non-empty string.
    log.debug("Found API_TOKEN variable: %s", mask_string(gandi_api_token))

    try:
        helpers.check_apitoken_format(gandi_api_token)
    except ValueError as err:
        log.error("API_TOKEN format error: %s", err)
        sys.exit(1)

    log.debug("Records found: %s", args.record)

    api = gandi.GandiAPI(GANDI_API_URL, gandi_api_token, args.dry_run)

    if not args.noipv4:
        current_ipv4 = gandi.get_current_ip(IPV4_PROVIDER_URL)
        update_request = DNSUpdateRequest(
            fqdn=args.zone,
            record_names=args.record,
            current_ip=current_ipv4,
            ttl=args.ttl,
            rtype="A",
        )
        api.update_records(update_request)

    if not args.noipv6:
        current_ipv6 = gandi.get_current_ip(IPV6_PROVIDER_URL)
        update_request = DNSUpdateRequest(
            fqdn=args.zone,
            record_names=args.record,
            current_ip=current_ipv6,
            ttl=args.ttl,
            rtype="AAAA",
        )
        api.update_records(update_request)
    log.info("Gandi DNS record update ended.")


if __name__ == " __main__":
    main()
