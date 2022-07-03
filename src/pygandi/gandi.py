import json
import logging
import os
from posixpath import split
import sys
import urllib.request

log = logging.getLogger(__name__)

class GandiAPI:
    def __init__(self, url, key, dry_run):
        self.url = url
        self.key = key
        self.dry_run = dry_run

    def update_records(self, fqdn, record_names, current_ip, ttl=3600,
                       rtype="A"):
        records=[]
        if any("," in s for s in record_names):
            records=record_names[0].split(',')
        else:
            records=record_names

        log.info("There are a total of %s record(s) to test", len(records))
        for name in records:
            record = self.get_domain_record_by_name(fqdn, name, rtype=rtype)

            if record is not None and current_ip in record['rrset_values']:
                log.info(
                    "Record %s for %s.%s is up to date (%s).",
                    rtype, name, fqdn, current_ip
                )
            elif not self.dry_run:
                request = urllib.request.Request(
                    f"{self.url}/domains/{fqdn}/records/{name}/{rtype}",
                    method="POST" if record is None else "PUT",
                    headers={
                        "Content-Type": "application/json",
                        "X-Api-Key": self.key
                    },
                    data=json.dumps({
                        "rrset_ttl": ttl,
                        "rrset_values": [current_ip],
                    }).encode()
                )
                with urllib.request.urlopen(request) as response:
                    log.debug(json.loads(response.read().decode()))
                log.info(
                    "Record %s for %s.%s is set to %s.",
                    rtype, name, fqdn, current_ip
                )
            else:
                log.info(
                    "Dry-run mode: Record %s for %s.%s is set to %s.",
                    rtype, name, fqdn, current_ip
                )

    def get_domain_record_by_name(self, fqdn, name, rtype="A"):
        try:
            request = urllib.request.Request(
                f"{self.url}/domains/{fqdn}/records/{name}/{rtype}"
            )
            request.add_header("X-Api-Key", self.key)
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError:
            return None

def get_current_ip(provider_url):
    """
    Use provider_url check that the entered domain name format is correct
    """
    try:
        response = urllib.request.urlopen(provider_url).read().decode('utf-8')
        log.info(f'Current IP address is : {response}')
        return response
    except urllib.error.HTTPError as http_error:
        log.error(f'HTTP error occurred: {http_error}')
        sys.exit(1)
    except Exception as err:
        log.error(f'Other error occurred: {err}')
        sys.exit(1)