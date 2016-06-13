def parse_domain_name(url):
    url = url.replace("http://", "")
    url = url.replace("/", "")
    return url
