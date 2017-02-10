from connections import connect_to_snapshot, connect_to_twitter
from sqlalchemy.sql import select
from pickling import write_pickle
from twitter import *
from time import sleep

engine, conn, meta = connect_to_snapshot("ml-snapshot.yml")

api = connect_to_twitter("api-keys.yml")

TwitterUsers = meta.tables["twitter_users"]
s = select([TwitterUsers.c.entity])
result = conn.execute(s)
existing_twitter_users = list(row[0]["id"] 
                              for row in result)

WINDOW = 15 * 60

connection_ids = create_connections_list(existing_twitter_users,
                                         api,
                                         window = WINDOW)

write_pickle("connection_ids.pkl", connection_ids)

sleep(window)

connections = create_user_info_list(connection_ids,
                                    api,
                                    window = WINDOW)

write_pickle("connections.pkl", connections)
