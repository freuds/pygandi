# Standard library imports
import json
import logging
import sys
import urllib.request
from dataclasses import dataclass
from typing import List, Optional

log = logging.getLogger(__name__)


@dataclass
class DNSRecord:
    """DNS record details."""

    fqdn: str
    name: str
    rtype: str = "A"
    ttl: int = 3600
    ip: Optional[str] = None


@dataclass
class RequestConfig:
    """Configuration for DNS record requests."""

    method: str
    headers: dict
    data: Optional[bytes] = None


@dataclass
class DNSUpdateRequest:
    """Parameters for updating DNS records."""

    fqdn: str
    record_names: List[str]
    current_ip: str
    ttl: int = 3600
    rtype: str = "A"


@dataclass
class GandiAPI:
    """API client for Gandi LiveDNS."""

    url: str
    key: str
    dry_run: bool

    def _create_record_request(
        self, record: DNSRecord, is_new: bool = True
    ) -> urllib.request.Request:
        """Create a request object for updating a DNS record."""
        config = RequestConfig(
            method="POST" if is_new else "PUT",
            headers={"Authorization": f"Bearer {self.key}"},
        )

        if record.ip:
            config.data = json.dumps(
                {
                    "rrset_ttl": record.ttl,
                    "rrset_values": [record.ip],
                }
            ).encode()

        return urllib.request.Request(
            f"{self.url}/domains/{record.fqdn}/records/{record.name}/{record.rtype}",
            method=config.method,
            headers=config.headers,
            data=config.data,
        )

    def _parse_record_names(self, record_names: List[str]) -> List[str]:
        """Parse record names from input, handling comma-separated values."""
        if any("," in s for s in record_names):
            return record_names[0].split(",")
        return record_names

    def update_records(self, update_request: DNSUpdateRequest) -> None:
        """Update DNS records for the given domain.

        Args:
            update_request: The DNS update request containing all required parameters
        """
        records = self._parse_record_names(update_request.record_names)
        log.info("There are a total of %s record(s) to check", len(records))

        for name in records:
            existing_record = self.get_domain_record_by_name(
                update_request.fqdn, name, rtype=update_request.rtype
            )
            record = DNSRecord(
                fqdn=update_request.fqdn,
                name=name,
                rtype=update_request.rtype,
                ttl=update_request.ttl,
                ip=update_request.current_ip,
            )

            if (
                existing_record is not None
                and update_request.current_ip in existing_record["rrset_values"]
            ):
                log.info(
                    "(%s) Record: %s.%s is already up to date (%s).",
                    update_request.rtype,
                    name,
                    update_request.fqdn,
                    update_request.current_ip,
                )
                continue

            if self.dry_run:
                log.info(
                    "Dry-run mode: Record %s for %s.%s will set to %s.",
                    update_request.rtype,
                    name,
                    update_request.fqdn,
                    update_request.current_ip,
                )
                continue

            request = self._create_record_request(record, is_new=existing_record is None)

            with urllib.request.urlopen(request) as response:
                log.debug(json.loads(response.read().decode()))
            log.info(
                "Record %s for %s.%s is set to %s.",
                update_request.rtype,
                name,
                update_request.fqdn,
                update_request.current_ip,
            )

    def get_domain_record_by_name(self, fqdn: str, name: str, rtype: str = "A") -> Optional[dict]:
        """Get a domain record by name.

        Args:
            fqdn: Fully qualified domain name
            name: Record name
            rtype: Record type (default: A)

        Returns:
            Optional[dict]: The record data if found, None otherwise
        """
        try:
            record = DNSRecord(fqdn=fqdn, name=name, rtype=rtype)
            request = urllib.request.Request(
                f"{self.url}/domains/{record.fqdn}/records/{record.name}/{record.rtype}",
                method="GET",
                headers={"Authorization": f"Bearer {self.key}"},
            )
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode())
                if isinstance(data, dict):
                    return data
                return None
        except urllib.error.HTTPError:
            return None


def get_current_ip(provider_url: str) -> str:
    """Get current IP address from the provider URL.

    Args:
        provider_url: URL to fetch the current IP address from

    Returns:
        str: Current IP address

    Raises:
        SystemExit: If there is an error fetching the IP address
    """
    try:
        with urllib.request.urlopen(provider_url) as response:
            ip = response.read().decode("utf-8").strip()
            if not isinstance(ip, str):
                raise ValueError("IP address must be a string")
            log.info("Current IP address is : %s", ip)
            return ip
    except urllib.error.HTTPError as http_error:
        log.error("HTTP error occurred: %s", http_error)
        sys.exit(1)
    except urllib.error.URLError as url_error:
        log.error("URL error occurred: %s", url_error)
        sys.exit(1)
