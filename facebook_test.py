from unittest import TestCase, main
from facebook import *
import responses 
import requests
from os import remove
from os.path import isfile

API_ENDPOINT = "https://graph.facebook.com/v2.8/{}?access_token=faketoken{}"

class TestGetFacebookPage(TestCase):
  def test_valid_page(self):
    uri = API_ENDPOINT.format("123456789", "")
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, uri, status = 200, 
               match_querystring = True) 
      response = get_facebook_page("123456789", 
                                   "faketoken") 
      self.assertEquals(response.status_code, 200)

  def test_invalid_page(self):
    uri = API_ENDPOINT.format("1234", "")
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, uri, status = 400, 
               match_querystring = True) 
      response = get_facebook_page("1234", 
                                   "faketoken") 
      self.assertEquals(response.status_code, 400)

  def test_specific_fields(self):
    uri = API_ENDPOINT.format("123456789", 
                              "&fields=id,name,category")
    page_info = {"id": "123456789",
                 "name": "First Last",
                 "category": "Public Figure"}
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, uri, status = 200, 
               json = page_info,
               match_querystring = True) 
      response = get_facebook_page("123456789", 
                                   "faketoken",
                                   "id,name,category") 
      self.assertEquals(response.json(), page_info)

class TestGetLikes(TestCase):
  def test_one_page_likes(self):
    uri = API_ENDPOINT.format("123456789/likes", "")
    data = [{"id": "987654321", "name": "One"},
            {"id": "192837465", "name": "Two"}]
    like_info = {"data": data}
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, uri, status = 200,
               json = like_info,
               match_querystring = True)
      likes = get_likes("123456789", "faketoken")
      self.assertEquals(likes, data)

  def test_multi_page_likes(self):
    uri = API_ENDPOINT.format("123456789/likes", "")
    page_one = [{"id": "987654321", "name": "One"},
                {"id": "192837465", "name": "Two"}]
    page_two = [{"id": "546372819", "name": "Three"},
                {"id": "918273645", "name": "Four"}]
    cursors = {"cursors": {"after": "aftercode",
                           "before": "beforecode"}}
    next_uri = API_ENDPOINT.format("123456789/likes",
                                   "&limit=2&after=aftercode")
    page_one_info = {"data": page_one,
                     "paging": {**cursors,
                                "next": next_uri}} 
    prev_uri = API_ENDPOINT.format("123456789/likes",
                                  "&limit=2&before=beforecode")
    page_two_info = {"data": page_two,
                     "paging": {**cursors,
                                "previous": prev_uri}}
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, uri, status = 200,
               json = page_one_info,
               match_querystring = True)
      rsps.add(responses.GET, next_uri, status = 200,
               json = page_two_info,
               match_querystring = True)
      likes = get_likes("123456789", "faketoken")
      self.assertEquals(likes, page_one + page_two)

class TestCreateLikesList(TestCase):
  def test_empty_list(self):
    id_list = []
    likes = create_likes_list(id_list, "faketoken")
    self.assertEquals(likes, [])

  def test_one_id_list(self):
    id_list = ["123456789"]
    id_uri = API_ENDPOINT.format("123456789", "")
    uri = API_ENDPOINT.format("123456789/likes", "")
    data = [{"id": "987654321", "name": "One"},
            {"id": "192837465", "name": "Two"}]
    like_info = {"data": data}
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, id_uri, status = 200,
               match_querystring = True)
      rsps.add(responses.GET, uri, status = 200,
               json = like_info,
               match_querystring = True)
      likes = create_likes_list(id_list, "faketoken") 
      self.assertEquals(likes, data) 

  def test_multiple_id_list(self):
    id_list = ["123456789", "987654321"]
    id_uris = [API_ENDPOINT.format("123456789", ""),
               API_ENDPOINT.format("987654321", "")]
    uri_one = API_ENDPOINT.format("123456789/likes", "")
    uri_two = API_ENDPOINT.format("987654321/likes", "")
    data_one = [{"id": "987654321", "name": "One"},
                {"id": "192837465", "name": "Two"}]
    data_two = [{"id": "192837465", "name": "Three"},
                {"id": "918273645", "name": "Four"}]
    like_one_info = {"data": data_one}
    like_two_info = {"data": data_two}
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, id_uris[0], status = 200,
               match_querystring = True)
      rsps.add(responses.GET, id_uris[1], status = 200,
               match_querystring = True)
      rsps.add(responses.GET, uri_one, status = 200,
               json = like_one_info,
               match_querystring = True)
      rsps.add(responses.GET, uri_two, status = 200,
               json = like_two_info,
               match_querystring = True)
      likes = create_likes_list(id_list, "faketoken") 
      self.assertEquals(likes, data_one + data_two) 

  def test_invalid_id_in_list(self):
    id_list = ["123456789", "987654321", "1234"]
    id_uris = [API_ENDPOINT.format("123456789", ""),
               API_ENDPOINT.format("987654321", ""),
               API_ENDPOINT.format("1234", "")]
    uri_one = API_ENDPOINT.format("123456789/likes", "")
    uri_two = API_ENDPOINT.format("987654321/likes", "")
    data_one = [{"id": "987654321", "name": "One"},
                {"id": "192837465", "name": "Two"}]
    data_two = [{"id": "192837465", "name": "Three"},
                {"id": "918273645", "name": "Four"}]
    like_one_info = {"data": data_one}
    like_two_info = {"data": data_two}
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, id_uris[0], status = 200,
               match_querystring = True)
      rsps.add(responses.GET, id_uris[1], status = 200,
               match_querystring = True)
      rsps.add(responses.GET, id_uris[2], status = 400,
               match_querystring = True)
      rsps.add(responses.GET, uri_one, status = 200,
               json = like_one_info,
               match_querystring = True)
      rsps.add(responses.GET, uri_two, status = 200,
               json = like_two_info,
               match_querystring = True)
      likes = create_likes_list(id_list, "faketoken") 
      self.assertEquals(likes, data_one + data_two) 
    log_file = open("log", "r")
    self.assertEquals("400: 1234\n", log_file.read())
    log_file.close()

  def tearDown(self):
    if isfile("log"):
      remove("log")

class TestCreatePageInfoList(TestCase):
  def test_empty_list(self):
    id_list = []
    info_list = create_page_info_list(id_list, "faketoken")
    self.assertEquals(info_list, [])

  def test_one_id_list(self):
    id_list = ["123456789"]
    uri = API_ENDPOINT.format("123456789", 
                              "&fields=id,name,category")
    page_info = {"id": "123456789",
                 "name": "First Last",
                 "category": "Public Figure"}
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, uri, status = 200, 
               json = page_info,
               match_querystring = True) 
      info_list = create_page_info_list(id_list, "faketoken")
      self.assertEquals(info_list, [page_info]) 

  def test_multi_id_list(self):
    id_list = ["123456789", "987654321"]
    uri_list = [API_ENDPOINT.format("123456789", 
                                    "&fields=id,name,category"),
                API_ENDPOINT.format("987654321", 
                                    "&fields=id,name,category")]
    pages_info = [{"id": "123456789",
                   "name": "First Last",
                   "category": "Public Figure"},
                  {"id": "987654321",
                   "name": "First Last",
                   "category": "Public Figure"}]
    with responses.RequestsMock() as rsps:
      rsps.add(responses.GET, uri_list[0], status = 200, 
               json = pages_info[0],
               match_querystring = True) 
      rsps.add(responses.GET, uri_list[1], status = 200, 
               json = pages_info[1],
               match_querystring = True) 
      info_list = create_page_info_list(id_list, "faketoken")
      self.assertEquals(info_list, pages_info)

if __name__ == '__main__':
  main()
