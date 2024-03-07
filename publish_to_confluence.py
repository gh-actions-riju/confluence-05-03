import os
import requests

class GitHubToConfluence:
    def __init__(self, github_token, confluence_server_url, confluence_space, confluence_page_title, confluence_api_token):
        self.github_token = github_token
        self.confluence_server_url = confluence_server_url
        self.confluence_space = confluence_space
        self.confluence_page_title = confluence_page_title
        self.confluence_api_token = confluence_api_token

    def fetch_github_file(self, repo_owner, repo_name, file_path):
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3.raw'
        }
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch GitHub file. Status Code: {response.status_code}")

    def publish_to_confluence(self, content):
        headers = {
            'Authorization': f'Basic {self.confluence_api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        page_data = {
            "type": "page",
            "title": self.confluence_page_title,
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage",
                }
            }
        }

        url = f'{self.confluence_server_url}/wiki/rest/api/content/{self.get_confluence_page_id()}'
        
        response = requests.put(url, json=page_data, headers=headers)
        
        if response.status_code == 200:
            print("Successfully published to Confluence.")
        else:
            raise Exception(f"Failed to publish to Confluence. Status Code: {response.status_code}")

    def get_confluence_page_id(self):
        headers = {
            'Authorization': f'Basic {self.confluence_api_token}',
            'Accept': 'application/json',
        }

        params = {
            'title': self.confluence_page_title,
            'spaceKey': self.confluence_space,
        }

        url = f'{self.confluence_server_url}/wiki/rest/api/content'
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if response.status_code == 200:
            if 'results' in data and data['results']:
                return data['results'][0]['id']
            else:
                raise Exception("Confluence page not found.")
        else:
            raise Exception(f"Failed to get Confluence page ID. Status Code: {response.status_code}")

# Example Usage
        
github_token = ''
confluence_server_url = 'https://confluence.xxxx.io'
confluence_space = 'Documentation (Markdown) Files'
confluence_page_title = 'Documentation (Markdown) Files'
confluence_api_token = ''

github_to_confluence = GitHubToConfluence(github_token, confluence_server_url, confluence_space, confluence_page_title, confluence_api_token)

# Fetch Markdown file from GitHub
repo_owner = 'gh-actions-riju'
repo_name = 'confluence-05-03'
file_path = 'index.md'
markdown_content = github_to_confluence.fetch_github_file(repo_owner, repo_name, file_path)

# Publish to Confluence
github_to_confluence.publish_to_confluence(markdown_content)
