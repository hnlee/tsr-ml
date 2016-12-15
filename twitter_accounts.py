from connections import connect_to_snapshot, connect_to_twitter
from sqlalchemy.sql import select
from time import sleep, time
from pickling import write_pickle

engine, conn, meta = connect_to_snapshot("ml-snapshot.yml")

api = connect_to_twitter("api-keys.yml")

TwitterUsers = meta.tables["twitter_users"]
s = select([TwitterUsers.c.entity])
result = conn.execute(s)
existing_twitter_users = dict((row[0]["screen_name"], row[0]["id"]) 
                              for row in result)

following_ids = []
follower_ids = []
WINDOW = 15 * 60
log_file = open("log", "w")
idx = 1

for twitter_id in existing_twitter_users.values():
  start = time()
  try:
    following_ids += api.friends_ids(twitter_id)
    follower_ids += api.followers_ids(twitter_id)
  except tweepy.TweepError as err:
    log_file.write("{}: {!s}".format(err,
                                     twitter_id))
    pass
  if idx % 7 == 0:
    sleep(WINDOW)
  if idx % 50 == 0:
    log_file.write("{!s} users processed".format(idx))
  idx += 1

write_pickle("following_ids.pkl", following_ids)
write_pickle("follower_ids.pkl", follower_ids)
