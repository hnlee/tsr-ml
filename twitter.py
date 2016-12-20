from tweepy import API, TweepError
from time import time, sleep

def create_id_screen_name_dict(id_list, api, window = 60 * 15):
  id_screen_name_dict = {}
  start = time()
  for idx, user_id in enumerate(id_list):
    if idx >= 900 and idx % 900 == 0:
      wait_for_next_window(start, api, window = window)
      start = time()
    screen_name =  get_screen_name(user_id, api)
    if screen_name:
      id_screen_name_dict[user_id] = screen_name
  return id_screen_name_dict

def get_screen_name(user_id, api, log = "log"):
  try:
    return api.get_user(user_id).screen_name
  except TweepError as err:
    log_file = open(log, "a")
    log_file.write("{}: {!s}\n".format(err,
                                       user_id))
    log_file.close()
    pass

def wait_for_next_window(start, api, window = 60 * 15):
  sleep(window - (time() - start))

def get_friends_ids(user_id, api, log = "log"):
  try:
    return api.friends_ids(user_id)
  except TweepError as err:
    log_file = open(log, "a")
    log_file.write("{}: {!s}\n".format(err,
                                       user_id))
    log_file.close()
    pass

def get_followers_ids(user_id, api, log = "log"):
  try:
    return api.followers_ids(user_id)
  except TweepError as err:
    log_file = open(log, "a")
    log_file.write("{}: {!s}\n".format(err,
                                       user_id))
    log_file.close()
    pass

def create_connections_list(id_list, api, window = 60 * 15, log = "log"):
  connections_list = []
  start = time()
  for idx, user_id in enumerate(id_list):
    friends_ids = get_friends_ids(user_id, api)
    followers_ids = get_followers_ids(user_id, api)
    if idx >= 7 and idx % 7 == 0:
      wait_for_next_window(start, api, window)
      start = time()
    if friends_ids:
      connections_list += friends_ids
    if followers_ids:
      connections_list += followers_ids
    log_file = open(log, "a")
    log_file.write("{!s} users done\n".format(idx + 1))
  return sorted(set(connections_list))
