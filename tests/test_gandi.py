"""Tests for the gandi module."""
import json
import urllib.error
import urllib.request
from io import BytesIO
from unittest.mock import MagicMock

import pytest

from pygandi.gandi import DNSRecord, DNSUpdateRequest, GandiAPI, get_current_ip


def test_dns_record_creation():
    """Test DNSRecord creation with default and custom values."""
    record = DNSRecord(fqdn="example.com", name="www")
    assert record.fqdn == "example.com"
    assert record.name == "www"
    assert record.rtype == "A"
    assert record.ttl == 3600
    assert record.ip is None

    record_with_custom = DNSRecord(
        fqdn="example.com", name="www", rtype="AAAA", ttl=7200, ip="2001:db8::1"
    )
    assert record_with_custom.rtype == "AAAA"
    assert record_with_custom.ttl == 7200
    assert record_with_custom.ip == "2001:db8::1"


def test_gandi_api_create_record_request():
    """Test GandiAPI._create_record_request method."""
    api = GandiAPI(url="https://api.gandi.net", key="test_key", dry_run=False)
    record = DNSRecord(fqdn="example.com", name="www", ip="192.0.2.1")

    # Test POST request (new record)
    request = api._create_record_request(record, is_new=True)
    assert request.method == "POST"
    assert request.get_full_url().startswith("https://api.gandi.net/domains/")
    assert request.get_header("Authorization") == "Bearer test_key"
    assert json.loads(request.data.decode()) == {"rrset_ttl": 3600, "rrset_values": ["192.0.2.1"]}

    # Test PUT request (update record)
    request = api._create_record_request(record, is_new=False)
    assert request.method == "PUT"


def test_parse_record_names():
    """Test GandiAPI._parse_record_names method."""
    api = GandiAPI(url="https://api.gandi.net", key="test_key", dry_run=False)

    # Test single record
    assert api._parse_record_names(["www"]) == ["www"]

    # Test multiple records
    assert api._parse_record_names(["www,blog,mail"]) == ["www", "blog", "mail"]

    # Test multiple arguments
    assert api._parse_record_names(["www", "blog"]) == ["www", "blog"]


def test_get_domain_record_by_name(mocker):
    """Test GandiAPI.get_domain_record_by_name method."""
    api = GandiAPI(url="https://api.gandi.net", key="test_key", dry_run=False)
    mock_response = MagicMock()
    mock_response.__enter__.return_value = mock_response
    response_data = {"rrset_type": "A", "rrset_ttl": 3600, "rrset_values": ["192.0.2.1"]}
    mock_response.read.return_value = json.dumps(response_data).encode("utf-8")

    mocker.patch("urllib.request.urlopen", return_value=mock_response)

    record = api.get_domain_record_by_name("example.com", "www")
    assert record["rrset_type"] == "A"
    assert record["rrset_values"] == ["192.0.2.1"]

    # Test non-existent record
    mock_response.read.side_effect = urllib.error.HTTPError(
        "url", 404, "Not Found", {}, BytesIO()
    )
    assert api.get_domain_record_by_name("example.com", "nonexistent") is None


def test_get_current_ip(mocker):
    """Test get_current_ip function."""
    mock_response = MagicMock()
    mock_response.__enter__.return_value = mock_response
    mock_response.read.return_value = "192.0.2.1".encode("utf-8")
    mocker.patch("urllib.request.urlopen", return_value=mock_response)

    ip = get_current_ip("https://api.ipify.org")
    assert ip == "192.0.2.1"

    # Test HTTP error
    mock_response.read.side_effect = urllib.error.HTTPError(
        "url", 500, "Server Error", {}, BytesIO()
    )
    with pytest.raises(SystemExit):
        get_current_ip("https://api.ipify.org")

    # Test URL error
    mock_response.read.side_effect = urllib.error.URLError("Connection failed")
    with pytest.raises(SystemExit):
        get_current_ip("https://api.ipify.org")


def test_update_records(mocker):
    """Test GandiAPI.update_records method."""
    api = GandiAPI(url="https://api.gandi.net", key="test_key", dry_run=False)

    # Mock get_domain_record_by_name
    mocker.patch.object(
        api,
        "get_domain_record_by_name",
        return_value={"rrset_values": ["192.0.2.1"]},
    )

    # Mock urlopen for the update request
    mock_response = MagicMock()
    mock_response.__enter__.return_value = mock_response
    mock_response.read.return_value = "{}".encode("utf-8")
    mocker.patch("urllib.request.urlopen", return_value=mock_response)

    # Test update with existing IP (no change needed)
    update_request = DNSUpdateRequest(
        fqdn="example.com",
        record_names=["www"],
        current_ip="192.0.2.1",
    )
    api.update_records(update_request)

    # Test update with new IP
    update_request = DNSUpdateRequest(
        fqdn="example.com",
        record_names=["www"],
        current_ip="192.0.2.2",
    )
    api.update_records(update_request)

    # Test dry run mode
    api.dry_run = True
    api.update_records(update_request)  # Should not make any HTTP requests

    # Test non-existent record (should create new record)
    api.dry_run = False
    mocker.patch.object(api, "get_domain_record_by_name", return_value=None)
    api.update_records(update_request)
