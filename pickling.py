from pickle import dump, load

def write_pickle(file_path, python_obj):
  pickle_file = open(file_path, "w")
  dump(python_obj, pickle_file)
  pickle_file.close()
