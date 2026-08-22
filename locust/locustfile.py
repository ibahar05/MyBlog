from locust import HttpUser, task


class QuickStartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v2/jwt/create/",
            data={"email": "ibahare05@gmail.com", "password": "134679@xxB"},
        ).json()
        self.client.headers = {"Authorization": f"Bearer {response.get('access',None)}"}
        return super().on_start()

    @task
    def post_list(self):
        self.client.get("/blog/api/v1/post/")
