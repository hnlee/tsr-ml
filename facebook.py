import requests

GRAPH_API = "https://graph.facebook.com/v2.8/"

def get_facebook_page(page_id, access_token, fields = ""):
  if fields:
    params = {"access_token": access_token,
              "fields": fields}
  else:
    params = {"access_token": access_token} 
  return requests.get(GRAPH_API + page_id, 
                      params = params)

def get_likes(page_id, access_token):
  likes = []
  response = requests.get(GRAPH_API + page_id + "/likes", 
                          params = {"access_token": 
                                    access_token})
  likes += response.json()["data"]
  while "paging" in response.json() and "next" in response.json()["paging"]:
    response = requests.get(response.json()["paging"]["next"])
    likes += response.json()["data"] 
  return likes

def create_likes_list(id_list, access_token, log = "log"):
  likes = []
  for page_id in id_list:
    check = get_facebook_page(page_id, access_token).status_code
    if check == 200:
      likes += get_likes(page_id, access_token)
    else:
      log_file = open("log", "a")
      log_file.write("{!s}: {}\n".format(check, page_id))
      log_file.close()
  return likes

def create_page_info_list(id_list, access_token):
  info_list = []
  fields = "id,name,category"
  for page_id in id_list:
    info_list.append(get_facebook_page(page_id,
                                       access_token,
                                       fields = fields).json()) 
  return info_list

  
