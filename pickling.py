from pickle import dump, load
from re import sub

def write_pickle(file_path, python_obj):
  pickle_file = open(file_path, "wb")
  dump(python_obj, pickle_file)
  pickle_file.close()

FB_KEYS = ["name", "id", "category"]

def write_fb_info_to_tsv(file_path, list_of_dict):
  if list_of_dict:
    tsv_file = open(file_path, "w")
    tsv_file.write("\t".join(FB_KEYS) + "\turl\n")
    for entry in list_of_dict:
      data = "\t".join(entry[key]
                      for key in FB_KEYS)
      url = "http://facebook.com/" + str(entry["id"])
      tsv_file.write(data + "\t" + url + "\n")
    tsv_file.close()

TWITTER_KEYS = ["screen_name", "id", "description"]
def write_tw_info_to_tsv(file_path, list_of_dict):
  if list_of_dict:
    tsv_file = open(file_path, "w")
    tsv_file.write("\t".join(TWITTER_KEYS) + "\turl\n")
    for entry in list_of_dict:
      data = "\t".join(sub(r"[\n|\r]+", r" ", 
                           str(entry[key]))
                       for key in TWITTER_KEYS)
      url = "http://twitter.com/" + str(entry["screen_name"])
      tsv_file.write(data + "\t" + url + "\n")
    tsv_file.close()


