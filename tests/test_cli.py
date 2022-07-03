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

def test_parser_fails_with_good_len_apikey(parser):
    """
    Without the good len of APIKey argument, the parser should exit with an error.
    """
    with pytest.raises(ValueError) as e:
        assert helpers.check_apikey_format("xxxx")
    assert str(e.value) == "APIKey format incorrect"


def test_parser_fails_without_zone(parser):
    """
    Without zone argument, the parser should exit with an error.
    """
    with pytest.raises(Exception, match="Invalid domain format"):
        assert helpers.check_domain_format("examplecom")


# @pytest.mark.skip(reason="just testing if skip works")
def test_parser_with_all_positional_arguments(parser):
    """
    With APIKey, domaine and records, the parser will not exit.
    """
    args = parser.parse_args(['xxxx', 'example.com', '@', 'www', 'subdomain'])

    assert args.apikey == 'xxxx'
    assert args.zone == 'example.com'
    assert args.record == ['@', 'www', 'subdomain']
