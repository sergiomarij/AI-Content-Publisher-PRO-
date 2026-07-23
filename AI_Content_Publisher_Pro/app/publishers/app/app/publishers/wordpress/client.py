import requests


class WordPressClient:

    def __init__(self, url, username, password):

        self.url = url.rstrip("/")

        self.username = username

        self.password = password

    def test(self):

        r = requests.get(
            self.url + "/wp-json/wp/v2/users/me",
            auth=(self.username, self.password),
            timeout=20,
        )

        return r.status_code == 200

    def publish(self, title, content, status="draft"):

        r = requests.post(
            self.url + "/wp-json/wp/v2/posts",
            auth=(self.username, self.password),
            json={
                "title": title,
                "content": content,
                "status": status,
            },
            timeout=30,
        )

        return r