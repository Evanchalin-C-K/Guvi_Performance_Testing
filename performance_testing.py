# Importing necessary modules and classes from Locust
from locust import HttpUser, SequentialTaskSet, task, between, events
import logging


# Defining class Inheriting Sequential task
class MySequentialTask(SequentialTaskSet):
    # Simulated user will wait between 2 and 5 seconds
    wait = between(2, 5)
    url = "https://65c0f239dc74300bce8d0afe.mockapi.io/users"

    # Define task to be performed by the simulated user
    @task
    # Perform HTTP GET request
    def get_data(self):
        response = self.client.get(self.url + "/5")
        if response.status_code == 200:
            print("Status : Success")
            logging.info("Success")
        else:
            print("Status : Failure")
            logging.info("Too many request")
    @task
    # Perform HTTP POST request
    def post_data(self):
        response = self.client.post(self.url, data={"Name": "Malathi", "City": "Tenkasi", "Country": "India"})
        if response.status_code == 201:
            print("Status : Success")
            logging.info("Data Posted Successfully")
        else:
            print("Status : Failure")
            logging.info("Failed to POST Data")

    @task
    # Perform HTTP UPDATE request
    def update_data(self):
        response = self.client.put(self.url + "/51", data={"City": "Chennai"})
        if response.status_code == 200:
            print("Status : Success")
            logging.info("UPDATED Successfully")
        else:
            print("Status : Failure")
            logging.info("UPDATE failed")

    @task
    # Perform HTTP DELETE request
    def delete_data(self):
        response = self.client.delete(self.url + "/60")
        if response.status_code == 404:
            print(" Successfully deleted")
            logging.info("Data deleted successfully")
        else:
            print(" Failed to delete")
            logging.info("No Such Data")


# Event handler for each request
@events.request.add_listener
def on_request(name, request_type, response, response_time, exception, **kwargs):
    Response_time = response_time / 1000
    print(f' Name : {name}', "\n", f'Request Type: {request_type}',
          "\n", f'Response Time : {Response_time:.3f}s'
          "\n", f'Response : {response.status_code}', "\n",
          f'Exception : {exception}', "\n", kwargs, "\n")
    assert response_time//1000 < 2


# Define a class inheriting HttpUser, representing simulated user
class user(HttpUser):
    host = "https://65c0f239dc74300bce8d0afe.mockapi.io/users"
    tasks = [MySequentialTask]
