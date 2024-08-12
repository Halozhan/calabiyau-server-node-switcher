from python_hosts import Hosts, HostsEntry


class ChangeHosts:
    def __init__(self, domain, ip_address):
        self.domain = domain
        self.ip_address = ip_address

    def change(self):
        """
        관리자 권한으로 실행해야 hosts 파일을 수정할 수 있습니다.
        require admin permission to modify hosts file.
        """
        try:
            # 동일한 도메인이 이미 hosts 파일에 있으면 삭제합니다.
            self.remove()
            hosts = Hosts()
            # hosts 파일에 도메인과 ip 주소를 추가합니다.
            hosts.add(
                [
                    HostsEntry(
                        entry_type="ipv4",
                        address=self.ip_address,
                        names=[self.domain],
                    )
                ]
            )
            hosts.write()
        except Exception as e:
            print(e)

    def remove(self):
        """
        관리자 권한으로 실행해야 hosts 파일을 수정할 수 있습니다.
        require admin permission to modify hosts file.
        """
        try:
            hosts = Hosts()
            # 기존 hosts 파일에 동일한 도메인이 있으면 삭제합니다.
            hosts.remove_all_matching(name=self.domain)
            hosts.write()
        except Exception as e:
            print(e)
