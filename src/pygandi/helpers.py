import re

def check_apikey_format(apikey):
    """
    check that the entered key len is 24 characters
     and match alphanumeric character
    """
    if not re.match(r"^[a-zA-Z0-9]{24}$", apikey):
        raise ValueError("APIKey format incorrect")
    else:
        return "APIKey format correct"

def check_domain_format(domain):
    """
    check that the entered domain name format is correct
    """
    if not re.match(r"(^[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", domain):
        raise Exception("Invalid domain format")
    else:
        return "Domain format correct"
