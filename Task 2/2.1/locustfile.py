from locust import HttpUser, between, task
import random

class WebsiteUser(HttpUser):
    wait_time = between(0.5, 2)
    
    @task(3)
    def index(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(1)
    def metrics(self):
        with self.client.get("/metrics", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    def on_start(self):
        print(f"User {self} started")