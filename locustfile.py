from locust import HttpLocust, TaskSet, between, task
import logging
from bs4 import BeautifulSoup
from http.client import HTTPConnection
import uuid
import resource

# FIXME: not sure why locust won't respect ulimit
resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

HTTPConnection.debugLevel = 1

logging.basicConfig()
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

logger = logging.getLogger('toodo_st')
logger.setLevel(logging.DEBUG)

class Storage(object):
   def __init__(self):
      self.session = None

class UserBehavior(TaskSet):
      storage = None
      # FIXME: enable when cookie auth works from within locust
      # def on_start(self):
      #   self.login()

      def parse_csrf_token_from_response_text(self, html_doc):
         soup = BeautifulSoup(html_doc, 'html.parser')
         for tag in soup.find_all('meta'):
            if not "name" in tag.attrs.keys():
               continue
            if tag.attrs["name"] == "csrf-token":
               return tag.attrs["content"]
         raise Exception('Could not determine csrf token')

      @task(1)
      def addItem(self):
         #response = self.client.get("/items/new/", cookies = {
         #   "_toodo_session": self.storage.session
         #}, verify=False)
         #logger.debug(response.cookies)
         #csrf_token = self.parse_csrf_token_from_response_text(response.text)
         #self.storage.session = response.cookies["_toodo_session"]

         # FIXME: remove when cookie auth works with locust
         csrf_token = "RIt8IXphuqLFePsM9UunyV7fWPEw2IUpf7fXQl3/10qXGNRhNEd/ch7iDJwCnqTr4Wa3xx1WJx3mjwfcX3D0vQ=="
         self.storage.session = "MTU4Njc5ODAwNHxEdi1CQkFFQ180SUFBUkFCRUFBQV8tal9nZ0FFQm5OMGNtbHVad3dKQUFkZlpteGhjMmhmQjF0ZGRXbHVkRGdLQkFBQ2UzMEdjM1J5YVc1bkRBNEFESEpsY1hWbGMzUnZjbDlwWkFaemRISnBibWNNRmdBVU5qZ3dZVGd5WXpFek9HWTFNVEF3WWpsall6Z0djM1J5YVc1bkRCUUFFbUYxZEdobGJuUnBZMmwwZVY5MGIydGxiZ2RiWFhWcGJuUTRDaUlBSU5PVHFFQk9Kc1hRMjVyM2tQZlZBeUtfdWU4MkxZNmlOSms0MEo0Q2p5UDNCbk4wY21sdVp3d1JBQTlqZFhKeVpXNTBYM1Z6WlhKZmFXUWFaMmwwYUhWaUxtTnZiUzluYjJaeWN5OTFkV2xrTGxWVlNVVF9nd1lCQVFSVlZVbEVBZi1FQUFBQUZmLUVFZ0FRcGx5T1Rac0pUeXVHRXZlWlN5X0pLQT09fLzB2jMGVU3Ub3RSdqUX02mRmZnLnL6xemzH_RTZyEbY"

         response = self.client.post("/items/", {
            "Title": str(uuid.uuid4()),
            "Body":"Some todo body",
            "Completed": False,
            "authenticity_token": csrf_token
         }, cookies = {
            "_toodo_session": self.storage.session
         }, verify=False)
         logger.debug("session:" + self.storage.session)
         logger.debug("csrf-token:" + csrf_token)

      def login(self):
         response = self.client.get("/signin/", verify=False)

         session = response.cookies["_toodo_session"]
         csrf_token = self.parse_csrf_token_from_response_text(response.text)
         response = self.client.post("/signin/", {
            "Email":"charandas108@gmail.com",
            "Password":"passwd",
            "authenticity_token": csrf_token
         }, cookies={
            "_toodo_session": session
         }, verify=False)
         self.storage.session = response.cookies["_toodo_session"]

class WebsiteUser(HttpLocust):
   # a dedicated storage for cookie session per user
   storage = Storage()
   UserBehavior.storage = storage
   tasks = [UserBehavior]
   wait_time = between(5.0, 9.0)
