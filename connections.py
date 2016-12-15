import psycopg2
import sqlalchemy
import yaml
import tweepy

def load_yaml(yaml_path):
  file = open(yaml_path, "r")
  info = yaml.load(file)
  file.close
  return info

def connect_to_snapshot(yaml_path):
  db_info = load_yaml(yaml_path)

  url = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(db_info["username"],
                                                      db_info["password"],
                                                      db_info["host"],
                                                      db_info["port"],
                                                      db_info["dbname"])
  engine = sqlalchemy.create_engine(url)
  conn = engine.connect()
  meta = sqlalchemy.MetaData(bind = engine)
  meta.reflect()

  return engine, conn, meta

def connect_to_twitter(yaml_path):
  api_keys = load_yaml(yaml_path)

  auth = tweepy.OAuthHandler(api_keys["twitter"]["consumer-key"],
                             api_keys["twitter"]["consumer-secret"])
  auth.set_access_token(api_keys["twitter"]["access-token"], 
                        api_keys["twitter"]["access-secret"])
  api = tweepy.API(auth)
  return api

