import re

def check_apikey_format(apikey):
    """
    check that the entered key len is 24 characters
    """
    if len(apikey) != 24:
        raise ValueError("APIKey incorrect")
    else:
        return "APIKey correct"

def check_domain_format(domain):
    """
    check that the entered domain name format is correct
    """
    if not re.match(r"(^[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", domain):
        raise Exception("Invalid domain format")
    else:
        return "Domain format correct"
