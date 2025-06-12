# pylint: disable=redefined-outer-name
import pytest

from pygandi import cli, helpers


@pytest.fixture()
def parser():
    return cli.create_parser()

def test_parser_fails_without_arguments(parser):
    """
    Without arguments, the parser should exit with an error.
    """
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_parser_fails_with_good_len_apitoken():
    """
    Without the good len of API_TOKEN argument, the parser should exit with an error.
    """
    with pytest.raises(ValueError) as e:
        assert helpers.check_apitoken_format("xxxx")
    assert str(e.value) == "API_TOKEN format incorrect"


def test_parser_fails_without_zone():
    """
    Without zone argument, the parser should exit with an error.
    """
    with pytest.raises(ValueError, match="Invalid domain format"):
        assert helpers.check_domain_format("examplecom")


# @pytest.mark.skip(reason="just testing if skip works")
def test_parser_with_all_positional_arguments(parser):
    """
    With domaine and records, the parser will not exit.
    """
    args = parser.parse_args(['example.com', '@', 'www', 'subdomain'])

    assert args.zone == 'example.com'
    assert args.record == ['@', 'www', 'subdomain']
