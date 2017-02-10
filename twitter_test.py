from unittest import TestCase, main
from twitter import *
from tweepy import TweepError
from os import remove
from os.path import isfile
from time import time

class MockAPI:
  def __init__(self):
    self.id_to_screen_name = {
        123456789: MockUser("ScreenName1"),
        987654321: MockUser("ScreenName2")
        }
    self.id_to_friends = {
        123456789: [987654321],
        987654321: [123456789]
        }
    self.id_to_followers = {
        123456789: [987654321],
        987654321: [123456789]
        }

  def get_user(self, user_id):
    if user_id not in self.id_to_screen_name:
      if user_id == 1234:
        raise TweepError("Invalid id")
      else:
        return MockUser("ScreenName3")
    else:
      return self.id_to_screen_name[user_id]

  def friends_ids(self, user_id):
    if user_id not in self.id_to_friends:
      raise TweepError("Invalid id")
    else:
      return self.id_to_friends[user_id]

  def followers_ids(self, user_id):
    if user_id not in self.id_to_followers:
      raise TweepError("Invalid id")
    else:
      return self.id_to_followers[user_id]

class MockUser:
  def __init__(self, screen_name):
    self.screen_name = screen_name
    self.description = "Description"

class TestCreateUserInfoList(TestCase):
  def setUp(self):
    self.api = MockAPI()

  def test_empty_list(self):
    id_list = []
    screen_names = create_user_info_list(id_list, self.api)
    self.assertEquals(screen_names, [])

  def test_one_id_list(self):
    id_list = [123456789]
    screen_names = create_user_info_list(id_list, self.api)
    self.assertEquals(screen_names,
                      [{"id": 123456789,
                        "screen_name": "ScreenName1",
                        "description": "Description"}])

  def test_multiple_id_list(self):
    id_list = [123456789, 987654321]
    screen_names = create_user_info_list(id_list, self.api)
    self.assertEquals(screen_names,
                      [{"id": 123456789,
                        "screen_name": "ScreenName1",
                        "description": "Description"},
                       {"id": 987654321,
                        "screen_name": "ScreenName2",
                        "description": "Description"}])

  def test_repeat_id_in_list(self):
    id_list = [123456789, 987654321, 123456789]
    screen_names = create_user_info_list(id_list, self.api)
    self.assertEquals(screen_names,
                      [{"id": 123456789,
                        "screen_name": "ScreenName1",
                        "description": "Description"},
                       {"id": 987654321,
                        "screen_name": "ScreenName2",
                        "description": "Description"}])

  def test_invalid_id_in_list(self):
    id_list = [123456789, 987654321, 1234]
    screen_names = create_user_info_list(id_list, self.api)
    self.assertEquals(screen_names,
                      [{"id": 123456789,
                        "screen_name": "ScreenName1",
                        "description": "Description"},
                       {"id": 987654321,
                        "screen_name": "ScreenName2",
                        "description": "Description"}])

  def test_more_than_900_requests_in_window(self):
    id_list = range(123456789, 123456789 + 901)
    start = time()
    screen_names = create_user_info_list(id_list, self.api, 1)
    delay = round(time() - start, 1)
    self.assertEquals(delay, 1.0)

class TestGetUserInfo(TestCase):
  def setUp(self):
    self.api = MockAPI()

  def test_blank_id(self):
    user_id = None
    user_info = get_user_info(user_id, self.api)
    self.assertEquals(user_info, None)

  def test_valid_id(self):
    user_id = 123456789
    user_info = get_user_info(user_id, self.api)
    self.assertEquals(user_info,
                      {"id": 123456789,
                       "screen_name": "ScreenName1",
                       "description": "Description"})

  def test_invalid_id(self):
    user_id = 1234
    user_info = get_user_info(user_id, self.api)
    log_file = open("log", "r")
    self.assertEquals("Invalid id: 1234\n", log_file.read())
    log_file.close()

  def tearDown(self):
    if isfile("log"):
      remove("log")

class TestWaitForNextWindow(TestCase):
  def setUp(self):
    self.api = MockAPI()

  def test_wait_full_window(self):
    start = time()
    wait_for_next_window(start, self.api, window = 1)
    delay = round(time() - start, 0)
    self.assertEquals(delay, 1.0)

  def test_wait_at_end_of_window(self):
    start = time()
    wait_for_next_window(start - 0.9, self.api, window = 1)
    delay = round(time() - start, 1)
    self.assertEquals(delay, 0.1)

  def test_wait_half_of_window(self):
    start = time()
    wait_for_next_window(start - 0.5, self.api, window = 1)
    delay = round(time() - start, 1)
    self.assertEquals(delay, 0.5)

class TestGetFriendIds(TestCase):
  def setUp(self):
    self.api = MockAPI()

  def test_blank_id(self):
    user_id = None
    friends_ids = get_friends_ids(user_id, self.api)
    self.assertEquals(friends_ids, None)

  def test_valid_id(self):
    user_id = 123456789
    friends_ids = get_friends_ids(user_id, self.api)
    self.assertEquals(friends_ids, [987654321])

  def test_invalid_id(self):
    user_id = 1234
    friends_ids = get_friends_ids(user_id, self.api)
    log_file = open("log", "r")
    self.assertEquals("Invalid id: 1234\n", log_file.read())

  def tearDown(self):
    if isfile("log"):
      remove("log")

class TestGetFollowerIds(TestCase):
  def setUp(self):
    self.api = MockAPI()

  def test_blank_id(self):
    user_id = None
    followers_ids = get_followers_ids(user_id, self.api)
    self.assertEquals(followers_ids, None)

  def test_valid_id(self):
    user_id = 123456789
    followers_ids = get_followers_ids(user_id, self.api)
    self.assertEquals(followers_ids, [987654321])

  def test_invalid_id(self):
    user_id = 1234
    followers_ids = get_followers_ids(user_id, self.api)
    log_file = open("log", "r")
    self.assertEquals("Invalid id: 1234\n", log_file.read())

  def tearDown(self):
    if isfile("log"):
      remove("log")

class TestCreateConnectionsList(TestCase):
  def setUp(self):
    self.api = MockAPI()

  def test_empty_list(self):
    id_list = []
    connections = create_connections_list(id_list, self.api)
    self.assertEquals(connections, [])

  def test_one_id_list(self):
    id_list = [123456789]
    connections = create_connections_list(id_list, self.api)
    self.assertEquals(connections, [987654321])

  def test_multiple_id_list(self):
    id_list = [123456789, 987654321]
    connections = create_connections_list(id_list, self.api)
    self.assertEquals(connections, [123456789, 987654321])

  def test_invalid_id_in_list(self):
    id_list = [123456789, 987654321, 1234]
    connections = create_connections_list(id_list, self.api)
    self.assertEquals(connections, [123456789, 987654321])

  def test_more_than_7_requests_in_window(self):
    id_list = [123456789 for i in range(8)] 
    start = time()
    connections = create_connections_list(id_list, self.api, window = 1)
    delay = round(time() - start, 1)
    self.assertEquals(delay, 1.0)

  def tearDown(self):
    if isfile("log"):
      remove("log")

if __name__ == '__main__':
  main()
