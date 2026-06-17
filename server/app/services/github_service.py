import requests


class GithubService:
    '''
        The github service class contains
        all necessary functions for GIthub Service Funtionality
    '''
    BASE_URL = "https://api.github.com"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept" : "application/vnd.github+json"
        }

    def get_user_repos(self):
        '''Get all repositories of a connected github user'''
        response = requests.get(
            f"{self.BASE_URL}/user/repos",
            headers=self._headers()
        )
        if response.status_code != 200:
            raise Exception("Failed to fetch repositories")
        
        return response.json()
    
    def get_repo_by_id(self, repo_id: int):
        '''Get a specific repository by id'''
        response = requests.get(
            f"{self.BASE_URL}/repositories/{repo_id}",
            headers=self._headers()
        )

        if response.status_code != 200:
            raise Exception("Failed to fetch repository")

        return response.json()

