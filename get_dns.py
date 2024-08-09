import dns.resolver, dns.exception


def query_domain(domain: str, dns_server: list):
    """
    Queries a DNS server for the IP addresses of a domain.
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = dns_server
    ip = []
    max_retries = 5

    # 여러번 시도해서 ip를 가져온다.
    for _ in range(max_retries):
        try:
            addresses = resolver.resolve(domain)
            for address in addresses:
                ip.append(address.to_text())
        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.exception.Timeout,
        ):
            print(f"DNS query failed for {domain} on {dns_server}")

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
    ip_list = sorted(ip_list)
    return ip_list


if __name__ == "__main__":
    from domains import domains
    from dns_servers import dns_servers

    for domain in domains:
        print(f"{domain}: {get_ip_addresses_from_multiple_dns(domain, dns_servers)}")
