import re


def check_apitoken_format(token: str) -> str:
    """
    check that the entered key len is 40 characters
     and match alphanumeric character

    Args:
        token: The API token to validate

    Returns:
        str: Success message if validation passes

    Raises:
        ValueError: If API token format is incorrect
    """
    if not re.match(r"^[a-zA-Z0-9]{40}$", token):
        raise ValueError("API_TOKEN format incorrect")
    return "API_TOKEN format correct"


def check_domain_format(domain: str) -> str:
    """
    check that the entered domain name format is correct

    Args:
        domain: The domain name to validate

    Returns:
        str: Success message if validation passes

    Raises:
        ValueError: If domain format is incorrect
    """
    if not re.match(r"(^[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", domain):
        raise ValueError("Invalid domain format")
    return "Domain format correct"
