import asyncio
import dns.asyncresolver


async def query_servers(
    region_code: str, region_name: str, max_servers: int = 150, port: int = 20000
):
    resolver = dns.asyncresolver.Resolver()
    servers = []
    for i in range(1, max_servers + 1):
        domain = f"klbqcp-prod-ds-{region_code}{i}-server.gxpan.cn"
        try:
            answer = await resolver.resolve(domain, "A")
            if not answer:
                break
            for record in answer:
                ip = record.address
                print(f"{region_name}.{region_code}:{i}번째 Server: {ip}")
                servers.append(f"{ip}:{port}")
        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.LifetimeTimeout,
        ):
            break
        except Exception as e:
            print(f"Error querying {domain}: {e}")
            break
    return servers


async def main():
    # 지역 이름과 지역 코드를 꺼내서 DNS 쿼리를 보내는 태스크 리스트를 만든다.
    tasks = [
        query_servers(region_code, region_name) for region_name, region_code in regions
    ]

    # 태스크가 모두 완료될 때까지 기다린다.
    results = await asyncio.gather(*tasks)

    # 각 지역의 서버 개수를 출력한다.
    for (region_name, region_code), servers in zip(regions, results):
        print(f"{region_name} 서버 개수: {len(servers)}")

    return results


if __name__ == "__main__":
    regions = [
        ("成都, Chengdu", "cd"),
        ("北京, Beijing", "bj"),
        ("南京, Nanjing", "nj"),
        ("广州, Guangzhou", "gz"),
    ]
    servers = asyncio.run(main())
    print(servers)
