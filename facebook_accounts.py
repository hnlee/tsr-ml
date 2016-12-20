from connections import connect_to_snapshot, connect_to_facebook
from sqlalchemy.sql import select
from pickling import write_pickle
from facebook import create_likes_list, create_page_info_list

engine, conn, meta = connect_to_snapshot("ml-snapshot.yml")

access_token = connect_to_facebook("api-keys.yml")

FacebookPages = meta.tables["facebook_pages"]
s = select([FacebookPages.c.entity])
result = conn.execute(s)
existing_facebook_pages = list(row[0]["id"] for row in result)

likes = create_likes_list(existing_facebook_pages,
                          access_token) 
likes_ids = list(entry["id"] for entry in likes)
likes_ids = list(set(likes_ids))

write_pickle("likes_ids.pkl", likes_ids)

likes_info = create_page_info_list(list(entry["id"] for entry in likes),
                                   access_token)

write_pickle("likes_info.pkl", likes_info)
