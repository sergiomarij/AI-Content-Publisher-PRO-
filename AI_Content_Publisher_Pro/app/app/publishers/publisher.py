import requests


class WordPressPublisher:

    def __init__(self, url, username, password):

        self.url = url.rstrip("/")
        self.username = username
        self.password = password

    def publish(self, title, content, status="draft"):

        endpoint = f"{self.url}/wp-json/wp/v2/posts"

        data = {
            "title": title,
            "content": content,
            "status": status
        }

        response = requests.post(
            endpoint,
            auth=(self.username, self.password),
            json=data,
            timeout=30
        )

        return response