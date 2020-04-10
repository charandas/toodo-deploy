from locust import HttpLocust, TaskSet, between, task
import logging
from bs4 import BeautifulSoup
from http.client import HTTPConnection
import uuid

HTTPConnection.debugLevel = 1

logging.basicConfig()
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class UserBehavior(TaskSet):
      def on_start(self):
         self.login()

      def parse_csrf_token_from_response_text(self, html_doc):
         soup = BeautifulSoup(html_doc, 'html.parser')         
         for tag in soup.find_all('meta'):
            if not "name" in tag.attrs.keys():
               continue
            if tag.attrs["name"] == "csrf-token":
               return tag.attrs["content"]
         raise Exception('Could not determine csrf token')

      @task(1)
      def items(self):
         self.client.get("/items", verify=False)

      @task(1)
      def newItemsPage(self):
         self.client.get("/items/new", verify=False)

      @task(1)
      def addItem(self):
         self.client.post("/items", {
            "Body":"Some todo:" + str(uuid.uuid4()),
            "Completed": False,
            "authenticity_token": self.csrf_token
         }, cookies = {
            "_toodo_session": self.session
         }, verify=False)

      def login(self):
         response = self.client.get("/signin", verify=False)
         session = response.cookies["_toodo_session"]
         self.csrf_token = self.parse_csrf_token_from_response_text(response.text)
         response = self.client.post("/signin", {
            "Email":"charandas108@gmail.com",
            "Password":"passwd",
            "authenticity_token": self.csrf_token
         }, cookies={
            "_toodo_session": session
         }, verify=False)
         self.session = response.cookies["_toodo_session"]

class WebsiteUser(HttpLocust):
   tasks = [UserBehavior]
   wait_time = between(5.0, 9.0)
