from api.api_client import APIClient


class ServersRequests(APIClient):
    SERVERS = "/servers"

    def __init__(self, base_url, token):
        super().__init__(base_url, token)
        self.endpoint = self.SERVERS

    def get_servers_list(self, params=None):
        return self.get_obj(
            endpoint=self.endpoint,
            headers=self.session.headers,
            params=params
        )

