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

    def get_categories(self):

        r = requests.get(
            self.url + "/wp-json/wp/v2/categories",
            auth=(self.username, self.password),
            timeout=20,
        )

        return r

    def get_tags(self):

        r = requests.get(
            self.url + "/wp-json/wp/v2/tags",
            auth=(self.username, self.password),
            timeout=20,
        )

        return r

    def upload_media(self, filename, data, content_type="image/jpeg"):

        r = requests.post(
            self.url + "/wp-json/wp/v2/media",
            auth=(self.username, self.password),
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            files={"file": (filename, data, content_type)},
            timeout=60,
        )

        return r
