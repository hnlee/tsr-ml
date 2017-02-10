from tweepy import API, TweepError
from time import time, sleep

def create_user_info_list(id_list, api, window = 60 * 15):
  user_info_list = []
  id_list = sorted(set(id_list))
  start = time()
  for idx, user_id in enumerate(id_list):
    if idx >= 900 and idx % 900 == 0:
      wait_for_next_window(start, api, window = window)
      start = time()
    user_info = get_user_info(user_id, api)
    if user_info:
      user_info_list.append(user_info)
  return user_info_list

def get_user_info(user_id, api, log = "log"):
  if not user_id:
    return None
  try:
    user = api.get_user(user_id)
    return {"id": user_id,
            "screen_name": user.screen_name,
            "description": user.description}
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
