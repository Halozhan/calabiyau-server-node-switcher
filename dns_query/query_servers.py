import json
import dns.asyncresolver
import asyncio


async def query_server(domain: str) -> list[str] | None:
    resolver = dns.asyncresolver.Resolver()
    server = []
    try:
        answer = await resolver.resolve(domain, "A")
        if not answer:
            return None
        for record in answer:
            ip = record.address
            server.append(ip)
        return server
    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.LifetimeTimeout,
    ) as e:
        raise e


# async def query_all(server_list, max_servers: int = 150):
#     tasks = []
#     for region, info in server_list.items():
#         for i in range(1, max_servers + 1):
#             domain = info["domain"].replace("{iterable}", str(i))
#             tasks.append(query_server(domain))
#     try:
#         results = await asyncio.gather(*tasks, return_exceptions=True)
#     except Exception:
#         pass
#     return results


# if __name__ == "__main__":
#     # 서버 목록을 JSON 파일에서 읽어옵니다.
#     server_list = json.load(open("server_list.json", "r", encoding="utf-8"))
#     results = asyncio.run(query_all(server_list))
#     results = [r for r in results if isinstance(r, dict)]
#     print(f"총 {len(results)}개의 서버를 찾았습니다.")
#     print("서버 목록:")
#     for result in results:
#         for domain, ips in result.items():
#             print(f"{domain}: {', '.join(ips)}")

#     print(results)
