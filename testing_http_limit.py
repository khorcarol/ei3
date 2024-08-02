import time
import requests
from threading import Thread, Event

# Constants
URL = "http://cogsihq.dyndns.org:8888/iolink/v1/devices/master1port1/parameters/4585/value"
DURATION_SECONDS = 60
THREAD_COUNT = 5


class LoadTester:
    def __init__(self, url, duration_seconds):
        self.url = url
        self.duration_seconds = duration_seconds
        self.successful_requests = 0
        self.failed_requests = 0
        self.stop_event = Event()

    def make_request(self):
        while not self.stop_event.is_set():
            try:
                response = requests.get(self.url)
                if response.status_code == 200:
                    self.successful_requests += 1
                else:
                    self.failed_requests += 1
            except requests.RequestException:
                self.failed_requests += 1

    def start_test(self, thread_count):
        threads = []
        self.stop_event.clear()

        # Start threads
        for _ in range(thread_count):
            thread = Thread(target=self.make_request)
            thread.start()
            threads.append(thread)

        # Run the test for the specified duration
        time.sleep(self.duration_seconds)
        self.stop_event.set()  # Signal threads to stop

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return self.successful_requests, self.failed_requests


if __name__ == "__main__":
    tester = LoadTester(URL, DURATION_SECONDS)
    successful_requests, failed_requests = tester.start_test(THREAD_COUNT)

    print(f"Load test completed.")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
