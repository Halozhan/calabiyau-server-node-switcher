import dns.resolver, dns.exception

dns_servers = [
    "8.8.8.8",  # Google Public DNS
    "1.1.1.1",  # Cloudflare DNS
    "9.9.9.9",  # Quad9 DNS
    "208.67.222.222",  # OpenDNS
    "210.2.4.8",
    "180.76.76.76",
    "210.5.56.145",
    "210.5.56.146",
    "223.6.6.6",
    "114.114.115.115",
    "223.5.5.5",
    "114.114.114.114",
    "218.92.205.30",
    "218.93.124.186",
    "218.93.26.250",
    "221.224.200.54",
    "221.231.118.114",
    "101.226.4.6",
    "218.30.118.6",
    "123.125.81.6",
    "1.2.4.8",
    "182.254.116.116",
    "123.123.123.123",
]


def query_domain(domain: str, dns_server: list):
    """
    Queries a DNS server for the IP addresses of a domain.
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = dns_server
    ip = []
    try:
        addresses = resolver.resolve(domain)
        for address in addresses:
            ip.append(address.to_text())
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        pass
    return ip


def get_ip_addresses_from_multiple_dns(domain: str, dns_servers: list):
    """
    Queries multiple DNS servers for the IP addresses of a domain.
    """
    ip_list = set()
    for dns_server in dns_servers:
        results = query_domain(domain, [dns_server])
        for result in results:
            ip_list.add(result)
    return ip_list


domains = [
    "ds-tj-1.klbq.qq.com",
    "ds-nj-1.klbq.qq.com",
    "ds-gz-1.klbq.qq.com",
    "ds-cq-1.klbq.qq.com",
]


if __name__ == "__main__":
    for domain in domains:
        print(f"{domain}: {get_ip_addresses_from_multiple_dns(domain, dns_servers)}")
