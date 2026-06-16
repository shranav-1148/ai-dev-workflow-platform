import requests


class GithubService:

    BASE_URL = "https://api.github.com"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept" : "application/vnd.github+json"
        }

    def get_user_repos(self):
        response = requests.get(
            f"{self.BASE_URL}/user/repos",
            headers=self._headers()
        )
        if response.status_code != 200:
            raise Exception("Failed to fetch repositories")
        
        return response.json()


def get_repository(owner: str, repo: str):
    pass

def get_pull_request(owner: str , repo:str):
    pass

def get_issues(owner:str, repo:str):
    pass