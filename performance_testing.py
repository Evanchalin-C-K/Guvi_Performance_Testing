import time

from locust import HttpUser, SequentialTaskSet, task, between, events


class MySequentialTask(SequentialTaskSet):
    wait = between(2, 5)
    url = "https://65c0f239dc74300bce8d0afe.mockapi.io/users"

    @task
    def get_data(self):
        response = self.client.get(self.url + "/5")
        if response.status_code == 200:
            print("Status : Success")
        else:
            print("Status : Failure")

    @task
    def post_data(self):
        response = self.client.post(self.url, data={"Name": "Malathi", "City": "Tenkasi", "Country": "India"})
        if response.status_code == 201:
            print("Status : Success")
        else:
            print("Status : Failure")

    @task
    def update_data(self):
        response = self.client.put(self.url + "/51", data={"City": "Chennai"})
        if response.status_code == 200:
            print("Status : Success")
        else:
            print("Status : Failure")

    @task
    def delete_data(self):
        response = self.client.delete(self.url + "/60")
        if response.status_code == 404:
            print(" Successfully deleted")
        else:
            print(" Failed to delete")


@events.request.add_listener
def on_request(name, request_type, response, response_time, exception, **kwargs):
    print(f' Name : {name}', "\n", f'Request Type: {request_type}',
          "\n", f'Response Time : {response_time}'
          "\n", f'Response : {response.status_code}', "\n",
          f'Exception : {exception}', "\n", kwargs, "\n")
    assert response_time//1000 < 2


class user(HttpUser):
    host = "https://65c0f239dc74300bce8d0afe.mockapi.io/users"
    tasks = [MySequentialTask]
