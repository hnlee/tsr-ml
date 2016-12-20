from unittest import TestCase, main
from pickling import write_pickle
from pickle import load, dump
from os import remove

class TestWritePickle(TestCase):
  def test_pickling_list(self):
    obj = [1, 2, 3]
    write_pickle("test.pkl", obj)
    self.pickle_file = open("test.pkl", "rb")
    unpickled = load(self.pickle_file) 
    self.assertEqual(obj, unpickled)

  def tearDown(self):
    self.pickle_file.close()
    remove("test.pkl") 

if __name__ == '__main__':
  main() 
